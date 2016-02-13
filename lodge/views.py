from datadog import statsd
from django.shortcuts import render, get_object_or_404

from lodge.models import Video
from lodge.urlnames import LodgeUrlNames


@statsd.timed('lodge.get.index')
def index_get(request, video_id):
    statsd.increment('lodge.hits.get.index')
    video = get_object_or_404(Video, pk=video_id)
    return render(request, LodgeUrlNames.INDEX.template, {'uri': video.url})
