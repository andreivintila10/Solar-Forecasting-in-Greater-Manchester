from time import clock
import sys
from datetime import datetime, timedelta, time, date
import urllib.request
import json


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
  url_template = "http://manunicast.seaes.manchester.ac.uk/charts/manunicast/{}{}{}/d02/meteograms/meteo_{}_{}-{}-{}_{}{}_data.txt"

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
  currentDatetime = datetime.now()
  delta_datetime = currentDatetime - datetime.timedelta(hour=numberOfHours) + datetime.timedelta(hour=1)
  forecastDates = getForecastDates(currentDatetime)

  if delta_datetime < forecastDates[1]:
    remainingNumberOfHours = (forecastDates[1] - delta_datetime + datetime.timedelta(hour=1)).hour
    return fetchData(remainingNumberOfHours, forecastDates[1] - 1)
  else:
    for index in range():
      


def main():
  start_time = clock()
  print('Version of Python: ' + sys.version + '\n')

  site_codes = ['WHIT', 'HOLM', 'MAN']
  
  currentDatetime = datetime.now()
  forecastDates = getForecastDates(currentDatetime)
  print(forecastDates[0])
  print(forecastDates[1])

  #whitworth_url = getURL(site_codes[0])
  #print(whitworth_url)
  #with urllib.request.urlopen(whitworth_url) as url:
  #  data = json.loads(url.read().decode())

  #print(data['slp'])

  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))


main()