#include <iostream>
#include <string.h>
#include <stdlib.h>
#include <fstream>


using namespace std;


struct data {
  unsigned short int region_id;
  char datetime_GMT[19];
  double generation_MW;
  double uncertainty_MW;
  double stats_error;
  double bias_error;
  double lcl_MW;
  double ucl_MW;
  unsigned int version_id;
  char version[135];
  double installedcapacity_MW;
  double capacity_MWp;
  unsigned int site_count;
  unsigned int calculation_time_s;
} regionalData[20000];


struct observatory {
  char location[11];
  char date[11];
  char time[8];
  double temperature;
  double dew_point;
  double relative_humidity;
  double wind_speed;
  double wind_direction;
  double total_solar_radiance;
  double precipitation;
} observatoryData[999999];


void meniu() {
  cout << "=====MENIU=====" << endl;
  cout << "1. Regional data" << endl;
  cout << "2. Observatory" << endl;
  cout << "===============" << endl;
}


unsigned int charToInt(char *numar) {
  int newNumar = 0;
  int length = strlen(numar);
  for (int index = 0; index < length; index++)
    newNumar = newNumar * 10 + (numar[index] - '0');

  return newNumar;
}


char *stripQuotes(char *word) {
  if (word[0] == '\"')
    strcpy(word, word + 1);
  if (word[strlen(word) - 1] == '\"')
    word[strlen(word) - 1] = '\0';

  return word;
}


char *changeDateFormat(char *date) {
  char day[3];
  day[0] = date[0];
  day[1] = date[1];
  day[2] = '\0';

  char month[3];
  month[0] = date[3];
  month[1] = date[4];
  month[2] = '\0';

  char year[5];
  year[0] = date[6];
  year[1] = date[7];
  year[2] = date[8];
  year[3] = date[9];
  year[4] = '\0';

  char *newDate = (char *) malloc(sizeof(char) * 11);
  strcpy(newDate, year);
  strcat(newDate, "-");
  strcat(newDate, month);
  strcat(newDate, "-");
  strcat(newDate, day);
  strcat(newDate, "\0");

  return newDate;
}


void readCsv(char fileName[19], char site[10], int &numar) {
  cout << "Reading " << site << " csv file..." << endl;
  cout << "  Input file name: " << fileName << endl;
  int ok;
  char *words;
  char skip[1024], line[1024];

  FILE *infile = fopen(fileName, "r");
  if (infile) {
    fgets(skip, sizeof(skip), infile);
    numar = 0;
    ok = 1;
    while (fgets(line, sizeof(line), infile)) {
      words = strtok(line, ", ");
      strcpy(observatoryData[numar].date, changeDateFormat(words));

      words = strtok(NULL, ", ");
      strcpy(observatoryData[numar].time, words);

      words = strtok(NULL, ", ");
      if (!strcmp(words, "NaN"))
        observatoryData[numar].temperature = -9999;
      else
        observatoryData[numar].temperature = atof(words);

      words = strtok(NULL, ", ");
      if (!strcmp(words, "NaN"))
        observatoryData[numar].dew_point = -9999;
      else
        observatoryData[numar].dew_point = atof(words);

      words = strtok(NULL, ", ");
      if (!strcmp(words, "NaN"))
        observatoryData[numar].relative_humidity = -9999;
      else
        observatoryData[numar].relative_humidity = atof(words);

      words = strtok(NULL, ", ");
      if (!strcmp(words, "NaN"))
        observatoryData[numar].wind_speed = -9999;
      else
        observatoryData[numar].wind_speed = atof(words);

      words = strtok(NULL, ", ");
      if (!strcmp(words, "NaN"))
        observatoryData[numar].wind_direction = -9999;
      else
        observatoryData[numar].wind_direction = atof(words);

      if (!strcmp(site, "Whitworth")) {
        words = strtok(NULL, ", ");
        if (!strcmp(words, "NaN"))
          observatoryData[numar].total_solar_radiance = -9999;
        else
          observatoryData[numar].total_solar_radiance = atof(words);
      }
      else if (!strcmp(site, "Holme Moss"))
        observatoryData[numar].total_solar_radiance = -9999;

      words = strtok(NULL, ", ");
      if (!strcmp(words, "NaN"))
        observatoryData[numar].precipitation = -9999;
      else
        observatoryData[numar].precipitation = atof(words);
      numar++;
    }
  }
  fclose(infile);
  cout << "  Number of lines read: " << numar << endl << endl;
}


void writeDbConnSql(FILE *outfile) {
  fprintf(outfile, "#!/bin/bash\n");
  fprintf(outfile, "\n");
  fprintf(outfile, "username=\"andrei\"\n");
  fprintf(outfile, "password=\"Vinti123!\"\n");
  fprintf(outfile, "database=\"weather_data\"\n");
  fprintf(outfile, "\n");
  fprintf(outfile, "mysql -u \"$username\" -p\"$password\" \"$database\"");
}


