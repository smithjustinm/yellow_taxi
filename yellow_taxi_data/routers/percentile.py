"""Percentile fastapi router for the yellow_taxi_data app."""
from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/percentile_distance",
    tags=["percentile_distance"],
    responses={404: {"description": "Not found"}},
)


class Percentile(BaseModel):
    """Percentile model that will be used to return a list of all trip distances
    for a given percentile.

    Attributes:
        percentile (int): Percentile
        trip_distance (List[float]): List of trip distances
    """

    percentile: int = 0
    trip_distance: List[float] = []


@router.get("/percentile_distance")
async def get_percentile_distance() -> Percentile:
    """Get the percentile for a given trip distance.

    Returns:
        (Percentile): Percentile
    """
    return Percentile()
