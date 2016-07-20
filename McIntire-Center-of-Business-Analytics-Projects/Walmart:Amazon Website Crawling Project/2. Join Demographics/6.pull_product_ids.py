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
with open("5.all_files_result.csv", "r") as readfile:
    reader = csv.reader(readfile)
    with open("6.amazon_category_item_id.csv", "w") as writefile:
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
                    # if datarow[0] == "www.walmart.com" and (datarow[1].startswith("ip/") or row[1] == "ip") and datarow[2] != 'undefined' and len(datarow) > 6:
                    if datarow[0] == "www.amazon.com" and (datarow[1].endswith("/dp") or datarow[1] == ("gp/product")) and len(datarow[2]) == 10:

                        for user in users:
                            if datarow[6] == user[0]:
                                data_time = datetime.datetime.fromtimestamp(int(datarow[4]) + 946598400)
                                matrix_time = datetime.datetime.strptime(user[1], "%Y-%m-%d %H:%M:%S")
                                # print "match", matrix_time, data_time
                                if data_time >= (matrix_time - datetime.timedelta(days = 3)) and data_time <= matrix_time:
                                    writer.writerow([user, data_time.strftime("%Y-%m-%d"), datarow[2]])
                print filename + "took" + str(time.clock() - starttime) + " seconds"
