## BigQuery Setup
Create an external table using the Yellow Taxi Trip Records.

Create a (regular/materialized) table in BQ using the Yellow Taxi Trip Records (do not partition or cluster this table).
```bash
CREATE OR REPLACE EXTERNAL TABLE `homework03.yellow_taxi_external`
OPTIONS (
  format = 'PARQUET',
  uris = ['gs://homeowkr03-bucket/*.parquet']
);
CREATE OR REPLACE TABLE `homework03.yellow_taxi`
AS
SELECT *
FROM `homework03.yellow_taxi_external`;
```
## Question 1. Counting records
What is count of records for the 2024 Yellow Taxi Data?

`SELECT COUNT(*) FROM 'homework03.yellow_taxi';`

Answer: `20332093`

## Question 2. Data read estimation
Write a query to count the distinct number of PULocationIDs for the entire dataset on both the tables.

What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?
```bash
SELECT COUNT(DISTINCT PULocationID) AS distinct_pu_locations FROM 'homework03.yellow_taxi';
SELECT COUNT(DISTINCT PULocationID) 
FROM 'homework03.yellow_taxi_external;
```
Answer: `0 MB for the External Table and 155.12 MB for the Materialized Table`

## Question 3. Understanding columnar storage
Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table.

Why are the estimated number of Bytes different?
```bash
SELECT PULocationID FROM 'homework03.yellow_taxi';
SELECT DOLocationID, DOLocationID FROM 'homework03.yellow_taxi';
```
Answer: BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.

## Question 4. Counting zero fare trips
How many records have a fare_amount of 0?

```bash
SELECT COUNT(fare_amount)
FROM 'homework03.yellow_taxi'
WHERE fare_amount=0;
```
Answer: `8333`

## Question 5. Partitioning and clustering
What is the best strategy to make an optimized table in Big Query if your query will always filter based on tpep_dropoff_datetime and order the results by VendorID (Create a new table with this strategy)

```bash
CREATE OR REPLACE TABLE 'homework03.yellow_taxi_optimized'
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT *
FROM 'homework03.yellow_taxi';
```
Answer: `Partition by tpep_dropoff_datetime and Cluster on VendorID`

## Question 6. Partition benefits
Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)

Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?

```bash
SELECT DISTINCT VendorID
FROM 'homework03.yellow_taxi'
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
310.24 MB
```bash
SELECT DISTINCT VendorID
FROM 'homework03.yellow_taxi_optimized'
WHERE tpep_dropoff_datetime BETWEEN '2024-03-01' AND '2024-03-15';
```
26.84 MB

Answer: `310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`

## Question 7. External table storage
Where is the data stored in the External Table you created?

Answer: `GCP Bucket`

## Question 8. Clustering best practices
It is best practice in Big Query to always cluster your data:

Answer: `False`

## Question 9. Understanding table scans
No Points: Write a SELECT count(*) query FROM the materialized table you created. How many bytes does it estimate will be read? Why?

`SELECT count(*) FROM 'homework03.yellow_taxi';`

Answer: 0B. BigQuery knows the number of rows without reading all columns.