void writeSql(char fileName[19], char site[11], int numar) {
  cout << "Writing " << site << " sql data to file..." << endl;
  cout << "  Output file name: " << fileName << endl;
  cout << "  Number of insert statements to write: " << numar << endl << endl;

  FILE *outfile = fopen(fileName, "w");
  if (outfile) {
    writeDbConnSql(outfile);
    fprintf(outfile, " <<MY_QUERY\n");
    for (int index = 0; index < numar; index++) {
      fprintf(outfile, "INSERT INTO Observatory VALUES (");
      fprintf(outfile, "'%s', ", site);
      fprintf(outfile, "'%s', ", observatoryData[index].date);
      fprintf(outfile, "'%s', ", observatoryData[index].time);

      if (observatoryData[index].temperature == -9999)
        fprintf(outfile, "NULL, ");
      else
        fprintf(outfile, "%f, ", observatoryData[index].temperature);

      if (observatoryData[index].dew_point == -9999)
        fprintf(outfile, "NULL, ");
      else
        fprintf(outfile, "%f, ", observatoryData[index].dew_point);

      if (observatoryData[index].relative_humidity == -9999)
        fprintf(outfile, "NULL, ");
      else
        fprintf(outfile, "%f, ", observatoryData[index].relative_humidity);

      if (observatoryData[index].wind_speed == -9999)
        fprintf(outfile, "NULL, ");
      else
        fprintf(outfile, "%f, ", observatoryData[index].wind_speed);

      if (observatoryData[index].wind_direction == -9999)
        fprintf(outfile, "NULL, ");
      else
        fprintf(outfile, "%f, ", observatoryData[index].wind_direction);

      if (observatoryData[index].total_solar_radiance == -9999)
        fprintf(outfile, "NULL, ");
      else
        fprintf(outfile, "%f, ", observatoryData[index].total_solar_radiance);

      if (observatoryData[index].precipitation == -9999)
        fprintf(outfile, "NULL);\n");
      else
        fprintf(outfile, "%f);\n", observatoryData[index].precipitation);
    }
    fprintf(outfile, "MY_QUERY");
  }
  fclose(outfile);
}


