# to use this script, run following command from the terminal
# python manage.py runscript scripts.database.enforcer -v3

# Group, Board, Standard, Subject, Chapter, QuestionTag - name is not empty
# User - usernames must be lowercase
# Home
#   parent is parent group
#   children are student group
#   num children > 0
#
# School
#   admin is admin group
#   name is not empty
#
# Classroom
#   classteacher has to be teacher
#   students have to be student
#   num students > 0
#   num subjectrooms > 0
#   school has to match for classteacher and all students
#
# Subjectroom
#   teacher is teacher
#   students are students
#   a student in a subjectroom also belongs to subjectrooms classroom
#   num students > 0
#   school has to match for subjectteacher and all students
#
# Admin - school has more than one classroom
# Teacher - either classteacher (classes_managed > 0) or subjectteacher (subjects_managed > 0)
# Parent - has home associated
# Student - part of some subjectroom, and one classroom
#
# Questions - standard-subject-chapter is supported
#
# Aql
#   all questions have same school, standard, subject as aql
#   no 2 aql with same school, standard, subject number
#   all questions have same chapter
#   standard-subject is supported
#
# Assignment
#   aql subject, school is same as subjectroom subject, school (standard of aql must be <= standard of classroom
#   due > assigned
#
# Submission
#   student belongs to assignment subjectroom
#   student belongs to assignments subjectroom,
#   student is student
#   timestamp must be <= due date of assignment
#
# Announcement
#   timestamp is in past



def run():
