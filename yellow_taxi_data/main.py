"""Main entrypoint for {{ cookiecutter.friendly_name }}."""


import structlog
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator, metrics

from yellow_taxi_data import __version__
from yellow_taxi_data.config.exception_handlers import validation_exception_handler
from yellow_taxi_data.config.settings import settings
from yellow_taxi_data.middleware import LogStatusCode
from yellow_taxi_data.routers import aggregate, health, percentile

settings.setup_logging()

logger = structlog.get_logger(__name__)


class InitApp(object):
    def __init__(self):
        self.app = FastAPI(
            title=settings.APPLICATION,
            description=settings.APPLICATION,
            version=__version__,
            docs_url="/",
        )

        self.app.add_middleware(GZipMiddleware, minimum_size=500)
        self.app.add_middleware(
            LogStatusCode, logger=logger.info, status_codes=[422, 500]
        )

        self.app.add_exception_handler(
            RequestValidationError, handler=validation_exception_handler
        )

        self.app.include_router(health.router)
        self.app.include_router(percentile.router)
        self.app.include_router(aggregate.router)

        @self.app.on_event("startup")
        async def startup():
            """Startup event handler."""

            # Add instrumentation after other routes
            instrumentor: Instrumentator = Instrumentator().instrument(self.app)
            instrumentor.add(metrics.default(metric_namespace="yellow_taxi_data"))

            instrumentor.expose(self.app)

            logger.info("yellow_taxi_data started")


def start():
    app = InitApp()
    return app.app


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        start(),
        host="0.0.0.0",
        port=9000,
        log_level="info",
    )
