################################################################

## WeatherData.py
## This is the file for weather collection
## Created by Miya Wang
## Last update: 12/2016

## All right reserved (c) 2016
##################################################################


#api_key = '9df031d5c848bb78f4b6365e4e7ce2e8'
api_key = '2bbae2422757b9be4efaa7722e9be466'
import forecastio
import datetime

years = [2014]
months = list(range(10, 13))
days = list(range(1, 32))
hours = list(range(0, 24))

import sqlite3 as lite

con = lite.connect('weather.db')
with con:
    cur = con.cursor()
    cur.execute('drop table if exists weather_3')
    create_table_query = 'create table weather_3' + '(temp,icon,windBearing,windSpeed,visibility,hour,date)'
    cur.execute(create_table_query)

for year in years:
    for month in months:
        for day in days:
            try:
                date = datetime.datetime(year, month, day)
                forecast = forecastio.load_forecast(api_key, 40.730610, -73.935242, time=date, units="us")
                hourly = forecast.hourly()
                for hour in hours:
                    hourly = forecast.hourly()
                    temp = hourly.data[hour].d['temperature']
                    icon = hourly.data[hour].d['icon']
                    windBearing = hourly.data[hour].d['windBearing']
                    windSpeed = hourly.data[hour].d['windSpeed']
                    visibility = hourly.data[hour].d['visibility']
                    row = [temp, icon, windBearing, windSpeed, visibility, hour, date]
                    cur.execute('''Insert into weather_3 values (?,?,?,?,?,?,?)''', row)
            except Exception:
                pass
with con:
    cur = con.cursor()
    cur.execute("""select count(*) from weather_3""")
    all_data = cur.fetchall()
    print(all_data)  # 15735 recordS+8394 FOR 2015+4228 FOR 2016 +2140