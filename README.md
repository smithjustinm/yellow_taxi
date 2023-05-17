# yellow_taxi

## Project Description

We will use the NYC “Yellow Taxi” Trips data provided as parquet files. You will need to find a way to collect those parquet files (as many as you can) to answer some questions.


The idea is to import all those parquet files to your TimescaleDB, so you will need to work on the data model and how you can store this information efficiently to run some queries. Remember that TimescaleDB is Postgres at its core, but with some amazing functionalities, like Hypertables, Continuous Aggregates, and Compression.

Questions to answer

Return all the trips over 0.9 percentile in the distance traveled for any Parquet files you can find there.
Create a continuous aggregate that rolls up stats on passenger count and fare amount by pickup location.
Do not implement, but explain your architecture on how you’ll solve this problem. Another request we have is to upload that information to another system daily. We need a solution that allows us to push some information into our Salesforce so Sales, Finance, and Marketing can make better decisions.
We need to have a daily dump of the trips into Salesforce.
We should avoid duplicates and have a clear way to backfill if needed.
