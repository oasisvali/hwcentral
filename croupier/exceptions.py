# TODO: better error message reporting (take args to show state)

class CroupierMalformedDataError(Exception):
    pass


class EmptyOptionsListError(CroupierMalformedDataError):
    pass


class InvalidRangeLengthError(CroupierMalformedDataError):
    pass


class InvalidRangeLimitsError(CroupierMalformedDataError):
    pass


class MissingIncludeRangesError(CroupierMalformedDataError):
    pass


class InvalidConstraintsTypeError(CroupierMalformedDataError):
    pass


class InvalidDenominatorConstraintError(CroupierMalformedDataError):
    pass


class InvalidSubstitutionTagContentError(CroupierMalformedDataError):
    pass


class RangeProcessingError(CroupierMalformedDataError):
    pass
