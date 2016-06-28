from collections import defaultdict

import django
from django.db.models import Q
from django.utils.html import escape

from core.models import AssignmentQuestionsList, Chapter, Submission, Standard
from core.utils.constants import HWCentralEnv
from core.utils.json import JSONModel
from core.utils.labels import get_date_label, get_subjectroom_label
from core.utils.references import HWCentralRepo, HWCentralOpen
from hwcentral.exceptions import InvalidHWCentralEnvError
from hwcentral.settings import ENVIRON


class AnnouncementRow(JSONModel):
    def __init__(self, announcement):
        self.message = escape(announcement.message)  # need to escape because user might have entered html tags
        self.timestamp = get_date_label(announcement.timestamp)
        self.source = announcement.get_source_label()
        self.target = announcement.get_target_label()


class SelectElem(JSONModel):
    def __init__(self, label, id, child_nodes):
        self.label = label
        self.id = id
        self.child_nodes = child_nodes


class AqlSelectElem(SelectElem):
    def __init__(self, aql):
        super(AqlSelectElem, self).__init__(aql.number, aql.pk, None)
        self.description = aql.description


class StudentSubjectRoomSelectElem(SelectElem):
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
                aqls = [AqlSelectElem(aql) for aql in aqls]
                chapters.append(SelectElem(chapter.name, chapter.pk, aqls))

        elif ENVIRON == HWCentralEnv.QA or ENVIRON == HWCentralEnv.LOCAL:
            # allow student to practice all available assignments - hence similar aql selection logic as teacher
            school_filter = Q(school=subjectroom.classRoom.school) | Q(school=HWCentralRepo.refs.SCHOOL)
            standard_subject_filter = Q(subject=subjectroom.subject) & Q(standard=subjectroom.classRoom.standard)

            aql_query = school_filter & standard_subject_filter

            for chapter_id in AssignmentQuestionsList.objects.filter(aql_query).values_list("chapter",
                                                                                            flat=True).distinct():
                chapter = Chapter.objects.get(pk=chapter_id)
                aqls = AssignmentQuestionsList.objects.filter(aql_query, chapter=chapter).order_by('number')
                aqls = [AqlSelectElem(aql) for aql in aqls]
                chapters.append(SelectElem(chapter.name, chapter.pk, aqls))

        else:
            raise InvalidHWCentralEnvError(ENVIRON)

        super(StudentSubjectRoomSelectElem, self).__init__(subjectroom.subject.name, subjectroom.pk, chapters)


class OpenSubjectRoomSelectElem(SelectElem):
    def __init__(self, subjectroom):
        assert subjectroom.classRoom.school == HWCentralOpen.refs.SCHOOL

        # check if there are aqls for current subjectroom
        query = AssignmentQuestionsList.objects.filter(subject=subjectroom.subject,
                                                       standard=subjectroom.classRoom.standard,
                                                       school=HWCentralRepo.refs.SCHOOL)

        chapters = []
        for chapter_id in query.values_list("chapter", flat=True).distinct():
            chapter = Chapter.objects.get(pk=chapter_id)
            aqls = query.filter(chapter=chapter).order_by('number')
            aqls = [AqlSelectElem(aql) for aql in aqls]
            chapters.append(SelectElem(chapter.name, chapter.pk, aqls))

        super(OpenSubjectRoomSelectElem, self).__init__(subjectroom.subject.name, subjectroom.pk, chapters)


class TeacherSubjectRoomSelectElem(SelectElem):
    def __init__(self, subjectroom):
        chapters = []

        school_filter = Q(school=subjectroom.classRoom.school) | Q(school=HWCentralRepo.refs.SCHOOL)
        standard_subject_filter = Q(subject=subjectroom.subject) & Q(standard=subjectroom.classRoom.standard)

        aql_query = school_filter & standard_subject_filter

        for chapter_id in AssignmentQuestionsList.objects.filter(aql_query).values_list("chapter", flat=True).distinct():
            chapter = Chapter.objects.get(pk=chapter_id)
            aqls = AssignmentQuestionsList.objects.filter(aql_query, chapter=chapter).order_by('number')
            aqls = [AqlSelectElem(aql) for aql in aqls]
            chapters.append(SelectElem(chapter.name, chapter.pk, aqls))

        super(TeacherSubjectRoomSelectElem, self).__init__(get_subjectroom_label(subjectroom), subjectroom.pk, chapters)


class TeacherSubjectRoomSelectOverrideElem(SelectElem):
    def __init__(self, subjectroom):
        standards = []

        for standard in Standard.objects.filter(number__lte=subjectroom.classRoom.standard.number).order_by('-number'):
            chapters = []

            school_filter = Q(school=subjectroom.classRoom.school) | Q(school=HWCentralRepo.refs.SCHOOL)
            standard_subject_filter = Q(subject=subjectroom.subject) & Q(standard=standard)

            aql_query = school_filter & standard_subject_filter

            for chapter_id in AssignmentQuestionsList.objects.filter(aql_query).values_list("chapter",
                                                                                            flat=True).distinct():
                chapter = Chapter.objects.get(pk=chapter_id)
                aqls = AssignmentQuestionsList.objects.filter(aql_query, chapter=chapter).order_by('number')
                aqls = [AqlSelectElem(aql) for aql in aqls]
                chapters.append(SelectElem(chapter.name, chapter.pk, aqls))

            if len(chapters) > 0:
                standards.append(SelectElem(standard.number, standard.pk, chapters))

        super(TeacherSubjectRoomSelectOverrideElem, self).__init__(get_subjectroom_label(subjectroom), subjectroom.pk,
                                                                   standards)
