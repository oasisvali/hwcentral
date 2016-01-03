from django.db.models import Q

from core.models import AssignmentQuestionsList, Chapter
from core.utils.json import JSONModel
from core.utils.labels import get_date_label
from core.utils.references import HWCentralRepo


class AnnouncementRow(JSONModel):
    def __init__(self, announcement):
        self.message = announcement.message
        self.timestamp = get_date_label(announcement.timestamp)
        self.source = announcement.get_source_label()

class SubjectRoomSelectElem(JSONModel):
    def __init__(self, subjectroom, question_set_override):
        self.subjectroom_id = subjectroom.pk
        self.chapters = []

        school_filter = Q(school=subjectroom.classRoom.school) | Q(school=HWCentralRepo.refs.SCHOOL)
        standard_subject_filter = Q(subject=subjectroom.subject)
        if question_set_override:
            standard_subject_filter =standard_subject_filter & Q(standard__number__lte=subjectroom.classRoom.standard.number)
        else:
            standard_subject_filter = standard_subject_filter & Q(standard=subjectroom.classRoom.standard)

        aql_query = school_filter & standard_subject_filter

        for chapter_id in AssignmentQuestionsList.objects.filter(aql_query).values_list("chapter", flat=True).distinct():
            chapter = Chapter.objects.get(pk=chapter_id)
            aqls = AssignmentQuestionsList.objects.filter(aql_query, chapter=chapter).order_by('number')
            self.chapters.append(ChapterSelectElem(chapter, aqls))

class ChapterSelectElem(JSONModel):
    def __init__(self, chapter, aqls):
        self.label = chapter.name
        self.chapter_id = chapter.pk
        self.aqls = [AqlSelectElem(aql) for aql in aqls]

class AqlSelectElem(JSONModel):
    def __init__(self, aql):
        self.label = aql.number
        self.aql_id = aql.pk
        self.description = aql.description