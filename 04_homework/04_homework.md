## Question 1. dbt Lineage and Execution
Given a dbt project with the following structure:

If you run dbt run --select int_trips_unioned, what models will be built?

Answer: `stg_green_tripdata, stg_yellow_tripdata, and int_trips_unioned (upstream dependencies)`

## Question 2. dbt Tests
You've configured a generic test like this in your schema.yml:

Your model fct_trips has been running successfully for months. A new value 6 now appears in the source data.

What happens when you run dbt test --select fct_trips?

Answer: `dbt will fail the test, returning a non-zero exit code`

## Question 3. Counting Records in fct_monthly_zone_revenue
After running your dbt project, query the fct_monthly_zone_revenue model.

What is the count of records in the fct_monthly_zone_revenue model?

```bash
SELECT COUNT(*)
FROM 'dbt_prod.fct_monthly_zone_revenue';
```
Answer: `12184`

## Question 4. Best Performing Zone for Green Taxis (2020)
Using the fct_monthly_zone_revenue table, find the pickup zone with the highest total revenue (revenue_monthly_total_amount) for Green taxi trips in 2020.

Which zone had the highest revenue?

```bash
SELECT 
    pickup_zone,
    SUM(revenue_monthly_total_amount) AS total_revenue
FROM 'dbt_prod.fct_monthly_zone_revenue'
WHERE service_type = 'Green'
  AND EXTRACT(YEAR FROM revenue_month) = 2020
GROUP BY pickup_zone
ORDER BY total_revenue DESC
LIMIT 1;
```
Answer: `East Harlem North	1817721.75`

## Question 5. Green Taxi Trip Counts (October 2019)
Using the fct_monthly_zone_revenue table, what is the total number of trips (total_monthly_trips) for Green taxis in October 2019?

```bash
SELECT SUM(total_monthly_trips)
FROM 'dbt_prod.fct_monthly_zone_revenue'
WHERE service_type = 'Green'
  AND EXTRACT(YEAR FROM revenue_month) = 2019
  AND EXTRACT(MONTH FROM revenue_month) = 10;
```

Answer: `384624`

## Question 6. Build a Staging Model for FHV Data
Create a staging model for the For-Hire Vehicle (FHV) trip data for 2019.

1. Load the FHV trip data for 2019 into your data warehouse

```bash
CREATE OR REPLACE EXTERNAL TABLE 'nytaxi.fhv_tripdata_ext'
OPTIONS(
  format = 'CSV',
  skip_leading_rows = 1,
  uris = ['gs://homeowkr03-bucket/fhv_tripdata_2019-*.csv']
);

CREATE OR REPLACE TABLE 'nytaxi.fhv_tripdata' AS
SELECT *
FROM 'nytaxi.fhv_tripdata_ext';
```

2. Create a staging model stg_fhv_tripdata with these requirements:
    - Filter out records where dispatching_base_num IS NULL
    - Rename fields to match your project's naming conventions (e.g., PUlocationID → pickup_location_id)

```bash
with source as (
    select *
    from {{ source('raw', 'fhv_tripdata') }}  -- points to FHV table
),

renamed as (
    select
        dispatching_base_num,
        cast(PUlocationID as int64) as pickup_location_id,
        cast(DOlocationID as int64) as dropoff_location_id,
        cast(pickup_datetime as timestamp) as pickup_datetime,
        cast(dropOff_datetime as timestamp) as dropoff_datetime,
        cast(SR_Flag as string) as shared_request_flag,
        Affiliated_base_number as affiliated_base_number
    from source
    where dispatching_base_num is not null
)

select * from renamed
```

What is the count of records in stg_fhv_tripdata?

`SELECT COUNT(*) FROM 'dbt_prod.stg_fhv_tripdata';`
Answer: `43244693`
