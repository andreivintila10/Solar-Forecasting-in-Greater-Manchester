#!/bin/bash

while true; do
  read -p "Are you sure you want to execute all scripts? [y/n]: " yn
  case $yn in
    [Yy]* ) break;;
    [Nn]* ) exit;;
    * ) echo "Please answer yes or no.";;
  esac
done

./266_2014.sql
./266_2015.sql
./266_2016.sql
./266_2017.sql
./266_2018.sql