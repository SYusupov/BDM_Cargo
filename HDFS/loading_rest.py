import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

import os

def rewrite_file(hdfs, hdfs_filepath, local_filepath):
    p_df = pq.read_table(local_filepath)

    with hdfs.open(hdfs_filepath, "wb") as writer:
        pq.write_table(p_df, writer)

localPath = '/home/sayyor/Desktop/BDMA_Studies/BigDataManagement/BDM_Cargo/product_requests'

# connecting to HDFS
hdfs = pa.hdfs.connect(host='localhost', port=9000)

## loading cities
# check if users file exists in HDFS
hdfs_filepath = "hdfs://localhost:9000/input/cities.parquet"
local_filepath = '../sample_output/cities-1681733837854.parquet'
rewrite_file(hdfs, hdfs_filepath, local_filepath)

## loading gas
hdfs_filepath = "hdfs://localhost:9000/input/gas.parquet"
local_filepath = '../sample_output/gas-1681745714614.parquet'
rewrite_file(hdfs, hdfs_filepath, local_filepath)

## loading DHL
hdfs_filepath = "hdfs://localhost:9000/input/DHL_Price.parquet"
local_filepath = '../sample_output/DHL_Processed_Domestic_Price.parquet'
rewrite_file(hdfs, hdfs_filepath, local_filepath)

hdfs_filepath = "hdfs://localhost:9000/input/DHL_Zone.parquet"
local_filepath = '../sample_output/DHL_Processed_Domestic_Zone.parquet'
rewrite_file(hdfs, hdfs_filepath, local_filepath)

## loading scheduledFlights
local_filepath = '../sample_output/scheduledFlights_4dirs_1682179837.parquet'
hdfs_filepath = "hdfs://localhost:9000/input/scheduledFlights.parquet"
rewrite_file(hdfs, hdfs_filepath, local_filepath)