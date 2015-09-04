from core.data_models.question import QuestionDM


###### Detailed variable constraints breakdown (Highest to Lowest priority)
#
#   _{ }_ is a substitution block       _{{ }}_ is an evaluation block
#
#   "options": [1, 0, -1.3, "oasis"]   list of options, values can be any string, int or float (if string, make sure to not use in any evaluation block)
#
#   NOTE: if option index 2 is selected as variable value, any subsequent options constraints will have the same selected index
#
#
#
#
#
#
#
#

class ConstraintBase(object):
    def evaluate(self):
        raise NotImplementedError("subclass of ConstraintBase must implement method evaluate")


class OptionsConstraint(ConstraintBase):
    def __init__(self, ):


class VariableConstraints(object):
    """
    Performs the variable value selection logic for all variables in a subpart.
    selection cannot happen in init as first all variables need to be initialized with the right type of constraints
    """

    def __init__(self, variable_constraints_data):
        self.values = {}  # this dictionary stores the selected value for each variable, where the variable is the key
        if variable_constraints_data is None or (len(variable_constraints_data) == 0):
            return

        # so there is a variable constraints block and it has some variables
        for variable in variable_constraints_data:
            constraints = VariableConstraints.process_constraints_block(variable_constraints_data[variable])
            self.values[variable] = constraints.evaulate()

    @classmethod
    def process_constraints_block(cls, constraints_block):
        """
        Looks at the constraints block and applies the right type of constraints based on constraint precedence
        """
        if len(constraints_block) == 0:
            return cls.default_constraints()


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
            subpart = self.question_data.subparts[i]
