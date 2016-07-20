__author__ = 'rs2bd'
import csv
import time
import datetime
from itertools import product

counter = 0
counter2 = 0
filelist = []
with open("amazon_category_item_id.csv", "r") as user_item_id_file, open("amazon_two_categories.csv", "r") as category_file, \
        open("amazon_matched_user_categories.csv", "w") as matched_file, open("amazon_unmatched_user_categories.csv", "w") as unmatched_file:
    user_item_id_reader = csv.reader(user_item_id_file)
    category_reader = csv.reader(category_file)
    matched_writer = csv.writer(matched_file, lineterminator = "\n")
    unmatched_writer = csv.writer(unmatched_file, lineterminator = "\n")
    for (datarow, matchingrow) in product(user_item_id_reader, category_reader):
        counter += 1
        flag = False
        for matchingrow in category_reader:
            counter += 1
            if datarow[2] == matchingrow[0]:
                flag = True
                matched_writer.writerow([datarow[0], datarow[1], datarow[2], matchingrow[2]])
        if flag == False:
            unmatched_writer.writerow(datarow)
    # filelist.append(datarow)
print counter
