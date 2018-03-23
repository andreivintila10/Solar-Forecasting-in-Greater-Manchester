import sys
from time import clock
import datetime
import mysql.connector
from mysql.connector import Error
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR
import pickle


start_time = clock()
print('Version of Python: ' + sys.version)

CONSTANT_DBUSER = 'andrei'
CONSTANT_DBPASSWORD = 'Vinti123!'
CONSTANT_DBHOST = 'localhost'
CONSTANT_DBDATABASE = 'weather_data'

CONSTANT_DB_PARAMS = {
    'user': CONSTANT_DBUSER, 
    'password': CONSTANT_DBPASSWORD,
    'host': CONSTANT_DBHOST,
    'database': CONSTANT_DBDATABASE
}


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

  date_object = datetime.date(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]))
  new_year_date = datetime.date(int(date_str[0:4]), 1, 1)

  day_of_the_year = (date_object - new_year_date).days + 1

  for index in range(1, 367):
    if index == day_of_the_year:
      dayOfTheYearFeatureVector.append(1.0)
    else:
      dayOfTheYearFeatureVector.append(0.0)

  return dayOfTheYearFeatureVector


def createDatetimeObject(date_str, time_str):
  datetimeObject = datetime.datetime(int(date_str[0:4]), int(date_str[5:7]), int(date_str[8:10]), int(time_str[0:2]), int(time_str[3:5]), int(time_str[6:8]))

  return datetimeObject


def areOneHourApart(datetime_object1, datetime_object2):
  delta = abs(datetime_object2 - datetime_object1)

  if delta.days == 0 and delta.seconds == 3600:
    return 1
  else:
    return 0


def createFeatureVector(left, right, normalised_max, normalised_min):
  featureVector = []
  for index in range(left, right):
    featureVector.append((float(temperature_array[index]) - normalised_min[0]) / (normalised_max[0] - normalised_min[0]))
    featureVector.append((float(dew_point_array[index]) - normalised_min[1]) / (normalised_max[1] - normalised_min[1]))
    featureVector.append((float(relative_humidity_array[index]) - normalised_min[2]) / (normalised_max[2] - normalised_min[2]))
    featureVector.append((float(wind_speed_array[index]) - normalised_min[3]) / (normalised_max[3] - normalised_min[3]))
    featureVector.append((float(wind_direction_array[index]) - normalised_min[4]) / (normalised_max[4] - normalised_min[4]))
    featureVector.append((float(total_solar_radiation_array[index]) - normalised_min[5]) / (normalised_max[5] - normalised_min[5]))
    featureVector.append((float(precipitation_array[index]) - normalised_min[6]) / (normalised_max[6] - normalised_min[6]))

  currentDatetime = createDatetimeObject(date_array[right - 1], time_array[right - 1])
  nextDatetime = currentDatetime + datetime.timedelta(hours=1)
  nextDate = str(nextDatetime.date())

  featureVector += generateTheDayFeatures(nextDate)
  featureVector += generateTheMonthFeatures(nextDate)
  featureVector += generateTheSeasonFeatures(nextDate)
  featureVector += generateTheDayOfTheYearFeatures(nextDate)
  featureVector.append(nextDatetime)

  return featureVector


