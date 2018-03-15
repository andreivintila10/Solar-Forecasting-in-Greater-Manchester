from time import clock, sleep
from datetime import datetime
import sys
import requests
import urllib.request
import json


def areWithing10Mins(datetime_object1, datetime_object2):
  delta = abs(datetime_object2 - datetime_object1)

  if delta.days == 0 and delta.seconds <= 600:
    return 1
  else:
    return 0


def main():
  start_time = clock()
  print('Version of Python: ' + sys.version)

  whitworth_url = "http://manunicast.seaes.manchester.ac.uk/charts/manunicast/20180315/d02/meteograms/meteo_HOLM_2018-03-14_1800_data.txt"
  upload_datetime = datetime(2018, 3, 14, 9, 0, 0)
  tries = 0

  while True:
    request = requests.get(whitworth_url)
    code = request.status_code
    tries += 1
    if not code == 200:
      print(str(tries) + "\tWeb page does not exist! (" + str(code) + ")")
      if areWithing10Mins(datetime.now(), upload_datetime):
        sleep(1)
      else:
        sleep(30)
    elif code == 200:
      datetime_live = datetime.now()
      statement = str(tries) + "\tWeb page went live at " + str(datetime_live) + " (" + str(code) + ")\n"
      print(statement)
      print('Fetching data...')
      with urllib.request.urlopen(whitworth_url) as url:
        data = json.loads(url.read().decode())

      print("Outputting data to 'forecast_update_holm.data'...")
      out = open("forecast_update_holm.data", "w")
      out.write(statement)
      out.write(str(data))
      out.close()
      break

  end_time = clock()
  run_time = end_time - start_time
  print('End program, ' + str(run_time))


main()