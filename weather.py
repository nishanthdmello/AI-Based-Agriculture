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



# import datetime as dt
# import requests
# import time

# # Function to get weather data for a specific day
# def get_daily_weather(api_key, lat, lon, timestamp):
#     url = f"http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&dt={timestamp}&appid={api_key}"
#     response = requests.get(url)
#     return response.json()

# # Function to loop through each day of the month
# def get_monthly_weather(api_key, lat, lon, year, month):
#     weather_data = []
#     num_days = (dt.date(year, month + 1, 1) - dt.date(year, month, 1)).days if month != 12 else 31
#     for day in range(1, num_days + 1):
#         timestamp = int(dt.datetime(year, month, day, 0, 0).timestamp())
#         daily_data = get_daily_weather(api_key, lat, lon, timestamp)
#         weather_data.append(daily_data)
#         time.sleep(1)  # to comply with rate limiting
#     print(daily_data)
#     return weather_data

# # Example usage
# api_key = "9898e60334b3a2f276b37b84df07b8a1"
# lat = 12.9762  # Latitude for London
# lon = 77.6033  # Longitude for London
# year = 2023
# month = 5

# monthly_weather_data = get_monthly_weather(api_key, lat, lon, year, month)
# print(monthly_weather_data)


# for daily_data in monthly_weather_data:
#     for hour_data in daily_data.get('hourly', []):
#         timestamp = hour_data['dt']
#         temperature = hour_data['temp']
#         humidity = hour_data['humidity']
#         rain = hour_data.get('rain', {}).get('1h', 0)  # Rain might not be present in the data
#         time_str = dt.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
#         print(f"Time: {time_str}, Temperature: {temperature}, Humidity: {humidity}, Rainfall: {rain}")




# import datetime as dt
# import requests

# base_url = "http://api.openweathermap.org/data/3.0/weather?"
# api_key = "9898e60334b3a2f276b37b84df07b8a1"

# city = "London"

# # url = base_url + "appid=" + api_key + "&q=" + city
# url="http://api.openweathermap.org/data/2.5/weather?q=Bengaluru&APPID=629342b6b97d5a67eb1f5b764ac1b60d"

# response =  requests.get(url).json()

# print(response)