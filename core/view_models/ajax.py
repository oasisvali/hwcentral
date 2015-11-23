from core.utils.json import JSONModel
from core.utils.labels import get_date_label


class AnnouncementRow(JSONModel):
    def __init__(self, announcement):
        self.message = announcement.message
        self.timestamp = get_date_label(announcement.timestamp)
        self.source = announcement.get_source_label()