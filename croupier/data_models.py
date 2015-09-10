from fractions import Fraction
import random

from core.data_models.question import QuestionDM






###### Detailed variable constraints breakdown (Highest to Lowest priority)
#
#   _{ }_ is a substitution block       _{{ }}_ is an evaluation block
#
#   "options": [1, 0, -1.3, "oasis"]   list of options, values can be any string, int or float
#                                      (if string, make sure to not use in any evaluation block)
#
#   NOTE: if option index 2 is selected as variable value, any subsequent options constraints in the same subpart will have the same selected index
#
#   "range": {  // only for ints and floats, no string, no fraction
#
#       "decimal": 2, // optional, if not specified only int values are taken. value denotes number of decimal places
#       "exclude": [  // NOTE: exclude overrides include. exclude ranges must be in ascending order
#         [1,2],  // excludes everything between 1 and 2, including 1 and 2
#         [34] // excludes the number 34
#         ],
#       "include": [    // this key must be present in the range block and must have at least one value. ranges must be ascending order
#         [-1,5] // includes everything between -1 and 5, including -1 and 5
#         [23],  // includes the number 23
#         ]
#     },
#
#   "fraction": {
#       "numerator": {
#         "options": [],
#         "rangeint": {
#           // cannot have decimal
#         }
#       },
#       "denominator": {  //NOTE: denominator will always autoatically exclude 0
#         "options": [],
#         "rangeint": {
#           // cannot have decimal
#         }
#       }
#     }
#
#
#
#
from croupier.exceptions import EmptyVariableConstraintsError, EmptyOptionsListError, InvalidRangeLengthError, \
    InvalidRangeLimitsError, MissingIncludeRangesError, InvalidConstraintsTypeError, InvalidDenominatorConstraintError, \
    RangeProcessingError


class ConstraintBase(object):
    def evaluate(self, *args):
        raise NotImplementedError("subclass of ConstraintBase must implement method evaluate")

class OptionsConstraint(ConstraintBase):
    def __init__(self, options_list):
        if len(options_list) == 0:
            raise EmptyOptionsListError()
        self.options_list = options_list

    def evaluate(self, options_selection_index):
        if options_selection_index is None:
            options_selection_index = random.randint(0, len(self.options_list) - 1)
        return (self.options_list[options_selection_index], options_selection_index)


class Range(object):
    def __init__(self, range_data):
        if len(range_data) == 1:
            self.min = range_data[0]
            self.max = range_data[0]
        elif len(range_data) == 2:
            self.min = range_data[0]
            self.max = range_data[1]
            if self.min > self.max:
                raise InvalidRangeLimitsError()
        else:
            raise InvalidRangeLengthError()


class Ranges(object):
    def __init__(self, ranges_data):
        if ranges_data is None:
            self.ranges = []
        else:
            self.ranges = [Range(elem) for elem in ranges_data]

        if len(self.ranges) == 0:
            return
        # check validity - range elements must be in ascending order with NO OVERLAP
        prev_range_max = self.ranges[0].max
        for range in self.ranges[1:]:
            if range.min <= prev_range_max:
                raise InvalidRangeLimitsError()
            prev_range_max = range.max


class RangeConstraintBase(ConstraintBase):
    def __init__(self, range_data):
        self.include_ranges = Ranges(range_data["include"])
        if len(self.include_ranges.ranges) == 0:
            raise MissingIncludeRangesError()
        self.exclude_ranges = Ranges(range_data.get("exclude"))

    def process_ranges(self, step):
        """
        Sets up the evaluation for the child classes of RangeConstraintBase by processing the include and exclude ranges
        and returning a list of valid ranges
        """

        processed_include_ranges = [include_range for include_range in self.include_ranges.ranges]

        for exclude_range in self.exclude_ranges.ranges:
            # modify each include range depending on how it overlaps with the current exclude range
            include_range_index = -1
            include_range_len = len(processed_include_ranges)
            while True:
                include_range_index += 1
                if (include_range_index == include_range_len):
                    break
                include_range = processed_include_ranges[include_range_index]
                # no overlap - preserve include range, move to next include range
                if (exclude_range.min > include_range.max) or \
                        (exclude_range.max < include_range.min):
                    continue
                # complete overlap - remove include range, update index and len, move to next include range
                elif (exclude_range.min <= include_range.min) and \
                        (exclude_range.max >= include_range.max):
                    processed_include_ranges.pop(include_range_index)
                    include_range_index -= 1
                    include_range_len -= 1
                    continue
                # left side overlap - shorten include range, move to next include range
                elif (exclude_range.min <= include_range.min) and (exclude_range.max >= include_range.min) and (
                    exclude_range.max < include_range.max):
                    processed_include_ranges[include_range_index] = Range(
                        [(exclude_range.max + step), include_range.max])
                    continue
                # right side overlap - shorten include range, move to next include range
                elif (exclude_range.max >= include_range.max) and (exclude_range.min <= include_range.max) and (
                    exclude_range.min > include_range.min):
                    processed_include_ranges[include_range_index] = Range(
                        [include_range.min, (exclude_range.min - step)])
                    continue
                # middle section overlap - split include range into 2, update index and len, move to next include range
                elif (exclude_range.max < include_range.max) and (exclude_range.min > include_range.min):
                    processed_include_ranges.pop(include_range_index)
                    processed_include_ranges.insert(include_range_index,
                                                    Range([(exclude_range.max + step), include_range.max]))
                    processed_include_ranges.insert(include_range_index,
                                                    Range([include_range.min, (exclude_range.min - step)]))
                    include_range_index += 1
                    include_range_len += 1
                    continue

                raise RangeProcessingError()

        if len(processed_include_ranges) == 0:
            raise RangeProcessingError()

        return processed_include_ranges

    def evaluate(self):
        processed_ranges = self.process_ranges(1)
        valid_choices = [random.randint(processed_range.min, processed_range.max) for processed_range in
                         processed_ranges]
        return random.choice(valid_choices)

    def check_valid_range_for_denominator(self):
        # first check if any of the excludes exclude 0
        for excluded_range in self.exclude_ranges.ranges:
            if excluded_range.min <= 0 and excluded_range.max >= 0:
                return
        # if 0 is not excluded, check if it is included
        for included_range in self.include_ranges.ranges:
            if included_range.min <= 0 and included_range.max >= 0:
                raise InvalidDenominatorConstraintError()


