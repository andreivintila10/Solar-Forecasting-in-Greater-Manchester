global date_array
global time_array
global temperature_array
global dew_point_array
global relative_humidity_array
global wind_speed_array
global wind_direction_array
global total_solar_radiance_array
global precipitation_array

date_array = []
time_array = []
temperature_array = []
dew_point_array = []
relative_humidity_array = []
wind_speed_array = []
wind_direction_array = []
total_solar_radiance_array = []
precipitation_array = []

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

  if month <= 2 || month == 12:
    seasonsFeatureVector = [1, 0, 0, 0]
  else if month >= 3 && month <= 5:
    seasonsFeatureVector = [0, 1, 0, 0]
  else if month >= 6 && month <= 8:
    seasonsFeatureVector = [0, 0, 1, 0]
  else if month >= 9 && month <= 11:
    seasonsFeatureVector = [0, 0, 0, 1]


def createFeatureVectors(noOfFeatures, noOfRecords):
  featureVector = []
  for index in range(1, noOfRecords - noOfFeatures):
    for index2 in (1, noOfFeatures):
      featureVector.append(temperature_array[index2])
      featureVector.append(dew_point_array[index2])
      featureVector.append(relative_humidity[index2])
      featureVector.append(wind_speed_array[index2])
      featureVector.append(wind_direction_array[index2])
      featureVector.append(total_solar_radiance_array[index2])
      featureVector.append(precipitation_array[index2])

      featureVector += generateTheDayFeatures()
      featureVector += generateTheMonthFeatures()
      featureVector += generateTheSeasonFeatures()
  return featureVector