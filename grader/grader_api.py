from datadog import statsd

from cabinet import cabinet_api


@statsd.timed('grader.grade.submission')
def grade(submission):
    submission_dm = cabinet_api.get_submission(submission)
    assert len(submission_dm.questions) == len(submission_dm.answers)

    # update the database object with marks - submission
    submission.marks = perform_correction(submission, submission_dm)
    submission.save()

    # update the submission in cabinet
    cabinet_api.update_submission(submission, submission_dm)


def perform_correction(submission, submission_dm):
    """
    performs correction, returns marks obtained and also registers ticks for edge
    """

    submission_dm.check_answers()
    register_ticks = (submission.completion > 0)  # ignore shell and empty submission as they are noise
    student = submission.student if register_ticks else None
    return submission_dm.calculate_marks(register_ticks, student)  # this call also registers ticks for edge
