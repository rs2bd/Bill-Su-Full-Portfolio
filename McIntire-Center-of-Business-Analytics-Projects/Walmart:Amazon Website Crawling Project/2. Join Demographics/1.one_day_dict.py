__author__ = 'rs2bd'
import csv
import datetime
import os

datetime_dict = {}
all_files = []
paths = []
for path in paths:
    dirs = os.listdir(path)
    csv.field_size_limit(2147483647)
    for file in dirs:
        all_files.append(path + "\\" + file)

with open("amazon_full_data.csv", "r") as datafile:
    datareader = csv.reader(datafile)
    datareader.next()
    for row in datareader:
        date = datetime.datetime.strptime(row[22] + " " + row[24], "%Y-%m-%d %H:%M:%S" )
        file = (datetime.datetime.strftime(date + datetime.timedelta(hours=5),"%Y%m%d_raw_qa.bcp"))
        directory = ""
        for items in all_files:
            if file in items:
                directory = items

        if directory in datetime_dict.keys():
            datetime_dict[directory].append((row[25], date.strftime("%Y-%m-%d %H:%M:%S")))
        else:
            datetime_dict[directory] = [(row[25], date.strftime("%Y-%m-%d %H:%M:%S"))]

with open("1.one_day_result.csv", "w") as write_category:
    writer = csv.writer(write_category, lineterminator='\n')
    for key in datetime_dict:
        writer.writerow([key, datetime_dict[key]])
