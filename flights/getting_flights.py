import requests
from datetime import date, timedelta
import json
import csv
import pandas as pd
import random

# FIRST: pip install pyarrow 

directs = "MAD-BCN, MAD-PMI, MAD-AGP, MAD-ALC, BCN-MAD, BCN-PMI, BCN-AGP, BCN-ALC, PMI-BCN, PMI-MAD, PMI-AGP, PMI-ALC, AGP-MAD, AGP-BCN, AGP-PMI, ALC-BCN, ALC-MAD, ALC-PMI".split(", ")
directs = [x for x in directs if 'ALC' not in x]
directs = [x.split("-") for x in directs]

# getting for the next week, BCN->MDR
days = 7
req_params = ['flightNumber', 'departureAirportFsCode', 'arrivalAirportFsCode', 'departureTime', 'arrivalTime', 'stops', 'departureTerminal', 'arrivalTerminal']
with open('scheduledFlights_4dirs.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(req_params)

for direct in directs[1:]:
    print(direct)
    for i in range(1, days+1):
        cur_date = date.today() + timedelta(days=i)
        print(cur_date)

        # scheduled flights by route, departing on the given date
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

        # with open("response2_FlightStats_SchedulesAPI.json", "w") as out:
        # json.dump(output, out)

        with open('scheduledFlights_4dirs.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            # writer.writerow(req_params)
            for idx in range(len(output['scheduledFlights'])):
                output_row = []
                for param in req_params:
                    if param in output['scheduledFlights'][idx]:
                        output_row.append(output['scheduledFlights'][idx][param])
                    # some do not have arrival/depature Terminals
                    else:
                        output_row.append(None)
                writer.writerow(output_row)

# Convert CSV to Parquet
df = pd.read_csv('scheduledFlights_4dirs.csv')
df.to_parquet('scheduledFlights_4dirs.parquet')