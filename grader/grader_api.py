from datadog import statsd

from cabinet import cabinet_api


@statsd.timed('grader.grade.submission')
def grade(submission, register_ticks):
    submission_dm = cabinet_api.get_submission(submission)
    assert len(submission_dm.questions) == len(submission_dm.answers)

    # update the database object with marks - submission
    submission.marks = perform_correction(submission, submission_dm, register_ticks)
    submission.save()

    # update the submission in cabinet
    cabinet_api.update_submission(submission, submission_dm)


def perform_correction(submission, submission_dm, register_ticks):
    """
    performs correction, returns marks obtained and also registers ticks for edge
    """

    submission_dm.check_answers()
    register_ticks = register_ticks and (
    submission.completion > 0)  # ignore shell and empty submission as they are noise

    if register_ticks:
        return submission_dm.calculate_marks(True, submission)  # this will also register ticks for edge
    else:
        return submission_dm.calculate_marks()
