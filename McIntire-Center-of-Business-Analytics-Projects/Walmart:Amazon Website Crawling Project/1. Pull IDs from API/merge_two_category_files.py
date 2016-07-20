__author__ = 'rs2bd'
import csv
with open("Amazon_recrawl_two_categories.csv", "r") as rf:
    reader = csv.reader(rf)
    with open("amazon_two_categories.csv", "a") as wf:
        writer = csv.writer(wf)
        for row in reader:
            writer.writerow(row)