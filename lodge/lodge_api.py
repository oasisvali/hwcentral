from lodge.models import Video


def get_video_uri(pk):
    return Video.objects.get(pk=pk).url
