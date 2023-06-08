# yellow_taxi

## Project Description

The project has two Makefile commands:
make up - to start the project
make down - to stop the project and remove any orphaned containers

This is a FastAPI project that exposes three main endpoints:
1. /distance/get_90th_percentile - this endpoint returns the 90th percentile of the trip distance
2. /aggregate/get_daily_aggs - this endpoint returns the daily aggregates for passenger count and fare by location
3. /aggregate/get_hourly_aggs - this endpoint returns the hourly aggregates for passenger count and fare by location

To use the endpoints, it is best to avoid the swagger UI since encoding large JSON files takes a long time.
Instead, after running the docker container, use a service like Postman to send requests to the endpoints or
use localhost:9000/<endpoint> in your browser.

The overall thinking behind the aggregate endpoints is to provide some visibility into the taxi service patterns
for a given location. One could imagine data like this being used to help taxi drivers decide where to wait for
fares or to help the taxi service decide where to place their cars.
