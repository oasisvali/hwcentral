from django.db import models

from hwcentral.settings import MAX_CHARFIELD_LENGTH


class Video(models.Model):
    url = models.CharField(max_length=MAX_CHARFIELD_LENGTH,
                           help_text='Embed url for external media')

    def __unicode__(self):
        return unicode(self.url)
