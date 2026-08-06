import logging
from pathlib import Path


def configure_logging() -> None:
    """Configure application-wide logging to server.log."""
    path = Path("output/server.log")
    path.parent.mkdir(exist_ok=True)

    root = logging.getLogger()
    root.setLevel(logging.INFO)

    logging.getLogger("httpx").setLevel(logging.WARNING)

    handler = logging.FileHandler(str(path))
    handler.setFormatter(
        logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
    )

    root.addHandler(handler)
