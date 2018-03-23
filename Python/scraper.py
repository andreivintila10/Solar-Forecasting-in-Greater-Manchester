from time import clock
import requests
from bs4 import BeautifulSoup
from time import sleep
from datetime import datetime
import mysql.connector
from mysql.connector import Error
import threading


start_time = clock()

url_whitworth = "http://whitworth.cas.manchester.ac.uk/current/index.html"
url_holme_moss = "http://whitworth.cas.manchester.ac.uk/current/indexHM.html"

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

rowNamesLists = [["Last Updated (UTC)", "Roof Level Temperature (C)",
                  "Relative Humidity (%)", "Dew Point Temperature (C)",
                  "Wind Speed (m/s)", "Wind Direction (Deg)",
                  "Accumulated Precipitation (mm last 24H)",
                  "Total Downward Solar Radiation (W/m2)"], 
                 ["Last Updated (UTC)", "Temperature (C)", "Relative Humidity (%)",
                  "Dew Point Temperature (C)", "Wind Speed (m/s)", "Wind Direction (Deg)",
                  "Accumulated Precipitation (mm last 24H)", "Total Downward Solar Radiation (W/m2)"]]


def parseValue(value):
  if value == "NaN" or value == "No Data":
    return "NULL"
  else:
    return value


def parseDatetime(datetime_str):
  datetimeObject = datetime.strptime(datetime_str, "%d %b %Y %H:%M")
  datetimeFormated = datetime.strftime(datetimeObject, "%Y-%m-%d %H:%M:%S")
  newDatetimeObject = datetime.strptime(datetimeFormated, "%Y-%m-%d %H:%M:%S")

  return newDatetimeObject


def getWeatherVariables(URL, site_name, rowNames):
  try:
    request = requests.get(URL, timeout=10)
    code = request.status_code
    if code == 200:
      soup = BeautifulSoup(request.text, 'html.parser')
      table = soup.table
      rows = table.findAll('tr')

      weather_variables = [None] * 8

      index = 0
      for row in rows:
        row_fields = row.findAll('td')
        if row_fields[0].get_text() == rowNames[index]:
          weather_variables[index] = parseValue(row_fields[1].get_text())

          if index == 7:
            break
          else:
            index += 1
    else:
      print(site_name + " did not respond!")

  except requests.exceptions.Timeout:
    print("Timeout occurred")
    return -1

  return weather_variables


def scraper_loop(URL, site_name, params, rowNames):
  location = site_name
  query_template = "INSERT INTO Observatory_live VALUES (\"{}\", \"{}\", \"{}\", {}, {}, {}, {}, {}, {}, {}) ON DUPLICATE KEY UPDATE Temperature={}, Dew_point={}, Relative_humidity={}, Wind_speed={}, Wind_direction={}, Total_solar_radiation={}, Precipitation={}"

  previous_weather_variables = weather_variables = [None] * 8
  currentThread = threading.currentThread()
  while getattr(currentThread, "do_run", True):
    weather_variables = getWeatherVariables(URL, site_name, rowNames)

    if weather_variables != -1:
      if previous_weather_variables[0] != weather_variables[0]:
        try:
          conn = mysql.connector.connect(**params)

          if conn.is_connected():
            cursor = conn.cursor()

            date = datetime.date(parseDatetime(weather_variables[0]))
            time = datetime.time(parseDatetime(weather_variables[0]))

            temperature = weather_variables[1]
            dew_point = weather_variables[3]
            relative_humidity = weather_variables[2]
            wind_speed = weather_variables[4]
            wind_direction = weather_variables[5]
            total_solar_radiation = weather_variables[7]
            precipitation = weather_variables[6]

            query = query_template.format(location, date, time, temperature, dew_point, relative_humidity, wind_speed, wind_direction, total_solar_radiation, precipitation, temperature, dew_point, relative_humidity, wind_speed, wind_direction, total_solar_radiation, precipitation)
            cursor.execute(query)
            conn.commit()
            cursor.close()
            conn.close()

            previous_weather_variables = weather_variables
            print("Stored weather data for " + location)
            sleep(5)
          else:
            print('Connection error!')
      
        except Error as e:
          print(e)
    else:
      print("Request timeout " + location)


def main():
  site_names = ["Whitworth", "Holme Moss"]
  thread1 = threading.Thread(name='Whitworth', target=scraper_loop, args=(url_whitworth, site_names[0], params, rowNamesLists[0]))
  thread2 = threading.Thread(name='Holme_Moss', target=scraper_loop, args=(url_holme_moss, site_names[1], params, rowNamesLists[1]))

  thread1.start()
  thread2.start()

  print("Running...")
  print("Type exit to end the program")

  input_usr = input()
  while input_usr != "exit":
    input_usr = input()

  thread1.do_run = False
  thread2.do_run = False

  thread1.join(1)
  thread2.join(1)

  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))


if __name__ == "__main__":
  main()