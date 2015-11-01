from django.core.management import call_command

DB_DUMP_FILE = 'db_dump.json'


def dump_db(outfile=DB_DUMP_FILE):
    # making copy of db state - the cabinet files can be rolled back easily through git but dont want to be left with a
    # corrupted db in case anything fails TODO: probably the right thing to do is use db transactions
    print 'Dumping db state to', outfile
    call_command('dumpdata', 'core', 'auth', 'sites', 'concierge', '--natural-foreign', '--indent', '4', '--exclude',
                 'sessions', '--exclude', 'admin', '--exclude', 'auth.permission', '--output', outfile)


def run():
    dump_db()


def snapshot_db():
    dump_db('db_snapshot.json')
