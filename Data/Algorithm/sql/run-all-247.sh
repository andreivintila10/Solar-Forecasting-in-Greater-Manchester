#!/bin/bash

while true; do
  read -p "Are you sure you want to execute all scripts? [y/n]: " yn
  case $yn in
    [Yy]* ) break;;
    [Nn]* ) exit;;
    * ) echo "Please answer yes or no.";;
  esac
done

#time ./247_2014.sql
#time ./247_2015.sql
#time ./247_2016.sql
time ./247_2017.sql
time ./247_2018.sql