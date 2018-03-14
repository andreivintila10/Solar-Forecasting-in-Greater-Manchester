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
DROP TABLE IF EXISTS pv_generation_actual;
CREATE TABLE pv_generation_actual (
  region_id int(10) UNSIGNED NOT NULL DEFAULT '0',
  datetime_GMT datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT 'GMT = Greenwich Mean Time',
  generation_MW double UNSIGNED NOT NULL DEFAULT '0',
  uncertainty_MW double UNSIGNED DEFAULT NULL,
  stats_error double UNSIGNED DEFAULT NULL,
  bias_error double UNSIGNED DEFAULT NULL,
  lcl_MW double UNSIGNED DEFAULT NULL COMMENT 'MW = Mega Watt',
  ucl_MW double UNSIGNED DEFAULT NULL COMMENT 'MW = Mega Watt',
  version_id int(10) UNSIGNED DEFAULT '0',
  version varchar(10) DEFAULT NULL,
  installedcapacity_MWp int(10) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'MWp = Mega Watt peak',
  capacity_MWp int(10) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'MWp = Mega Watt peak',
  site_count int(10) UNSIGNED NOT NULL DEFAULT '0',
  calculation_time_s int(10) UNSIGNED NOT NULL DEFAULT '0' COMMENT 'Measured in seconds'
);
MY_QUERY