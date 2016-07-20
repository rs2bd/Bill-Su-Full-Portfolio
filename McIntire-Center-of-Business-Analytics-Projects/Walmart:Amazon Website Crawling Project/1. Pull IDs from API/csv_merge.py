import csv

for i in range(1,8):
    filename = "result_" + str(i) + ".csv"
    with open(filename, "r") as f:
        reader = csv.reader(f)
        with open("amazon_categories.csv", "a") as r:
            writer = csv.writer(r, lineterminator='\n')
            if i == 1:
                writer.writerow(["ID", "Category"])
            for row in reader:
                writer.writerow(row)