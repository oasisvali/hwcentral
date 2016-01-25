# This file provides the utility methods to access files from the hwcentral-cabinet repository
# The access urls are built differently depending on the hwcentral settings DEBUG flag
import os

import requests
from datadog import statsd
from django.core.signing import Signer
from django.core.urlresolvers import reverse
from django.utils.http import urlsafe_base64_encode

from cabinet.exceptions import CabinetSubmissionExistsError, CabinetSubmissionMissingError, CabinetConnectionError, \
    Cabinet404Error, SubpartOutOfOrderException
from core.data_models.aql import AQLMetaDM
from core.data_models.question import QuestionContainer, build_question_subpart_from_data
from core.data_models.submission import SubmissionDM
from core.routing.urlnames import UrlNames
from core.utils.constants import HWCentralQuestionDataType, HttpMethod, HWCentralEnv
from core.utils.json import dump_json_string
from croupier.constraints import SubpartVariableConstraints
from croupier.data_models import UndealtQuestionDM
from hwcentral import settings
from hwcentral.exceptions import InvalidHWCentralEnvError

CABINET_PORT = 9878

if settings.ENVIRON == HWCentralEnv.LOCAL:
    CABINET_ENDPOINT = 'localhost'
elif settings.ENVIRON == HWCentralEnv.QA:
    CABINET_ENDPOINT = '10.130.97.154'
elif settings.ENVIRON == HWCentralEnv.CIRCLECI:
    CABINET_ENDPOINT = 'localhost'
elif settings.ENVIRON == HWCentralEnv.PROD:
    CABINET_ENDPOINT = '10.176.7.252'
else:
    raise InvalidHWCentralEnvError(settings.ENVIRON)

CABINET_ENDPOINT = 'http://' + CABINET_ENDPOINT + ':' + str(CABINET_PORT) + '/'
CONFIG_FILE_EXTENSION = '.json'
ENCODING_SEPERATOR = ':'

SIGNER = Signer()

def build_config_filename(id_num):
    return str(id_num) + CONFIG_FILE_EXTENSION


def build_aql_meta_url_stub(assignment_questions_list):
    return os.path.join(CABINET_ENDPOINT, 'aql_meta',
                        str(assignment_questions_list.school.board.pk),
                        str(assignment_questions_list.school.pk),
                        str(assignment_questions_list.standard.number),
                        str(assignment_questions_list.subject.pk))  # no chapter here as aql can be cross-chapter


def build_aql_meta_data_url(assignment_questions_list):
    return os.path.join(build_aql_meta_url_stub(assignment_questions_list),
                        build_config_filename(assignment_questions_list.pk))


def build_question_url_stub(question, question_data_type):
    return os.path.join(CABINET_ENDPOINT, 'questions', question_data_type,
                        str(question.school.board.pk),
                        str(question.school.pk),
                        str(question.standard.number),
                        str(question.subject.pk),
                        str(question.chapter.pk))


def build_question_data_url(question, question_data_type, question_id):
    return os.path.join(build_question_url_stub(question, question_data_type),
                        build_config_filename(question_id))


def build_cabinet_images_url_stub():
    return os.path.join(CABINET_ENDPOINT, 'images')

def get_resource(url):
    try:
        response = requests.get(url)
    except Exception:
        raise CabinetConnectionError(url, HttpMethod.GET)
    if response.status_code == 404:
        raise Cabinet404Error(url)
    return response

def get_resource_content(url):
    return (get_resource(url)).json()


@statsd.timed('cabinet.get.static')
def get_static_content(url):
    return get_resource(url)


def get_resource_exists(url):
    try:
        get_resource(url)
        return True
    except Cabinet404Error:
        return False

def get_question(question):
    # NOTE: cannot just use the Question's from_data method as we dont have all the data available in one dictionary.
    # it must first be aggregated by looking at the container in cabinet
    container_url = build_question_data_url(question, HWCentralQuestionDataType.CONTAINER, question.pk)
    container = QuestionContainer(get_resource_content(container_url))

    subparts = []
    variable_constraints_list = []
    for i, subpart in enumerate(container.subparts):
        subpart_url = build_question_data_url(question, HWCentralQuestionDataType.SUBPART, subpart)
        subpart_data = get_resource_content(subpart_url)

        question_part = build_question_subpart_from_data(subpart_data)
        subpart_variable_constraints = SubpartVariableConstraints(subpart_data.get('variable_constraints'))

        if i != question_part.subpart_index:
            raise SubpartOutOfOrderException(question_part.subpart_index, i, question.pk)
        subparts.append(question_part)
        variable_constraints_list.append(subpart_variable_constraints)

    return UndealtQuestionDM(question.pk, container, subparts, variable_constraints_list)


