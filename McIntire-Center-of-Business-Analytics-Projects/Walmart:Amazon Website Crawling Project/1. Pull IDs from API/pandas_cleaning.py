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
user_data = pandas.read_csv("amazon_category_item_id.csv", names = ["User ID", "Date", "Item ID"])
joined = pandas.merge(category, user_data, how = "right")
joined.to_csv("joined_result", sep=",")
