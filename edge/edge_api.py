from collections import defaultdict

from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db.models import Avg

from core.models import QuestionTag, SubjectRoom
from core.utils.references import HWCentralGroup
from edge.models import Tick, StudentProficiency, SubjectRoomProficiency, SubjectRoomQuestionMistake
from focus.models import Remedial
from hwcentral.exceptions import InvalidContentTypeError
from scripts.database.question_bank_reset import hwcentral_truncate_tables


def register_tick(question, mark, submission):
    if submission.assignment.content_type == ContentType.objects.get_for_model(SubjectRoom):
        subjectroom = submission.assignment.content_object
    elif submission.assignment.content_type == ContentType.objects.get_for_model(Remedial):
        subjectroom = submission.assignment.content_object.focusRoom.subjectRoom
    elif submission.assignment.content_type == ContentType.objects.get_for_model(User):
        raise NotImplementedError("Ticks cannot be registered for practice assignments")
    else:
        raise InvalidContentTypeError(submission.assignment.content_type)

    new_tick = Tick(student=submission.student, question=question, mark=mark,
                    subjectRoom=subjectroom)
    new_tick.save()


def calculate_edge_data():
    report = process_ticks()
    report += update_percentiles()
    report += update_subjectroom_proficiencies()
    report += 'Edge data calculated successfully\n'

    return report


def process_ticks():
    acks = 0

    # for every unacknowledged tick
    for tick in Tick.objects.filter(ack=False):
        # find its student
        student = tick.student
        assert student.userinfo.group == HWCentralGroup.refs.STUDENT

        # for every questiontag covered
        for questiontag in tick.question.tags.all():
            # get the proficiency (create if doesnt exist)
            try:
                student_proficiency = StudentProficiency.objects.get(student=student, questiontag=questiontag,
                                                                     subjectRoom=tick.subjectRoom)
            except StudentProficiency.DoesNotExist:
                student_proficiency = StudentProficiency(student=student, questiontag=questiontag,
                                                         subjectRoom=tick.subjectRoom)
                student_proficiency.save()

            # now update the proficiency as a result of this tick
            student_proficiency.update_basic(tick)

        # update the SubjectRoomQuestionMistake record
        try:
            subjectroom_question_mistake = SubjectRoomQuestionMistake.objects.get(subjectRoom=tick.subjectRoom,
                                                                                  question=tick.question)
        except SubjectRoomQuestionMistake.DoesNotExist:
            subjectroom_question_mistake = SubjectRoomQuestionMistake(subjectRoom=tick.subjectRoom,
                                                                      question=tick.question)
            subjectroom_question_mistake.save()
        subjectroom_question_mistake.update(tick)

        # acknowledge tick
        tick.acknowledge()
        acks += 1

    return "Processed %s ticks\n" % acks


def update_percentiles():
    """
    NOTE: The percentile rank calculation is not limited by subjectroom, classroom, school or board it is grouped on subject and standard and board
    """
    percentiles_calculated = 0

    # for every questiontag
    for questiontag in QuestionTag.objects.all():
        # get a sorted list of all proficiencies which pertain to this questiontag and group them by subject and standard and board
        student_proficiencies = StudentProficiency.objects.filter(questiontag=questiontag).order_by('rate')

        grouped_proficiencies = defaultdict(list)
        for student_proficiency in student_proficiencies:
            grouped_proficiencies[student_proficiency.build_grouping_key()].append(student_proficiency)

        for proficiency_group in grouped_proficiencies.itervalues():
            count = len(proficiency_group)

            prev_rate = 0
            rank = 0

            # loop through proficiencies in ascending order, and set percentiles
            for i, student_proficiency in enumerate(proficiency_group):
                assert student_proficiency.rate >= prev_rate
                if (student_proficiency.rate - prev_rate) > 0.0000001:
                    prev_rate = student_proficiency.rate
                    rank = i

                student_proficiency.update_percentile_and_score(float(rank) / count)

            # correction for highest percentile
            for student_proficiency in proficiency_group[rank:]:
                student_proficiency.update_percentile_and_score(1.0)

            percentiles_calculated += 1

    return "Calculated %s Percentiles\n" % percentiles_calculated

def update_subjectroom_proficiencies():
    subjectroom_proficiencies_updated = 0

    # for every subjectroom
    for subjectroom in SubjectRoom.objects.all():
        # get all student proficiency values for this subjectroom, and group by the questiontags
        questiontags = StudentProficiency.objects.filter(subjectRoom=subjectroom).values('questiontag').distinct()
        for questiontag in questiontags:
            questiontag = QuestionTag.objects.get(pk=questiontag['questiontag'])
            # check if subjectroom proficiency entry exists
            try:
                subjectroom_proficiency = SubjectRoomProficiency.objects.get(subjectRoom=subjectroom,
                                                                             questiontag=questiontag)
            except SubjectRoomProficiency.DoesNotExist:  # (create if doesnt exist)
                subjectroom_proficiency = SubjectRoomProficiency(subjectRoom=subjectroom, questiontag=questiontag)
                subjectroom_proficiency.save()

            enrolled_student_proficiencies = StudentProficiency.objects.filter(subjectRoom=subjectroom,
                                                                               questiontag=questiontag)

            # use django aggregates to calculate averages
            subjectroom_proficiency.update(
                    enrolled_student_proficiencies.aggregate(Avg('rate'))['rate__avg'],
                    enrolled_student_proficiencies.aggregate(Avg('percentile'))['percentile__avg']
            )

            subjectroom_proficiencies_updated += 1

    return "Updated %s Subjectroom Proficiencies\n" % subjectroom_proficiencies_updated


def reset_edge_data():
    hwcentral_truncate_tables([
        'edge_tick',
        'edge_studentproficiency',
        'edge_subjectroomproficiency'
        'edge_subjectroomquestionmistake'
    ])
