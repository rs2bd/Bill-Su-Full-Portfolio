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

with open("2.starting_file_result.csv", "r") as datafile:
    datareader = csv.reader(datafile)
    for row in datareader:
        date = datetime.datetime.strptime(row[2], "%Y-%m-%d %H:%M:%S" )
        files = []
        for i in range(0,4):
            files.append(datetime.datetime.strftime(date + datetime.timedelta(hours = 5) - datetime.timedelta(days=i),"%Y%m%d_raw_qa.bcp"))


        directory = []
        for item in files:
            for items in all_files:
                if item in items:
                    directory.append(items)

        for file in directory:
            if file in datetime_dict.keys():
                datetime_dict[file].append((row[1], date.strftime("%Y-%m-%d %H:%M:%S")))
            else:
                datetime_dict[file] = [(row[1], date.strftime("%Y-%m-%d %H:%M:%S"))]

with open("5.all_files_result.csv", "w") as write_category:
    writer = csv.writer(write_category, lineterminator='\n')
    for key in datetime_dict:
        writer.writerow([key, datetime_dict[key]])
