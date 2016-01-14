from django.contrib.auth.models import User
from django.db import models

from core.models import Question, FRACTION_VALIDATOR


class Tick(models.Model):
    """
    Maps to the result of correction of a single subpart
    """
    student = models.ForeignKey(User, help_text='The student whose answer resulted in this tick.')
    question = models.ForeignKey(Question, help_text='The question which the target subpart of this tick belongs to.')
    mark = models.FloatField(help_text='Mark (fraction) obtained for this subpart.',
                             validators=FRACTION_VALIDATOR)

    def __unicode__(self):
        return unicode("%s on subpart of question %s" % (self.student, self.question.pk))
