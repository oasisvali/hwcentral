class CabinetError(Exception):
    def __init__(self, type, msg, *args, **kwargs):
        super(CabinetError, self).__init__("Cabinet %s Error : %s" % (type, msg))


class CabinetSubmissionExistsError(CabinetError):
    def __init__(self, msg, *args, **kwargs):
        super(CabinetSubmissionExistsError, self).__init__("SubmissionExists", msg)


class CabinetSubmissionMissingError(CabinetError):
    def __init__(self, msg, *args, **kwargs):
        super(CabinetSubmissionMissingError, self).__init__("SubmissionMissing", msg)
