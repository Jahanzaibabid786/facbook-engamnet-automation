import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

class Logger:
    def __init__(self, log_dir: str = "logs", global_log: str = "application.log"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)
        self.global_log_path = self.log_dir / global_log
        self.profile_loggers = {}
        self._setup_global_logger()

    def _setup_global_logger(self):
        self.global_logger = logging.getLogger("global")
        self.global_logger.setLevel(logging.INFO)
        self.global_logger.handlers.clear()

        file_handler = logging.FileHandler(self.global_log_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        self.global_logger.addHandler(file_handler)
        self.global_logger.addHandler(console_handler)

    def get_profile_logger(self, profile_id: str) -> logging.Logger:
        if profile_id in self.profile_loggers:
            return self.profile_loggers[profile_id]

        logger = logging.getLogger(f"profile_{profile_id}")
        logger.setLevel(logging.INFO)
        logger.handlers.clear()

        profile_log_path = self.log_dir / f"{profile_id}.log"
        file_handler = logging.FileHandler(profile_log_path, encoding='utf-8')
        file_handler.setLevel(logging.INFO)

        formatter = logging.Formatter('[%(asctime)s] %(levelname)s: %(message)s', datefmt='%H:%M:%S')
        file_handler.setFormatter(formatter)

        logger.addHandler(file_handler)
        logger.propagate = False

        self.profile_loggers[profile_id] = logger
        return logger

    def info(self, message: str, profile_id: Optional[str] = None):
        self.global_logger.info(message)
        if profile_id:
            profile_logger = self.get_profile_logger(profile_id)
            profile_logger.info(message)

    def error(self, message: str, profile_id: Optional[str] = None):
        self.global_logger.error(message)
        if profile_id:
            profile_logger = self.get_profile_logger(profile_id)
            profile_logger.error(message)

    def warning(self, message: str, profile_id: Optional[str] = None):
        self.global_logger.warning(message)
        if profile_id:
            profile_logger = self.get_profile_logger(profile_id)
            profile_logger.warning(message)

    def debug(self, message: str, profile_id: Optional[str] = None):
        self.global_logger.debug(message)
        if profile_id:
            profile_logger = self.get_profile_logger(profile_id)
            profile_logger.debug(message)

logger = Logger()
