from django.db.models import Avg

from core.models import QuestionTag, SubjectRoom
from core.utils.references import HWCentralGroup
from edge.models import Tick, Proficiency, SubjectRoomProficiency


def register_tick(student, question, mark):
    new_tick = Tick(student=student, question=question, mark=mark)
    new_tick.save()


def update_subjectroom_proficiencies():
    # for every question tag
    for questiontag in QuestionTag.objects.all():
        # for every subjectroom
        for subjectroom in SubjectRoom.objects.all():
            # see if any proficiency values exist
            student_ids = subjectroom.students.values_list('pk', flat=True)
            set = Proficiency.objects.filter(questiontag=questiontag, student__pk__in=student_ids)

            if set.count() == 0:
                continue

            # get the proficiency (create if doesnt exist)
            try:
                proficiency = SubjectRoomProficiency.objects.get(subjectRoom=subjectroom, questiontag=questiontag)
            except SubjectRoomProficiency.DoesNotExist:
                proficiency = SubjectRoomProficiency(subjectRoom=subjectroom, questiontag=questiontag)
                proficiency.save()

            proficiency.rate = set.aggregate(Avg('rate'))['rate__avg']
            proficiency.percentile = set.aggregate(Avg('percentile'))['percentile__avg']
            proficiency.score = proficiency.rate * 0.7 + proficiency.percentile * 0.3
            proficiency.save()


def calculate_proficiencies():
    # for every unacknowledged tick
    for tick in Tick.objects.filter(ack=False):
        # find its student
        student = tick.student
        assert student.userinfo.group == HWCentralGroup.refs.STUDENT

        # for every questiontag covered
        for questiontag in tick.question.tags.all():
            # get the proficiency (create if doesnt exist)
            try:
                proficiency = Proficiency.objects.get(student=student, questiontag=questiontag)
            except Proficiency.DoesNotExist:
                proficiency = Proficiency(student=student, questiontag=questiontag)
                proficiency.save()

            # now update the proficiency as a result of this tick
            proficiency.update_basic(tick)

        # acknowledge tick
        tick.acknowledge()

    update_relscores()
    update_subjectroom_proficiencies()


def update_relscores():
    # for every questiontag
    for questiontag in QuestionTag.objects.all():
        # get a sorted list of all proficiencies which pertain to this questiontag
        proficiencies = Proficiency.objects.filter(questiontag=questiontag).order_by('rate')
        count = proficiencies.count()
        # loop through proficiencies in ascending order, and set percentiles
        # TODO: consider setting same percentile value for same rate?
        for i, proficiency in enumerate(proficiencies):
            proficiency.update_relative(float(i) / count)
