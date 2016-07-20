import csv
categories = []
with open("amazon_no_access_result.csv", "r") as f:
    reader = csv.reader(f)
    with open("amazon_category_crawl.csv", "w") as r:
        writer_category = csv.writer(r, lineterminator='\n')
        for row in reader:
            if row[1] not in categories:
                categories.append(row[1])

        for item in categories:
            writer_category.writerow([item])