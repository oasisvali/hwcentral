from cabinet import cabinet


def grade(submission):
    submission_dm = cabinet.get_submission(submission)
    assert len(submission_dm.questions) == len(submission_dm.answers)
