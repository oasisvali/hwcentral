### NOTE: these functions are a hacky way to make testing work with cabinet. Do not use these in code
import requests
from cabinet.cabinet_api import build_submission_data_url
from cabinet.exceptions import CabinetConnectionError
from core.models import Submission
from core.utils.constants import HttpMethod


def delete_submission(submission_id):
    submission_url = build_submission_data_url(Submission.objects.get(pk=submission_id))
    delete_resource(submission_url)

def delete_resource(url):
    try:
        requests.delete(url)
    except Exception:
        raise CabinetConnectionError(url, HttpMethod.DELETE)