from flask import Flask, jsonify, request

import requests
import datetime


api_key = '94be0d70f52a4bfe92a61219242606'

# Base URL
base_url = 'http://api.weatherapi.com/v1'

# Endpoint (for example, current weather data)
endpoint = '/history.json'

app = Flask(__name__)

# Function to calculate daily weather averages for a location
def get_daily_averages(location):
  today = datetime.datetime.now()

  # Define dictionaries to store daily totals
  daily_rainfall = {}
  daily_humidity = {}
  daily_temperature = {}

  # Loop through the past 7 days
  for i in range(7):
    date = today - datetime.timedelta(days=i)
    date_str = date.strftime('%Y-%m-%d')

    url = f"{base_url}{endpoint}?key={api_key}&q={location}&dt={date_str}"

    response = requests.get(url)

    if response.status_code == 200:
      data = response.json()

      if 'forecast' in data and 'forecastday' in data['forecast']:
        daily_data = data['forecast']['forecastday'][0]

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

  # Calculate average values for each parameter
  average_values = {}
  for parameter, daily_values in [('rainfall (mm)', daily_rainfall), 
                                  ('humidity (%)', daily_humidity), 
                                  ('temperature (°C)', daily_temperature)]:
    total_value = sum(daily_values.values())
    day_count = len(daily_values)
    if day_count > 0:
      average_values[parameter] = total_value / day_count
    else:
      average_values[parameter] = "No data available"

  return average_values

@app.route('/weather/averages')
def get_weather_averages():
  # Get location from query parameter
  location = request.args.get('location')

  if not location:
    return jsonify({'error': 'Missing required parameter: location'}), 400

  # Calculate daily averages for the provided location
  average_values = get_daily_averages(location)

  # Return JSON response
  return jsonify(average_values)

if __name__ == '__main__':
  app.run(debug=True)