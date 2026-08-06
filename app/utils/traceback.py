import traceback

from fastapi import Request
from fastapi.responses import RedirectResponse


def format_exception(exc: Exception) -> str:
    return "".join(traceback.format_exception(exc))


def redirect_error_page(request: Request, message: str) -> RedirectResponse:
    request.session["error"] = message
    return RedirectResponse(request.url_for("error-page"))


def redirect_exception_to_error_page(
    request: Request, exc: Exception
) -> RedirectResponse:
    return redirect_error_page(request, format_exception(exc))
