select pickup_loc_id, bucket_daily, approx_percentile(0.90, fare_daily) as percentile_fare, approx_percentile(0.90, pasenger_daily) as percentile_passenger, taxi_zone.borough, taxi_zone.zone_text
from yt_trips_daily
right join taxi_zone
on yt_trips_daily.pickup_loc_id = taxi_zone.location_id
