__author__ = 'rs2bd'
import csv
import datetime
import ast
import os

all_files = []
for path in paths:
    dirs = os.listdir(path)
    csv.field_size_limit(2147483647)
    for file in dirs:
        all_files.append(path + "\\" + file)

with open("2.starting_file_result.csv", "r") as second, open("1.one_day_result.csv", "r") as first, \
        open("3.mismatch_result.csv", "w") as w:
    reader2 = csv.reader(second)
    reader = csv.reader(first)
    writer = csv.writer(w, lineterminator = "\n")
    second_list = []
    first_list = []
    differences = []
    result_dict = {}
    for row2 in reader2:
        second_list.append((row2[1], row2[2]))

    for row in reader:
        list = ast.literal_eval(row[1])
        for item in list:
            first_list.append(item)

    for item in first_list:
        if item not in second_list:
            differences.append(item)

    for item in differences:
        date = datetime.datetime.strptime(item[1], "%Y-%m-%d %H:%M:%S" )
        file = (datetime.datetime.strftime(date,"%Y%m%d_raw_qa.bcp"))
        for f in all_files:
            if file in f:
                file = f
                if f in result_dict.keys():
                    result_dict[f].append((item[0], item[1]))
                else:
                    result_dict[f] = [(item[0], item[1])]
    print len(first_list), len(second_list), len(differences)
    for key in result_dict:
        writer.writerow([key, result_dict[key]])

