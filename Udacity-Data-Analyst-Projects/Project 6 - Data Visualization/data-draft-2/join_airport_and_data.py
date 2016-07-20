__author__ = 'billsu'
import json
import csv
import pandas
import datetime
import numpy as np
import sys

datafile = pandas.read_csv("airline_delay_causes.csv")
airport_file = pandas.read_json("airports.json")

datafile = datafile.rename(columns=lambda x: x.strip())
# datafile["date"] = datafile["year"].map(str) + "-" + datafile["month"].map(str)
# datafile["date"] = pandas.to_datetime(datafile["date"], format = "%Y-%m")
datafile = datafile[["year", 'airport', 'arr_flights', 'arr_del15', 'carrier_ct', 'weather_ct', "nas_ct",
                     "security_ct", "late_aircraft_ct"]]
grouped = datafile.groupby(["airport", "year"])
grouped = grouped.agg(np.sum)
records = pandas.DataFrame(grouped.to_records())
records['growth_rate'] = records['arr_flights'].pct_change()
records['delay_change'] = records['arr_del15'].pct_change()

records = records[records['year'] < 2016]
records = records[records['year'] > 2004]

# records = records[records["date"] != pandas.to_datetime("2003-06-01", format="%Y-%m-%d")]
records.to_csv("clean_data.csv", index= False)