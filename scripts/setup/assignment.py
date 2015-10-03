# to use this script, run following command from the terminal
# python manage.py runscript scripts.setup.assignment -v3
# --script-args="#r <path-to-root-folder> #b board_id #s school_id #t standard_number #j subject_id #n aql_number #o <path-to-cabinet-repo>"

# This script can be used to set up a complete assignment (AQL according to core terminology)
#
# It requires the AQL's data files to be in the GDrive structure - These are treated as READ-ONLY by this script
#     - <root-folder>/<board-id>/<school-id>/><standard-number>/<subject-id>/
#         -{aql-number}.json {along with img folder}
#         -<chapter-id>/
#               -subparts/{subparts numbered 1+.json along with img folder}
#               -containers/{containers numbered 1+.json along with img folder}
#
# The output from this script ends up in the cabinet git repo it is pointed to. The additions (to the cabinet) are:
#     - <repo-root>/
#           -aql_meta/<board-id>/<school-id>/><standard-number>/<subject-id>/{aql-pk}.json  w/img
#           -questions/
#                   -containers/<board-id>/<school-id>/<standard-id>/<subject-id>/<chapter-id>/{question-pk.json} w/ img
#                   -raw/<board-id>/<school-id>/<standard-id>/<subject-id>/<chapter-id>/{original-subpart-number.json} w/ img
#

import argparse
import json
import os
import shutil

from PIL import Image
from django.core.management import call_command

from core.models import AssignmentQuestionsList, Board, School, Standard, Subject, Question, Chapter, QuestionTag
from core.utils.json import dump_json_string
from scripts.database import enforcer
from scripts.database.enforcer import get_aql_uid
from scripts.database.enforcer_exceptions import EnforcerError
from scripts.email.hwcentral_users import runscript_args_workaround

DATA_FILE_EXT = '.json'
IMG_FILE_EXT = '.png'
IMG_DIR = 'img'
DB_DUMP_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'db_dump' + DATA_FILE_EXT)


def aql_data_raw_process(aql_data_raw):
    return aql_data_raw


def aql_data_process(aql_data):
    return aql_data


def question_container_data_raw_process(question_container_data_raw):
    return question_container_data_raw


def question_container_data_process(question_container_data):
    return question_container_data


def question_subpart_data_raw_process(question_subpart_data_raw):
    return question_subpart_data_raw


def question_subpart_data_process(question_subpart_data):
    return question_subpart_data


def get_aql_data_for_cabinet(aql_data):
    return {
        "revision": aql_data["revision"]
    }


def copy_img_folder(src_dir, dest_dir):
    # first check if src dir has img dir
    src_dir = os.path.join(src_dir, IMG_DIR)
    if not os.path.exists(src_dir):
        return

    # make the destination img directory
    dest_dir = os.path.join(dest_dir, IMG_DIR)

    try:
        shutil.rmtree(dest_dir)  # remove the existing img dir, start from scratch
    except OSError:
        pass  # directory did not exist
    os.makedirs(dest_dir)

    # loop through all the images in the src dir, apply watermark and save them in dest dir
    for img in os.listdir(src_dir):
        src_img_path = os.path.join(src_dir, img)
        src_img = Image.open(src_img_path)
        # dest_img = watermark(src_img)
        dest_img = src_img
        dest_img.save(os.path.join(dest_dir, os.path.splitext(img)[0] + IMG_FILE_EXT), "png")

    return


def add_question_tags(new_question, tags):
    # for every tag in tags, check if the tag exists, if it does, just associate the new question with it
    # if it does not exist, create a new tag in the database and associate the new question with it

    for tag in tags:
        tag_name = tag.lower()
        try:
            tag_db = QuestionTag.objects.get(name=tag_name)
        except QuestionTag.DoesNotExist:
            tag_db = QuestionTag(name=tag_name)
            tag_db.save()

        new_question.tags.add(tag_db)


def get_question_container_data_for_cabinet(question_container_data):
    return {
        "hint": question_container_data.get("hint"),
        "content": question_container_data.get("content"),
        "subparts": question_container_data["subparts"]
    }


