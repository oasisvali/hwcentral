# -*- coding: utf-8 -*-
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):
    def forwards(self, orm):
        # Deleting model 'Class'
        db.delete_table(u'core_class')

        # Removing M2M table for field students on 'Class'
        db.delete_table(db.shorten_name(u'core_class_students'))

        # Deleting model 'ClassAccessLevel'
        db.delete_table(u'core_classaccesslevel')

        # Adding model 'Classroom'
        db.create_table(u'core_classroom', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('access', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ClassroomAccessLevel'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.School'])),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('standard', self.gf('django.db.models.fields.PositiveIntegerField')()),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='classes_managed_set',
                                                                              to=orm['auth.User'])),
        ))
        db.send_create_signal(u'core', ['Classroom'])

        # Adding M2M table for field students on 'Classroom'
        m2m_table_name = db.shorten_name(u'core_classroom_students')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('classroom', models.ForeignKey(orm[u'core.classroom'], null=False)),
            ('user', models.ForeignKey(orm[u'auth.user'], null=False))
        ))
        db.create_unique(m2m_table_name, ['classroom_id', 'user_id'])

        # Adding model 'ClassroomAccessLevel'
        db.create_table(u'core_classroomaccesslevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
        ))
        db.send_create_signal(u'core', ['ClassroomAccessLevel'])

        # Deleting field 'Assignment._type'
        db.delete_column(u'core_assignment', '_type_id')

        # Deleting field 'Assignment._class'
        db.delete_column(u'core_assignment', '_class_id')

        # Adding field 'Assignment.assignmentType'
        db.add_column(u'core_assignment', 'assignmentType',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.AssignmentType']),
                      keep_default=False)

        # Adding field 'Assignment.classroom'
        db.add_column(u'core_assignment', 'classroom',
                      self.gf('django.db.models.fields.related.ForeignKey')(default=1, to=orm['core.Classroom']),
                      keep_default=False)


    def backwards(self, orm):
        # Adding model 'Class'
        db.create_table(u'core_class', (
            ('access', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.ClassAccessLevel'])),
            ('school', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.School'])),
            ('teacher', self.gf('django.db.models.fields.related.ForeignKey')(related_name='classes_managed_set',
                                                                              to=orm['auth.User'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Subject'])),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('standard', self.gf('django.db.models.fields.PositiveIntegerField')()),
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

        # Adding model 'ClassAccessLevel'
        db.create_table(u'core_classaccesslevel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, unique=True)),
        ))
        db.send_create_signal(u'core', ['ClassAccessLevel'])

        # Deleting model 'Classroom'
        db.delete_table(u'core_classroom')

        # Removing M2M table for field students on 'Classroom'
        db.delete_table(db.shorten_name(u'core_classroom_students'))

        # Deleting model 'ClassroomAccessLevel'
        db.delete_table(u'core_classroomaccesslevel')


        # User chose to not deal with backwards NULL issues for 'Assignment._type'
        raise RuntimeError("Cannot reverse this migration. 'Assignment._type' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration        # Adding field 'Assignment._type'
        db.add_column(u'core_assignment', '_type',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.AssignmentType']),
                      keep_default=False)


        # User chose to not deal with backwards NULL issues for 'Assignment._class'
        raise RuntimeError("Cannot reverse this migration. 'Assignment._class' and its values cannot be restored.")

        # The following code is provided here to aid in writing a correct migration        # Adding field 'Assignment._class'
        db.add_column(u'core_assignment', '_class',
                      self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.Class']),
                      keep_default=False)

        # Deleting field 'Assignment.assignmentType'
        db.delete_column(u'core_assignment', 'assignmentType_id')

        # Deleting field 'Assignment.classroom'
        db.delete_column(u'core_assignment', 'classroom_id')


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
            'assigned': ('django.db.models.fields.DateTimeField', [], {}),
            'assignmentType': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.AssignmentType']"}),
            'classroom': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.Classroom']"}),
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
        u'core.classroom': {
            'Meta': {'object_name': 'Classroom'},
            'access': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.ClassroomAccessLevel']"}),
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
        u'core.classroomaccesslevel': {
            'Meta': {'object_name': 'ClassroomAccessLevel'},
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
            'home': ('django.db.models.fields.PositiveIntegerField', [], {'default': '0'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'school': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['core.School']"}),
            'user': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['auth.User']", 'unique': 'True'})
        }
    }

    complete_apps = ['core']