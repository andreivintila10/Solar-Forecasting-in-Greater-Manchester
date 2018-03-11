import sys
from time import clock
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
  day = int(date[8:9])

  dayFeatureVector = []
  for index in range(1, 31):
    if index == day:
      dayFeatureVector.append(1)
    else:
      dayFeatureVector.append(0)

  return dayFeatureVector


def generateTheMonthFeatures(date):
  month = int(date[5:6])

  monthFeatureVector = []
  for index in range(1, 12):
    if index == month:
      monthFeatureVector.append(1)
    else:
      monthFeatureVector.append(0)

  return monthFeatureVector


def generateTheSeasonFeatures(date):
  month = int(date[5:6])

  if month <= 2 or month == 12:
    seasonsFeatureVector = [1, 0, 0, 0]
  elif month >= 3 and month <= 5:
    seasonsFeatureVector = [0, 1, 0, 0]
  elif month >= 6 and month <= 8:
    seasonsFeatureVector = [0, 0, 1, 0]
  elif month >= 9 and month <= 11:
    seasonsFeatureVector = [0, 0, 0, 1]
  return seasonsFeatureVector


def createFeatureVectors(noOfFeatures, noOfRecords):
  featureVectors = []
  for index in range(1, noOfRecords - noOfFeatures):
    featureVector = []
    for index2 in range(index, index + noOfFeatures):
      featureVector.append(temperature_array[index2])
      featureVector.append(dew_point_array[index2])
      featureVector.append(relative_humidity_array[index2])
      featureVector.append(wind_speed_array[index2])
      featureVector.append(wind_direction_array[index2])
      featureVector.append(total_solar_radiation_array[index2])
      featureVector.append(precipitation_array[index2])

    featureVector += generateTheDayFeatures(date_array[index2])
    featureVector += generateTheMonthFeatures(date_array[index2])
    featureVector += generateTheSeasonFeatures(date_array[index2])

    featureVectors.append(featureVector)

  return featureVectors


try:
  conn = mysql.connector.connect(**params)

  if conn.is_connected():
    print('Connected!')
  else:
    print('Connection error!')

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
  for (location, date, time, temperature, dew_point, relative_humidity, wind_spd, wind_dir, solar_rad, precip) in cursor:
    print(location + ' ' + str(date) + ' ' + str(time) + ' ' + str(temperature) + ' ' + str(dew_point) + ' ' + str(relative_humidity) + ' ' + str(wind_spd) + ' ' + str(wind_dir) + ' ' +$
    date_array.append(str(date))
    time_array.append(str(time))
    temperature_array.append(str(temperature))
    dew_point_array.append(str(dew_point))
    relative_humidity_array.append(str(relative_humidity))
    wind_speed_array.append(str(wind_spd))
    wind_direction_array.append(str(wind_dir))
    total_solar_radiation_array.append(str(solar_rad))
    precipitation_array.append(str(precip))

  recordsLength = len(temperature_array)
  print ('Check array: ')
  print (date_array[int(recordsLength / 2)] + ' ' + time_array[int(recordsLength / 2)] + ' ' + temperature_array[int(recordsLength / 2)] + ' ' + dew_point_array[int(recordsLength / 2)] $
  cursor.close()

  noOfFeatures = 2
  outfile = "test_features(" + str(noOfFeatures) + ").csv"
  out = open(outfile, "w")

  featureVectors = createFeatureVectors(noOfFeatures, recordsLength)
  print('The feature vectors are: ')

  vectorsLength = len(featureVectors)
  for index in range(1, vectorsLength):
    print('  ' + str(featureVectors[index]))
    vectorLength = len(featureVectors[index])
    for index2 in range(1, vectorLength):
      out.write(str(featureVectors[index][index2]))
      if index2 < vectorLength - 1:
        out.write(', ')
    out.write('\n')

  out.close()

except Error as e:
  print(e)

finally:
  conn.close()
  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))