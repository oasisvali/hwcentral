import json
import os

from django.core.management import call_command

from core.models import Chapter
from core.utils.constants import HWCentralEnv
from hwcentral import settings
from hwcentral.exceptions import InvalidStateError
from hwcentral.settings import PROJECT_ROOT
from scripts.database.enforcer import enforcer_check
from scripts.fixtures.dump_data import snapshot_db, dump_db
from scripts.setup.assignment import setup_assignment

with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'question_bank_reloader_config.json'), 'r') as f:
    CONFIG = json.load(f)

HOME_DIR = os.path.expanduser('~')
VAULT_CONTENT_PATH = os.path.join(HOME_DIR, 'hwcentral-vault', 'content')
OUTPUT_CABINET_PATH = os.path.join(HOME_DIR, 'hwcentral-cabinet')

DUMPFILE_DIR = os.path.join(PROJECT_ROOT, 'core', 'fixtures', 'qb')


def trim_qb_dump(outfile, start_aql_id):
    trim_chapter = 0
    trim_questiontag = 0
    trim_question = 0
    trim_questionsubpart = 0
    trim_assignmentquestionslist = 0

    if start_aql_id > 1:
        # get the trim limits for all models by looking at the dump file for the previous aql id (if it exists)
        prev_aql_id = start_aql_id - 1
        for file in os.listdir(DUMPFILE_DIR):
            if (file == str(prev_aql_id) + '.json') or ('to' + str(prev_aql_id) + '.json' in file):
                with open(os.path.join(DUMPFILE_DIR, file), 'r') as f:
                    prev_dump = json.load(f)
                    break
        else:
            raise InvalidStateError("Previous aql %s dump file not found" % prev_aql_id)

        # find max values for each model. These will be the trim values
        for elem in prev_dump:
            elem_model = elem["model"]
            elem_pk = elem["pk"]

            if elem_model == "core.chapter":
                if elem_pk > trim_chapter:
                    trim_chapter = elem_pk

            elif elem_model == "core.questiontag":
                if elem_pk > trim_questiontag:
                    trim_questiontag = elem_pk

            elif elem_model == "core.question":
                if elem_pk > trim_question:
                    trim_question = elem_pk

            elif elem_model == "core.questionsubpart":
                if elem_pk > trim_questionsubpart:
                    trim_questionsubpart = elem_pk

            elif elem_model == "core.assignmentquestionslist":
                if elem_pk > trim_assignmentquestionslist:
                    trim_assignmentquestionslist = elem_pk

            else:
                raise InvalidStateError("Unexpected model %s in qb dump" % elem_model)

    with open(outfile, 'r') as f:
        qb_dump = json.load(f)
    trimmed_qb_dump = []

    for elem in qb_dump:
        elem_model = elem["model"]
        elem_pk = elem["pk"]
        if elem_model == "core.chapter":
            if elem_pk > trim_chapter:
                trimmed_qb_dump.append(elem)

        elif elem_model == "core.questiontag":
            if elem_pk > trim_questiontag:
                trimmed_qb_dump.append(elem)

        elif elem_model == "core.question":
            if elem_pk > trim_question:
                trimmed_qb_dump.append(elem)

        elif elem_model == "core.questionsubpart":
            if elem_pk > trim_questionsubpart:
                trimmed_qb_dump.append(elem)

        elif elem_model == "core.assignmentquestionslist":
            if elem_pk > trim_assignmentquestionslist:
                trimmed_qb_dump.append(elem)

        else:
            raise InvalidStateError("Unexpected model %s in qb dump" % elem_model)

    with open(outfile, 'w') as f:
        json.dump(trimmed_qb_dump, f, indent=4)


def build_dumpfile_name(aql_ids):
    if len(aql_ids) == 1:
        dumpfile_name = str(aql_ids[0])
    else:
        dumpfile_name = str(aql_ids[0]) + 'to' + str(
            aql_ids[-1])

    return os.path.join(DUMPFILE_DIR, dumpfile_name + '.json')


def process_block(question_bank_block):
    # first add the chapters
    for chapter in question_bank_block['chapters']:
        new_chapter = Chapter(name=chapter)
        new_chapter.save()

    # now use the assignment setup script to set up the aql and its dependencies
    aql_ids = []
    for assignment in question_bank_block['assignments']:
        try:
            assignment_chapter = Chapter.objects.get(name=assignment['chapter'])
        except Chapter.DoesNotExist:
            # create new chapter entry
            new_chapter = Chapter(name=assignment['chapter'])
            new_chapter.save()
            assignment_chapter = new_chapter

        aql_id = setup_assignment(
            VAULT_CONTENT_PATH,
            OUTPUT_CABINET_PATH,
            question_bank_block['board'],
            question_bank_block['school'],
            question_bank_block['standard'],
            question_bank_block['subject'],
            assignment_chapter.pk,
            assignment['number']
        )

        aql_ids.append(aql_id)

    # now dump the changes made to the database selectively to the right file
    outfile = build_dumpfile_name(aql_ids)
    dump_db(outfile, ['core.chapter', 'core.questiontag', 'core.question', 'core.questionsubpart',
                      'core.assignmentquestionslist'])

    # trim the file to only contain data relevant to the current block
    return trim_qb_dump(outfile, aql_ids[0])


def run():
    assert settings.ENVIRON == HWCentralEnv.LOCAL

    snapshot_db()

    # first truncate the questiontag, question, chapter and aql tables
    # flush full database and start from clean state
    call_command('flush', '--noinput')
    call_command('loaddata', 'skeleton')
    call_command('loaddata', 'qa_school')

    # now reload the entire config
    total_skipped_assignments = 0
    for i in xrange(len(CONFIG['blocks'])):
        block = CONFIG['blocks'][i]
        if block == "new_blocks_below":
            break
        else:
            total_skipped_assignments += len(block['assignments'])
            print 'skipping block'

    # load skipped blocks into db
    print 'loading %s skipped assignments into db' % total_skipped_assignments
    collected_assignments = 0
    collected_fixtures = []
    for file in os.listdir(DUMPFILE_DIR):
        file_aqls = os.path.splitext(file)[0].split('to')
        aql_start = int(file_aqls[0])
        aql_end = int(file_aqls[-1])
        if aql_start <= aql_end and aql_end <= total_skipped_assignments:
            fixture_path = os.path.join('qb', file)
            collected_fixtures.append((aql_start, fixture_path))
            collected_assignments += (aql_end - aql_start) + 1

    assert collected_assignments == total_skipped_assignments
    for fixture in sorted(collected_fixtures, key=lambda t: t[0]):
        call_command('loaddata', fixture[1])

    for j in xrange(i + 1, len(CONFIG['blocks'])):
        process_block(CONFIG['blocks'][j])

    enforcer_check()
