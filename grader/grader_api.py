from cabinet import cabinet_api


def grade(submission):
    submission_dm = cabinet_api.get_submission(submission)
    assert len(submission_dm.questions) == len(submission_dm.answers)

    # update the database object with marks - submission
    submission.marks = submission_dm.calculate_marks()  # NOTE: the call to calculate marks also performs checking
    submission.save()

    # update the submission in cabinet
    cabinet_api.update_submission(submission, submission_dm)
