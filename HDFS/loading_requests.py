import pyarrow as pa
import pyarrow.parquet as pq
import pandas as pd

import os

localPath = '/home/sayyor/Desktop/BDMA_Studies/BigDataManagement/BDM_Cargo/product_requests'

# connecting to HDFS
hdfs = pa.hdfs.connect(host='localhost', port=9000)

# check if users file exists in HDFS
users_filepath = "hdfs://localhost:9000/input/requests.parquet"
users_file_exists = pa.HadoopFileSystem.exists(hdfs, path=users_filepath)

if not users_file_exists:
    # create user parquet file
    columns = [
        'product_id','product_weight_g','product_length_cm','product_height_cm',
        'product_width_cm','product_category_name_english','product_name',
        'product_image_link','user_id','request_date','Filename'
    ]
    df = pd.DataFrame(columns=columns)
    # df_parq = df.to_parquet(localPath+'/users.parquet')
    p_df = pa.Table.from_pandas(df)

    with hdfs.open(users_filepath, "wb") as writer:
        pq.write_table(p_df, writer)

# find all new users to append
new_users = [filename for filename in os.listdir(localPath) if filename.startswith("request") and filename.endswith('.csv') and filename != 'requests.csv']

dataset = pq.ParquetDataset(users_filepath, filesystem=hdfs)
table = dataset.read()
df = table.to_pandas()

for user_file in new_users:
    df1 = pd.read_csv(localPath+'/'+user_file)
    df = pd.concat([df, df1])

print(df.head())

# writing back the users parquet file
p_df = pa.Table.from_pandas(df)
with hdfs.open(users_filepath, "wb") as writer:
    pq.write_table(p_df, writer)