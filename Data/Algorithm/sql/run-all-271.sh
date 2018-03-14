#!/bin/bash

while true; do
  read -p "Are you sure you want to execute all scripts? [y/n]: " yn
  case $yn in
    [Yy]* ) break;;
    [Nn]* ) exit;;
    * ) echo "Please answer yes or no.";;
  esac
done

./271_2014.sql
./271_2015.sql
./271_2016.sql
./271_2017.sql
./271_2018.sql