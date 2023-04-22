import requests
from datetime import date, timedelta, datetime
import json
import csv
import time
import pandas as pd
import random

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def get_flight_data():
    directs = "MAD-BCN, MAD-PMI, MAD-AGP, MAD-ALC, BCN-MAD, BCN-PMI, BCN-AGP, BCN-ALC, PMI-BCN, PMI-MAD, PMI-AGP, PMI-ALC, AGP-MAD, AGP-BCN, AGP-PMI, ALC-BCN, ALC-MAD, ALC-PMI".split(", ")
    directs = [x for x in directs if 'ALC' not in x]
    directs = [x.split("-") for x in directs]

    days = 7
    req_params = ['flightNumber', 'departureAirportFsCode', 'arrivalAirportFsCode', 'departureTime', 'arrivalTime', 'stops', 'departureTerminal', 'arrivalTerminal']
    timestamp = int(time.time())
    file_name = f'logs/scheduledFlights_4dirs_{timestamp}.csv'
    with open(file_name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(req_params)
    
    for direct in directs:
        for i in range(1, days+1):
            cur_date = date.today() + timedelta(days=i)

            params = {
                'appId':'8d9f59d5',
                'appKey':'434d9d90d914eef00c84cad6add63688',
                'departureAirportCode':direct[0],
                'arrivalAirportCode':direct[1],
                'year':cur_date.year,
                'month':cur_date.month,
                'day':cur_date.day,
                'codeType':'IATA'
            }

            api_result = requests.get(
                "https://api.flightstats.com/flex/schedules/rest/v1/json"
                f"/from/{params['departureAirportCode']}/to/{params['arrivalAirportCode']}"
                f"/departing/{params['year']}/{params['month']}/{params['day']}"
                f"?appId={params['appId']}"
                f"&appKey={params['appKey']}"
                f"&codeType={params['codeType']}")
            
            output = api_result.json()

            
            with open(file_name, 'a', newline='') as file:
                writer = csv.writer(file)
                for idx in range(len(output['scheduledFlights'])):
                    output_row = []
                    for param in req_params:
                        if param in output['scheduledFlights'][idx]:
                            output_row.append(output['scheduledFlights'][idx][param])
                        else:
                            output_row.append(None)
                    writer.writerow(output_row)
    df = pd.read_csv(file_name)
    df.to_parquet(f'logs/scheduledFlights_4dirs_{timestamp}.parquet')

default_args = {
    "owner": "airflow",
    "retries": 0,
    "start_date": datetime(2023, 4, 16),
}

dag = DAG(
    "flight_data_dag",
    default_args=default_args,
    description="Retrieve flight data",
    schedule_interval="@daily",  # Daily execution
    catchup=False,
    tags=["cargo"],
)

get_flight_data_task = PythonOperator(
    task_id="get_flight_data",
    python_callable=get_flight_data,
    dag=dag,
)
