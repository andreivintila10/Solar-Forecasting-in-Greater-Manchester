from time import clock
import sys
from datetime import datetime, timedelta, time, date
import requests
import urllib.request
import json
import pickle
import numpy as np


def getForecastDates(currentDatetime):
  forecast_update_hour = 9
  timeOfFirstForecast = time(18, 0, 0)

  #print("Current datetime: " + str(currentDatetime))
  currentTime = datetime.time(currentDatetime)

  if currentTime.hour < forecast_update_hour:
    currentDatetime -= timedelta(days=1)
    #print("Adjusted datetime: " + str(currentDatetime))

  year1 = currentDatetime.year
  month1 = currentDatetime.month
  day1 = currentDatetime.day

  datetime_yesterday = currentDatetime - timedelta(days=1)
  #print("Datetime yesterday: " + str(datetime_yesterday))
  year2 = datetime_yesterday.year
  month2 = datetime_yesterday.month
  day2 = datetime_yesterday.day
  
  first_date = date(year1, month1, day1)
  second_date = datetime(year2, month2, day2, timeOfFirstForecast.hour, timeOfFirstForecast.minute)

  forecastDates = []
  forecastDates.append(first_date)
  forecastDates.append(second_date)

  return forecastDates


def getURL(forecastDates, site_code):
  url_template = "http://manunicast.seaes.manchester.ac.uk/charts/manunicast/{}{}{}/d02/meteograms/meteo_{}_{}-{}-{}_{}{}_swdown_data.txt"

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


def fetchData(numberOfHours, startDatetime, site_code):
  delta_datetime = startDatetime - timedelta(hours=numberOfHours) + timedelta(hours=1)
  #print("Delta: " + str(delta_datetime))
  forecastDates = getForecastDates(startDatetime)
  #print("Forecast dates: " + str(forecastDates[0]) + ", " + str(forecastDates[1]))
  trainingVector = []
  if delta_datetime < forecastDates[1]:
    #print("need more features...")
    #print("Start datetime: " + str(startDatetime))
    #print("Delta: " + str(delta_datetime))
    #print("Forecast dates: " + str(forecastDates[0]) + ", " + str(forecastDates[1]))
    delta_hours = forecastDates[1] - delta_datetime
    #print("Delta hours: " + str(delta_hours))
    remainingNumberOfHours = delta_hours.days * 24 + delta_hours.seconds / 3600
    #print("Remaining hours: " + str(remainingNumberOfHours))
    #print(remainingNumberOfHours)
    left = datetime(forecastDates[1].year, forecastDates[1].month, forecastDates[1].day, forecastDates[1].hour)
    trainingVector = fetchData(remainingNumberOfHours, forecastDates[1] - timedelta(hours=1), site_code)
    #print("Left: ", str(left))
  else:
    left = datetime(delta_datetime.year, delta_datetime.month, delta_datetime.day, delta_datetime.hour)
  
  #print("Left: " + str(left))
  whitworth_url = getURL(forecastDates, site_code)
  while True:
    request = requests.get(whitworth_url)
    code = request.status_code
    if code == 200:
      with urllib.request.urlopen(whitworth_url) as url:
        data = json.loads(url.read().decode())
      break
    else:
        sleep(30)

  dataLength = len(data['xlab'])
  for index in range(0, dataLength):
    #print("xlab: " + data['xlab'][3])
    date_formated = datetime(int(data['xlab'][index][0:4]), int(data['xlab'][index][5:7]), int(data['xlab'][index][8:10]), int(data['xlab'][index][11:13]))
    #print("Date_formated: " + str(date_formated))
    if left == date_formated and left <= startDatetime:
      trainingVector.append(data['temp2m'][index])
      trainingVector.append(data['td2m'][index])
      trainingVector.append(data['rh2m'][index])
      trainingVector.append(data['wspd'][index])
      trainingVector.append(data['wdir'][index])
      trainingVector.append(data['swdown'][index])
      trainingVector.append(data['precip'][index])
      left += timedelta(hours=1)
      #print("Left: " + str(left))
    #print("TRAINING VECTOR: " + str(trainingVector))
  return trainingVector


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

  #print("Month type: " + str(type(monthFeatureVector[-2])))
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

  site_codes = ['WHIT', 'HOLM', 'MAN']

  #currentDatetime = datetime.now()
  currentDatetime = datetime(2018, 2, 10, 20)
  print("Current datetime: " + str(currentDatetime))
  forecastDates = getForecastDates(currentDatetime)

  numberOfHours = 24
  test_data_vectors = []
  for index in range(0, 24):
    test_data = fetchData(numberOfHours, currentDatetime, site_codes[0])

    nextDatetime = currentDatetime + timedelta(hours=1)
    nextDate = str(nextDatetime.date())

    test_data += generateTheDayFeatures(nextDate)
    test_data += generateTheMonthFeatures(nextDate)
    test_data += generateTheSeasonFeatures(nextDate)
    test_data += generateTheDayOfTheYearFeatures(nextDate)
    test_data.append(nextDatetime)

    test_data_vectors.append(test_data)
    currentDatetime = nextDatetime
    #print(currentDatetime)
  
  
  dateVector = []
  for index in range(0, len(test_data_vectors)):
    #print(test_data_vectors[index][-1])
    dateVector.append(test_data_vectors[index].pop(-1))
    #print(test_data_vectors[index][-1])
    for index2 in range(0, len(test_data_vectors[index])):
      test_data_vectors[index][index2] = float(test_data_vectors[index][index2])
      #sys.stdout.write(str(test_data_vectors[index][index2]) + ", ")
    #print("Test_vector length: " + str(len(test_data_vectors[index])))
    #sys.stdout.write("\n")

  #print("Test_vector length: " + str(len(test_data_vectors[0])))
  #print(dateVector)

  #print(str(test_data))
  model_in = open("finalised_svr.pkl", "rb")
  model = pickle.load(model_in)
  model_in.close()
  test_data_matrix = np.matrix(test_data_vectors)
  prediction = model.predict(test_data_matrix)
  print("Prediction: " + str(prediction))

  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))


main()