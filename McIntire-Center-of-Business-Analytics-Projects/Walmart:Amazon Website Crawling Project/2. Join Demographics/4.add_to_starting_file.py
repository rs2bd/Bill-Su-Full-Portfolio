__author__ = 'rs2bd'
import csv
import ast
import datetime
import os

#Note: This is practically the same code as step 2, the result is also appended in the resulting file of the second step.
#The only differences is that we opened the different file. Placed here for logical clearity.

csv.field_size_limit(500*1024*1024)
differences = {}
tuple_list = []
with open("3.mismatch_result.csv", "r") as r, open("2.starting_file_result.csv", "a") as w:
    reader = csv.reader(r)
    writer = csv.writer(w, lineterminator = "\n")
    for row in reader:
        list = ast.literal_eval(row[1])
        users = {}
        for item in list:
            users[item[0]] = (item[1])
        already = []
        counter = 0
        flag = False
        if row[0] == "tuple":
            for entry in list:
                tuple_list.append(entry)
        else:
            with open(row[0], "r") as datafile:
                datareader = csv.reader(datafile, delimiter='\t')

                for datarow in datareader:

                    if len(datarow) > 6:
                        if (datarow[6] in users.keys()):
                            clickstream_time = datetime.datetime.fromtimestamp(float(datarow[4]) + 946598400)
                            time = datetime.datetime.strptime(users[datarow[6]], "%Y-%m-%d %H:%M:%S")



                            if time == clickstream_time:
                                counter += 1
                                # print time, clickstream_time, datarow
                                already.append((datarow[6], users[datarow[6]]))
                                writer.writerow([row[0], datarow[6], users[datarow[6]]])

        for tuple in list:
            if tuple not in already:
                tuple_list.append(tuple)

        print row[0], len(users.keys()), counter


all_files = []
for path in paths:
    dirs = os.listdir(path)
    csv.field_size_limit(2147483647)
    for file in dirs:
        all_files.append(path + "\\" + file)