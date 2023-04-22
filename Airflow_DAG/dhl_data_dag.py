import pandas as pd
import requests
import io
import time

from airflow import DAG
import datetime as dt
from airflow.utils.dates import days_ago
from airflow.operators.python_operator import PythonOperator

default_args = {
    'owner':'airflow',
    'email':['tianheng@example.com'],
    'start_date':days_ago(0),
    'retries':1,
    "retry_delay":dt.timedelta(minutes = 5)}

dag = DAG("dhl_data_loading_dag",
          description = "Loading DHL data to the temporary landing",
          default_args = default_args,
          schedule_interval = dt.timedelta(days=30),
          tags=['cargo'])



def dhl_raw_data_loader(url):

    username = '997-icu'
    token = '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'

    session = requests.Session()
    session.auth = (username, token)
    

    cursor = session.get(url)
    if cursor.ok == False:
        print("Something went wrong when fetching the file from {}".format(url))
        return 0
    else:
        file = cursor.content
        return file

def dhl_raw_data_loader_whole():
    Domestic_Price_url = "https://raw.githubusercontent.com/SYusupov/BDM_Cargo/main/dhl_service_fee/raw_data/Domestic_Price.txt" 
    Domestic_Zona_url = "https://raw.githubusercontent.com/SYusupov/BDM_Cargo/main/dhl_service_fee/raw_data/Domestic_Zona.csv"
    Zona_Matrix_url = "https://raw.githubusercontent.com/SYusupov/BDM_Cargo/main/dhl_service_fee/raw_data/Zona_Matrix.csv"
    
    DP = dhl_raw_data_loader(Domestic_Price_url)
    DZ = dhl_raw_data_loader(Domestic_Zona_url)
    ZM = dhl_raw_data_loader(Zona_Matrix_url)

    timestamp = int(time.time())
    if DP != 0:
        DP_df = pd.read_csv(io.StringIO(DP.decode('utf-8')),sep=" ",names = ["Peso(en kg)", "A", "B","C","D"],skiprows=[0])
        print(DP_df.head(),"\n")
        DP_df.to_csv(f"logs/Domestic_Price_{timestamp}.csv",index = False,encoding = "utf_8_sig")
    if DZ != 0:
        DZ_df = pd.read_csv(io.StringIO(DZ.decode('utf-8')),sep=",")
        print(DZ_df.head(),"\n")
        DZ_df.to_csv(f"logs/Domestic_Zona_{timestamp}.csv",index = False,encoding = "utf_8_sig")
    if ZM != 0:
        ZM_df = pd.read_csv(io.StringIO(ZM.decode('utf-8')),sep = ',')
        print(ZM_df.head(),"\n")
        ZM_df.to_csv(f"logs/Zona_Matrix_{timestamp}.csv",index = False,encoding = "utf_8_sig")
    
  
dhl_data_loader_task = PythonOperator(
    task_id='get_dhl_raw_data',
    python_callable=dhl_raw_data_loader_whole,
    dag=dag
)


    
    