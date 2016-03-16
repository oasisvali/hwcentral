import argparse

from django.core.management import call_command

from scripts.email.hwcentral_users import runscript_args_workaround

STANDARD_OPTIONS = [  # append apps/models you want to dump
    '--natural-foreign',
    '--indent', '4',
    '--exclude', 'sessions',
    '--exclude', 'admin',
    '--exclude', 'auth.permission',
    '--output'  # append output file
]

ALL_APPS = [  # list of all hwcentral apps that have db models
    'core',
    'auth',
    'sites',
    'concierge',
    'ink',
    'edge',
    'focus',
    'lodge'
]


def dump_db(outfile, to_dump=ALL_APPS):
    # making copy of db state - the cabinet files can be rolled back easily through git but dont want to be left with a
    # corrupted db in case anything fails TODO: probably the right thing to do is use db transactions
    print 'Dumping db state to', outfile
    params = to_dump + STANDARD_OPTIONS + [outfile]
    call_command('dumpdata', *params)


def run(*args):
    parser = argparse.ArgumentParser(description="Dump the entire database to a fixture")
    parser.add_argument('--outfile', '-o',
                        help="path to the output fixture file",
                        required=True)

    argv = runscript_args_workaround(args)
    processed_args = parser.parse_args(argv)
    print 'Running with args:', processed_args
    dump_db(processed_args.outfile)


def snapshot_db():
    dump_db('db_snapshot.json')
