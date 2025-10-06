import logging
import os
from logging.handlers import RotatingFileHandler
from pathlib import Path


class Logger:
    def __init__(
        self,
        mode: str = "dev",
        preregistered_loggers: list[str] | None = None,
        backups_count: int = 5,
        max_log_size: int = 10,
        log_file_name: str = "app",
    ) -> None:
        self.base_log_dir = Path("logs")

        self._setup_log_dir()

        self.mode = mode
        self.level_log = logging.INFO if self.mode == "dev" else logging.DEBUG
        self.backups_count = backups_count
        self.max_log_size = max_log_size
        self.log_file_name = log_file_name
        self.log_file_path = self.base_log_dir / f"{log_file_name}.log"
        self.base_preregistered_loggers = (
            preregistered_loggers if preregistered_loggers else ["aiogram"]
        )

        # if self.mode == "dev":
        #     self.base_preregistered_loggers.extend(["sqlalchemy", "alembic"])

        for registered_logger in self.base_preregistered_loggers:
            self.get_logger(registered_logger).setLevel(self.level_log)

    def _file_handler(self) -> logging.Handler:
        """Метод создаёт обработчик логов, который пишет в файл"""
        log_file = RotatingFileHandler(
            encoding="utf-8",
            maxBytes=self.max_log_size * 1024 * 1024,
            filename=self.log_file_path,
            backupCount=self.backups_count,
        )

        log_file.setLevel(self.level_log)
        log_file.setFormatter(PlainFormatter())

        return log_file

    def _console_handler(self) -> logging.Handler:
        """Метод создаёт обработчик, который выводит логи в консоль"""
        log_console = logging.StreamHandler()

        log_console.setLevel(self.level_log)
        log_console.setFormatter(ColorFormatter())

        return log_console

    def _setup_log_dir(self) -> None:
        """Метод создания папки logs"""
        return os.makedirs(self.base_log_dir, exist_ok=True)

    def get_logger(self, name: str) -> logging.Logger:
        log = logging.getLogger(name)

        if not log.hasHandlers():
            log.setLevel(self.level_log)
            log.addHandler(self._file_handler())
            log.addHandler(self._console_handler())

        return log


class ColorFormatter(logging.Formatter):
    def __init__(self) -> None:
        self.FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(funcName)s - %(message)s"

        self.COLORS = {
            "DEBUG": "\033[94m",
            "INFO": "\033[92m",
            "WARNING": "\033[93m",
            "ERROR": "\033[91m",
            "CRITICAL": "\033[95m",
            "RESET": "\033[0m",
        }

        super().__init__(self.FORMAT)

    def format(self, record: logging.LogRecord) -> str:
        original_levelname = record.levelname
        colored_levelname = f"{self.COLORS.get(record.levelname, '')}{record.levelname}{self.COLORS.get('RESET')}"

        record.levelname = colored_levelname

        formatted = super().format(record)

        record.levelname = original_levelname

        return formatted


class PlainFormatter(logging.Formatter):
    def __init__(self):
        super().__init__(
            "%(asctime)s - %(name)s - %(levelname)s - %(pathname)s:%(lineno)d - %(funcName)s - %(message)s"
        )
