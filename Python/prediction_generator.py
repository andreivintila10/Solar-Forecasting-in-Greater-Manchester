from time import clock, sleep
import sys
from datetime import datetime, timedelta, time, date
import mysql.connector
from mysql.connector import Error
import requests
import urllib.request
import json
import pickle
import numpy as np


CONSTANT_ONE_HOUR = timedelta(hours=1)
CONSTANT_ONE_DAY = timedelta(days=1)

CONSTANT_DBUSER = 'u667487650_vinti'
CONSTANT_DBPASSWORD = 'Vinti123!'
CONSTANT_DBHOST = 'sql152.main-hosting.eu'
CONSTANT_DBDATABASE = 'u667487650_solar'

CONSTANT_DB_PARAMS = {
    'user': CONSTANT_DBUSER,
    'password': CONSTANT_DBPASSWORD,
    'host': CONSTANT_DBHOST,
    'database': CONSTANT_DBDATABASE
}


def getForecastDates(currentDatetime):
  forecast_update_hour = 9
  timeOfFirstForecast = time(18, 0, 0)

  currentTime = datetime.time(currentDatetime)
  if currentTime.hour < forecast_update_hour:
    currentDatetime -= CONSTANT_ONE_DAY

  year1 = currentDatetime.year
  month1 = currentDatetime.month
  day1 = currentDatetime.day

  datetime_yesterday = currentDatetime - CONSTANT_ONE_DAY
  year2 = datetime_yesterday.year
  month2 = datetime_yesterday.month
  day2 = datetime_yesterday.day
  
  first_date = date(year1, month1, day1)
  second_date = datetime(year2, month2, day2, timeOfFirstForecast.hour, timeOfFirstForecast.minute)

  forecastDates = []
  forecastDates.append(first_date)
  forecastDates.append(second_date)

  return forecastDates


def getURL(dateOfReference, site_code):
  url_template = "http://manunicast.seaes.manchester.ac.uk/charts/manunicast/{}{}{}/d02/meteograms/meteo_{}_{}-{}-{}_{}{}_swdown_data.txt"
  forecastDates = getForecastDates(dateOfReference)

  year1 = str(forecastDates[0].year).zfill(4)
  month1 = str(forecastDates[0].month).zfill(2)
  day1 = str(forecastDates[0].day).zfill(2)

  year2 = str(forecastDates[1].year).zfill(4)
  month2 = str(forecastDates[1].month).zfill(2)
  day2 = str(forecastDates[1].day).zfill(2)
  hour2 = str(forecastDates[1].hour).zfill(2)
  minute2 = str(forecastDates[1].minute).zfill(2)

  url = url_template.format(year1, month1, day1, site_code, year2, month2, day2, hour2, minute2)

  return url


def siteCodeToName(site_code):
  if site_code == "WHIT":
    return "Whitworth"
  elif site_code == "HOLM":
    return "Holme Moss"
  elif site_code == "MAN":
    return "Manchester Airport"
  else:
    return "Unknown"


def createDatetimeObject(date_str, time_str):
  datetimeObject = datetime(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]), int(time_str[0:2]), int(time_str[3:5]), int(time_str[6:8]))

  return datetimeObject


def generateVariablesLibrary(datetime_array, temperature_array, dew_point_array, relative_humidity_array, wind_speed_array, wind_direction_array, total_solar_radiation_array, precipitation_array):
  collection = {}
  collection['Datetime'] = datetime_array
  collection['Temperature'] = temperature_array
  collection['Dew_point'] = dew_point_array
  collection['Relative_humidity'] = relative_humidity_array
  collection['Wind_speed'] = wind_speed_array
  collection['Wind_direction'] = wind_direction_array
  collection['Total_solar_radiation'] = total_solar_radiation_array
  collection['Precipitation'] = precipitation_array

  return collection


def fetchForecastedDataForGivenHour(thisDatetime, site_code):
  try:
    url_string = getURL(thisDatetime, site_code)
    request = requests.get(url_string, timeout=10)
    code = request.status_code
    if code == 200:
      with urllib.request.urlopen(url_string) as url:
        data = json.loads(url.read().decode())

      weather_variables = []
      dataLength = len(data['xlab'])
      for index in range(0, dataLength):
        currentDatetime = datetime(int(data['xlab'][index][0:4]), int(data['xlab'][index][5:7]), int(data['xlab'][index][8:10]), int(data['xlab'][index][11:13]), 0, 0)
        if thisDatetime == currentDatetime:
          weather_variables.append(currentDatetime)
          weather_variables.append(data['temp2m'][index])
          weather_variables.append(data['td2m'][index])
          weather_variables.append(data['rh2m'][index])
          weather_variables.append(data['wspd'][index])
          weather_variables.append(data['wdir'][index])
          weather_variables.append(data['swdown'][index])
          weather_variables.append(data['precip'][index])
          break
    else:
      print("  Web page does not exist! (" + str(code) + ")")
      sleep(20)

  except requests.exceptions.Timeout:
    print ("Timeout occurred")

  return weather_variables


