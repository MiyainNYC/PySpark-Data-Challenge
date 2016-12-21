api_key = '9df031d5c848bb78f4b6365e4e7ce2e8'
import forecastio
import datetime

years = [2013, 2014, 2015, 2016]
months = list(range(1, 13))
days = list(range(1, 32))
hours = list(range(0, 24))

import sqlite3 as lite

con = lite.connect('weather.db')
with con:
    cur = con.cursor()
    cur.execute('drop table if exists weather')
    create_table_query = 'create table weather' + '(temp,icon,windBearing,windSpeed,visibility,hour,date)'
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
                    cur.execute('''Insert into weather values (?,?,?,?,?,?,?)''', row)
            except Exception:
                pass
with con:
    cur = con.cursor()
    cur.execute("""select count(*) from weather""")
    all_data = cur.fetchall()
    print(all_data)  # 15735 records