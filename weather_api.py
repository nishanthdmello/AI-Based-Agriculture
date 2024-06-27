import requests
import datetime

api_key = '94be0d70f52a4bfe92a61219242606'

# Base URL
base_url = 'http://api.weatherapi.com/v1'

# Endpoint (for example, current weather data)
endpoint = '/history.json'

# Location for which to get the weather
location = '12.8615,77.6647'

# Get today's date
today = datetime.datetime.now()

# Define dictionaries to store daily totals
daily_rainfall = {}
daily_humidity = {}
daily_temperature = {}

# Loop through the past 7 days
for i in range(7):
  # Calculate the date for the current iteration
  date = today - datetime.timedelta(days=i)
  date_str = date.strftime('%Y-%m-%d')

  # Complete URL
  url = f"{base_url}{endpoint}?key={api_key}&q={location}&dt={date_str}"

  # Make the request
  response = requests.get(url)

  # Check if request was successful
  if response.status_code == 200:
    # Parse the JSON data
    data = response.json()

    # Check if 'forecast' exists
    if 'forecast' in data and 'forecastday' in data['forecast']:
      daily_data = data['forecast']['forecastday'][0]

      # Extract daily values (adjust based on API structure)
      try:
        daily_rainfall[date_str] = daily_data.get('day', {}).get('totalprecip_mm', 0)
        daily_humidity[date_str] = daily_data.get('day', {}).get('avghumidity', 0)
        daily_temperature[date_str] = daily_data.get('day', {}).get('avgtemp_c', 0)
      except KeyError:
        print(f"Error: Missing data for '{date_str}'")
    else:
      print(f"Error: Data not found for {date_str}")
  else:
    print(f"Error: {response.status_code} for date: {date_str}")

# Calculate and print average values for each parameter
print("Average weather values for the past week:")
for parameter, daily_values in [('rainfall (mm)', daily_rainfall), 
                                ('humidity (%)', daily_humidity), 
                                ('temperature (°C)', daily_temperature)]:
  total_value = sum(daily_values.values())
  day_count = len(daily_values)
  if day_count > 0:
    average_value = total_value / day_count
    print(f"\t- Average {parameter}: {average_value:.2f}")
  else:
    print(f"\t- No data available for {parameter}")
