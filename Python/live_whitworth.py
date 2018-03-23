import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import mysql.connector
from mysql.connector import Error


url_whitworth = "http://whitworth.cas.manchester.ac.uk/current/index.html"

dbuser = 'u667487650_vinti'
dbpassword = 'Vinti123!'
dbhost = 'sql152.main-hosting.eu'
dbdatabase = 'u667487650_solar'

params = {
    'user': dbuser,
    'password': dbpassword,
    'host': dbhost,
    'database': dbdatabase
}


def parseDatetime(datetime_str):
  datetimeObject = datetime.strptime(datetime_str, "%d %b %Y %H:%M")
  datetimeFormated = datetime.strftime(datetimeObject, "%Y-%m-%d %H:%M:%S")
  newDatetimeObject = datetime.strptime(datetimeFormated, "%Y-%m-%d %H:%M:%S")
  print(str(type(newDatetimeObject)))
  return newDatetimeObject


def getWeatherVariables(URL, site_name):
  print("Getting data from " + site_name + "...")
  request = requests.get(URL)
  code = request.status_code
  if code == 200:
    rowNames = ["Last Updated (UTC)", "Roof Level Temperature (C)",
                "Relative Humidity (%)", "Dew Point Temperature (C)",
                "Wind Speed (m/s)", "Wind Direction (Deg)",
                "Accumulated Precipitation (mm last 24H)",
                "Total Downward Solar Radiation (W/m2)"]

    soup = BeautifulSoup(request.text, 'html.parser')
    table = soup.table
    rows = table.findAll('tr')

    weather_variables = [None] * 8

    index = 0
    for row in rows:
      row_fields = row.findAll('td')
      if row_fields[0].get_text() == rowNames[index]:
        weather_variables[index] = row_fields[1].get_text()
        print("  Extracted " + rowNames[index] + "  " + str(row_fields[1].get_text()))

        if index == 7:
          print("")
          break
        else:
          index += 1
  else:
    print(site_name + " did not respond!")

  return weather_variables


def main():
  site_names = ["Whitworth", "Holme Moss"]
  conn = mysql.connector.connect(**params)

  if conn.is_connected():
    print('Connected to Observatory_live!')
  else:
    print('Connection error!')
  cursor = conn.cursor()

  print("Running...(Press CTRL + C to end)")
  location = site_names[0]
  previous_weather_variables = [None] * 8
  weather_variables = [None] * 8
  while True:
    weather_variables = getWeatherVariables(url_whitworth, site_names[0])

    if previous_weather_variables[0] != weather_variables[0]:
      date = datetime.date(parseDatetime(weather_variables[0]))
      time = datetime.time(parseDatetime(weather_variables[0]))
      temperature = weather_variables[1]
      dew_point = weather_variables[3]
      relative_humidity = weather_variables[2]
      wind_speed = weather_variables[4]
      wind_direction = weather_variables[5]
      total_solar_radiation = weather_variables[7]
      precipitation = weather_variables[6]

      print("Querying...")
      query_template = "INSERT INTO Observatory_live VALUES (\"{}\", \"{}\", \"{}\", {}, {}, {}, {}, {}, {}, {}) ON DUPLICATE KEY UPDATE Temperature={}, Dew_point={}, Relative_humidity={}, Wind_speed={}, Wind_direction={}, Total_solar_radiation={}, Precipitation={}"
      query = query_template.format(location, date, time, temperature, dew_point, relative_humidity, wind_speed, wind_direction, total_solar_radiation, precipitation, temperature, dew_point, relative_humidity, wind_speed, wind_direction, total_solar_radiation, precipitation)
      cursor.execute(query)
      conn.commit()

    previous_weather_variables = weather_variables
    sleep(1)

  cursor.close()

   
main()