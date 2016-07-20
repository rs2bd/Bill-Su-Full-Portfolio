__author__ = 'billsu'
import json
import csv
import pandas
import datetime
#
# data = []
#
# with open("airline_delay_causes.csv", "r") as datafile:
#     reader = csv.DictReader(datafile)
#     for row in reader:
#         data.append(row)
datafile = pandas.read_csv("airline_delay_causes.csv")
airport_file = pandas.read_json("airports.json")
#
# with open('airports.json') as airport_file:
#     data = json.load(airport_file)
#     for row in data:
#         print row
joined = pandas.merge(datafile, airport_file, left_on= "airport", right_on= "iata")
joined = joined.rename(columns=lambda x: x.strip())
joined["date"] = joined["year"].map(str) + "-" + joined["month"].map(str)
joined.to_csv("joined_result.csv")


