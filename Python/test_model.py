from time import clock
import sys
from datetime import datetime, timedelta
import urllib.request
import json


def getURL(site_code):
  url_template = "http://manunicast.seaes.manchester.ac.uk/charts/manunicast/{}{}{}/d02/meteograms/meteo_{}_{}-{}-{}_1800_data.txt"
  forecast_update_hour = 9

  datetime_now = datetime.now()
  #print("Datetime now: " + str(datetime_now))
  time_now = datetime.time(datetime_now)

  if datetime_now.hour < forecast_update_hour:
  	datetime_now -= timedelta(days=1)
  	#print("Adjusted datetime: " + str(datetime_now))

  year1 = datetime_now.year
  month1 = str(datetime_now.month).zfill(2)
  day1 = str(datetime_now.day).zfill(2)

  datetime_yesterday = datetime_now - timedelta(days=1)
  #print("Datetime yesterday: " + str(datetime_yesterday))
  year2 = datetime_yesterday.year
  month2 = str(datetime_yesterday.month).zfill(2)
  day2 = str(datetime_yesterday.day).zfill(2)

  url = url_template.format(year1, month1, day1, site_code, year2, month2, day2)
  return url


def main():
  start_time = clock()
  print('Version of Python: ' + sys.version + '\n')

  site_codes = ['WHIT', 'HOLM', 'MAN']
  
  whitworth_url = getURL(site_codes[0])
  #print(whitworth_url)
  with urllib.request.urlopen(whitworth_url) as url:
    data = json.loads(url.read().decode())

  #print(data['slp'])

  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))


main()