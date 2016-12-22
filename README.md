# Green-cab-ridership

# Dataset

All TLC Trip Record Data for Green Cab in NYC from 2013 through 2016.(5.22 Gigabytes, 45299607 records)

### Features

1. [Features Provided](http://www.nyc.gov/html/tlc/downloads/pdf/data_dictionary_trip_records_green.pdf)

2. Features Modified or Added:

* Year, Month, Day, Day of Week, Hour, IsHoliday, Trip_time

* Hourly Weather Data including: summary,temperature, WindBearing, WindSpeed, Visibility

# Tools
* PySpark

# Methodology

* Exploratory & Visualization
* Machine Learning Model

# Questions to be answered:

* number of trip: by year/month/day of week/hour/is holiday/weather(summary)
* number of trip: pay_type/RateCodeID
* Pick-up & Drop off location comparison(2013 VS 2016)
* Tip percentage distribution: by year/month/day of week/hour/is holiday/weather(summary)
* Efficiency(Fare_amount/time_interval): by year/month/day of week/hour/is holiday/weather
* distance distribution: by year/month/day of week/hour/is holiday/weather
* network: hub
* **Is this trip "efficient" ?**