def get_question_with_img_urls(user, question):
    undealt_question_dm = get_question(question)
    undealt_question_dm.question_data.build_img_urls(user)
    return undealt_question_dm

def build_submission_data_url(submission):
    return os.path.join(CABINET_ENDPOINT, 'submissions',
                        str(submission.assignment.subjectRoom.classRoom.school.pk),
                        str(submission.assignment.subjectRoom.classRoom.standard.number),
                        submission.assignment.subjectRoom.classRoom.division,
                        str(submission.assignment.subjectRoom.subject.pk),
                        str(submission.assignment.pk),
                        build_config_filename(submission.pk))


@statsd.timed('cabinet.get.submission')
def get_submission(submission):
    submission_url = build_submission_data_url(submission)

    return SubmissionDM.build_from_data(get_resource_content(submission_url))


@statsd.timed('cabinet.get.aql_meta')
def get_aql_meta(assignment_questions_list):
    aql_meta_url = build_aql_meta_data_url(assignment_questions_list)

    return AQLMetaDM(assignment_questions_list.pk, get_resource_content(aql_meta_url))


@statsd.timed('cabinet.put.submission')
def build_submission(submission, shell_submission_dm):
    """
    Used to build a shell submission file in the cabinet
    Throws CabinetSubmissionExistsError if trying to create submission which already exists
    """

    # submission is indirectly used to save the order of the questions and the order of the options
    # (basically the containers with their subparts fully dealt and shuffled)

    submission_url = build_submission_data_url(submission)

    if submission_exists(submission):
        raise CabinetSubmissionExistsError("file exists for resource at: %s" % submission_url)

    # TODO: possible race condition here

    nginx_cabinet_put(submission_url, dump_json_string(shell_submission_dm))


def nginx_cabinet_put(url, json_str):
    try:
        requests.put(url, data=json_str)
    except Exception:
        raise CabinetConnectionError(url, HttpMethod.PUT)

@statsd.timed('cabinet.update.submission')
def update_submission(submission, submission_dm):
    submission_url = build_submission_data_url(submission)

    if not submission_exists(submission):
        raise CabinetSubmissionMissingError("file missing for resource at: %s" % submission_url)

    nginx_cabinet_put(submission_url, dump_json_string(submission_dm))


def submission_exists(submission):
    submission_url = build_submission_data_url(submission)
    return get_resource_exists(submission_url)


def get_img_url(stub_url, img_filename):
    return os.path.join(stub_url, 'img', img_filename)

def get_img_url_secure(user, unsecure_url):
    raw_secure_url = user.username + ENCODING_SEPERATOR + unsecure_url
    signed_secure_url = SIGNER.sign(raw_secure_url)
    return reverse(UrlNames.SECURE_STATIC.name, args=[urlsafe_base64_encode(signed_secure_url)])

def get_question_img_url(question, question_data_type, img_filename):
    return get_img_url(build_question_url_stub(question, question_data_type), img_filename)

def get_question_img_url_secure(user, question, question_data_type, img_filename):
    img_url = get_question_img_url(question, question_data_type, img_filename)
    return get_img_url_secure(user, img_url)

def get_aql_meta_img_url(assignment_questions_list, img_filename):
    return get_img_url(build_aql_meta_url_stub(assignment_questions_list), img_filename)

def get_aql_meta_img_url_secure(user, assignment_questions_list, img_filename):
    img_url = get_aql_meta_img_url(assignment_questions_list, img_filename)
    return get_img_url_secure(user, img_url)

def get_school_stamp_url(school):
    return os.path.join(build_cabinet_images_url_stub(), 'school', str(school.pk) + '.png')

def get_school_stamp_url_secure(user):
    school_url = get_school_stamp_url(user.userinfo.school)
    return get_img_url_secure(user, school_url)

@statsd.timed('cabinet.get.assignment')
def build_undealt_assignment(user, assignment_questions_list):
    undealt_question_dms = []
    # TODO: verify that the ordering of questions returned by this manytomanyfield lookup is consistent
    for question_db in assignment_questions_list.questions.all():
        undealt_question_dms.append(get_question_with_img_urls(user, question_db))

    return undealt_question_dms






