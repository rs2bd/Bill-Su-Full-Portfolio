__author__ = 'billsu'
import urllib2
import re
from bs4 import BeautifulSoup
import csv

#importing a dataset with three information: Reviewer Name, Reviewer ID, Reviewer Total Reviews
data = []
with open('amazon_no_access_result.csv', 'a') as csvfile:
    writer = csv.writer(csvfile, lineterminator='\n')
    with open("amazon_no_access.csv", "r") as readfile:
        reader = csv.reader(readfile)
        counter = 0
        for row in reader:
            counter = counter + 1
            print counter
            url = 'http://www.amazon.com/dp/' + row[0]
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
                cat = soup.find("div", {"id": "nav-subnav"})["data-category"]
                result = 0
                writer.writerow([row[0], cat])
        #
        # fieldnames = data[1].keys()
        # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # writer.writeheader()
        # for item in data:
        #     writer.writerow(item)

        # print a_string

        #1,3 + 4 + 2 + 4 + 2

        # #
        # - reviewer name (e.g., Ol' Dan "ExTexan")
        # - reviewer ID (e.g., A2EMQB1VX2YFW6)
        # - product (e.g., Hitachi 29-Piece High Speed Gold Oxide Metal Drill Bit Set With Green Case 728078G)
        # - price (e.g., $65.73)
        # - X of Y people find it helpful (store X and Y)
        # - star rating (e.g., 4) out of 5 stars
        # - review date (e.g., January 7, 2015)
        # - verified purchase (yes/no)
        # - review text
        # - calculated review order (oldest = 1, newest = 116 in this case)
        # - look up overall average star rating for that product (e.g., 3.3) of 5 stars
        #