def createFeatureVectors(noOfFeatures, noOfRecords): 
  normalised_max = [33.1, 20.270806, 100, 28.678068, 359.997838, 1313.080833, 166.65]
  normalised_min = [-2.2, -12.020113, 10.97667, 0.0, 0.000263, -12.983455, 0.0]
  normalisationLength = len(normalised_max)
  for index in range(0, normalisationLength):
    normalised_max[index] += normalised_max[index] / 20
    normalised_min[index] -= normalised_min[index] / 20

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
      featureVector = createFeatureVector(left, right, normalised_max, normalised_min)
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
  conn = mysql.connector.connect(**CONSTANT_DB_PARAMS)

  if conn.is_connected():
    print('Connected!')
  else:
    print('Connection error!')

  date_array = []
  time_array = []
  temperature_array = []
  dew_point_array = []
  relative_humidity_array = []
  wind_speed_array = []
  wind_direction_array = []
  total_solar_radiation_array = []
  precipitation_array = []

  print('Computing the feature vectors...')
  print('Querying ' + CONSTANT_DBDATABASE + ' on Observatory...')
  cursor = conn.cursor()
  query1 = ("SELECT DISTINCT * FROM Observatory WHERE Location='Whitworth' AND TIME_FORMAT(Time, '%i:%s')='00:00' AND Temperature IS NOT NULL AND Dew_point IS NOT NULL AND Relative_humidity IS NOT NULL AND Wind_speed IS NOT NULL AND Wind_direction IS NOT NULL AND Total_solar_radiation IS NOT NULL AND Precipitation IS NOT NULL ORDER BY Date ASC, Time ASC")
  cursor.execute(query1)

  for (location, date, time, temperature, dew_point, relative_humidity, wind_spd, wind_dir, solar_rad, precip) in cursor:
    date_array.append(str(date))
    time = str(time)
    if len(time) == 7:
      time = "0" + time

    time_array.append(str(time))
    temperature_array.append(str(temperature))
    dew_point_array.append(str(dew_point))
    relative_humidity_array.append(str(relative_humidity))
    wind_speed_array.append(str(wind_spd))
    wind_direction_array.append(str(wind_dir))
    total_solar_radiation_array.append(str(solar_rad))
    precipitation_array.append(str(precip))

  print('Getting training labels...')
  print('Querying ' + CONSTANT_DBDATABASE + ' on pv_generation_actual...')
  query2 = ("SELECT DISTINCT datetime_GMT, generation_MW FROM pv_generation_actual WHERE region_id=266 AND TIME_FORMAT(datetime_GMT, '%i:%s')='00:00' AND generation_MW IS NOT NULL ORDER BY datetime_GMT ASC")
  cursor.execute(query2)

  generationVector = []
  for (datetime_GMT, generation_MW) in cursor:
    tuple = []
    tuple.append(datetime_GMT)
    tuple.append(str(generation_MW))
    generationVector.append(tuple)

  cursor.close()

  recordsLength = len(temperature_array)

  noOfFeatures = 24
  print('Computing the feature vectors...')
  featureVectors = createFeatureVectors(noOfFeatures, recordsLength)

  print('Matching feature vectors to existing labels...')
  labelsVector = []
  vectorsLength = len(featureVectors)
  index = 0
  while index < vectorsLength:
    ok = 0
    generationLength = len(generationVector)
    thisDatetime = featureVectors[index].pop()
    for index2 in range(0, generationLength):
      if thisDatetime == generationVector[index2][0]:
        ok = 1
        break

    if ok:
      labelsVector.append(generationVector[index2][1])
      del generationVector[index2]
      index += 1
    else:
      del featureVectors[index]
      vectorsLength = len(featureVectors)

  vectorsLength = len(featureVectors)
  for index in range(0, vectorsLength):
    vectorLength = len(featureVectors[index])
    for index2 in range(0, vectorLength):
      featureVectors[index][index2] = float(featureVectors[index][index2])

  labelsLength = len(labelsVector)
  for index in range(0, labelsLength):
    labelsVector[index] = float(labelsVector[index])

  training_data = np.matrix(featureVectors)
  training_labels = np.array(labelsVector)

  print("Training MLPRegressor...")
  mlp = MLPRegressor(verbose=1)
  mlp.fit(training_data, training_labels)

  print("Saving MLPRegressor model to file...")
  filename = 'finalised_mlp_normalised.pkl'
  model_out = open(filename, 'wb')
  pickle.dump(mlp, model_out)
  model_out.close()

  print("Training Linear Regression...")
  lr = LinearRegression()
  lr.fit(training_data, training_labels)

  print("Saving Linear Regression model to file...")
  filename = 'finalised_lr_normalised.pkl'
  model_out = open(filename, 'wb')
  pickle.dump(lr, model_out)
  model_out.close()

  print("Training SVR...")
  svr = SVR(verbose=True)
  svr.fit(training_data, training_labels)

  print("Saving SVR model to file...")
  filename = 'finalised_svr_normalised.pkl'
  model_out = open(filename, 'wb')
  pickle.dump(svr, model_out)
  model_out.close()

except Error as e:
  print(e)
 
finally:
  conn.close()
  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))