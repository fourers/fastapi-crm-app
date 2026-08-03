import traceback


def format_exception(exc: Exception) -> str:
    return "".join(traceback.format_exception(exc))
