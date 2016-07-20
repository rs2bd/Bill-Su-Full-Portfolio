__author__ = 'rs2bd'

import csv
import datetime
import ast
import sys
import time
counter = 0
csv.field_size_limit(500*1024*1024)
test = set()
starttime = time.clock()
with open("full_data_user_name_by_date", "r") as readfile:
    reader = csv.reader(readfile)
    with open("clickstream sample - walmart.csv", "a") as writefile:
        writer = csv.writer(writefile, lineterminator = "\n")
        for row in reader:
            counter += 1
            filename = row[0]
            users = ast.literal_eval(row[1])
            count = 0
            with open(filename, "r") as datafile:
                datareader = csv.reader(datafile, delimiter='\t')
                for datarow in datareader:
                    count += 1
                    # if datarow[0] == "www.amazon.com" and (datarow[1].endswith("/dp") or datarow[1] == ("gp/product")) and len(datarow[2]) == 10:
                    if datarow[0] == "www.walmart.com":
                        for user in users:
                            if datarow[6] == user:
                                data_time = datetime.datetime.fromtimestamp(float(datarow[4]) + 946598400)
                                print count
                                test.add(user)
                                # writer.writerow([user, data_time.strftime("%Y-%m-%d"), datarow[2]])
                                writer.writerow(datarow)
                print filename + "took" + str(time.clock() - starttime) + " seconds"
                break