def get_question_subpart_data_for_cabinet(question_subpart_data):
    return question_subpart_data


def run(*args):
    parser = argparse.ArgumentParser(description="Load an AQL into the system")
    parser.add_argument('--root', '-r',
                        help="full path to the root folder where the data files are located in GDrive format",
                        required=True)
    parser.add_argument('--board', '-b', type=long, help="board id for the new aql", required=True)
    parser.add_argument('--school', '-s', type=long, help="school id for the new aql", required=True)
    parser.add_argument('--standard', '-t', type=int, help="standard number for the new aql", required=True)
    parser.add_argument('--subject', '-j', type=long, help="subject id for the new aql", required=True)
    parser.add_argument('--number', '-n', type=int, help="filename for the new aql's metadata file in the raw cabinet",
                        required=True)
    parser.add_argument('--output', '-o',
                        help='full path to the hwcentral-cabinet repository where the processed data files are put in cabinet format',
                        required=True)

    argv = runscript_args_workaround(args)
    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args

    # first validate the arguments against the exiting database
    board = Board.objects.get(pk=processed_args.board)
    school = School.objects.get(pk=processed_args.school)
    standard = Standard.objects.get(number=processed_args.standard)
    subject = Subject.objects.get(pk=processed_args.subject)

    # making copy of db state - the cabinet files can be rolled back easily through git but dont want to be left with a
    # corrupted db in case anything fails TODO: probably the right thing to do is use db transactions
    print 'Dumping db state to', DB_DUMP_FILE
    call_command('dumpdata', 'core', 'auth', 'sites', 'concierge', '--natural-foreign', '--indent', '4', '--exclude',
                 'sessions', '--exclude', 'admin', '--exclude', 'auth.permission', '--output', DB_DUMP_FILE)

    # build path to aql data file
    aql_data_file_dir = os.path.join(
        processed_args.root,
        str(processed_args.board),
        str(processed_args.school),
        str(processed_args.standard),
        str(processed_args.subject)
    )
    aql_data_file_path = os.path.join(
        aql_data_file_dir,
        str(processed_args.number) + DATA_FILE_EXT
    )

    with open(aql_data_file_path, 'r') as f:
        aql_data_raw = f.read().strip()

    print 'Processing AQL data'
    aql_data_raw = aql_data_raw_process(aql_data_raw)
    aql_data = json.loads(aql_data_raw)
    aql_data = aql_data_process(aql_data)

    # aql data has revision, questions and description
    # transfer the revision, put the description in db and then deal with the questions
    print 'Creating new AQL in db'
    new_aql = AssignmentQuestionsList(school=school, standard=standard, subject=subject,
                                      number=1,  # this will be validated at the end
                                      description=aql_data['description'])
    new_aql.save()

    print 'Putting AQL metadata into cabinet'
    aql_output_dir = os.path.join(
        processed_args.output,
        'aql_meta',
        str(processed_args.board),
        str(processed_args.school),
        str(processed_args.standard),
        str(processed_args.subject)
    )

    try:
        os.makedirs(aql_output_dir)
    except OSError:
        # the output dir already exists, no need to do anything
        pass
    with open(os.path.join(aql_output_dir, str(new_aql.pk) + DATA_FILE_EXT), 'w') as f:
        f.write(dump_json_string(get_aql_data_for_cabinet(aql_data)))

    # finally, copy over the img folder too - and apply watermarks
    print 'Copying AQL images'
    copy_img_folder(aql_data_file_dir, aql_output_dir)

    # now lets grab the question data too

    questions = aql_data['questions']
    question_data_file_path_stub = os.path.join(
        processed_args.root,
        str(processed_args.board),
        str(processed_args.school),
        str(processed_args.standard),
        str(processed_args.subject)
    )

    for chapter_block in questions:
        chapter_id = chapter_block['chapter']
        print 'Encountered chapter id:', chapter_id
        chapter = Chapter.objects.get(pk=chapter_id)

        question_data_file_path_stub_with_chapter = os.path.join(question_data_file_path_stub, str(chapter.pk))
        question_container_data_file_path_stub = os.path.join(question_data_file_path_stub_with_chapter, 'containers')
        question_subpart_data_file_path_stub = os.path.join(question_data_file_path_stub_with_chapter, 'subparts')

        print 'Prepping output dirs in cabinet for question metadata files'
        question_container_output_dir = os.path.join(
            processed_args.output,
            'questions', 'containers',
            str(processed_args.board),
            str(processed_args.school),
            str(processed_args.standard),
            str(processed_args.subject),
            str(chapter.pk)
        )

        try:
            os.makedirs(question_container_output_dir)
        except OSError:
            # the output dir already exists, no need to do anything
            pass

        question_subpart_output_dir = os.path.join(
            processed_args.output,
            'questions', 'raw',
            str(processed_args.board),
            str(processed_args.school),
            str(processed_args.standard),
            str(processed_args.subject),
            str(chapter.pk)
        )

        try:
            os.makedirs(question_subpart_output_dir)
        except OSError:
            # the output dir already exists, no need to do anything
            pass

        for question in chapter_block['numbers']:
            print 'Processing data for question:', question
            question_container_data_file_path = os.path.join(question_container_data_file_path_stub,
                                                             str(question) + DATA_FILE_EXT)

            with open(question_container_data_file_path, 'r') as f:
                question_container_data_raw = f.read().strip()

            question_container_data_raw = question_container_data_raw_process(question_container_data_raw)
            question_container_data = json.loads(question_container_data_raw)
            question_container_data = question_container_data_process(question_container_data)

            # question container data has subparts and tags (and other metadata which is to be carried over into cabinet)
            print 'Creating new question in db'
            new_question = Question(school=school, standard=standard, subject=subject, chapter=chapter)
            new_question.save()
            add_question_tags(new_question, question_container_data['tags'])

            print "Adding newly created question to new AQL's question list"
            new_aql.questions.add(new_question)

            with open(os.path.join(question_container_output_dir, str(new_question.pk) + DATA_FILE_EXT), 'w') as f:
                f.write(dump_json_string(get_question_container_data_for_cabinet(question_container_data)))

            # now lets handle the subparts for this question
            subparts = question_container_data['subparts']
            for subpart in subparts:
                print 'Processing data for subpart:', subpart
                question_subpart_data_file_path = os.path.join(question_subpart_data_file_path_stub,
                                                               str(subpart) + DATA_FILE_EXT)

                with open(question_subpart_data_file_path, 'r') as f:
                    question_subpart_data_raw = f.read().strip()

                question_subpart_data_raw = question_subpart_data_raw_process(question_subpart_data_raw)
                question_subpart_data = json.loads(question_subpart_data_raw)
                question_subpart_data = question_subpart_data_process(question_subpart_data)

                with open(os.path.join(question_subpart_output_dir, str(subpart) + DATA_FILE_EXT), 'w') as f:
                    f.write(dump_json_string(get_question_subpart_data_for_cabinet(question_subpart_data)))

        # finally, copy over the img folder too - and apply watermarks - do this at chapter level only to avoid repetition
        print 'Copying container images'
        copy_img_folder(question_container_data_file_path_stub, question_container_output_dir)
        print 'Copying subpart images'
        copy_img_folder(question_subpart_data_file_path_stub, question_subpart_output_dir)

    # now validate the number of the aql we just created in the db
    new_aql_uid = get_aql_uid(new_aql)
    while True:
        for aql in AssignmentQuestionsList.objects.exclude(pk=new_aql.pk):
            if get_aql_uid(aql) == new_aql_uid:
                new_aql.number += 1
                new_aql.save()
                new_aql_uid = get_aql_uid(new_aql)
                break
        else:  # read as no-break
            print 'Settled on number %s for new aql' % new_aql.number
            break

    # run enforcer script at the end
    print 'Running enforcer script'
    try:
        enforcer.run()
    except EnforcerError, e:
        print str(e)
        print
        print 'The enforcer encountered errors! Rolling back the db to original state...'
        call_command('flush', '--noinput')
        call_command('loaddata', DB_DUMP_FILE)
        print 'Remember to rollback the cabinet repo before running this setup script again'
