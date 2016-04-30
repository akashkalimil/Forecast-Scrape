import requests
import sqlite3 as lite
import datetime

api_key = "<api_key>"
url = 'https://api.forecast.io/forecast/' + 33c992470e825ea4735c70979636dd7c

cities = { "Atlanta": '33.762909,-84.422675',
            "Austin": '30.303936,-97.754355',
            "Boston": '42.331960,-71.020173',
            "Chicago": '41.837551,-87.681844',
            "Cleveland": '41.478462,-81.679435'
        }
end_date = datetime.datetime.now() 
con = lite.connect('weather.db')
cur = con.cursor()


cities.keys()
with con:
    cur.execute('CREATE TABLE daily_temp ( day_of_reading INT, city1 REAL, city2 REAL, city3 REAL, city4 REAL, city5 REAL);') 



query_date = end_date - datetime.timedelta(days=30) #the current value being processed

with con:
    while query_date < end_date:
        cur.execute("INSERT INTO daily_temp(day_of_reading) VALUES (?)", (int(query_date.strftime('%s')),))
        query_date += datetime.timedelta(days=1)


for k,v in cities.iteritems():
    query_date = end_date - datetime.timedelta(days=30) #set value each time through the loop of cities
    while query_date < end_date:
        #query for the value
        r = requests.get(url + v + ',' +  query_date.strftime('%Y-%m-%dT12:00:00'))

        with con:
            #insert the temperature max to the database
            cur.execute('UPDATE daily_temp SET ' + k + ' = ' + str(r.json()['daily']['data'][0]['temperatureMax']) + ' WHERE day_of_reading = ' + query_date.strftime('%s'))

        #increment query_date to the next day for next operation of loop
        query_date += datetime.timedelta(days=1) #increment query_date to the next day


con.close() # a good practice to close connection to database