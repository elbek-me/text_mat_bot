import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging(level: str, log_dir: Path) -> None:
    log_dir.mkdir(parents=True, exist_ok=True)
    fmt = logging.Formatter("%(asctime)s | %(levelname)-8s | %(name)s | %(message)s")

    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(fmt)

    file = RotatingFileHandler(
        log_dir / "bot.log", maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
    )
    file.setFormatter(fmt)

    root = logging.getLogger()
    root.setLevel(level.upper())
    root.handlers = [console, file]

    logging.getLogger("aiogram.event").setLevel(logging.WARNING)
