from django.shortcuts import get_object_or_404

from lodge.models import Video


def get_video_uri(pk):
    return get_object_or_404(Video, pk=pk).url
