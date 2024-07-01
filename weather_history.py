import requests
import datetime
import csv

# Digvijay API key
api_key = '94be0d70f52a4bfe92a61219242606'

# Base URL
base_url = 'http://api.weatherapi.com/v1'

# Endpoint (for example, current weather data)
endpoint = '/history.json'

# Location for which to get the weather
location = '12.8615,77.6647'

# Get today's date
today = datetime.datetime.now()

# Calculate the date 370 days ago
two_hundred_days_ago = today - datetime.timedelta(days=370)

# Initialize an empty list to store daily data
daily_data = []

# Loop over each day in the last 370 days
for i in range(370):
    # Calculate the date for the current iteration
    date = two_hundred_days_ago + datetime.timedelta(days=i)
    date_str = date.strftime('%Y-%m-%d')

    # Complete URL
    url = f"{base_url}{endpoint}?key={api_key}&q={location}&dt={date_str}"

    # Make the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()

        # Extract daily data and append to the list
        if 'forecast' in data and 'forecastday' in data['forecast']:
            day_data = data['forecast']['forecastday'][0]['day']
            daily_data.append({
                'date': date_str,
                'rainfall': day_data['totalprecip_mm'],
                'humidity': day_data['avghumidity'],
                'temperature': day_data['avgtemp_c']
            })
    else:
        print(f"Error: {response.status_code} for date: {date_str}")

# Define the CSV file name
csv_file = '367_days_daily_weather_data.csv'

# Write data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['date', 'rainfall', 'humidity', 'temperature'])
    writer.writeheader()
    writer.writerows(daily_data)

print(f"Data saved to {csv_file}")