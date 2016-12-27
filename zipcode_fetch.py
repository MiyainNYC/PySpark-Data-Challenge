################################################################

## feb2016set.py
## This is the file for ridership zip location collection and cleansing for 2016 2015 prticularly
## Created by Miya Wang
## Last update: 12/2016

## All right reserved (c) 2016
##################################################################


import pandas as pd
import io
import requests
import datetime
from geopy.geocoders import Nominatim
from pandas.tseries.holiday import USFederalHolidayCalendar as calendar


col_name = ['VendorID', 'lpep_pickup_datetime', 'Lpep_dropoff_datetime'
    , 'Store_and_fwd_flag', 'RateCodeID', 'Pickup_longitude', 'Pickup_latitude'
    , 'Dropoff_longitude', 'Dropoff_latitude'
    , 'Passenger_count', 'Trip_distance', 'Fare_amount'
    , 'Extra', 'MTA_tax'
    , 'Tip_amount', 'Tolls_amount', 'Ehail_fee', 'improvement_surcharge'
    , 'Total_amount', 'Payment_type', 'Trip_type']

years = ['2015','2016']
months = ['01','02','03','04','05','06']

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

            c = c[c['VendorID'].isin(list(range(1,3)))!=0]
            c = c[c['Store_and_fwd_flag'].isin(list(['Y','N']))!=0]
            c = c[c['RateCodeID'].isin(list(range(1,7)))!=0]
            c = c[c['Passenger_count']<=5]
            c = c[c['Trip_distance']>0]
            c = c[c['Fare_amount']>0]
            c = c[c['MTA_tax']>0]
            c = c[c['Extra']>0]
            c = c[c['Tip_amount']>0]
            c = c[c['Tolls_amount']>0]
            c = c[c['improvement_surcharge']>0]
            c = c[c['Total_amount']>0]
            c = c[c['Payment_type'].isin(list(range(1,7)))!=0]
            c = c[c['Trip_type'].isin(list(range(1,3)))!=0]


            c['lpep_pickup_datetime'] = pd.to_datetime(c['lpep_pickup_datetime'], format='%Y-%m-%d %H:%M:%S')
            c['Lpep_dropoff_datetime'] = pd.to_datetime(c['Lpep_dropoff_datetime'], format='%Y-%m-%d %H:%M:%S')

            s = datetime.datetime.strptime('2016-01-01', '%Y-%m-%d')
            e = datetime.datetime.strptime('2016-12-31', '%Y-%m-%d')

            c = c[(c['lpep_pickup_datetime'] >= s) & (c['lpep_pickup_datetime'] <= e)]

            c['interval_min'] = list(map(lambda x: x / 60, list(
                map(lambda x: x.total_seconds(), list(c['Lpep_dropoff_datetime'] - c['lpep_pickup_datetime'])))))
            c = c[c['interval_min']>0]
            c = c[c['Trip_distance']/c['interval_min']<0.417]
            c = c[c['Trip_distance'] / c['interval_min'] > 0.17]
            c = c[c['Fare_amount'] / c['interval_min'] > 1]
            c = c[c['Fare_amount'] / c['interval_min'] < 30]

            print('%s rows deleted, %s rows remained'%((shape_origin[0]- len(c)),len(c)))

            c['weekofday'] = list(map(lambda x: x.weekday(), c['lpep_pickup_datetime']))
            c['hour'] = list(map(lambda x: x.hour, c['lpep_pickup_datetime']))
            c['day'] = list(map(lambda x: x.day, c['lpep_pickup_datetime']))
            c['month'] = list(map(lambda x: x.month, c['lpep_pickup_datetime']))
            c['year'] = list(map(lambda x: x.year, c['lpep_pickup_datetime']))
            c['date'] = list(map(lambda x: x.date(), c['lpep_pickup_datetime']))
            c['date'] = pd.to_datetime(c['date'], format='%Y-%m-%d')
            c['Holiday'] = c['date'].isin(holidays)

            col_geo = ['Pickup_longitude', 'Pickup_latitude', 'Dropoff_longitude', 'Dropoff_latitude']
            for col in col_geo:
                c[col] = c[col].astype('str')

            geolocator = Nominatim()
            pickup_lat_long = zip(c['Pickup_latitude'], c['Pickup_longitude'])
            dropoff_lat_long = zip(c['Dropoff_latitude'], c['Dropoff_longitude'])
            pickup_zipcode = []
            dropoff_zipcode = []




            for i, j in pickup_lat_long:
                try:
                    zipcode = geolocator.reverse(','.join([i, j]), timeout=10).address.split(',')[-2].strip()
                    pickup_zipcode.append(zipcode)
                except AttributeError:
                    pickup_zipcode.append(' ')
                except:
                    pickup_zipcode.append(' ')
                    print('too many request')
                    pass



            for i, j in dropoff_lat_long:
                try:
                    zipcode = geolocator.reverse(','.join([i, j]), timeout=10).address.split(',')[-2].strip()
                    dropoff_zipcode.append(zipcode)
                except AttributeError:
                    dropoff_zipcode.append(' ')
                except:
                    dropoff_zipcode.append(' ')
                    print('too many request')
                    pass


            c['pickup_zipcode'] = pickup_zipcode
            c['dropoff_zipcode'] = dropoff_zipcode

            print('%d columns added'%(c.shape[1]-shape_origin[1]))

            col_del = ['VendorID', 'lpep_pickup_datetime', 'Lpep_dropoff_datetime','Ehail_fee']
            for col in col_del:
                c = c.drop(col, 1)

            c = c.reindex_axis(sorted(c.columns), axis=1)

            print('shape:%s rows %s columns' % (c.shape[0], c.shape[1]))

            c.to_csv('ride_geo.csv')


c.head()

