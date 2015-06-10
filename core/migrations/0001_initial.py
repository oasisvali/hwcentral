# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):
    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('auth', '0006_require_contenttypes_0002'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Announcement',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('object_id',
                 models.PositiveIntegerField(help_text=b'The primary key of the target of this announcement.')),
                ('message',
                 models.CharField(help_text=b'The textual message to be conveyed to the target.', max_length=255)),
                ('timestamp',
                 models.DateTimeField(help_text=b'Timestamp of when this announcement was issued.', auto_now_add=True)),
                ('content_type', models.ForeignKey(
                    help_text=b'The type of the target of this announcement. Can be a SubjectRoom, ClassRoom or School.',
                    to='contenttypes.ContentType')),
            ],
        ),
        migrations.CreateModel(
            name='Assignment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('assigned', models.DateTimeField(help_text=b'Timestamp of when this assignment was assigned.')),
                ('due', models.DateTimeField(help_text=b'Timestamp of when this assignment is due.')),
                ('meta', models.FilePathField(help_text=b"Path to this assignment's metadata file.",
                                              path=b'/Users/oasis/hwcentral/core/assignments', max_length=255,
                                              match=b'\\d+.json')),
            ],
        ),
        migrations.CreateModel(
            name='Board',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                (
                'name', models.CharField(help_text=b'A string descriptor for the board.', unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name',
                 models.CharField(help_text=b'A string descriptor for the chapter.', unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('division',
                 models.CharField(help_text=b'The division name of this classroom, as a string.', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Group',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name',
                 models.CharField(help_text=b'A string descriptor for the user group.', unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Home',
            fields=[
                ('parent', models.OneToOneField(related_name='home', primary_key=True, serialize=False,
                                                to=settings.AUTH_USER_MODEL,
                                                help_text=b'The parent user for whom the home is defined.')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('meta', models.FilePathField(help_text=b"Path to this question's metadata file.",
                                              path=b'/Users/oasis/hwcentral/core/questions', max_length=255,
                                              match=b'\\d+.json')),
                ('chapter',
                 models.ForeignKey(help_text=b'The chapter that this question pertains to.', to='core.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='School',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(help_text=b'Full name of the school. Must be unique.', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Standard',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('number',
                 models.PositiveIntegerField(help_text=b'A positive integer representing the standard.', unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='SubChapter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name',
                 models.CharField(help_text=b'A string descriptor for the sub-chapter.', unique=True, max_length=255)),
                ('chapter',
                 models.ForeignKey(help_text=b'The chapter that this sub-chapter belongs to.', to='core.Chapter')),
            ],
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name',
                 models.CharField(help_text=b'A string descriptor for the subject.', unique=True, max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SubjectRoom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('classRoom',
                 models.ForeignKey(help_text=b'The classroom that this subjectroom belongs to.', to='core.ClassRoom')),
            ],
        ),
        migrations.CreateModel(
            name='Submission',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('marks', models.FloatField(help_text=b'Marks (percentage) obtained by this submission.', null=True)),
                ('timestamp',
                 models.DateTimeField(help_text=b'Timestamp of when this submission was submitted.', auto_now=True)),
                ('completion', models.FloatField(help_text=b'Completion (percentage) of this submission.')),
                ('meta', models.FilePathField(help_text=b"Path to this submission's metadata file.",
                                              path=b'/Users/oasis/hwcentral/core/submissions', max_length=255,
                                              match=b'\\d+.json')),
                ('assignment',
                 models.ForeignKey(help_text=b'The assignment that this submission is for.', to='core.Assignment')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL,
                                              help_text=b'The user object that this info is associated with.')),
                ('group', models.ForeignKey(help_text=b'Please select the type of user account to be created.',
                                            to='core.Group')),
                ('school',
                 models.ForeignKey(help_text=b'Please select the school that this user belongs to.', to='core.School')),
            ],
        ),
        migrations.AddField(
            model_name='submission',
            name='student',
            field=models.ForeignKey(help_text=b'The student user responsible for this submission.',
                                    to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subjectroom',
            name='students',
            field=models.ManyToManyField(help_text=b'The set of student users in this subjectroom.',
                                         related_name='subjects_enrolled_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='subjectroom',
            name='subject',
            field=models.ForeignKey(help_text=b'The subject that is taught in this subjectroom.', to='core.Subject'),
        ),
        migrations.AddField(
            model_name='subjectroom',
            name='teacher',
            field=models.ForeignKey(related_name='subjects_managed_set', to=settings.AUTH_USER_MODEL,
                                    help_text=b'The teacher user teaching this subjectroom.'),
        ),
        migrations.AddField(
            model_name='school',
            name='admin',
            field=models.ForeignKey(help_text=b'The admin user who manages this school.', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='school',
            name='board',
            field=models.ForeignKey(help_text=b'The board/curriculum that this school follows.', to='core.Board'),
        ),
        migrations.AddField(
            model_name='question',
            name='school',
            field=models.ForeignKey(
                help_text=b"The school question bank that this question belongs to. Use 'hwcentral' if it belongs to the global question bank.",
                to='core.School'),
        ),
        migrations.AddField(
            model_name='question',
            name='standard',
            field=models.ForeignKey(help_text=b'The standard that this question is for.', to='core.Standard'),
        ),
        migrations.AddField(
            model_name='question',
            name='subChapters',
            field=models.ManyToManyField(help_text=b'The set of sub-chapter that this question covers.',
                                         to='core.SubChapter'),
        ),
        migrations.AddField(
            model_name='question',
            name='subject',
            field=models.ForeignKey(help_text=b'The subject that this question is for.', to='core.Subject'),
        ),
        migrations.AddField(
            model_name='home',
            name='students',
            field=models.ManyToManyField(help_text=b'The set of student users managed by the parent of this home.',
                                         related_name='homes_enrolled_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='classroom',
            name='classTeacher',
            field=models.ForeignKey(related_name='classes_managed_set', to=settings.AUTH_USER_MODEL,
                                    help_text=b'The teacher user managing this classroom.'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='school',
            field=models.ForeignKey(help_text=b'The school that this classroom belongs to.', to='core.School'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='standard',
            field=models.ForeignKey(help_text=b'The standard of this classroom.', to='core.Standard'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(help_text=b'The set of student users in this classroom.',
                                         related_name='classes_enrolled_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='assignment',
            name='questions',
            field=models.ManyToManyField(help_text=b'The set of questions that make up this assignment.',
                                         to='core.Question'),
        ),
        migrations.AddField(
            model_name='assignment',
            name='subjectRoom',
            field=models.ForeignKey(help_text=b'The subjectroom that this assignment belongs to.',
                                    to='core.SubjectRoom'),
        ),
    ]
