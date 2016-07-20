__author__ = 'billsu'
from amazonproduct import API
import csv
import json
import urllib2
import time
import re
from bs4 import BeautifulSoup
import hashlib
import hmac
count_csv = 0
data = []

counter = 0
filename = "amazon_no_access.csv"
with open(filename, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter= ',')
    for row in reader:
        api = API(locale='us')
        counter = counter + 1
        if counter % 100 == 0:
            print counter
        try: result = api.item_lookup(row[0])
        except Exception, e:
            print str(e)
            if str(e) == "AWS.ECommerceService.ItemNotAccessible: This item is not accessible through the Product Advertising API.":
                data.append((row[0], "no access"))
            else:
                data.append((row[0], "invalid"))
            time.sleep(1)
            continue
        try:
            for item in result.Items.Item:
                    category = item.ItemAttributes.ProductGroup
                    data.append((row[0], category))
        except:
            data.append((row[0], "error"))
            pass
        time.sleep(1)
        if count_csv == 20:
            with open('result_3.csv', 'a') as writingcsv:
                writer = csv.writer(writingcsv, delimiter = ",", quotechar='|', lineterminator='\n')
                for item in data:
                    writer.writerow([item[0], item[1]])
            data = []
            count_csv = 0

        count_csv = count_csv + 1

