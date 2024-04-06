import logging


class IgnoreMissingBuild503Errors(logging.Filter):
    """
    Filters out 503 errors for missing builds.
    """

    def filter(self, record):
        # Message is of the format `"GET /download_check/.../ HTTP/1.1" 503 125`
        message = record.getMessage()
        return "download_check" not in message and " 503 " not in message
