__author__ = 'rs2bd'
import csv
import datetime
import os
from collections import Counter
from itertools import product
import pandas

fieldname = ["ID","v1","X1","website","X","social","review","coupon","search","ppt","ppo","app","opp","maxcat","age","gender","income","size","edu","child","race","eth","time","day","timeofday","user","prevcheckout","prevsocial","prevreview","prevcoupon","prevsearch","prevppt","prevppo","prevapp","prevopp","totalcheckout","prevsite","socbyweb","revbyweb","coupbyweb","searchbyweb","pptbyweb","ppobyweb","appbyweb","oppbyweb","HUDummy2","HUscorediff2","Hedonic","Utilitarian","brandfamilarity","rank","pageviewspermillion","pageviewsperuser","reachpermillion","nvals"]
cate = pandas.read_csv("7.1.amazon_perfectly_joined_result.csv")
cate["Date"] = pandas.to_datetime(cate["User ID"].apply(eval).apply(pandas.Series)[1], format = "%Y-%m-%d %H:%M:%S")
cate["User ID"] = cate["User ID"].apply(eval).apply(pandas.Series)[0]
categories = cate["Category"].drop_duplicates().tolist()
counter = 0
with open("amazon_full_data.csv", "r") as f, open("8.amazon_final_result.csv", "w") as w:
    reader = csv.DictReader(f, fieldnames= fieldname)
    fieldnameW = fieldname + categories
    writer = csv.DictWriter(w, fieldnames= fieldnameW, lineterminator = "\n")
    writer.writeheader()
    reader.next()
    for row in reader:
        temp = row
        date = datetime.datetime.strptime(row["time"] + " " + row["timeofday"], "%Y-%m-%d %H:%M:%S" )
        min_date = date - datetime.timedelta(days = 3)
        list = cate[(cate["User ID"] == row["user"]) & (cate["Date"] >= min_date) & (cate["Date"] <= date)]
        cate_dict = list["Category"].value_counts().to_dict()
        for item in categories:
            if item not in cate_dict.keys():
                temp[item] = None
            else: temp[item] = cate_dict[item]
        writer.writerow(temp)
        counter += 1
        if counter % 100 == 0:
            print counter


# data["day"] = data["day"].apply(lambda x: datetime.datetime.strftime(datetime.datetime.striptime(x, "%-m/%-d/%Y"), "%Y-%m-%d"))
# print data["day"]
# pandas.merge(data, cate, left_on= "Date", right_on="")
#
# for datarow in datareader:
#     relevant_rows = []
#     date = datetime.datetime.strptime(datarow[22] + " " + datarow[24], "%Y-%m-%d" )
#     min_date = date - datetime.timedelta(days=3)
#     catedate = datetime.datetime.strptime(datarow[22] + " " + datarow[24], "%Y-%m-%d" )
#
