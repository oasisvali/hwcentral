class InvalidStateException(Exception):
    pass


class NoneArgumentException(Exception):
    def __init__(self, message, errors):
        Exception.__init__(self, "Unexpected None argument: " + message)