class RangeConstraint(RangeConstraintBase):
    def __init__(self, range_data):
        super(RangeConstraint, self).__init__(range_data)
        self.decimal = range_data.get("decimal")

    def evaluate(self):
        if self.decimal:
            step = 1.0 / (10 ** self.decimal)
            processed_ranges = super(RangeConstraint, self).process_ranges(step)
            valid_choices = [random.uniform(processed_range.min, processed_range.max) for processed_range in
                             processed_ranges]
            return float(("{0:.%uf}" % self.decimal).format(random.choice(valid_choices)))

        else:
            return super(RangeConstraint, self).evaluate()


class RangeIntConstraint(RangeConstraintBase):
    pass


class FractionElemConstraintBase(ConstraintBase):
    def __init__(self, fraction_elem_data):
        self.is_options_constraint = False
        if len(fraction_elem_data) == 0:
            self.constraint = SubpartVariableConstraints.default_constraints()
            return
        if "options" in fraction_elem_data:
            self.constraint = OptionsConstraint(fraction_elem_data['options'])
            self.is_options_constraint = True
            return
        if "rangeint" in fraction_elem_data:
            self.constraint = RangeIntConstraint(fraction_elem_data['rangeint'])
            return

        raise InvalidConstraintsTypeError()

    def evaluate(self, option_selection_index):
        if self.is_options_constraint:
            return self.constraint.evaluate(option_selection_index)
        return (self.constraint.evaluate(), option_selection_index)


class FractionDenominatorConstraint(FractionElemConstraintBase):
    def __init__(self, fraction_elem_data):
        # denominator needs an added check against 0 valuation
        super(FractionDenominatorConstraint, self).__init__(fraction_elem_data)
        if self.is_options_constraint:
            if 0 in self.constraint.options_list:
                raise InvalidDenominatorConstraintError()
        else:
            # constraint is a range
            self.constraint.check_valid_range_for_denominator()


class FractionNumeratorConstraint(FractionElemConstraintBase):
    pass


class FractionConstraint(ConstraintBase):
    def __init__(self, fraction_data):
        self.numerator = FractionNumeratorConstraint(fraction_data["numerator"])
        self.denominator = FractionDenominatorConstraint(fraction_data["denominator"])

    def evaluate(self, options_selection_index):
        numerator_value, options_selection_index = self.numerator.evaluate(options_selection_index)
        denominator_value, options_selection_index = self.denominator.evaluate(options_selection_index)
        # use Fraction for simplification
        return (Fraction(numerator_value, denominator_value), options_selection_index)


class SubpartVariableConstraints(object):
    """
    Performs the variable value selection logic for all variables in a subpart.
    selection cannot happen in init as first all variables need to be initialized with the right type of constraints
    """

    def __init__(self, variable_constraints_data):
        self.values = {}  # this dictionary stores the selected value for each variable, where the variable is the key
        self.options_selection_index = None
        self.variable_constraints_data = variable_constraints_data

    def process(self):
        if self.variable_constraints_data is None:  # no variable constraints block
            return

        if (len(self.variable_constraints_data) == 0):
            raise EmptyVariableConstraintsError()

        # so there is a variable constraints block and it has some variables
        for variable in self.variable_constraints_data:
            self.values[variable] = self.process_constraints_block(self.variable_constraints_data[variable])

    @classmethod
    def default_constraints(cls):
        return RangeConstraint({
            "include": [
                [2, 40]
            ]
        })

    def process_constraints_block(self, constraints_block):
        """
        Looks at the constraints block and applies the right type of constraints based on constraint precedence
        """
        if len(constraints_block) == 0:
            return SubpartVariableConstraints.default_constraints().evaluate()

        if "options" in constraints_block:
            value, self.options_selection_index = OptionsConstraint(constraints_block['options']).evaluate(
                self.options_selection_index)
            return value

        if "range" in constraints_block:
            return RangeConstraint(constraints_block['range']).evaluate()

        if "fraction" in constraints_block:
            value, self.options_selection_index = FractionConstraint(constraints_block['fraction']).evaluate(
                self.options_selection_index)
            return value

        raise InvalidConstraintsTypeError()



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
