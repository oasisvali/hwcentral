from core.view_models.json import JSONViewModel


class Submission(JSONViewModel):
    def __init__(self, aql_randomized_dealt):
        self.questions = aql_randomized_dealt
        self.answers = []
        for question in aql_randomized_dealt:
            self.answers.append([None] * len(question.subparts))

