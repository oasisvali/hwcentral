class InvalidStateException(Exception):
    pass


class InvalidHWCentralGroupException(Exception):
    def __init__(self, message, errors):
        Exception.__init__(self, "Invalid HWCentral Group: " + message)


class NoneArgumentException(Exception):
    def __init__(self, message, errors):
        Exception.__init__(self, "Unexpected None argument: " + message)