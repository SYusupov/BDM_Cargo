import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

import os

localPath = '/home/sayyor/Desktop/BDMA_Studies/BigDataManagement/BDM_Cargo/product_requests'

# connecting to HDFS
hdfs = pa.hdfs.connect(host='localhost', port=9000)

# check if users file exists in HDFS
users_filepath = "hdfs://localhost:9000/input/users.parquet"
users_file_exists = pa.HadoopFileSystem.exists(hdfs, path=users_filepath)

if not users_file_exists:
    # create user parquet file
    columns = [
        'user_id','firstname','lastname','gender','nationality','mobile','dob',
        'is_traveller','streetName','streetNumber','buildingNumber','postalCode',
        'city','provence','country','Filename'
    ]
    df = pd.DataFrame(columns=columns)
    # df_parq = df.to_parquet(localPath+'/users.parquet')
    p_df = pa.Table.from_pandas(df)

    with hdfs.open(users_filepath, "wb") as writer:
        pq.write_table(p_df, writer)

# find all new users to append
new_users = [filename for filename in os.listdir(localPath) if filename.startswith("user") and filename.endswith('.csv') and filename != 'users.csv']

dataset = pq.ParquetDataset(users_filepath, filesystem=hdfs)
table = dataset.read()
df = table.to_pandas()
df = df.astype({'is_traveller':bool})

for user_file in new_users:
    df1 = pd.read_csv(localPath+'/'+user_file)
    df1 = df1.astype({'is_traveller':bool})
    df = pd.concat([df, df1])

# writing back the users parquet file
p_df = pa.Table.from_pandas(df)
with hdfs.open(users_filepath, "wb") as writer:
    pq.write_table(p_df, writer)