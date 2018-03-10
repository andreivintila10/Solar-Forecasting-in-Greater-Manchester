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
    cout << "2. ManUniCast" << endl;
    cout << "3. Observatory" << endl;
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

void string_copy(char *to, char *from) {
    for (int index = 0; index < strlen(from); index++)
        to[index] = from[index];
}

void string_concatenate(char *to, char *from) {
    int lengthTo = strlen(to);
    int lengthFrom = strlen(from);
    for (int index = 0; index < lengthFrom; index++) {
        to[lengthTo] = from[index];
        lengthTo++;
    }
}

char *changeDateFormat(char *date) {
    int length = strlen(date);
    char day[3];
    day[0] = date[0];
    day[1] = date[1];
    day[2] = '\0';
    printf("%s ", day);

    char month[3];
    month[0] = date[3];
    month[1] = date[4];
    month[2] = '\0';
    printf("%s ", month);

    char year[5];
    year[0] = date[6];
    year[1] = date[7];
    year[2] = date[8];
    year[3] = date[9];
    year[4] = '\0';
    printf("%s ", year);

    char *newDate = (char *) malloc(sizeof(char) * 12);
    strcpy(newDate, year);
    strcat(newDate, "-");
    strcat(newDate, month);
    strcat(newDate, "-");
    strcat(newDate, day);
    strcat(newDate, "\0");
    printf("%s\n", newDate);

    return newDate;
}

int main() {
    meniu();

    int op;
    char fileName[30], skip[1024], line[1024], word[100];
    char *words, *temp;
    int numar, ok, index;
    FILE *infile, *outfile;
    cout << "Option: ";
    cin >> op;
    system("cls");

    switch (op) {
        case 1: cout << "1. Regional data..." << endl;
                cout << "File name: ";
                cin >> fileName;

                char in_name[50];
                strcpy(in_name, "raw/");
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
                        string_copy(regionalData[numar].datetime_GMT, stripQuotes(words));

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
                        string_copy(regionalData[numar].version, stripQuotes(words));

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

                        /*cout << regionalData[numar].region_id << " "
                             << regionalData[numar].datetime_GMT << " "
                             << regionalData[numar].generation_MW << " "
                             << regionalData[numar].uncertainty_MW << " "
                             << regionalData[numar].stats_error << " "
                             << regionalData[numar].bias_error << " "
                             << regionalData[numar].lcl_MW << " "
                             << regionalData[numar].ucl_MW << " "
                             << regionalData[numar].version_id << " "
                             << regionalData[numar].version << " "
                             << regionalData[numar].installedcapacity_MW << " "
                             << regionalData[numar].capacity_MWp << " "
                             << regionalData[numar].site_count << " "
                             << regionalData[numar].calculation_time_s << endl;*/
                        numar++;

                    }
                  }
                }
                fclose(infile);

                char out_name[50];
                strcpy(out_name, "sql/");
                strcat(out_name, fileName);
                strcat(out_name, ".sql");
                outfile = fopen(out_name, "w");
                if (outfile) {
                    //fprintf(outfile, "region_id,datetime_GMT,generation_MW,uncertainty_MW,stats_error,bias_error,lcl_MW,ucl_MW,version_id,version,installedcapacity_MWp,capacity_MWp,site_count,calculation_time_s\n");
                    fprintf(outfile, "#!/bin/bash\n");
                    fprintf(outfile, "\n");
                    fprintf(outfile, "username=\"andrei\"\n");
                    fprintf(outfile, "password=\"Vinti123!\"\n");
                    fprintf(outfile, "database=\"weather_data\"\n");
                    fprintf(outfile, "\n");
                    fprintf(outfile, "mysql -u \"$username\" -p\"$password\" \"$database\" <<MY_QUERY\n");
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
                        /*outfile << regionalData[index].region_id << ","
                                << regionalData[index].datetime_GMT << ","
                                << (regionalData[index].generation_MW == -1.0 ? NULL : regionalData[index].generation_MW) << ","
                                << (regionalData[index].uncertainty_MW == -1 ? NULL : regionalData[index].uncertainty_MW) << ","
                                << (regionalData[index].stats_error == -1 ? NULL : regionalData[index].stats_error) << ","
                                << (regionalData[index].bias_error == -1 ? NULL : regionalData[index].bias_error) << ","
                                << (regionalData[index].lcl_MW == -1 ? NULL : regionalData[index].lcl_MW) << ","
                                << (regionalData[index].ucl_MW == -1 ? NULL : regionalData[index].ucl_MW) << ","
                                << regionalData[index].version_id << ","
                                << regionalData[index].version << ","
                                << (regionalData[index].installedcapacity_MW == -1 ? NULL : regionalData[index].installedcapacity_MW) << ","
                                << (regionalData[index].capacity_MWp == -1 ? NULL : regionalData[index].capacity_MWp) << ","
                                << regionalData[index].site_count << ","
                                << regionalData[index].calculation_time_s;*/


                        /*if (index < numar - 1)
                            fprintf(outfile, "\n");*/
                    }
                    fprintf(outfile, "MY_QUERY");
                }
                fclose(outfile);
                break;

        case 2: cout << "ManUniCast Data..." << endl;
                break;

        case 3: cout << "Observatory Data..." << endl;
                char *day, *month, *year, *dash;
                infile = fopen("csv/2013.csv", "r");
                if (infile) {
                  fgets(skip, sizeof(skip), infile);
                  numar = 0;
                  ok = 1;
                  while (fgets(line, sizeof(line), infile)) {
                    words = strtok(line, ", ");
                    printf("Transform: %s \n", words);
                    printf("Before changeDate\n");
                    string_copy(observatoryData[numar].date, changeDateFormat(words));
                    printf("This: %s ", observatoryData[numar].date);

                    words = strtok(NULL, ", ");
                    string_copy(observatoryData[numar].time, words);
                    printf("%s\n", observatoryData[numar].time);
                    printf("Once again: %s\n", observatoryData[numar].date);

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

                    words = strtok(NULL, ", ");
                    if (!strcmp(words, "NaN"))
                        observatoryData[numar].total_solar_radiance = -9999;
                    else
                        observatoryData[numar].total_solar_radiance = atof(words);

                    words = strtok(NULL, ", ");
                    if (!strcmp(words, "NaN"))
                        observatoryData[numar].precipitation = -9999;
                    else
                        observatoryData[numar].precipitation = atof(words);
                    numar++;
                  }
                }
                fclose(infile);

                outfile = fopen("sql/2013_Whitworth.sql", "w");
                if (outfile) {
                    fprintf(outfile, "#!/bin/bash\n");
                    fprintf(outfile, "\n");
                    fprintf(outfile, "username=\"andrei\"\n");
                    fprintf(outfile, "password=\"Vinti123!\"\n");
                    fprintf(outfile, "database=\"weather_data\"\n");
                    fprintf(outfile, "\n");
                    fprintf(outfile, "mysql -u \"$username\" -p\"$password\" \"$database\" <<MY_QUERY\n");
                    for (index = 0; index < numar; index++) {
                        fprintf(outfile, "INSERT INTO Observatory VALUES (");
                        printf("%s ", observatoryData[index].date);
                        fprintf(outfile, "'%s', ", observatoryData[index].date);
                        printf("%s\n", observatoryData[index].time);
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
                break;

        default: cout << "Invalid option!" << endl;
                 break;
    }
    return 0;
}
