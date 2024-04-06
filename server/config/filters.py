import logging


class IgnoreMissingBuild503Errors(logging.Filter):
    """
    Filters out 503 errors for missing builds.
    """

    def filter(self, record):
        status_code = getattr(record, "status_code", None)
        return status_code != 503
