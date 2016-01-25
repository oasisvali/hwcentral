from core.data_models.question import QuestionDM




class UndealtQuestionDM(object):
    """
    Contains randomization data in addition to the regular question subpart data. Performs the variable substitution and
    expression evaluation logic
    """

    def __init__(self, question_id, container, subparts, variable_constraints_list):
        assert len(subparts) == len(variable_constraints_list)
        assert len(container.subparts) == len(subparts)

        self.question_data = QuestionDM(question_id, container, subparts)
        self.variable_constraints_list = variable_constraints_list

    def deal(self):
        values = {}  # common dict which will be extended with every subsequent subpart's variable values
        for i, constraints in enumerate(self.variable_constraints_list):
            constraints.process()  # first select the value based on constraint
            values.update(constraints.values)
            self.question_data.subparts[i].evaluate_substitute(values)

        return self.question_data
