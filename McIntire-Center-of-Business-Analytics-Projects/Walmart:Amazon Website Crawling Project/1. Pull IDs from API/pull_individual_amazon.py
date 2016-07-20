__author__ = 'rs2bd'
from amazonproduct import API

import csv

# with open("amazon_category_item_id.csv", "r") as file:
#     reader = csv.reader(file)
#     for row in reader:
api = API(locale='us')
try:
    result = api.item_lookup("B009A17D6O")
    for item in result.Items.Item:
        category = item.ItemAttributes.ProductGroup
        print category
except Exception, e:
    print str(e)