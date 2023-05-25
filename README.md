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

### Tradeoffs
A few tradeoffs were made in the design of this project. The first is that the data was uploaded manually to the
database. Without a running Airflow instance, it was not possible to automate the data upload (and local Airflow might
not have cut it for this project; though I started down that path, as one can see with [this repo](https://github.com/smithjustinm/airflow_operations)).

The second tradeoff was choosing to use a basic aggregate function to get the
distance percentile instead of relying on the Timescale hyperfunction. However, the table used is a hypertable, which
does result in better performance.


### Daily Data Drops to Salesforce
The daily data drops to Salesforce could be handled in a few ways. The most common is to use a tool like Airflow to
schedule the data drops. Custom operators make it easy to connect to Salesforce and upload the data. Using tools like
Astronomer, it is easy to deploy Airflow to the cloud and schedule the data drops. A (very) basic design for a gitflow
workflow is shown below via the link:

[Astronomer-Gitflow](https://lucid.app/lucidchart/669f5feb-2bc5-437e-9566-5ce07d0e328b/edit?viewport_loc=207%2C323%2C1489%2C1045%2C0_0&invitationId=inv_1bae5d5f-3944-46cc-9782-fb428f2c80ba)

#### Backfilling
Backfilling data is a common task in data engineering. In this case, the data drops would need to be backfilled to
ensure that the data in Salesforce is accurate. This could be done by using a tool like Airflow to schedule the data
drops. The data drops could be scheduled to run every day at a certain time. If the data drops fail, Airflow will
automatically retry the data drops. If the data drops fail for a long period of time, the data drops could be manually
backfilled by running the data drops for the missing days.


#### Avoiding Duplicate Data
Again, using a tool like Airflow is a good way to avoid duplicate data. DAGs can be set up to ensure that the data
drops are not run more than once. The atomicity and idempotency of the data drops can be ensured by proper testing and
Airflow configuration.
