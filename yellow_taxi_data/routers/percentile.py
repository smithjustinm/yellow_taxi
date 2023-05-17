"""Percentile fastapi router for the yellow_taxi_data app."""

from fastapi import APIRouter

from yellow_taxi_data.database.postgres import Timescale

router = APIRouter(
    prefix="/distance",
    tags=["distance"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_90th_percentile")
async def get_percentile_distance():
    """Get the percentile for a given trip distance from the database.

    Returns:
        dict: Dictionary with all trips above 90th percentile for trip distance.
    """
    timescale = Timescale()
    return await timescale.get_distance_by_percentile()
