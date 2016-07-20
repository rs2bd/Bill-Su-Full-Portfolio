__author__ = 'rs2bd'
import csv
import datetime
import os

datetime_dict = {}
all_files = []
paths = ["Z:\comScore\mm2query\ExtractedLogs2012","Z:\comScore\mm2query\ExtractedLogs2013_2014\\157-161","Z:\comScore\mm2query\ExtractedLogs2013_2014\\162-166","Z:\comScore\mm2query\ExtractedLogs2013_2014\\167-171"]
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
        min_date = date - datetime.timedelta(days=3)
        files = []
        for i in range(0,4):
            files.append(datetime.datetime.strftime(date - datetime.timedelta(days=i),"%Y%m%d_raw_qa.bcp"))


        directory = []
        for item in files:
            for items in all_files:
                if item in items:
                    directory.append(items)

        for file in directory:
            if file in datetime_dict.keys():
                datetime_dict[file].append(row[25])
            else:
                datetime_dict[file] = [row[25]]

with open("full_data_user_name_by_date", "w") as write_category:
    writer = csv.writer(write_category, lineterminator='\n')
    for key in datetime_dict:
        writer.writerow([key, datetime_dict[key]])
