class Submission(JSONViewModel):
    def __init__(self, aql_randomized_dealt):
        self.questions = aql_randomized_dealt.questions
        self.answers = [None] * len(aql_randomized_dealt.questions)

