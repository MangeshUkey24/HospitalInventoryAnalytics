"""
------------------------------------------------------------
Hospital Inventory Analytics System (HIAS)
Logger Module
------------------------------------------------------------
Author  : Mangesh Ukey
Version : 1.0
------------------------------------------------------------
"""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

from settings import Settings


class AppLogger:
    """
    Singleton logger for the application.
    """

    _logger = None

    @classmethod
    def get_logger(cls):

        if cls._logger is not None:
            return cls._logger

        # Create log directory if it doesn't exist
        Path(Settings.LOG_DIR).mkdir(parents=True, exist_ok=True)

        logger = logging.getLogger(Settings.APP_SHORT_NAME)
        logger.setLevel(logging.INFO)
        logger.propagate = False

        if not logger.handlers:

            formatter = logging.Formatter(
                "%(asctime)s | %(levelname)-8s | %(filename)s:%(lineno)d | %(message)s",
                datefmt="%d-%m-%Y %H:%M:%S"
            )

            # File Handler
            file_handler = RotatingFileHandler(
                filename=Settings.LOG_FILE,
                maxBytes=5 * 1024 * 1024,      # 5 MB
                backupCount=5,
                encoding="utf-8"
            )

            file_handler.setLevel(logging.INFO)
            file_handler.setFormatter(formatter)

            # Console Handler
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)
            console_handler.setFormatter(formatter)

            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        cls._logger = logger

        return logger

    @classmethod
    def info(cls, message):
        cls.get_logger().info(message)

    @classmethod
    def warning(cls, message):
        cls.get_logger().warning(message)

    @classmethod
    def error(cls, message):
        cls.get_logger().error(message)

    @classmethod
    def debug(cls, message):
        cls.get_logger().debug(message)

    @classmethod
    def critical(cls, message):
        cls.get_logger().critical(message)

    @classmethod
    def exception(cls, message):
        cls.get_logger().exception(message)