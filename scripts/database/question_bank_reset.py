# truncates the following tables in the database and then reloads all the question bank fixtures
import os

from django.core.management import call_command
from django.db import connection

from hwcentral.settings import PROJECT_ROOT


def hwcentral_raw_sql_execute(sql_cmd):
    with connection.cursor() as conn:
        conn.execute(sql_cmd)

QB_TRUNCATE_CMD = """

BEGIN;
SET FOREIGN_KEY_CHECKS = 0;

TRUNCATE `core_question_tags`;
TRUNCATE `core_question`;
TRUNCATE `core_questiontag`;
TRUNCATE `core_assignmentquestionslist_questions`;
TRUNCATE `core_assignmentquestionslist`;

SET FOREIGN_KEY_CHECKS = 1;
COMMIT;
"""

def run():
    # first truncate all tables which form the question bank
    hwcentral_raw_sql_execute(QB_TRUNCATE_CMD)

    # now reload all question bank fixtures
    for fixture in os.listdir(os.path.join(PROJECT_ROOT, 'core', 'fixtures', 'qb')):
        call_command('loaddata', os.path.join('qb', fixture))

