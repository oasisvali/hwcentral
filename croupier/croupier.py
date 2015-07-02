import random


class Croupier(object):
    """
    The main class offered by the croupier app that performs all the randomization and template substitution tasks
    """

    def randomize_for_seed(self, seed, collection):
        """
        Shuffles the given list IN-PLACE into a random order using the given seed
        """
        random.seed(seed)
        random.shuffle(collection)


    def get_question_ordering(self, student, assignment):
        """
        Returns the randomized question order for the given assignment using the student's pk as seed
        @param student:     The student for which a unique question ordering is to be generated
        @param assignment:  The assignment for which the ordering is required (determines the questions)
        @return:    List of question Ids of all questions in the assignment in a unique order
        """

        question_list = list(assignment.assignmentQuestionsList.questions.all())
        self.randomize_for_seed(student.pk, question_list)
        return question_list

    def get_option_ordering_for_student(self, student, MCQ):