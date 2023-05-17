from fastapi import APIRouter, Response

from yellow_taxi_data.database.postgres import Timescale

router = APIRouter(
    prefix="/aggregate",
    tags=["aggregate"],
    responses={404: {"description": "Not found"}},
)


@router.get("/get_daily_aggs")
async def get_daily_aggs():
    """Get the aggregate stats that roll up on passenger_count, fare, and pickup_loc_id.

    Returns:
        dict: Dictionary with aggregate stats.
    """
    timescale = Timescale()
    data = await timescale.get_daily_aggregate()
    return Response(content=data, media_type="application/json")


@router.get("/get_hourly_aggs")
async def get_hourly_aggs():
    """Get the aggregate stats that roll up on passenger_count, fare, and pickup_loc_id.

    Returns:
        dict: Dictionary with aggregate stats.
    """
    timescale = Timescale()
    data = await timescale.get_hourly_aggregate()
    return Response(content=data, media_type="application/json")
