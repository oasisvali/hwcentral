# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'Submission', fields ['path']
        db.delete_unique(u'core_submission', ['path'])

        # Deleting model 'ClassroomAccessLevel'
        db.delete_table(u'core_classroomaccesslevel')

        # Deleting model 'Topic'
        db.delete_table(u'core_topic')

        # Deleting model 'AssignmentType'
        db.delete_table(u'core_assignmenttype')

        # Adding model 'Chapter'
        db.create_table(u'core_chapter', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'core', ['Chapter'])

        # Adding model 'Question'
        db.create_table(u'core_question', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.School'])),
            ('standard', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
            ('chapter', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Chapter'])),
            ('conf', self.gf('django.db.models.fields.FilePathField')(path='/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/questions', max_length=255, match='\\d+\\.xml')),
        ))
        db.send_create_signal(u'core', ['Question'])

        # Adding model 'SubjectRoom'
        db.create_table(u'core_subjectroom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('classRoom', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ClassRoom'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='subjects_managed_set', to=orm['auth.User'])),
        ))
        db.send_create_signal(u'core', ['SubjectRoom'])

        # Adding M2M table for field students on 'SubjectRoom'
        m2m_table_name = db.shorten_name(u'core_subjectroom_students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('subjectroom', models.ForeignKey(orm[u'core.subjectroom'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['subjectroom_id', 'user_id'])

        # Adding model 'Home'
        db.create_table(u'core_home', (
            ('parent', self.gf('django.db.models.fields.related.ForeignKey')(related_name='homes_managed_set', primary_key=True, to=orm['auth.User'])),
        ))
        db.send_create_signal(u'core', ['Home'])

        # Adding M2M table for field children on 'Home'
        m2m_table_name = db.shorten_name(u'core_home_children')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('home', models.ForeignKey(orm[u'core.home'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['home_id', 'user_id'])

        # Deleting field 'Classroom.access'
        db.delete_column(u'core_classroom', 'access_id')

        # Deleting field 'Classroom.teacher'
        db.delete_column(u'core_classroom', 'teacher_id')

        # Deleting field 'Classroom.created'
        db.delete_column(u'core_classroom', 'created')

        # Deleting field 'Classroom.subject'
        db.delete_column(u'core_classroom', 'subject_id')

        # Adding field 'ClassRoom.division'
        db.add_column(u'core_classroom', 'division',
                      self.gf('django.db.models.fields.CharField')(default=1, max_length=255),
                      keep_default=False)

        # Adding field 'ClassRoom.classTeacher'
        db.add_column(u'core_classroom', 'classTeacher',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, related_name='classes_managed_set', to=orm['auth.User']),
                      keep_default=False)

        # Deleting field 'Assignment.classroom'
        db.delete_column(u'core_assignment', 'classroom_id')

        # Deleting field 'Assignment.assignmentType'
        db.delete_column(u'core_assignment', 'assignmentType_id')

        # Deleting field 'Assignment.duration'
        db.delete_column(u'core_assignment', 'duration')

        # Deleting field 'Assignment.path'
        db.delete_column(u'core_assignment', 'path')

        # Adding field 'Assignment.chapter'
        db.add_column(u'core_assignment', 'chapter',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Chapter']),
                      keep_default=False)

        # Adding field 'Assignment.subjectRoom'
        db.add_column(u'core_assignment', 'subjectRoom',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.SubjectRoom']),
                      keep_default=False)

        # Adding field 'Assignment.conf'
        db.add_column(u'core_assignment', 'conf',
                      self.gf('django.db.models.fields.FilePathField')(default=1, path='/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/assignments', max_length=255, match='\\d+\\.xml'),
                      keep_default=False)

        # Removing M2M table for field topics on 'Assignment'
        db.delete_table(db.shorten_name(u'core_assignment_topics'))

        # Adding M2M table for field questions on 'Assignment'
        m2m_table_name = db.shorten_name(u'core_assignment_questions')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('assignment', models.ForeignKey(orm[u'core.assignment'], null=False)),
            ('question', models.ForeignKey(orm[u'core.question'], null=False))
        ))
        db.create_unique(m2m_table_name, ['assignment_id', 'question_id'])

        # Deleting field 'Submission.assigment'
        db.delete_column(u'core_submission', 'assigment_id')

        # Deleting field 'Submission.grade'
        db.delete_column(u'core_submission', 'grade')

        # Adding field 'Submission.assignment'
        db.add_column(u'core_submission', 'assignment',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Assignment']),
                      keep_default=False)

        # Adding field 'Submission.marks'
        db.add_column(u'core_submission', 'marks',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)


        # Changing field 'Submission.path'
        db.alter_column(u'core_submission', 'path', self.gf('django.db.models.fields.FilePathField')(path='/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/submissions', max_length=255, match='\\d+\\.xml'))
        # Deleting field 'School.phone'
        db.delete_column(u'core_school', 'phone')

        # Deleting field 'School.address'
        db.delete_column(u'core_school', 'address')

        # Deleting field 'School.registered'
        db.delete_column(u'core_school', 'registered')

        # Deleting field 'UserInfo.home'
        db.delete_column(u'core_userinfo', 'home')


    def backwards(self, orm):
        # Adding model 'ClassroomAccessLevel'
        db.create_table(u'core_classroomaccesslevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal(u'core', ['ClassroomAccessLevel'])

        # Adding model 'Topic'
        db.create_table(u'core_topic', (
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal(u'core', ['Topic'])

        # Adding model 'AssignmentType'
        db.create_table(u'core_assignmenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal(u'core', ['AssignmentType'])

        # Deleting model 'Chapter'
        db.delete_table(u'core_chapter')

        # Deleting model 'Question'
        db.delete_table(u'core_question')

        # Deleting model 'SubjectRoom'
        db.delete_table(u'core_subjectroom')

        # Removing M2M table for field students on 'SubjectRoom'
        db.delete_table(db.shorten_name(u'core_subjectroom_students'))

        # Deleting model 'Home'
        db.delete_table(u'core_home')

        # Removing M2M table for field children on 'Home'
        db.delete_table(db.shorten_name(u'core_home_children'))


        # User chose to not deal with backwards NULL issues for 'Classroom.access'
        raise RuntimeError("Cannot reverse this migration. 'Classroom.access' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Classroom.access'
        db.add_column(u'core_classroom', 'access',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ClassroomAccessLevel']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Classroom.teacher'
        raise RuntimeError("Cannot reverse this migration. 'Classroom.teacher' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Classroom.teacher'
        db.add_column(u'core_classroom', 'teacher',
                      self.gf('django.db.models.fields.related.ForeignKey')(related_name='classes_managed_set', to=orm['auth.User']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Classroom.created'
        raise RuntimeError("Cannot reverse this migration. 'Classroom.created' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Classroom.created'
        db.add_column(u'core_classroom', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Classroom.subject'
        raise RuntimeError("Cannot reverse this migration. 'Classroom.subject' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Classroom.subject'
        db.add_column(u'core_classroom', 'subject',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject']),
                      keep_default=False)

        # Deleting field 'ClassRoom.division'
        db.delete_column(u'core_classroom', 'division')

        # Deleting field 'ClassRoom.classTeacher'
        db.delete_column(u'core_classroom', 'classTeacher_id')


        # User chose to not deal with backwards NULL issues for 'Assignment.classroom'
        raise RuntimeError("Cannot reverse this migration. 'Assignment.classroom' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Assignment.classroom'
        db.add_column(u'core_assignment', 'classroom',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Classroom']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Assignment.assignmentType'
        raise RuntimeError("Cannot reverse this migration. 'Assignment.assignmentType' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Assignment.assignmentType'
        db.add_column(u'core_assignment', 'assignmentType',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.AssignmentType']),
                      keep_default=False)

        # Adding field 'Assignment.duration'
        db.add_column(u'core_assignment', 'duration',
                      self.gf('django.db.models.fields.TimeField')(null=True),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Assignment.path'
        raise RuntimeError("Cannot reverse this migration. 'Assignment.path' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Assignment.path'
        db.add_column(u'core_assignment', 'path',
                      self.gf('django.db.models.fields.FilePathField')(max_length=255, path='/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/assignments', unique=True, recursive=True, match='assignment_\\d+\\.xml'),
                      keep_default=False)

        # Deleting field 'Assignment.chapter'
        db.delete_column(u'core_assignment', 'chapter_id')

        # Deleting field 'Assignment.subjectRoom'
        db.delete_column(u'core_assignment', 'subjectRoom_id')

        # Deleting field 'Assignment.conf'
        db.delete_column(u'core_assignment', 'conf')

        # Adding M2M table for field topics on 'Assignment'
        m2m_table_name = db.shorten_name(u'core_assignment_topics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('assignment', models.ForeignKey(orm[u'core.assignment'], null=False)),
            ('topic', models.ForeignKey(orm[u'core.topic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['assignment_id', 'topic_id'])

        # Removing M2M table for field questions on 'Assignment'
        db.delete_table(db.shorten_name(u'core_assignment_questions'))


        # User chose to not deal with backwards NULL issues for 'Submission.assigment'
        raise RuntimeError("Cannot reverse this migration. 'Submission.assigment' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'Submission.assigment'
        db.add_column(u'core_submission', 'assigment',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Assignment']),
                      keep_default=False)

        # Adding field 'Submission.grade'
        db.add_column(u'core_submission', 'grade',
                      self.gf('django.db.models.fields.FloatField')(null=True),
                      keep_default=False)

        # Deleting field 'Submission.assignment'
        db.delete_column(u'core_submission', 'assignment_id')

        # Deleting field 'Submission.marks'
        db.delete_column(u'core_submission', 'marks')


        # Changing field 'Submission.path'
        db.alter_column(u'core_submission', 'path', self.gf('django.db.models.fields.FilePathField')(max_length=255, path='/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/submissions', unique=True, recursive=True, match='submission_\\d+\\.xml'))
        # Adding unique constraint on 'Submission', fields ['path']
        db.create_unique(u'core_submission', ['path'])


        # User chose to not deal with backwards NULL issues for 'School.phone'
        raise RuntimeError("Cannot reverse this migration. 'School.phone' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'School.phone'
        db.add_column(u'core_school', 'phone',
                      self.gf('django.db.models.fields.CharField')(max_length=255),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'School.address'
        raise RuntimeError("Cannot reverse this migration. 'School.address' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'School.address'
        db.add_column(u'core_school', 'address',
                      self.gf('django.db.models.fields.TextField')(),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'School.registered'
        raise RuntimeError("Cannot reverse this migration. 'School.registered' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration        # Adding field 'School.registered'
        db.add_column(u'core_school', 'registered',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True),
                      keep_default=False)

        # Adding field 'UserInfo.home'
        db.add_column(u'core_userinfo', 'home',
                      self.gf('django.db.models.fields.PositiveIntegerField')(default=0),
                      keep_default=False)


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.assignment': {
            'Meta': {'object_name': 'Assignment'},
            'assigned': ('django.db.models.fields.DateTimeField', [], {}),
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Chapter']"}),
            'conf': ('django.db.models.fields.FilePathField', [], {'path': "'/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/assignments'", 'max_length': '255', 'match': "'\\\\d+\\\\.xml'"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'questions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['core.Question']", 'symmetrical': 'False'}),
            'subjectRoom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.SubjectRoom']"})
        },
        u'core.board': {
            'Meta': {'object_name': 'Board'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.chapter': {
            'Meta': {'object_name': 'Chapter'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.classroom': {
            'Meta': {'object_name': 'ClassRoom'},
            'classTeacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'classes_managed_set'", 'to': u"orm['auth.User']"}),
            'division': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.School']"}),
            'standard': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'classes_enrolled_set'", 'symmetrical': 'False', 'to': u"orm['auth.User']"})
        },
        u'core.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.home': {
            'Meta': {'object_name': 'Home'},
            'children': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'homes_enrolled_set'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'parent': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'homes_managed_set'", 'primary_key': 'True', 'to': u"orm['auth.User']"})
        },
        u'core.question': {
            'Meta': {'object_name': 'Question'},
            'chapter': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Chapter']"}),
            'conf': ('django.db.models.fields.FilePathField', [], {'path': "'/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/questions'", 'max_length': '255', 'match': "'\\\\d+\\\\.xml'"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.School']"}),
            'standard': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Subject']"})
        },
        u'core.school': {
            'Meta': {'object_name': 'School'},
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Board']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.subject': {
            'Meta': {'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.subjectroom': {
            'Meta': {'object_name': 'SubjectRoom'},
            'classRoom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ClassRoom']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'students': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'subjects_enrolled_set'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Subject']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'subjects_managed_set'", 'to': u"orm['auth.User']"})
        },
        u'core.submission': {
            'Meta': {'object_name': 'Submission'},
            'assignment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Assignment']"}),
            'completion': ('django.db.models.fields.FloatField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'marks': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            'path': ('django.db.models.fields.FilePathField', [], {'path': "'/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/submissions'", 'max_length': '255', 'match': "'\\\\d+\\\\.xml'"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Group']"}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.School']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        }
    }

    complete_apps = ['core']