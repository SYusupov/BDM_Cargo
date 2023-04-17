import requests
from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def get_gas_data():
    requests.get('http://10.192.139.60:8081/gas/simulator')

# Define default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Create the DAG
dag = DAG(
    dag_id='gas_data_dag',
    default_args=default_args,
    schedule_interval=None,  # This means the DAG will not be scheduled; it can only be triggered manually.
    start_date=datetime(2023, 4, 17),
    catchup=False,
    tags=['cargo']
)

get_gas_data_task = PythonOperator(
    task_id='get_gas_data',
    python_callable=get_gas_data,
    dag=dag
)
