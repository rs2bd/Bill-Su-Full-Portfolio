import csv

with open("unique_amazon.csv", "r") as f:
    reader = csv.reader(f)
    with open("amazon_invalid.csv", "w") as r:
        writer_invalid = csv.writer(r, lineterminator='\n')
        with open("amazon_error.csv", "w") as r:
            writer_error = csv.writer(r, lineterminator='\n')
            with open("amazon_correct.csv", "w") as r:
                writer_correct = csv.writer(r, lineterminator='\n')
                with open("amazon_no_access.csv", "w") as r:
                    writer_no_access = csv.writer(r, lineterminator='\n')
                    for row in reader:
                        if row[1] == "invalid":
                            writer_invalid.writerow(row)
                        elif row[1] == "error":
                            writer_error.writerow(row)
                        elif row[1] == "no access":
                            writer_no_access.writerow(row)
                        else:
                            writer_correct.writerow(row)