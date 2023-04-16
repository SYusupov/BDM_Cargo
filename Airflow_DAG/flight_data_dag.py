import requests
from datetime import date, timedelta, datetime
import json
import csv

from airflow import DAG
from airflow.operators.python_operator import PythonOperator

def get_flight_data():
    days = 7
    for i in range(1, days+1):
        cur_date = date.today() + timedelta(days=i)
        print(cur_date)

        # scheduled flights by route, departing on the given date
        params = {
            'appId':'8d9f59d5',
            'appKey':'434d9d90d914eef00c84cad6add63688',
            'departureAirportCode':'BCN',
            'arrivalAirportCode':'MAD',
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

        # with open("response2_FlightStats_SchedulesAPI.json", "w") as out:
        # json.dump(output, out)

        req_params = ['flightNumber', 'departureAirportFsCode', 'arrivalAirportFsCode', 'departureTime', 'arrivalTime', 'stops', 'departureTerminal', 'arrivalTerminal']
        with open('logs/scheduledFlights2.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # writer.writerow(req_params)
            for idx in range(len(output['scheduledFlights'])):
                writer.writerow([output['scheduledFlights'][idx][param] for param in req_params])

    params = {
    'access_key': 'e78c58f49ec83555fef1d339c0cc83ee',
    'dep_iata': 'BCN',
    'arr_iata': 'MAD'
    }

    # request 1, param: just access_key
    # api_result = requests.get('https://api.aviationstack.com/v1/flights', params)

    # request 2
    api_result = requests.get('http://api.aviationstack.com/v1/routes', params)
    api_response = api_result.json()
    print(api_response)

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
