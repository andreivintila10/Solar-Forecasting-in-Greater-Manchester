import mysql.connector

print("Hello world\n")

username = 'andrei'
password = 'Vinti123!'
host = '130.88.96.145'
database = 'weather_data'

conn = mysql.connector.connect(user=username, password=password,
                              host=host,
                              database=database)
#conn.close()


exit = input("Press close to exit...")