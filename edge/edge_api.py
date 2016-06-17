from collections import namedtuple

from django.db.models import Avg

from core.models import SubjectRoom
from core.utils.references import HWCentralGroup
from edge.models import Tick, StudentProficiency, SubjectRoomProficiency, SubjectRoomQuestionMistake
from scripts.database.question_bank_reset import hwcentral_truncate_tables


def register_tick(question, mark, submission):
    new_tick = Tick(student=submission.student, question=question, mark=mark,
                    subjectRoom=submission.assignment.get_subjectroom())
    new_tick.save()


# NOTE: Race condition chance when this is called outside of grade_overnight from request handling flow
def calculate_edge_data():
    tick_acks, proficiency_groups_processed = process_ticks()
    report = "Processed %s ticks\n" % tick_acks
    if tick_acks > 0:
        report += update_percentiles(proficiency_groups_processed)
        report += update_subjectroom_proficiencies(proficiency_groups_processed)

    return report


# utility class for organizing attributes that uniquely define the set of proficiencies that will be percentiled
ProficiencyGrouping = namedtuple('ProficiencyGrouping', ['questiontag', 'subject', 'standard', 'board'])

def process_ticks():
    acks = 0

    # this set helps to keep track of the proficiency group (subject + standard + board + questiontag) whose proficiencies
    # will need to be reordered as a result of the ticks that are processed
    proficiency_groups_processed = set()

    # for every unacknowledged tick
    for tick in Tick.objects.filter(ack=False):
        # find its student
        student = tick.student
        assert (student.userinfo.group == HWCentralGroup.refs.STUDENT or
                student.userinfo.group == HWCentralGroup.refs.OPEN_STUDENT)

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

            proficiency_groups_processed.add(ProficiencyGrouping(
                questiontag,
                tick.subjectRoom.subject,
                tick.subjectRoom.classRoom.standard,
                tick.subjectRoom.classRoom.school.board
            ))

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

    return acks, proficiency_groups_processed


def update_percentiles(proficiency_groups_processed):
    """
    NOTE: The percentile rank calculation is not limited by subjectroom, classroom, school or board it is grouped on subject and standard and board
    """
    percentiles_calculated = 0

    # iterate through all the proficiency groups updated in the latest run
    for proficiency_group in proficiency_groups_processed:
        student_proficiencies = StudentProficiency.objects.filter(
            questiontag=proficiency_group.questiontag,
            subjectRoom__subject=proficiency_group.subject,
            subjectRoom__classRoom__standard=proficiency_group.standard,
            subjectRoom__classRoom__school__board=proficiency_group.board
        ).order_by('rate')

        count = student_proficiencies.count()

        prev_rate = 0
        rank = 0

        # loop through proficiencies in ascending order, and set percentiles
        for i, student_proficiency in enumerate(student_proficiencies):
            # sanity check for sort
            assert student_proficiency.rate >= prev_rate

            # custom logic to ensure same percentile for same rate
            if (student_proficiency.rate - prev_rate) > 0.0000001:
                prev_rate = student_proficiency.rate
                rank = i

            student_proficiency.update_percentile_and_score(float(rank) / count)

        # correction for highest percentile
        for student_proficiency in student_proficiencies[rank:]:
            student_proficiency.update_percentile_and_score(1.0)

        percentiles_calculated += 1

    return "Calculated %s Percentiles\n" % percentiles_calculated


def update_subjectroom_proficiencies(proficiency_groups_processed):
    subjectroom_proficiencies_updated = 0

    # build seperate lists of
    for proficiency_group in proficiency_groups_processed:
        questiontag = proficiency_group.questiontag

        for subjectroom in SubjectRoom.objects.filter(
                subject=proficiency_group.subject,
                classRoom__standard=proficiency_group.standard,
                classRoom__school__board=proficiency_group.board
        ):
            enrolled_student_proficiencies = StudentProficiency.objects.filter(subjectRoom=subjectroom,
                                                                               questiontag=questiontag)

            if not enrolled_student_proficiencies.exists():
                continue

            # check if subjectroom proficiency entry exists
            try:
                subjectroom_proficiency = SubjectRoomProficiency.objects.get(subjectRoom=subjectroom,
                                                                             questiontag=questiontag)
            except SubjectRoomProficiency.DoesNotExist:  # (create if doesnt exist)
                subjectroom_proficiency = SubjectRoomProficiency(subjectRoom=subjectroom, questiontag=questiontag)
                subjectroom_proficiency.save()

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
        'edge_subjectroomproficiency',
        'edge_subjectroomquestionmistake'
    ])
