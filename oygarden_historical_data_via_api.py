import requests
import pandas as pd
from datetime import datetime, timedelta
import re

client_id = 'b81ff387-2723-48d0-877c-1a26edf1001c'

# First find the source ID for Øygarden
sources_endpoint = 'https://frost.met.no/sources/v0.jsonld'
r = requests.get(sources_endpoint, auth=(client_id, ''))
if r.status_code == 200:
    sources = r.json()['data']
    source_id = next((s['id'] for s in sources 
                     if s.get('municipality') == 'ØYGARDEN'), None)
    if source_id:
        print(f"Found source ID: {source_id}")
    else:
        print("No weather station found in Øygarden")
        exit(1)
else:
    print(f"Error getting sources: {r.status_code}")
    exit(1)

# Define endpoint and parameters
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': source_id,
    'elements': 'air_temperature',  
    'referencetime': '2014-01-01/2014-12-31',  
}

# Extract start and end dates from referencetime
start_date, end_date = re.match(r'(\d{4}-\d{2}-\d{2})/(\d{4}-\d{2}-\d{2})', parameters['referencetime']).groups()

# Get the weather data
r = requests.get(endpoint, parameters, auth=(client_id, ''))
json = r.json()

# Check if the request worked
if r.status_code == 200:
    data = json['data']
    print('Data retrieved successfully!')
    
    # Convert to DataFrame using a list comprehension and concat
    frames = []
    for item in data:
        row = pd.DataFrame(item['observations'])
        row['referenceTime'] = item['referenceTime']
        row['sourceId'] = item['sourceId']
        frames.append(row)
    
    df = pd.concat(frames, ignore_index=True)
    
    # Clean up DataFrame to only include date and temperature, then calculate daily means
    clean_df = (df[['referenceTime', 'value']]
                .rename(columns={'referenceTime': 'date', 'value': 'temperature'})
                .assign(
                    date=lambda x: pd.to_datetime(x['date']).dt.date,
                    temperature=lambda x: pd.to_numeric(x['temperature'])
                )
                .groupby('date')['temperature']
                .mean()
                .round(1)  # Round to 1 decimal place
                .reset_index())
    
    print("Daily mean temperatures:")
    print(clean_df.head())
    
    # Generate filename with date range
    filename = f'Øygarden_temperature_{start_date}_to_{end_date}.csv'
    clean_df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])

