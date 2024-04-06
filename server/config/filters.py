def ignore_503_errors(record):
    if hasattr(record, "status_code") and record.status_code == 503:
        return False
    return True
