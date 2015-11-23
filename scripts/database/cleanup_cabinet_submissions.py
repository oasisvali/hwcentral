import os

from core.models import Submission
from core.utils.constants import HWCentralEnv
from hwcentral import settings
from scripts.database.question_bank_reloader import HOME_DIR

CABINET_SUBMISSIONS_DIR = os.path.join(HOME_DIR, 'hwcentral-cabinet', 'submissions')


def handle_submissions_dir(dir, submissions_db):
    for elem in os.listdir(dir):
        elem_path = os.path.join(dir, elem)
        if os.path.isdir(elem_path):
            handle_submissions_dir(elem_path, submissions_db)
        else:
            assert os.path.isfile(elem_path)
            if long(elem[:-5]) not in submissions_db:
                print 'Removing', elem_path
                os.remove(elem_path)


def run():
    assert settings.ENVIRON == HWCentralEnv.LOCAL

    # first build a set of all submission pks in the database
    submissions_db = set()
    submissions_db.update(submission.pk for submission in Submission.objects.all())
    print 'Found %s submissions in db' % len(submissions_db)

    # now loop through cabinet submissions recursively and if submission file does not exist in database, delete it from cabinet
    handle_submissions_dir(CABINET_SUBMISSIONS_DIR, submissions_db)

    print 'Cleanup complete'
