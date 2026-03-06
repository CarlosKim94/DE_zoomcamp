## Module 6 Homework
In this homework we'll put what we learned about Spark in practice.
For this homework we will be using the Yellow 2025-11 data from the official website:

`wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-11.parquet`

## Question 1: Install Spark and PySpark
- Install Spark
- Run PySpark
- Create a local spark session
- Execute spark.version.

```bash
import pyspark
from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .master("local[*]") \
    .appName('test') \
    .getOrCreate()

print(f"Spark version: {spark.version}")
spark.stop()
```

Answer: `Spark version: 4.1.1`

## Question 2: Yellow November 2025
Read the November 2025 Yellow into a Spark Dataframe.
Repartition the Dataframe to 4 partitions and save it to parquet.
What is the average size of the Parquet (ending with .parquet extension) Files that were created (in MB)? Select the answer which most closely matches.

Answer: `24.4`

## Question 3: Count records
How many taxi trips were there on the 15th of November?
Consider only trips that started on the 15th of November.

```bash
from pyspark.sql.functions import col
df.filter(
    (col("tpep_pickup_datetime") >= "2025-11-15") &
    (col("tpep_pickup_datetime") < "2025-11-16")
).count()
```
Answer: `162604`

## Question 4: Longest trip
What is the length of the longest trip in the dataset in hours?

```bash
df.createOrReplaceTempView("trips")
spark.sql("""
SELECT 
    MAX((unix_timestamp(tpep_dropoff_datetime) - unix_timestamp(tpep_pickup_datetime)) / 3600.0) AS longest_trip_hours
FROM trips
""").show()
```

Answer: `90.646667`

## Question 5: User Interface
Spark's User Interface which shows the application's dashboard runs on which local port?

Answer: `localhost:4040`

## Question 6: Least frequent pickup location zone
Load the zone lookup data into a temp view in Spark:

`wget https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv`

Using the zone lookup data and the Yellow November 2025 data, what is the name of the LEAST frequent pickup location Zone?

```bash
zone_df = spark.read \
    .option("header", "true") \
    .csv("taxi_zone_lookup.csv")

zone_df.createOrReplaceTempView("zones")
spark.sql("""
SELECT
    z.Zone,
    COUNT(*) AS pickup_count
FROM trips t
JOIN zones z
ON t.PULocationID = z.LocationID
GROUP BY z.Zone
ORDER BY pickup_count ASC
LIMIT 1
""").show()
```

Answer: `Arden Heights`