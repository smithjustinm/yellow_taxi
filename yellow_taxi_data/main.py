"""Main entrypoint for {{ cookiecutter.friendly_name }}."""

import structlog
import uvicorn
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.gzip import GZipMiddleware
from prometheus_fastapi_instrumentator import Instrumentator, metrics
from starlette.middleware.cors import CORSMiddleware

from yellow_taxi_data import __version__
from yellow_taxi_data.config.exception_handlers import validation_exception_handler
from yellow_taxi_data.config.settings import settings
from yellow_taxi_data.middleware import LogStatusCode
from yellow_taxi_data.routers import health, percentile

settings.setup_logging()

logger = structlog.get_logger(__name__)

app: FastAPI = FastAPI(
    title=settings.APPLICATION,
    description=settings.APPLICATION,
    version=__version__,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(GZipMiddleware, minimum_size=500)
app.add_middleware(LogStatusCode, logger=logger.info, status_codes=[422, 500])

app.add_exception_handler(RequestValidationError, handler=validation_exception_handler)


app.include_router(health.router)
app.include_router(percentile.router)

# Add instrumentation after other routes
instrumentor: Instrumentator = Instrumentator().instrument(app)
instrumentor.add(metrics.default(metric_namespace="yellow_taxi_data"))


@app.on_event("startup")
async def startup():
    """Startup event handler."""

    # Start Prometheus
    instrumentor.expose(app)

    logger.info("yellow_taxi_data started", **settings.get_cleansed_settings())


def start():
    """Launched with `poetry run start` at root level."""
    uvicorn.run("yellow_taxi_data.main:app", host="0.0.0.0", port=9000, reload=True)
