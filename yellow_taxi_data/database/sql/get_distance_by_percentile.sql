/* return all trips that are over the 90th percentile for distance from the table */
SELECT pickup_ts, pickup_loc_id, trip_distance, fare
FROM public.yellow_taxi_distances_daily
WHERE trip_distance > (SELECT percentile_cont(0.9) WITHIN GROUP (ORDER BY trip_distance) FROM public.yellow_taxi_distances_daily)
ORDER BY trip_distance DESC;
