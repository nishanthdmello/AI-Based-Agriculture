import requests
import datetime
import csv
# digvijay API key
api_key = '94be0d70f52a4bfe92a61219242606'

# Base URL
base_url = 'http://api.weatherapi.com/v1'

# Endpoint (for example, current weather data)
endpoint = '/history.json'

# Location for which to get the weather
location = '12.8615,77.6647'

# Get today's date
today = datetime.datetime.now()

# Calculate the date one month ago
one_month_ago = today - datetime.timedelta(days=30)

# Initialize an empty list to store hourly data
hourly_data = []

# Loop over each day in the last month
for i in range(30):
    # Calculate the date for the current iteration
    date = one_month_ago + datetime.timedelta(days=i)
    date_str = date.strftime('%Y-%m-%d')

    # Complete URL
    url = f"{base_url}{endpoint}?key={api_key}&q={location}&dt={date_str}"

    # Make the request
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Parse the JSON data
        data = response.json()

        # Extract hourly data and append to the list
        if 'forecast' in data and 'forecastday' in data['forecast']:
            for hour in data['forecast']['forecastday'][0]['hour']:
                hourly_data.append({
                    'time': hour['time'],
                    'rainfall': hour['precip_mm'],
                    'humidity': hour['humidity'],
                    'temperature': hour['temp_c']
                })
    else:
        print(f"Error: {response.status_code} for date: {date_str}")

# Define the CSV file name
csv_file = 'weather_data.csv'

# Write data to the CSV file
with open(csv_file, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=['time', 'rainfall', 'humidity', 'temperature'])
    writer.writeheader()
    writer.writerows(hourly_data)

print(f"Data saved to {csv_file}")