"""Configuration for yellow_taxi_data app."""

import os

from pydantic.env_settings import BaseSettings

from yellow_taxi_data import __version__


class AppSettings(BaseSettings):
    """
    Configuration storage for yellow_taxi_data.
    """

    #: Name and version of the application.
    APPLICATION: str = f"yellow_taxi_data ({__version__})"

    #: Environment we're running in (dev/prod/...)
    ENVIRONMENT: str = "dev"

    #: The logging level of the application
    LOG_LEVEL: str = "INFO"

    #: Enable custom metrics
    PROMETHEUS_CUSTOM_METRIC_TRACKING_ENABLED: bool = True

    # TimescaleDB connection string
    HOST: str = os.getenv("host")
    PORT: str = "32217"
    USER: str = "tsdbadmin"
    PASSWORD: str = os.getenv("password")
    DBNAME: str = "tsdb"
    TIMESCALE_CONNECTION_STRING: str = (
        f"postgresql://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}"
    )

    def setup_logging(self):
        """
        Configure the logging.
        """
        import logging.config

        import structlog

        from yellow_taxi_data.config.logging_info import (
            STD_LIB_PROCESSORS,
            STRUCTLOG_PROCESSORS,
        )

        log_level = self.LOG_LEVEL.upper()

        structlog.configure(
            processors=STRUCTLOG_PROCESSORS,
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )

        gunicorn_error_logger = logging.getLogger("gunicorn.error")
        gunicorn_error_logger.setLevel(logging.INFO)
        uvicorn_access_logger = logging.getLogger("uvicorn.access")
        uvicorn_access_logger.setLevel(logging.INFO)

        logging.config.dictConfig(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "plain": {
                        "()": structlog.stdlib.ProcessorFormatter,
                        "processor": structlog.processors.JSONRenderer(),
                        "foreign_pre_chain": STD_LIB_PROCESSORS,
                    },
                },
                "handlers": {
                    "default": {"class": "logging.StreamHandler", "formatter": "plain"}
                },
                "root": {
                    "handlers": ["default"],
                    "level": log_level,
                    "propagate": True,
                },
                "loggers": {
                    "gunicorn.error": {
                        "handlers": ["default"],
                        "level": log_level,
                        "propagate": False,
                    },
                    "uvicorn": {
                        "handlers": ["default"],
                        "level": log_level,
                        "propagate": False,
                    },
                },
            }
        )


settings = AppSettings()
