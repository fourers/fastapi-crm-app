import logging

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


def request_validation_exception_handler(exc: RequestValidationError) -> JSONResponse:
    errors = jsonable_encoder(exc.errors())
    try:
        errors = [add_summary_to_validation_error(error) for error in errors]
    except Exception:
        logger.warning("Error adding summary to validation error", exc_info=True)

    return JSONResponse(
        status_code=422,
        content={"detail": errors, "summary": str(exc)},
    )


def add_summary_to_validation_error(error: dict) -> dict:
    field_name = format_field_name(error.get("loc", []))
    msg = error.get("msg", "validation error")
    error_type = error.get("type")
    error_type_suffix = f" ({error_type})" if error_type else ""
    error["summary"] = f"{field_name}: {msg}{error_type_suffix}"
    return error


def format_field_name(values: list[str]) -> str:
    if not values:
        return "unknown"
    if len(values) == 1:
        return values[0]

    if values[0] == "body":
        return ".".join(values[1:])
    else:
        return ".".join(values)
