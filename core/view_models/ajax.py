from collections import defaultdict

import django
from django.db.models import Q
from django.utils.html import escape

from core.models import AssignmentQuestionsList, Chapter, Submission
from core.utils.constants import HWCentralEnv
from core.utils.json import JSONModel
from core.utils.labels import get_date_label
from core.utils.references import HWCentralRepo
from hwcentral.exceptions import InvalidHWCentralEnvError
from hwcentral.settings import ENVIRON


class AnnouncementRow(JSONModel):
    def __init__(self, announcement):
        self.message = escape(announcement.message)  # need to escape because user might have entered html tags
        self.timestamp = get_date_label(announcement.timestamp)
        self.source = announcement.get_source_label()

class SubjectRoomSelectElem(JSONModel):
    def __init__(self, subjectroom, chapters):
        self.subjectroom_id = subjectroom.pk
        self.chapters = chapters

class StudentSubjectRoomSelectElem(SubjectRoomSelectElem):
    def __init__(self, student, subjectroom):
        chapters = []

        if ENVIRON == HWCentralEnv.PROD or ENVIRON == HWCentralEnv.CIRCLECI:
            accessible_aqls = defaultdict(set)
            for submission in Submission.objects.filter(
                    assignment__subjectRoom=subjectroom,
                    student=student,
                    assignment__due__lte=django.utils.timezone.now()
            ):
                # this aql has already been assigned to the student i.e. it is accessible
                aql = submission.assignment.assignmentQuestionsList
                accessible_aqls[aql.chapter.pk].add(aql.pk)

            for chapter_id, aql_set in accessible_aqls.iteritems():
                chapter = Chapter.objects.get(pk=chapter_id)
                aqls = AssignmentQuestionsList.objects.filter(pk__in=list(aql_set)).order_by('number')

                chapters.append(ChapterSelectElem(chapter, aqls))

        elif ENVIRON == HWCentralEnv.QA or ENVIRON == HWCentralEnv.LOCAL:
            # allow student to practice all available assignments - hence similar aql selection logic as teacher
            school_filter = Q(school=subjectroom.classRoom.school) | Q(school=HWCentralRepo.refs.SCHOOL)
            standard_subject_filter = Q(subject=subjectroom.subject) & Q(standard=subjectroom.classRoom.standard)

            aql_query = school_filter & standard_subject_filter

            for chapter_id in AssignmentQuestionsList.objects.filter(aql_query).values_list("chapter",
                                                                                            flat=True).distinct():
                chapter = Chapter.objects.get(pk=chapter_id)
                aqls = AssignmentQuestionsList.objects.filter(aql_query, chapter=chapter).order_by('number')
                chapters.append(ChapterSelectElem(chapter, aqls))

        else:
            raise InvalidHWCentralEnvError(ENVIRON)

        super(StudentSubjectRoomSelectElem, self).__init__(subjectroom, chapters)


class TeacherSubjectRoomSelectElem(SubjectRoomSelectElem):
    def __init__(self, subjectroom, question_set_override):
        chapters = []

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
            chapters.append(ChapterSelectElem(chapter, aqls))

        super(TeacherSubjectRoomSelectElem, self).__init__(subjectroom, chapters)

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