def fetchActualWeatherVariables(dateOfReference, hoursBehind, site_code):
  limitLeft = dateOfReference - hoursBehind + CONSTANT_ONE_HOUR
  limitRight = dateOfReference
  
  limitLeft_date = limitLeft.date()
  limitRight_date = limitRight.date()

  datetime_array = []
  temperature_array = []
  dew_point_array = []
  relative_humidity_array = []
  wind_speed_array = []
  wind_direction_array = []
  total_solar_radiation_array = []
  precipitation_array = []

  try:
    conn = mysql.connector.connect(**CONSTANT_DB_PARAMS)

    if conn.is_connected():
      print('Connected!')
    else:
      print('Connection error!')

    cursor = conn.cursor()
    query_template = "SELECT DISTINCT * FROM Observatory_live WHERE Location=\"{}\" AND Date >= \"{}\" AND Date <= \"{}\" AND TIME_FORMAT(Time, '%i:%s')='00:00' AND Temperature IS NOT NULL AND Dew_point IS NOT NULL AND Relative_humidity IS NOT NULL AND Wind_speed IS NOT NULL AND Wind_direction IS NOT NULL AND Total_solar_radiation IS NOT NULL AND Precipitation IS NOT NULL ORDER BY Date ASC, Time ASC"
    query = query_template.format(siteCodeToName(site_code), limitLeft_date, limitRight_date)
    cursor.execute(query)
    for (location, currentDate, currentTime, temperature, dew_point, relative_humidity, wind_spd, wind_dir, solar_rad, precip) in cursor:
      datetimeObject = createDatetimeObject(str(currentDate), str(currentTime).zfill(8))
      if datetimeObject >= limitLeft and datetimeObject <= limitRight:
        datetime_array.append(datetimeObject)
        temperature_array.append(str(temperature))
        dew_point_array.append(str(dew_point))
        relative_humidity_array.append(str(relative_humidity))
        wind_speed_array.append(str(wind_spd))
        wind_direction_array.append(str(wind_dir))
        total_solar_radiation_array.append(str(solar_rad))
        precipitation_array.append(str(precip))

    cursor.close()
    conn.close()

  except Error as e:
    print(e)

  actual = generateVariablesLibrary(datetime_array, temperature_array, dew_point_array, relative_humidity_array, wind_speed_array, wind_direction_array, total_solar_radiation_array, precipitation_array)
  index = limitLeft
  index2 = 0
  weather_variables = []
  while index <= limitRight:
    if index2 >= len(actual['Datetime']):
      weather_variables = fetchForecastedDataForGivenHour(index, site_code)
      actual['Datetime'].append(weather_variables[0])
      actual['Temperature'].append(weather_variables[1])
      actual['Dew_point'].append(weather_variables[2])
      actual['Relative_humidity'].append(weather_variables[3])
      actual['Wind_speed'].append(weather_variables[4])
      actual['Wind_direction'].append(weather_variables[5])
      actual['Total_solar_radiation'].append(weather_variables[6])
      actual['Precipitation'].append(weather_variables[7])
    elif index2 < len(actual['Datetime']) and actual['Datetime'][index2] != index:
      weather_variables = fetchForecastedDataForGivenHour(index, site_code)
      actual['Datetime'].insert(index2, weather_variables[0])
      actual['Temperature'].insert(index2, weather_variables[1])
      actual['Dew_point'].insert(index2, weather_variables[2])
      actual['Relative_humidity'].insert(index2, weather_variables[3])
      actual['Wind_speed'].insert(index2, weather_variables[4])
      actual['Wind_direction'].insert(index2, weather_variables[5])
      actual['Total_solar_radiation'].insert(index2, weather_variables[6])
      actual['Precipitation'].insert(index2, weather_variables[7])

    index2 += 1
    index += CONSTANT_ONE_HOUR

  return actual


