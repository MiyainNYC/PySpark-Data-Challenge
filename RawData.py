################################################################

## RawData.py
## This is the file for ridership collection
## Created by Miya Wang
## Last update: 12/2016

## All right reserved (c) 2016
##################################################################


import pandas as pd
import io
import requests
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar
import sqlite3 as lite


con = lite.connect('raw_cab.db')

col_name = ['VendorID', 'lpep_pickup_datetime', 'Lpep_dropoff_datetime'
    , 'Store_and_fwd_flag', 'RateCodeID', 'Pickup_longitude', 'Pickup_latitude'
    , 'Dropoff_longitude', 'Dropoff_latitude'
    , 'Passenger_count', 'Trip_distance', 'Fare_amount'
    , 'Extra', 'MTA_tax'
    , 'Tip_amount', 'Tolls_amount', 'Ehail_fee', 'improvement_surcharge'
    , 'Total_amount', 'Payment_type', 'Trip_type']

years = ['2013' , '2014', '2015', '2016']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

for year in years:

    start = year + '-01-01'
    end = year + '-12-31'
    dr = pd.date_range(start=start, end=end)
    cal = calendar()
    holidays = cal.holidays(start=dr.min(), end=dr.max())

    for month in months:

        url = 'https://s3.amazonaws.com/nyc-tlc/trip+data/green_tripdata_' + year + '-' + month + '.csv'
        s = requests.get(url).content
        c = pd.read_csv(io.StringIO(s.decode('utf-8')), header=None, skiprows=[0])
        if len(c.columns) > 10:
            c = c.ix[:, :20]
            c.columns = col_name
            shape_origin = c.shape
            print('%s :%s' % (year, month))

            c['lpep_pickup_datetime'] = pd.to_datetime(c['lpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
            c['Lpep_dropoff_datetime'] = pd.to_datetime(c['Lpep_dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')
            c['interval_min'] = list(map(lambda x: x / 60, list(
                map(lambda x: x.total_seconds(), list(c['Lpep_dropoff_datetime'] - c['lpep_pickup_datetime'])))))

            c['weekofday'] = list(map(lambda x: x.weekday(), c['lpep_pickup_datetime']))
            c['hour'] = list(map(lambda x: x.hour, c['lpep_pickup_datetime']))
            c['day'] = list(map(lambda x: x.day, c['lpep_pickup_datetime']))
            c['month'] = list(map(lambda x: x.month, c['lpep_pickup_datetime']))
            c['year'] = list(map(lambda x: x.year, c['lpep_pickup_datetime']))
            c['date'] = list(map(lambda x: x.date(), c['lpep_pickup_datetime']))
            c['date'] = pd.to_datetime(c['date'], format='%Y-%m-%d')
            c['Holiday'] = c['date'].isin(holidays)



            col_del = ['VendorID', 'lpep_pickup_datetime', 'Lpep_dropoff_datetime', 'Pickup_longitude',
                       'Pickup_latitude', 'Dropoff_longitude', 'Dropoff_latitude', 'Ehail_fee']
            for col in col_del:
                c = c.drop(col, 1)

            c = c.reindex_axis(sorted(c.columns), axis=1)

            print('shape:%s rows %s columns' % (c.shape[0], c.shape[1]))

            c.to_sql(name='trip', con=con, flavor='sqlite', if_exists='append')