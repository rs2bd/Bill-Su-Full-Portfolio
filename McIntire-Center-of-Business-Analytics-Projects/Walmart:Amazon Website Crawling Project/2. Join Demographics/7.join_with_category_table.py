__author__ = 'rs2bd'
__author__ = 'billsu'
import csv
import json
import urllib2
import re
from bs4 import BeautifulSoup
import hashlib
import hmac
import sys
import os
import numpy
import pandas


csv.field_size_limit(2147483647)
date = []
category = pandas.read_csv("amazon_two_categories.csv", names = ["Item ID", "API Category", "Category"])
category["Item ID"] = category["Item ID"].astype(str)
user_data = pandas.read_csv("6.amazon_category_item_id.csv", names = ["User ID", "Date", "Item ID"])
user_data["Item ID"]= user_data["Item ID"].astype(str)
perfectly_joined = pandas.merge(category, user_data, how = "inner")
perfectly_joined.to_csv("7.1.amazon_perfectly_joined_result.csv", sep=",")
joined = pandas.merge(category, user_data, how= "right")
empties = joined[~joined["Item ID"].isin(perfectly_joined["Item ID"])]
empties.to_csv("7.2.amazon_imperfectly_joined_result.csv", sep= ",")