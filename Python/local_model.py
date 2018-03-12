import sys
from time import clock
import datetime
import mysql.connector
from mysql.connector import Error

start_time = clock()
print('Version of Python: ' + sys.version)

dbuser = 'andrei'
dbpassword = 'Vinti123!'
dbhost = '130.88.96.145'
dbdatabase = 'weather_data'

params = {
    'user': dbuser,
    'password': dbpassword,
    'host': dbhost,
    'database': dbdatabase
}


def generateTheDayFeatures(date):
  day = int(date[8:10])

  dayFeatureVector = []
  for index in range(1, 32):
    if index == day:
      dayFeatureVector.append(1)
    else:
      dayFeatureVector.append(0)

  return dayFeatureVector


def generateTheMonthFeatures(date):
  month = int(date[5:7])

  monthFeatureVector = []
  for index in range(1, 13):
    if index == month:
      monthFeatureVector.append(1)
    else:
      monthFeatureVector.append(0)

  return monthFeatureVector


def generateTheSeasonFeatures(date):
  month = int(date[5:7])

  if month <= 2 or month == 12:
    seasonsFeatureVector = [1, 0, 0, 0]
  elif month >= 3 and month <= 5:
    seasonsFeatureVector = [0, 1, 0, 0]
  elif month >= 6 and month <= 8:
    seasonsFeatureVector = [0, 0, 1, 0]
  elif month >= 9 and month <= 11:
    seasonsFeatureVector = [0, 0, 0, 1]

  return seasonsFeatureVector


def generateTheDayOfTheYearFeatures(date_str):
  dayOfTheYearFeatureVector = []

  date_object = datetime.date(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]))
  new_year_date = datetime.date(int(date_str[0:4]), 1, 1)

  day_of_the_year = (date_object - new_year_date).days + 1

  for index in range(1, 367):
    if index == day_of_the_year:
      dayOfTheYearFeatureVector.append(1)
    else:
      dayOfTheYearFeatureVector.append(0)

  return dayOfTheYearFeatureVector


def createDatetimeObject(date, time):
  datetime_object = datetime.datetime(int(date[0:4]), int(date[5:7]), int(date[8:10]), int(time[0:2]), int(time[3:5]), int(time[6:8]))
  return datetime_object


def areOneHourApart(datetime_object1, datetime_object2):
  delta = abs(datetime_object2 - datetime_object1)

  if delta.days == 0 and delta.seconds == 3600:
    return 1
  else:
    return 0


def createFeatureVector(left, right):
  featureVector = []
  for index in range(left, right):
    featureVector.append(temperature_array[index])
    featureVector.append(dew_point_array[index])
    featureVector.append(relative_humidity_array[index])
    featureVector.append(wind_speed_array[index])
    featureVector.append(wind_direction_array[index])
    featureVector.append(total_solar_radiation_array[index])
    featureVector.append(precipitation_array[index])

  currentDatetime = createDatetimeObject(date_array[right - 1], time_array[right - 1])
  nextDatetime = currentDatetime + datetime.timedelta(hours=1)
  nextDate = str(nextDatetime.date())
  nextTime = str(nextDatetime.time())

  featureVector += generateTheDayFeatures(nextDate)
  featureVector += generateTheMonthFeatures(nextDate)
  featureVector += generateTheSeasonFeatures(nextDate)
  featureVector += generateTheDayOfTheYearFeatures(nextDate)
  featureVector.append(nextDate + " " + nextTime)

  return featureVector


def createFeatureVectors(noOfFeatures, noOfRecords):
  left = 0
  right = left + noOfFeatures
  previousOk = 0
  previousDatetime = createDatetimeObject(date_array[left], time_array[left])
  featureVectors = []
  while right <= noOfRecords:
    ok = 1
    for index in range(left + 1, right):
      currentDatetime = createDatetimeObject(date_array[index], time_array[index])

      if not areOneHourApart(previousDatetime, currentDatetime):
        ok = 0
        break

      previousDatetime = currentDatetime

    if ok:
      featureVector = createFeatureVector(left, right)
      featureVectors.append(featureVector)

      left += 1
      right += 1
      previousOk = 1
    else:
      if previousOk:
        left = right - 1
        right = left + noOfFeatures
      else:
        left += 1
        right += 1
      previousOk = 0

    previousDatetime = createDatetimeObject(date_array[left], time_array[left])

  return featureVectors


try:
  conn = mysql.connector.connect(**params)

  if conn.is_connected():
    print('Connected!')
  else:
    print('Connection error!')

  print('Querying the database...')
  cursor = conn.cursor()
  query = ("SELECT DISTINCT * FROM Observatory WHERE Location='Whitworth' AND TIME_FORMAT(Time, '%i:%s')='00:00' AND Temperature IS NOT NULL AND Dew_point IS NOT NULL AND Relative_humidity IS NOT NULL AND Wind_speed IS NOT NULL AND Wind_direction IS NOT NULL AND Total_solar_radiation IS NOT NULL AND Precipitation IS NOT NULL ORDER BY Date ASC")
  cursor.execute(query)

  date_array = []
  time_array = []
  temperature_array = []
  dew_point_array = []
  relative_humidity_array = []
  wind_speed_array = []
  wind_direction_array = []
  total_solar_radiation_array = []
  precipitation_array = []

  featureVectors = []
  time = ""
  for (location, date, time, temperature, dew_point, relative_humidity, wind_spd, wind_dir, solar_rad, precip) in cursor:
    date_array.append(str(date))
    time = str(time)
    if len(time) == 7:
      time = '0' + time

    time_array.append(str(time))
    temperature_array.append(str(temperature))
    dew_point_array.append(str(dew_point))
    relative_humidity_array.append(str(relative_humidity))
    wind_speed_array.append(str(wind_spd))
    wind_direction_array.append(str(wind_dir))
    total_solar_radiation_array.append(str(solar_rad))
    precipitation_array.append(str(precip))
    #print(location + ' ' + str(date) + ' ' + str(time) + ' ' + str(temperature) + ' ' + str(dew_point) + ' ' + str(relative_humidity) + ' ' + str(wind_spd) + ' ' + str(wind_dir) + ' ' + str(solar_rad) + ' ' + str(precip))

  recordsLength = len(temperature_array)

  noOfFeatures = 24
  outfile = "test_features(" + str(noOfFeatures) + ").csv"
  out = open(outfile, "w")

  print('Computing the feature vectors...')
  featureVectors = createFeatureVectors(noOfFeatures, recordsLength)

  print('Storing the feature vectors to file...')
  labelsFor = []
  vectorsLength = len(featureVectors)
  for index in range(0, vectorsLength):
    labelsFor.append(featureVectors[index].pop())
    print(str(featureVectors[index]))
    vectorLength = len(featureVectors[index])
    for index2 in range(0, vectorLength):
      out.write(str(featureVectors[index][index2]))

      if index2 < vectorLength - 1:
        out.write(', ')

    out.write('\n')

  out.close()

  print(labelsFor)
  print('Querying the database...')
  query2 = ("SELECT DISTINCT generation_MW FROM pv_generation_actual WHERE region_id=247 AND TIME_FORMAT(datetime_GMT, '%i:%s')='00:00' AND generation_MW IS NOT NULL ORDER BY datetime_GMT ASC")
  cursor.execute(query2)

  labelVector = []
  for (datetime, generation) in cursor:
    #print(' ' + str(datetime) + ' ' + str(generation))
    labelVector.append(generation)
  cursor.close()

except Error as e:
  print(e)

finally:
  conn.close()
  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))