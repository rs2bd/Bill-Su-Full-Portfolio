import csv
import re
matching = {}
counter = 0
with open("Amazon_Recrawl_Matching.csv", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        matching[row[0]] = row[1]
with open("amazon_no_access_result.csv", "r") as readfile:
    reader1 = csv.reader(readfile)
    with open("Amazon_recrawl_two_categories.csv", "w") as writefile:
        writer = csv.writer(writefile, lineterminator = "\n")
        for row in reader1:
            if row[1] in matching.keys():
                writer.writerow([row[0], row[1], matching[row[1]]])
            else: counter = counter + 1
print counter