def fetchForecastedWeatherVariables(dateOfReference, hoursAhead, site_code):
  limitLeft = dateOfReference + CONSTANT_ONE_HOUR
  limitRight = dateOfReference + hoursAhead

  datetime_array = []
  temperature_array = []
  dew_point_array = []
  relative_humidity_array = []
  wind_speed_array = []
  wind_direction_array = []
  total_solar_radiation_array = []
  precipitation_array = []

  try:
    url_string = getURL(dateOfReference, site_code)
    request = requests.get(url_string, timeout=10)
    code = request.status_code
    if code == 200:
      with urllib.request.urlopen(url_string) as url:
        data = json.loads(url.read().decode())

      dataLength = len(data['xlab'])
      for index in range(0, dataLength):
        currentDatetime = datetime(int(data['xlab'][index][0:4]), int(data['xlab'][index][5:7]), int(data['xlab'][index][8:10]), int(data['xlab'][index][11:13]), 0, 0)
        if limitLeft <= limitRight:
          if limitLeft == currentDatetime:
            datetime_array.append(currentDatetime)
            temperature_array.append(data['temp2m'][index])
            dew_point_array.append(data['td2m'][index])
            relative_humidity_array.append(data['rh2m'][index])
            wind_speed_array.append(data['wspd'][index])
            wind_direction_array.append(data['wdir'][index])
            total_solar_radiation_array.append(data['swdown'][index])
            precipitation_array.append(data['precip'][index])
            limitLeft += CONSTANT_ONE_HOUR
        else:
          break
    else:
      print("  Web page does not exist! (" + str(code) + ")")
      sleep(20)

  except requests.exceptions.Timeout:
    print ("Timeout occurred")

  return generateVariablesLibrary(datetime_array, temperature_array, dew_point_array, relative_humidity_array, wind_speed_array, wind_direction_array, total_solar_radiation_array, precipitation_array)


def generateForecast(dateOfReference, hoursBehind, hoursAhead, site_code):
  if dateOfReference.minute == 0:
    dateOfReference -= CONSTANT_ONE_HOUR
  dateOfReference = dateOfReference.replace(minute=0, second=0, microsecond=0)
  features = {}
  features['actual'] = fetchActualWeatherVariables(dateOfReference, hoursBehind, site_code)
  features['forecasted'] = fetchForecastedWeatherVariables(dateOfReference, hoursAhead, site_code)

  return features


def generateTheDayFeatures(date):
  day = int(date[8:10])

  dayFeatureVector = []
  for index in range(1, 32):
    if index == day:
      dayFeatureVector.append(1.0)
    else:
      dayFeatureVector.append(0.0)

  return dayFeatureVector


def generateTheMonthFeatures(date):
  month = int(date[5:7])

  monthFeatureVector = []
  for index in range(1, 13):
    if index == month:
      monthFeatureVector.append(1.0)
    else:
      monthFeatureVector.append(0.0)

  return monthFeatureVector


def generateTheSeasonFeatures(date):
  month = int(date[5:7])

  if month <= 2 or month == 12:
    seasonsFeatureVector = [1.0, 0.0, 0.0, 0.0]
  elif month >= 3 and month <= 5:
    seasonsFeatureVector = [0.0, 1.0, 0.0, 0.0]
  elif month >= 6 and month <= 8:
    seasonsFeatureVector = [0.0, 0.0, 1.0, 0.0]
  elif month >= 9 and month <= 11:
    seasonsFeatureVector = [0.0, 0.0, 0.0, 1.0]

  return seasonsFeatureVector


def generateTheDayOfTheYearFeatures(date_str):
  dayOfTheYearFeatureVector = []
  
  date_object = date(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]))
  new_year_date = date(int(date_str[0:4]), 1, 1)

  day_of_the_year = (date_object - new_year_date).days + 1

  for index in range(1, 367):
    if index == day_of_the_year:
      dayOfTheYearFeatureVector.append(1.0)
    else:
      dayOfTheYearFeatureVector.append(0.0)

  return dayOfTheYearFeatureVector


