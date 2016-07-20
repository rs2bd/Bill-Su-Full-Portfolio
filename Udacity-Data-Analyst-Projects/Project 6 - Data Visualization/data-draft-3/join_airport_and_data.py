__author__ = 'billsu'
import json
import csv
import pandas
import datetime
import numpy as np
import sys

# def check_percentile(x):
#     if (x <= airports.quantile(.5)):
#         return "High"
#     else:
#         return "Low"

datafile = pandas.read_csv("airline_delay_causes.csv")

datafile = datafile.rename(columns=lambda x: x.strip())
datafile["date"] = datafile["year"].map(str) + "-" + datafile["month"].map(str)
datafile["date"] = pandas.to_datetime(datafile["date"], format = "%Y-%m")
datafile = datafile[["date", 'airport', 'arr_flights', 'arr_del15', 'carrier_ct', 'weather_ct', "nas_ct",
                     "security_ct", "late_aircraft_ct"]]
grouped = datafile.groupby(["airport", "date"])
grouped = grouped.agg(np.sum)
records = pandas.DataFrame(grouped.to_records())
records['delay_percentage'] = records['arr_del15']/records['arr_flights']
records['growth_rate'] = records['arr_flights'].pct_change()
records['delay_change'] = records['arr_del15'].pct_change()
records['delay_percentage_change'] = records['delay_percentage'].pct_change()
records = records[records["date"] != pandas.to_datetime("2003-06-01", format="%Y-%m-%d")]

regrouped = records.groupby(['airport'])
regrouped = regrouped.agg(np.mean)

airport_size = {}
for item in regrouped['arr_flights'].iteritems():
    airport_size[item[0]] = item[1]

# airports = pandas.Series(airport_size)
# airports.name = "airport"

# airports = airports.apply(check_percentile)
# airport_size = airports.to_dict()

# def assign_things(x):
#     if x in airport_size.keys():
#         return airport_size[x]

# records["size"] = records['airport'].apply(assign_things)
datafile = records.groupby(['date']).agg(np.mean)
datafile = pandas.DataFrame(datafile.to_records())

datafile = datafile[['date', 'delay_change', 'growth_rate', "delay_percentage", "delay_percentage_change"]]
datafile['year'] = datafile['date'].apply(lambda x: x.year)
datafile.to_csv("cleaned_with_size.csv", index = False)


