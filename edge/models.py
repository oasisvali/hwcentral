from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models
from django.db.models import Q

from core.models import Question, FRACTION_VALIDATOR, QuestionTag, SubjectRoom
from core.utils.references import EdgeSpecialTags

POSITIVE_VALIDATOR = [
    MinValueValidator(0.0),
]

class Tick(models.Model):
    """
    Maps to the result of correction of a single subpart
    """
    student = models.ForeignKey(User, help_text='The student whose answer resulted in this tick.')
    question = models.ForeignKey(Question, help_text='The question which the target subpart of this tick belongs to.')
    mark = models.FloatField(help_text='Mark (fraction) obtained for this subpart.',
                             validators=FRACTION_VALIDATOR)
    ack = models.BooleanField(help_text="Whether this tick has been acknowledged while calculating proficiency",
                              default=False)
    subjectRoom = models.ForeignKey(SubjectRoom,
                                    help_text="The subjectroom whose assignment's submission contains this tick")

    def __unicode__(self):
        return unicode("%s on subpart of question %s" % (self.student, self.question.pk))

    def acknowledge(self):
        self.ack = True
        self.save()

class Proficiency(models.Model):
    """
    Abstract base class to reduce duplication
    """
    questiontag = models.ForeignKey(QuestionTag, help_text='The tag that the proficiency is being calculated in.')
    rate = models.FloatField(help_text="The proficiency rate in this questiontag",
                             validators=FRACTION_VALIDATOR, default=0.0)

    percentile = models.FloatField(help_text="The percentile value (as a Fraction) for this proficiency",
                                   validators=FRACTION_VALIDATOR, default=0.0)

    score = models.FloatField(help_text="The final score that this proficiency is compared by (as a Fraction)",
                              validators=FRACTION_VALIDATOR, default=0.0)

    subjectRoom = models.ForeignKey(SubjectRoom,
                                    help_text="The subjectroom whose student's proficiency or average proficiency is being recorded")

    class Meta:
        abstract = True

    def update_percentile_and_score(self, percentile):
        self.percentile = percentile
        self.score = self.calculate_score()
        self.save()

    def calculate_score(self):
        return (0.7 * self.rate) + (0.3 * self.percentile)

    @classmethod
    def get_positives(cls, subjectroom, extra_condition=None):
        filter_condition = Q(subjectRoom=subjectroom) & Q(score__gte=0.8)
        if extra_condition:
            filter_condition &= extra_condition
        return cls.objects.filter(filter_condition).exclude(EdgeSpecialTags.refs.FILTER).order_by('-score')[:10]

    @classmethod
    def get_negatives(cls, subjectroom, extra_condition=None):
        filter_condition = Q(subjectRoom=subjectroom) & Q(score__lte=0.4)
        if extra_condition:
            filter_condition &= extra_condition
        return cls.objects.filter(filter_condition).exclude(EdgeSpecialTags.refs.FILTER).order_by('score')[:10]

    @classmethod
    def get_special_tags(cls, subjectroom, extra_condition=None):
        filter_condition = Q(questiontag=EdgeSpecialTags.refs.APPLICATION) & Q(subjectRoom=subjectroom)
        if extra_condition:
            filter_condition &= extra_condition
        try:
            application = cls.objects.get(filter_condition)
        except cls.DoesNotExist:
            application = None

        filter_condition = Q(questiontag=EdgeSpecialTags.refs.CONCEPTUAL) & Q(subjectRoom=subjectroom)
        if extra_condition:
            filter_condition &= extra_condition
        try:
            conceptual = cls.objects.get(filter_condition)
        except cls.DoesNotExist:
            conceptual = None

        filter_condition = Q(questiontag=EdgeSpecialTags.refs.CRITICAL_THINKING) & Q(subjectRoom=subjectroom)
        if extra_condition:
            filter_condition &= extra_condition
        try:
            critical = cls.objects.get(filter_condition)
        except cls.DoesNotExist:
            critical = None

        return application, conceptual, critical


class StudentProficiency(Proficiency):
    """
    Stores the total and averages that a student has obtained in a certain questiontag
    """

    total = models.FloatField(help_text="Total tick marks that the user has obtained in this questiontag",
                              validators=POSITIVE_VALIDATOR, default=0.0)
    student = models.ForeignKey(User, help_text='The student whose proficieny is being logged.')

    ticks = models.PositiveIntegerField(help_text='The number of ticks that this proficiency has been calculated over',
                                        default=0)


    def update_basic(self, tick):
        assert tick.student == self.student
        assert tick.question.tags.filter(pk=self.questiontag.pk).exists()
        assert tick.subjectRoom.students.filter(pk=self.student.pk).exists()

        # update tick counter
        self.ticks += 1
        # update total counter
        self.total += tick.mark
        # update rate
        self.rate = (self.total / float(self.ticks))
        self.save()

    def build_grouping_key(self):
        return "%s_%s_%s" % (
            self.subjectRoom.subject.pk,
            self.subjectRoom.classRoom.standard.number,
            self.subjectRoom.classRoom.school.board
        )


class SubjectRoomProficiency(Proficiency):
    def update(self, rate, percentile):
        self.rate = rate
        self.update_percentile_and_score(percentile)


class SubjectRoomQuestionMistake(models.Model):
    subjectRoom = models.ForeignKey(SubjectRoom,
                                    help_text='The subjectroom whose students have made the question mistakes which are being aggregated')
    question = models.ForeignKey(Question,
                                 help_text='The question for which incorrect answers are tallied to create this record')
    regression = models.FloatField(help_text="Abslute value of all the marks lost due to incorrect answers",
                                   validators=POSITIVE_VALIDATOR, default=0.0)

    def update(self, tick):
        assert tick.question == self.question
        assert tick.subjectRoom == self.subjectRoom

        self.regression += (1 - tick.mark)
        self.save()
