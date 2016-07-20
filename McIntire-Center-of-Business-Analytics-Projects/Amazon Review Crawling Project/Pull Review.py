__author__ = 'billsu'
import urllib2
import re
from bs4 import BeautifulSoup
import csv
people = []
with open('author_50_100.csv', 'r') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        people.append(row)
#importing a dataset with three information: Reviewer Name, Reviewer ID, Reviewer Total Reviews
data = []
with open('reviews_50_100.csv', 'w') as csvfile:
    fieldnames = ['Product', 'Product Stars', 'Author', 'Text', 'Price', 'Review Stars', 'Author ID', 'Date', 'Title', 'Verified_Purchase', 'Helpfulness Total', 'Helpfulness', "Review Ranking"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for a in people:
        counter = int(a["Total Reviews"])
        author = a["Author"]
        author_id = a["Author ID"]
        page = int(a["Total Reviews"])/10
        for b in range(1,page):
            url = 'http://www.amazon.com/gp/cdp/member-reviews/' + author_id + "?sort_by=MostRecentReview&page=" + str(b)
            response = None
            timer = 0

            while response == None and timer < 10:
                try: response = urllib2.urlopen(url)
                except:
                    timer = timer + 1
                    continue
                if timer > 4:
                    print "Time Time Is " + str(timer)

            #
            # with open('htmlreader.txt', 'w') as f:
            #     for lines in response.read():
            #         write_data = f.writelines(lines)
            entry = {}
            entry["Author"] = author
            entry["Author ID"] = author_id

            soup = BeautifulSoup(response.read(), "html.parser")
            try: block = soup.find_all("table", border = "0", cellpadding = "0", cellspacing = "0", width = "100%")[2]
            except: print soup.find_all("table", border = "0", cellpadding = "0", cellspacing = "0", width = "100%")[1]

            # print len(block.contents)
            x = 1
            y = 3
            #
            while y < len(block.contents):
                a_string = str(block.contents[x])
                b_string = str(block.contents[y])
                x = x+6
                y = y+6

                # Star Rating from Main Product Page
                entry["Review Ranking"] = counter
                counter = counter - 1

                try:
                    url_p = re.search("<a href=\"(.+)\">", a_string).group(1)
                    timer_p = 0
                    response_p = None
                    while response_p == None and timer_p < 10:
                        try: response_p = urllib2.urlopen(url_p)
                        except:
                            timer_p = timer_p + 1
                            continue
                    entry["Product Stars"] = re.search("title=\"(.+) out of (.+) stars", response_p.read()).group(1)

                except:
                    entry["Product Stars"] = "N/A"

                # Product
                try: entry["Product"] = re.search("<a href=.+><img alt=[\"\'](.+?)[\"\'] b.+?<\/a>", a_string).group(1)
                except: entry["Product"] = "N/A"

                # Price
                if re.search("Price:<\/span> \$(.+)<\/b>", a_string) != None:
                    entry["Price"] = re.search("Price:<\/span> \$(.+)<\/b>", a_string).group(1)

                # Helpfulness
                if re.search("(\d) of (\d) people found the following review helpful", b_string) != None:
                    entry["Helpfulness"] = re.search("(\d) of (\d) people found the following review helpful", b_string).group(1)
                    entry["Helpfulness Total"] = re.search("(\d) of (\d) people found the following review helpful", b_string).group(2)

                # Stars
                entry["Review Stars"] = re.search("title=\"(.+) out of (.+) stars", b_string).group(1)

                # Verified Purchase
                if re.search("Verified Purchase", b_string):
                    entry["Verified_Purchase"] = "Yes"

                # Review Title
                entry["Title"] = re.search("<b>(.+)<\/b>, <nobr>(.+)<\/nobr>", b_string).group(1)

                # Review Date
                entry["Date"] = re.search("<b>(.+)<\/b>, <nobr>(.+)<\/nobr>", b_string).group(2)

                # Review Text
                if re.search("<div class=\"reviewText\">(.+)<\/div>", b_string) != None:
                    entry["Text"] = re.search("<div class=\"reviewText\">(.+)<\/div>", b_string).group(1)
                elif re.search("<span class=\"tiny\">(.+)<\/div>", b_string) != None:
                    entry["Text"] = re.search("<span class=\"tiny\">(.+)<\/div>", b_string).group(1)
                # for i in range(0,20):
                #     a_string = str(block.contents[i])
                #     try: re.search("Price:<\/span> \$(.+)<\/b>", a_string).group(1)
                #     except: print i

                writer.writerow(entry)