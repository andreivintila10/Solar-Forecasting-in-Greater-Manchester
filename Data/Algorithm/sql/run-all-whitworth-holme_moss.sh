#!/bin/bash

while true; do
  read -p "Are you sure you want to execute all scripts? [y/n]: " yn
  case $yn in
    [Yy]* ) break;;
    [Nn]* ) exit;;
    * ) echo "Please answer yes or no.";;
  esac
done

printf "\n"
printf "2013_Whitworth.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2013_Whitworth.sql ; } 2> 2013_Whitworth_time.txt
printf "2014_Whitworth.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2014_Whitworth.sql ; } 2> 2014_Whitworth_time.txt
printf "2015_Whitworth.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2015_Whitworth.sql ; } 2> 2015_Whitworth_time.txt
printf "2016_Whitworth.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2016_Whitworth.sql ; } 2> 2016_Whitworth_time.txt
printf "2017_Whitworth.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2017_Whitworth.sql ; } 2> 2017_Whitworth_time.txt

printf "\n"
printf "2013_HolmeMoss.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2013_HolmeMoss.sql ; } 2> 2013_HolmeMoss_time.txt
printf "2014_HolmeMoss.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2014_HolmeMoss.sql ; } 2> 2014_HolmeMoss_time.txt
printf "2015_HolmeMoss.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2015_HolmeMoss.sql ; } 2> 2015_HolmeMoss_time.txt
printf "2016_HolmeMoss.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2016_HolmeMoss.sql ; } 2> 2016_HolmeMoss_time.txt
printf "2017_HolmeMoss.sql running...\n"
{ time E:/University/Courses/Year\ 3/3rd\ Year\ Project/Solar-Forecasting-in-Greater-Manchester/Data/Algorithm/sql/2017_HolmeMoss.sql ; } 2> 2017_HolmeMoss_time.txt