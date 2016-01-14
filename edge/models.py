from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from core.models import Question, FRACTION_VALIDATOR, QuestionTag, SubjectRoom

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

    def __unicode__(self):
        return unicode("%s on subpart of question %s" % (self.student, self.question.pk))

    def acknowledge(self):
        self.ack = True
        self.save()


class Proficiency(models.Model):
    """
    Stores the total and averages that a student has obtained in a certain questiontag
    """

    total = models.FloatField(help_text="Total tick marks that the user has obtained in this questiontag",
                              validators=POSITIVE_VALIDATOR, default=0.0)
    student = models.ForeignKey(User, help_text='The student whose proficieny is being logged.')
    questiontag = models.ForeignKey(QuestionTag, help_text='The tag that the proficiency is being calculated in.')
    ticks = models.PositiveIntegerField(help_text='The number of ticks that this proficieny has been calculated over',
                                        default=0)
    rate = models.FloatField(help_text="The proficiency rate in this questiontag",
                             validators=FRACTION_VALIDATOR, default=0.0)

    percentile = models.FloatField(help_text="The percentile value (as a Fraction) for this proficiency",
                                   validators=FRACTION_VALIDATOR, default=0.0)
    score = models.FloatField(help_text="The final score that this proficiency is compared by (as a Fraction)",
                              validators=FRACTION_VALIDATOR, default=0.0)

    def update_basic(self, tick):
        assert tick.student == self.student
        assert tick.question.tags.filter(pk=self.questiontag.pk).exists()

        # update tick counter
        self.ticks += 1
        # update total counter
        self.total += tick.mark
        # update rate
        self.rate = (self.total / float(self.ticks))
        self.save()

    def update_relative(self, percentile):
        self.percentile = percentile
        self.score = (0.7 * self.rate) + (0.3 * self.percentile)
        self.save()


class SubjectRoomProficiency(models.Model):
    subjectRoom = models.ForeignKey(SubjectRoom)
    questiontag = models.ForeignKey(QuestionTag)
    rate = models.FloatField(help_text="The proficiency rate in this questiontag",
                             validators=FRACTION_VALIDATOR, default=0.0)

    percentile = models.FloatField(help_text="The percentile value (as a Fraction) for this proficiency",
                                   validators=FRACTION_VALIDATOR, default=0.0)
    score = models.FloatField(help_text="The final score that this proficiency is compared by (as a Fraction)",
                              validators=FRACTION_VALIDATOR, default=0.0)
