import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def configure_logging() -> None:
    """Configure application-wide logging to server.log."""
    path = Path("output/server.log")
    path.parent.mkdir(exist_ok=True)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    logging.getLogger("httpx").setLevel(logging.WARNING)

    # avoid duplicate handlers if configure_logging() is called more than once
    for handler in list(root.handlers):
        root.removeHandler(handler)
        handler.close()

    handler = RotatingFileHandler(
        str(path),
        maxBytes=5 * 1024 * 1024,
        backupCount=5,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    root.addHandler(handler)
