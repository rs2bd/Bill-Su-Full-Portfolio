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
import pandas
import urllib2
import re
from bs4 import BeautifulSoup
import csv
count_csv = 0
counter = 0
data = []
df = pandas.read_csv("7.2.amazon_imperfectly_joined_result.csv")
df_list = df["Item ID"].tolist()
df_set = set(df_list)
print df_set


with open('amazon_no_access_result.csv', 'a') as csvfile, open("error_ids.csv", "a") as error:
    writer = csv.writer(csvfile, lineterminator='\n')
    writer2 = csv.writer(error, lineterminator = "\n")
    counter = 0
    for row in df_set:
        counter = counter + 1
        print counter
        url = 'http://www.amazon.com/dp/' + row
        response = None
        timer = 0
        while response == None and timer < 10:
            try: response = urllib2.urlopen(url)
            except:
                timer = timer + 1
            continue


        #
        # with open('htmlreader.txt', 'w') as f:
        #     for lines in response.read():
        #         write_data = f.writelines(lines)
        if response != None:
            soup = BeautifulSoup(response.read(), "html.parser")
            if soup.find("div", {"id": "nav-subnav"}) != None:
                if "data-category" in soup.find("div", {"id": "nav-subnav"}).attrs:
                    cat = soup.find("div", {"id": "nav-subnav"})["data-category"]
                    # ["data-category"]
                    result = 0
                    writer.writerow([row, cat])
                else:
                    print "no_data_category"
                    writer2.writerow([row])
            else:
                print "no_response"
                writer2.writerow([row])
        else:
            print "no_response"
            writer2.writerow([row])