def main():
  start_time = clock()
  print('Version of Python: ' + sys.version + '\n')
  
  if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Please supply just one argument!")
    sys.exit()

  site_codes = ['WHIT', 'HOLM', 'MAN']
  query_template = "INSERT INTO Predictions VALUES (\"{}\", {}) ON DUPLICATE KEY UPDATE generation_MW={}"

  dateOfReference = datetime.now()
  #dateOfReference = datetime(2018, 3, 22, 6, 0, 0, 0)
  hoursBehind = timedelta(hours=24)
  hoursAhead = timedelta(hours=24)
  numberOfHoursBehind = 24
  numberOfHoursAhead = 24

  print("Computing normalisation values (Max/Min)...")
  normalised_max = [33.1, 20.270806, 100, 28.678068, 359.997838, 1313.080833, 166.65]
  normalised_min = [-2.2, -12.020113, 10.97667, 0.0, 0.000263, -12.983455, 0.0]
  normalisationLength = len(normalised_max)
  for index in range(0, normalisationLength):
    normalised_max[index] += normalised_max[index] / 20
    normalised_min[index] -= normalised_min[index] / 20

  print("Generating test vectors...")
  while True:
    weather_data_library = generateForecast(dateOfReference, hoursBehind, hoursAhead, site_codes[0])

    datetime_array = weather_data_library['actual']['Datetime'] + weather_data_library['forecasted']['Datetime']
    temperature_array = weather_data_library['actual']['Temperature'] + weather_data_library['forecasted']['Temperature']
    dew_point_array = weather_data_library['actual']['Dew_point'] + weather_data_library['forecasted']['Dew_point']
    relative_humidity_array = weather_data_library['actual']['Relative_humidity'] + weather_data_library['forecasted']['Relative_humidity']
    wind_speed_array = weather_data_library['actual']['Wind_speed'] + weather_data_library['forecasted']['Wind_speed']
    wind_direction_array = weather_data_library['actual']['Wind_direction'] + weather_data_library['forecasted']['Wind_direction']
    total_solar_radiation_array = weather_data_library['actual']['Total_solar_radiation'] + weather_data_library['forecasted']['Total_solar_radiation']
    precipitation_array = weather_data_library['actual']['Precipitation'] + weather_data_library['forecasted']['Precipitation']

    currentDatetime = dateOfReference.replace(minute=0, second=0, microsecond=0)
    test_data_vectors = []
    for index in range(0, numberOfHoursAhead):
      test_data = []
      for index2 in range(0, numberOfHoursBehind):
        test_data.append((float(temperature_array[index2 + index]) - normalised_min[0]) / (normalised_max[0] - normalised_min[0]))
        test_data.append((float(dew_point_array[index2 + index]) - normalised_min[1]) / (normalised_max[1] - normalised_min[1]))
        test_data.append((float(relative_humidity_array[index2 + index]) - normalised_min[2]) / (normalised_max[2] - normalised_min[2]))
        test_data.append((float(wind_speed_array[index2 + index]) - normalised_min[3]) / (normalised_max[3] - normalised_min[3]))
        test_data.append((float(wind_direction_array[index2 + index]) - normalised_min[4]) / (normalised_max[4] - normalised_min[4]))
        test_data.append((float(total_solar_radiation_array[index2 + index]) - normalised_min[5]) / (normalised_max[5] - normalised_min[5]))
        test_data.append((float(precipitation_array[index2 + index]) - normalised_min[6]) / (normalised_max[6] - normalised_min[6]))

      nextDatetime = currentDatetime + CONSTANT_ONE_HOUR
      nextDate = str(nextDatetime.date())

      test_data += generateTheDayFeatures(nextDate)
      test_data += generateTheMonthFeatures(nextDate)
      test_data += generateTheSeasonFeatures(nextDate)
      test_data += generateTheDayOfTheYearFeatures(nextDate)
      test_data.append(nextDatetime)

      test_data_vectors.append(test_data)
      currentDatetime = nextDatetime

    dateVector = []
    for index in range(0, len(test_data_vectors)):
      dateVector.append(test_data_vectors[index].pop(-1))
      for index2 in range(0, len(test_data_vectors[index])):
        test_data_vectors[index][index2] = float(test_data_vectors[index][index2])

    print("Making predictions...")
    fileName = "finalised_" + str(sys.argv[1]) + "_normalised.pkl"
    model_in = open(fileName, "rb")
    model = pickle.load(model_in)
    model_in.close()
    test_data_matrix = np.matrix(test_data_vectors)
    prediction = model.predict(test_data_matrix)

    try:
      conn = mysql.connector.connect(**CONSTANT_DB_PARAMS)

      if conn.is_connected():
        print('Connected!')
      else:
        print('Connection error!')

      print('Querying ' + CONSTANT_DBDATABASE + ' on Predictions...')
      cursor = conn.cursor()
      for index in range(len(prediction)):
        query = query_template.format(dateVector[index], prediction[index], prediction[index])
        cursor.execute(query)
        conn.commit()

    except Error as e:
      print(e)

    finally:
       cursor.close()
       conn.close()

    current_time = datetime.now()
    next_prediction_hour = current_time.hour + 1
    next_prediction_time = datetime.now().replace(hour=next_prediction_hour, minute=1, second=0, microsecond=0)
    seconds_to_wait = (next_prediction_time - current_time).seconds
    print("Time to wait before next prediction: " + str(seconds_to_wait))
    sleep(seconds_to_wait)

  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))

  return 0


main()