class CabinetError(Exception):
    def __init__(self, type, msg, *args, **kwargs):
        super(CabinetError, self).__init__("Cabinet %s Error : %s" % (type, msg))


class CabinetSubmissionExistsError(CabinetError):
    def __init__(self, msg, *args, **kwargs):
        super(CabinetSubmissionExistsError, self).__init__("SubmissionExists", msg)


class CabinetSubmissionMissingError(CabinetError):
    def __init__(self, msg, *args, **kwargs):
        super(CabinetSubmissionMissingError, self).__init__("SubmissionMissing", msg)

class CabinetConnectionError(CabinetError):
    def __init__(self, url, method, *args, **kwargs):
        super(CabinetConnectionError, self).__init__("CouldNotConnect", "url: %s method: %s" % (url, method))

class Cabinet404Error(CabinetError):
    def __init__(self, url, *args, **kwargs):
        super(Cabinet404Error, self).__init__("ResourceNotFound", "url: %s" % url)


class SubpartOutOfOrderException(CabinetError):
    def __init__(self, subpart_index, subpart_order, question_id, *args, **kwargs):
        super(SubpartOutOfOrderException, self).__init__("SubpartOrder",
                                                         "Found index: %s Expected index: %s for question: %s" % (
                                                         subpart_index, subpart_order, question_id))