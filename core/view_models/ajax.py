from core.utils.json import JSONModel
from core.utils.labels import get_datetime_label


class AnnouncementRow(JSONModel):
    def __init__(self, announcement):
        self.message = announcement.message
        self.timestamp = get_datetime_label(announcement.timestamp)
        self.source = announcement.get_source_label()