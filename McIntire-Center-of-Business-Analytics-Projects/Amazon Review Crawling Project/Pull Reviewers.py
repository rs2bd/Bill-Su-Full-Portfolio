__author__ = 'billsu'
import urllib2
import re
import csv
from bs4 import BeautifulSoup

with open('authors.csv', 'w') as csvfile:
    fieldnames = ['Ranking', 'Percent Helpful', 'Author', 'Total Reviews', 'Author ID', 'Helpful Votes']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(1,1000):
        page = i
        response = None
        counter = 0
        while response == None and counter < 10:
            try: response = urllib2.urlopen("http://www.amazon.com/review/top-reviewers/ref=cm_cr_tr_link_3?ie=UTF8&page=" + str(page))
            except: counter = counter + 1
        soup = BeautifulSoup(response.read(), "html.parser")
        data = []
        for i in range((page-1) * 10 + 1, (page)*10 + 1):
            entry = {}
            id = "reviewer" + str(i)
            entry["Ranking"] = i
            try: block = soup.find_all("tr", id = id)[0]
            except: continue
            entry["Author ID"] = block.find_all("td")[1].contents[3]['name'].strip().encode('ascii', 'ignore').decode('ascii')
            entry["Author"] = block.find_all("td")[2].contents[1].contents[0].contents[0].strip().encode('ascii', 'ignore').decode('ascii')
            entry["Total Reviews"] = int(block.find_all("td")[3].contents[0].strip().replace(",", ""))
            entry["Helpful Votes"] = int(block.find_all("td")[4].contents[0].strip().replace(",", ""))
            entry["Percent Helpful"] = float(block.find_all("td")[5].contents[0].strip().replace("%", ""))/100
            writer.writerow(entry)

