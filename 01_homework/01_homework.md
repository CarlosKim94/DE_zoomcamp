## Question 1. Understanding Docker images

Run docker with the python:3.13 image. Use an entrypoint bash to interact with the container.
What's the version of pip in the image?
```bash
docker pull python:3.13
docker run -it --entrypoint bash python:3.13
pip --version
```
Answer: `pip 25.3 from /usr/local/lib/python3.13/site-packages/pip (python 3.13)`

## Question 2. Understanding Docker networking and docker-compose

Given the docker-compose.yaml, what is the hostname and port that pgadmin should use to connect to the postgres database?
Answer: hostname = db, port = 5432

#### Prepare the Data

Download the green taxi trips data for November 2025:

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/green_tripdata_2025-11.parquet`
You will also need the dataset with zones:

`wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv`

## Question 3. Counting short trips

For the trips in November 2025 (lpep_pickup_datetime between '2025-11-01' and '2025-12-01', exclusive of the upper bound), how many trips had a trip_distance of less than or equal to 1 mile?

`uv run pgcli -h localhost -p 5433 -u root -d ny_taxi`

```bash
SELECT count(*)
FROM ny_taxi_data
WHERE lpep_pickup_datetime >= '2025-11-01'
AND lpep_pickup_datetime < '2025-12-01'
AND trip_distance <= 1;
```
Answer: `8007`

## Question 4. Longest trip for each day

Which was the pick up day with the longest trip distance? Only consider trips with trip_distance less than 100 miles (to exclude data errors).

Use the pick up time for your calculations.
```bash
SELECT lpep_pickup_datetime, trip_distance
FROM ny_taxi_data
WHERE trip_distance < 100
ORDER BY trip_distance DESC
LIMIT 1;
```
Answer: `2025-11-14 15:36:27  | 88.03 `

## Question 5. Biggest pickup zone

Which was the pickup zone with the largest total_amount (sum of all trips) on November 18th, 2025?

```bash
SELECT z."Zone" AS pickup_zone, SUM(t.total_amount) AS total_revenue
FROM ny_taxi_data t
JOIN taxi_zone_data z
ON t."PULocationID" = z."LocationID"
WHERE t.lpep_pickup_datetime >= '2025-11-18'
  AND t.lpep_pickup_datetime < '2025-11-19'
GROUP BY z."Zone"
ORDER BY total_revenue DESC
LIMIT 1;
```

Answer: `East Harlem North | 9281.919999999996`

## Question 6. Largest tip

For the passengers picked up in the zone named "East Harlem North" in November 2025, which was the drop off zone that had the largest tip?

Note: it's tip , not trip. We need the name of the zone, not the ID.

```bash
SELECT do_zone."Zone" AS dropoff_zone, SUM(t.tip_amount) AS total_tip
FROM ny_taxi_data t
JOIN taxi_zone_data pu_zone
ON t."PULocationID" = pu_zone."LocationID"
JOIN taxi_zone_data do_zone
ON t."DOLocationID" = do_zone."LocationID"
WHERE pu_zone."Zone" = 'East Harlem North'
  AND t.lpep_pickup_datetime >= '2025-11-01'
  AND t.lpep_pickup_datetime < '2025-12-01'
GROUP BY do_zone."Zone"
ORDER BY total_tip DESC
LIMIT 1;
```

Answer: `Upper East Side North | 4242.009999999992`