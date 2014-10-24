# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Adding model 'Group'
        db.create_table(u'core_group', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'core', ['Group'])

        # Adding model 'Board'
        db.create_table(u'core_board', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'core', ['Board'])

        # Adding model 'Subject'
        db.create_table(u'core_subject', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'core', ['Subject'])

        # Adding model 'AssignmentType'
        db.create_table(u'core_assignmenttype', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'core', ['AssignmentType'])

        # Adding model 'ClassAccessLevel'
        db.create_table(u'core_classaccesslevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'core', ['ClassAccessLevel'])

        # Adding model 'School'
        db.create_table(u'core_school', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('board', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Board'])),
            ('admin', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('registered', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('address', self.gf('django.db.models.fields.TextField')()),
            ('phone', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'core', ['School'])

        # Adding model 'UserInfo'
        db.create_table(u'core_userinfo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['auth.User'], unique=True)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Group'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.School'])),
        ))
        db.send_create_signal(u'core', ['UserInfo'])

        # Adding model 'Topic'
        db.create_table(u'core_topic', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
        ))
        db.send_create_signal(u'core', ['Topic'])

        # Adding model 'Class'
        db.create_table(u'core_class', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ClassAccessLevel'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.School'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('standard', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='classes_managed_set',
                                                                              to=orm['auth.User'])),
        ))
        db.send_create_signal(u'core', ['Class'])

        # Adding M2M table for field students on 'Class'
        m2m_table_name = db.shorten_name(u'core_class_students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('class', models.ForeignKey(orm[u'core.class'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['class_id', 'user_id'])

        # Adding model 'Assignment'
        db.create_table(u'core_assignment', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('assigned', self.gf('django.db.models.fields.DateTimeField')()),
            ('due', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('duration', self.gf('django.db.models.fields.TimeField')(null=True)),
            ('path', self.gf('django.db.models.fields.FilePathField')(
                path='/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/assignments', unique=True,
                max_length=255, recursive=True, match='assignment_\\d+\\.xml')),
            ('_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.AssignmentType'])),
            ('_class', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Class'])),
        ))
        db.send_create_signal(u'core', ['Assignment'])

        # Adding M2M table for field topics on 'Assignment'
        m2m_table_name = db.shorten_name(u'core_assignment_topics')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('assignment', models.ForeignKey(orm[u'core.assignment'], null=False)),
            ('topic', models.ForeignKey(orm[u'core.topic'], null=False))
        ))
        db.create_unique(m2m_table_name, ['assignment_id', 'topic_id'])

        # Adding model 'Submission'
        db.create_table(u'core_submission', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('assigment', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Assignment'])),
            ('student', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('grade', self.gf('django.db.models.fields.FloatField')(null=True)),
            ('timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('completion', self.gf('django.db.models.fields.FloatField')()),
            ('path', self.gf('django.db.models.fields.FilePathField')(
                path='/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/submissions', unique=True,
                max_length=255, recursive=True, match='submission_\\d+\\.xml')),
        ))
        db.send_create_signal(u'core', ['Submission'])


    def backwards(self, orm):
        # Deleting model 'Group'
        db.delete_table(u'core_group')

        # Deleting model 'Board'
        db.delete_table(u'core_board')

        # Deleting model 'Subject'
        db.delete_table(u'core_subject')

        # Deleting model 'AssignmentType'
        db.delete_table(u'core_assignmenttype')

        # Deleting model 'ClassAccessLevel'
        db.delete_table(u'core_classaccesslevel')

        # Deleting model 'School'
        db.delete_table(u'core_school')

        # Deleting model 'UserInfo'
        db.delete_table(u'core_userinfo')

        # Deleting model 'Topic'
        db.delete_table(u'core_topic')

        # Deleting model 'Class'
        db.delete_table(u'core_class')

        # Removing M2M table for field students on 'Class'
        db.delete_table(db.shorten_name(u'core_class_students'))

        # Deleting model 'Assignment'
        db.delete_table(u'core_assignment')

        # Removing M2M table for field topics on 'Assignment'
        db.delete_table(db.shorten_name(u'core_assignment_topics'))

        # Deleting model 'Submission'
        db.delete_table(u'core_submission')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [],
                            {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')",
                     'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': (
                'django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [],
                       {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [],
                                 {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)",
                     'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'core.assignment': {
            'Meta': {'object_name': 'Assignment'},
            '_class': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Class']"}),
            '_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AssignmentType']"}),
            'assigned': ('django.db.models.fields.DateTimeField', [], {}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'due': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'duration': ('django.db.models.fields.TimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.FilePathField', [],
                     {'path': "'/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/assignments'",
                      'unique': 'True', 'max_length': '255', 'recursive': 'True',
                      'match': "'assignment_\\\\d+\\\\.xml'"}),
            'topics': (
                'django.db.models.fields.related.ManyToManyField', [],
                {'to': u"orm['core.Topic']", 'symmetrical': 'False'})
        },
        u'core.assignmenttype': {
            'Meta': {'object_name': 'AssignmentType'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.board': {
            'Meta': {'object_name': 'Board'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.class': {
            'Meta': {'object_name': 'Class'},
            'access': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ClassAccessLevel']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.School']"}),
            'standard': ('django.db.models.fields.PositiveIntegerField', [], {}),
            'students': ('django.db.models.fields.related.ManyToManyField', [],
                         {'related_name': "'classes_enrolled_set'", 'symmetrical': 'False', 'to': u"orm['auth.User']"}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Subject']"}),
            'teacher': ('django.db.models.fields.related.ForeignKey', [],
                        {'related_name': "'classes_managed_set'", 'to': u"orm['auth.User']"})
        },
        u'core.classaccesslevel': {
            'Meta': {'object_name': 'ClassAccessLevel'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.school': {
            'Meta': {'object_name': 'School'},
            'address': ('django.db.models.fields.TextField', [], {}),
            'admin': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'board': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Board']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'registered': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.subject': {
            'Meta': {'object_name': 'Subject'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'core.submission': {
            'Meta': {'object_name': 'Submission'},
            'assigment': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Assignment']"}),
            'completion': ('django.db.models.fields.FloatField', [], {}),
            'grade': ('django.db.models.fields.FloatField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'path': ('django.db.models.fields.FilePathField', [],
                     {'path': "'/Users/oasis/.virtualenvs/djangopy2env/projects/hwcentral/core/submissions'",
                      'unique': 'True', 'max_length': '255', 'recursive': 'True',
                      'match': "'submission_\\\\d+\\\\.xml'"}),
            'student': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"}),
            'timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        u'core.topic': {
            'Meta': {'object_name': 'Topic'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'subject': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Subject']"})
        },
        u'core.userinfo': {
            'Meta': {'object_name': 'UserInfo'},
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.School']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['core']