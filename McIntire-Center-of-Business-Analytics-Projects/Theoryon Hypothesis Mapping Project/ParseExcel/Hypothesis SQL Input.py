__author__ = 'billsu'
import openpyxl as xl
import re
import csv
wb = xl.load_workbook(filename  = "Annotation Spreadsheet.xlsx")
sheet_ranges = wb['Hypothesis']


Data = []
for i in range(3, 5461):
    if sheet_ranges['B' + str(i)].value != None and sheet_ranges['I' + str(i)].value != None and sheet_ranges['J' + str(i)].value != 0:
        # Let's first lock in source IDs, which is column B
        Source_ID = sheet_ranges['B' + str(i)].value
        if Source_ID == None:
            for j in range(1,30):
                Source_ID = sheet_ranges['B' + str(i-j)].value
                if Source_ID != None:
                    break


        # Now Hypothesis ID
        H_ID = sheet_ranges['I' + str(i)].value
        if H_ID == None or re.match(".*[0-9].*", str(H_ID)) == None:
            for j in range(1,100):
                if sheet_ranges['I' + str(i-j)].value != None and re.match(".*[0-9].*", str(sheet_ranges['I' + str(i-j)].value)) != None:
                    H_ID = sheet_ranges['I' + str(i-j)].value
                    break
        H_ID = str(Source_ID) + "-" + re.match(".*([0-9]+[a-zA-Z]?).*", str(H_ID)).group(1).lower()




        # Now Text of Hypothesis
        H = sheet_ranges['J' + str(i)].value
        if H == None:
            for j in range(1,60):
                H = sheet_ranges['J' + str(i-j)].value
                if H != None:
                    break
        Annotation = []
        for z in range(0,5):
            for j in ["K", "L", "M", "N", "O", "P", "Q"]:
                if sheet_ranges[j + str(i+z)].value != None:
                    Annotation.append(sheet_ranges[j + str(i+z)].value)
                else:
                    break
                    break
        # Now Annotation of Hypothesis

        Data.append({
            "SourceId" : Source_ID,
            "HypothesisId": H_ID,
            "Text": H,
            "Annotation": Annotation

        }

    )

final = []
for item in Data:
    if item["Annotation"] != []:
        final.append(item)

keys = final[1].keys()
for item in final:
    item["Text"] = item["Text"].encode("UTF-8")
with open('HypothesisContent.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, keys)
    w.writeheader()
    for item in final:
        w.writerow(item)