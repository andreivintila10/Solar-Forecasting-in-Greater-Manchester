#!/bin/bash

while true; do
  read -p "This will drop your current table and create another one.\nDo you wish to continue? [y/n]: " yn
  case $yn in
    [Yy]* ) break;;
    [Nn]* ) exit;;
    * ) echo "Please answer yes or no.";;
  esac
done

username="andrei"
password="Vinti123!"
database="weather_data"

mysql -u "$username" -p"$password" "$database" <<MY_QUERY
DROP TABLE IF EXISTS Observatory;
CREATE TABLE Observatory (
    Location VARCHAR(10) DEFAULT NULL,
    Date DATE,
    Time TIME,
    Temperature DOUBLE DEFAULT NULL COMMENT 'Degree Celsius',
    Dew_point DOUBLE DEFAULT NULL COMMENT 'Degree Celsius',
    Relative_humidity DOUBLE UNSIGNED DEFAULT NULL COMMENT 'Percentage',
    Wind_speed DOUBLE UNSIGNED DEFAULT NULL COMMENT 'm/s',
    Wind_direction DOUBLE UNSIGNED DEFAULT NULL COMMENT 'Degree',
    Total_solar_radiation DOUBLE DEFAULT NULL COMMENT 'W/m2',
    Precipitation DOUBLE UNSIGNED DEFAULT NULL COMMENT 'mm'
);
MY_QUERY