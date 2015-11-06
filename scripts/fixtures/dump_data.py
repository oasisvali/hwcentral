from django.core.management import call_command

DB_DUMP_FILE = 'db_dump.json'
STANDARD_OPTIONS = [    # append apps/models you want to dump
    '--natural-foreign',
    '--indent', '4',
    '--exclude', 'sessions',
    '--exclude', 'admin',
    '--exclude', 'auth.permission',
    '--output' # append output file
]


def dump_db(outfile=DB_DUMP_FILE, to_dump=['core', 'auth', 'sites', 'concierge']):
    # making copy of db state - the cabinet files can be rolled back easily through git but dont want to be left with a
    # corrupted db in case anything fails TODO: probably the right thing to do is use db transactions
    print 'Dumping db state to', outfile
    params = to_dump + STANDARD_OPTIONS + [outfile]
    call_command('dumpdata', *params)


def run():
    dump_db()


def snapshot_db():
    dump_db('db_snapshot.json')
