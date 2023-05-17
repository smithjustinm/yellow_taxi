"""Health and readiness fastapi routers for the yellow_taxi_data app."""
from typing import Any, Dict, List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/healthcheck",
    tags=["healthcheck"],
    responses={404: {"description": "Not found"}},
)


class ErrorModel(BaseModel):
    """Error model.

    Attributes:
        ErrorCode (str): Error code
        FieldName (str): Field name
        Message (str): Message
        Meta (Dict[str, Any]): Meta data for the error
    """

    ErrorCode: str = ""
    FieldName: str = ""
    Message: str = ""
    Meta: Dict[str, Any] = {}


class HealthModel(BaseModel):
    """Response to health check requests.

    Attributes:
        healthy (bool): Am I healthy?
        dependencies (List): Currently empty
    """

    healthy: bool = True
    dependencies: List = []


class ReadyModel(BaseModel):
    """Response to ready check requests.

    Attributes:
        ready (bool): Am I ready?
        description (str): Description of readiness
    """

    ready: bool = True
    description: str = "yellow_taxi_data is ready"


@router.get("/")
async def healthy_check() -> HealthModel:
    """Check to see if the service is healthy.

    Returns:
        (HealthModel): HealthModel
    """
    healthbody: HealthModel = HealthModel()
    return healthbody


@router.get("/ready")
async def ready_check() -> ReadyModel:
    """Check to see if the service is ready.

    Returns:
        (ReadyModel): ReadyModel
    """
    readybody: ReadyModel = ReadyModel()
    return readybody