int main() {
  meniu();

  int op;
  char fileName[30], skip[1024], line[1024], in_name[19], out_name[19];
  char *words, *temp;
  int numar, ok, index;
  FILE *infile, *outfile;
  cout << "Option: ";
  cin >> op;
  system("cls");

  switch (op) {
    case 1: cout << "1. Regional data..." << endl;
            cout << "File name (without extension): ";
            cin >> fileName;

            strcpy(in_name, "json/");
            strcat(in_name, fileName);
            strcat(in_name, ".data");

            infile = fopen(in_name, "r");
            if (infile) {
              for (int index = 1; index <= 19; index++)
                fgets(skip, sizeof(skip), infile);

              numar = 0;
              ok = 1;
              while (fgets(line, sizeof(line), infile)) {
                if (!strcmp(line + strlen(line) - 4, "\"],\n"))
                    line[strlen(line) - 3] = '\0';
                else if (!strcmp(line + strlen(line) - 3, "\"]\n"))
                    line[strlen(line) - 2] = '\0';
                else
                    ok = 0;

                if (ok) {
                  strcpy(line, line + 2);
                  words = strtok(line, ",");
                  regionalData[numar].region_id = charToInt(stripQuotes(words));

                  words = strtok(NULL, ",");
                  strcpy(regionalData[numar].datetime_GMT, stripQuotes(words));

                  words = strtok(NULL, ",");
                  temp = stripQuotes(words);
                  if (strcmp(temp, "null"))
                    regionalData[numar].generation_MW = atof(temp);
                  else
                    regionalData[numar].generation_MW = -1.0;

                  words = strtok(NULL, ",");
                  temp = stripQuotes(words);
                  if (strcmp(temp, "null"))
                    regionalData[numar].uncertainty_MW = atof(temp);
                  else
                    regionalData[numar].uncertainty_MW = -1.0;

                  words = strtok(NULL, ",");
                  temp = stripQuotes(words);
                  if (strcmp(temp, "null"))
                    regionalData[numar].stats_error = atof(temp);
                  else
                    regionalData[numar].stats_error = -1.0;

                  words = strtok(NULL, ",");
                  temp = stripQuotes(words);
                  if (strcmp(temp, "null"))
                    regionalData[numar].bias_error = atof(temp);
                  else
                    regionalData[numar].bias_error = -1.0;

                  words = strtok(NULL, ",");
                  temp = stripQuotes(words);
                  if (strcmp(temp, "null"))
                    regionalData[numar].lcl_MW = atof(temp);
                  else
                    regionalData[numar].lcl_MW = -1.0;

                  words = strtok(NULL, ",");
                  temp = stripQuotes(words);
                  if (strcmp(temp, "null"))
                    regionalData[numar].ucl_MW = atof(temp);
                  else
                    regionalData[numar].ucl_MW = -1.0;

                  words = strtok(NULL, ",");
                  regionalData[numar].version_id = charToInt(stripQuotes(words));

                  words = strtok(NULL, ",");
                  strcpy(regionalData[numar].version, stripQuotes(words));

                  words = strtok(NULL, ",");
                  temp = stripQuotes(words);
                  if (strcmp(temp, "null"))
                    regionalData[numar].installedcapacity_MW = atof(temp);
                  else
                    regionalData[numar].installedcapacity_MW = -1.0;

                  words = strtok(NULL, ",");
                  temp = stripQuotes(words);
                  if (strcmp(temp, "null"))
                    regionalData[numar].capacity_MWp = atof(temp);
                  else
                    regionalData[numar].capacity_MWp = -1.0;

                  words = strtok(NULL, ",");
                  regionalData[numar].site_count = charToInt(stripQuotes(words));

                  words = strtok(NULL, ",");
                  regionalData[numar].calculation_time_s = charToInt(stripQuotes(words));

                  numar++;
                }
              }
            }
            fclose(infile);

            strcpy(out_name, "sql/");
            strcat(out_name, fileName);
            strcat(out_name, ".sql");

            outfile = fopen(out_name, "w");
            if (outfile) {
              writeDbConnSql(outfile);
              fprintf(outfile, " <<MY_QUERY\n");
              for (index = 0; index < numar; index++) {
                fprintf(outfile, "INSERT INTO pv_generation_actual VALUES (");
                fprintf(outfile, "%d, ", regionalData[index].region_id);
                fprintf(outfile, "'%s', ", regionalData[index].datetime_GMT);

                if (regionalData[index].generation_MW == -1)
                  fprintf(outfile, "NULL, ");
                else
                  fprintf(outfile, "%f, ", regionalData[index].generation_MW);

                if (regionalData[index].uncertainty_MW == -1)
                  fprintf(outfile, "NULL, ");
                else
                  fprintf(outfile, "%f, ", regionalData[index].uncertainty_MW);

                if (regionalData[index].stats_error == -1)
                  fprintf(outfile, "NULL, ");
                else
                  fprintf(outfile, "%f, ", regionalData[index].stats_error);

                if (regionalData[index].bias_error == -1)
                  fprintf(outfile, "NULL, ");
                else
                  fprintf(outfile, "%f, ", regionalData[index].bias_error);

                if (regionalData[index].lcl_MW == -1)
                  fprintf(outfile, "NULL, ");
                else
                  fprintf(outfile, "%f, ", regionalData[index].lcl_MW);

                if (regionalData[index].ucl_MW == -1)
                  fprintf(outfile, "NULL, ");
                else
                  fprintf(outfile, "%f, ", regionalData[index].ucl_MW);

                fprintf(outfile, "%d, ", regionalData[index].version_id);
                fprintf(outfile, "'%s', ", regionalData[index].version);

                if (regionalData[index].installedcapacity_MW == -1)
                  fprintf(outfile, "NULL, ");
                else
                  fprintf(outfile, "%f, ", regionalData[index].installedcapacity_MW);

                if (regionalData[index].capacity_MWp == -1)
                  fprintf(outfile, "NULL, ");
                else
                  fprintf(outfile, "%f, ", regionalData[index].capacity_MWp);

                fprintf(outfile, "%d, ", regionalData[index].site_count);
                fprintf(outfile, "%d);\n", regionalData[index].calculation_time_s);
              }

              fprintf(outfile, "MY_QUERY");
            }
            fclose(outfile);
            break;

    case 2: cout << "Observatory Data..." << endl;
            system("cls");
            cout << "Choose site..." << endl;
            cout << "  1. Whitworth" << endl;
            cout << "  2. Holme Moss" << endl << endl;

            cout << "Option: ";
            cin >> op;
            system("cls");

            char siteName[11];
            if (op == 1) {
              strcpy(siteName, "Whitworth");
              for (index = 2013; index <= 2017; index++) {
                sprintf(in_name, "csv/%d_Whitworth.csv", index);
                readCsv(in_name, siteName, numar);

                sprintf(out_name, "sql/%d_Whitworth.sql", index);
                writeSql(out_name, siteName, numar);
              }
            }
            else if (op == 2) {
              strcpy(siteName, "Holme Moss");
              for (index = 2013; index <= 2017; index++) {
                sprintf(in_name, "csv/%d_HolmeMoss.csv", index);
                readCsv(in_name, siteName, numar);

                sprintf(out_name, "sql/%d_HolmeMoss.sql", index);
                writeSql(out_name, siteName, numar);
              }
            }
            else
              cout << "Invalid site!" << endl;
            break;

    default: cout << "Invalid option!" << endl;
             break;
  }
  return 0;
}
