import pandas as pd

df = pd.read_parquet("green_tripdata_2025-11.parquet")
print(df.head())
print(df.dtypes)
# df = pd.read_csv('green_tripdata_2020-02.csv')