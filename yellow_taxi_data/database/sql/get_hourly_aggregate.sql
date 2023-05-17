select pickup_loc_id, bucket, approx_percentile(0.90, fare_hourly) as percentile_fare, approx_percentile(0.90, passenger_hourly) as percentile_passenger, taxi_zone.borough, taxi_zone.zone_text
from yt_trips_hourly
right join taxi_zone
on yt_trips_hourly.pickup_loc_id = taxi_zone.location_id
