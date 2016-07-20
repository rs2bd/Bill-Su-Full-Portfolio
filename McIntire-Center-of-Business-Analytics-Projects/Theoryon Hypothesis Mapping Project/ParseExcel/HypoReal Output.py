__author__ = 'billsu'
import openpyxl as xl
import re
import csv
wb = xl.load_workbook(filename  = "Annotation Spreadsheet.xlsx")
sheet_ranges = wb['Hypothesis']


Data = []
id_counter = 1
for i in range(3, 5461):
     if sheet_ranges['V' + str(i)].value != None and sheet_ranges['U' + str(i)].value != None and sheet_ranges['W' + str(i)].value != 0:
        # Let's first lock in source IDs, which is column B
        Source_ID = sheet_ranges['B' + str(i)].value
        if Source_ID == None:
            for j in range(1,30):
                Source_ID = sheet_ranges['B' + str(i-j)].value
                if Source_ID != None:
                    break


        H_ID = sheet_ranges['I' + str(i)].value
        if H_ID == None or re.match(".*[0-9].*", str(H_ID)) == None:
            for j in range(1,100):
                if sheet_ranges['I' + str(i-j)].value != None and re.match(".*[0-9].*", str(sheet_ranges['I' + str(i-j)].value)) != None:
                    H_ID = sheet_ranges['I' + str(i-j)].value
                    break
        H_ID = str(Source_ID) + "-" + re.match(".*([0-9]+[a-zA-Z]?).*", str(H_ID)).group(1).lower()


        Type = sheet_ranges['U' + str(i)].value
        Indep = sheet_ranges['V' + str(i)].value
        Mod = sheet_ranges['W' + str(i)].value
        Dep = sheet_ranges['X' + str(i)].value
        Supported = sheet_ranges['Y' + str(i)].value
        P_Value = sheet_ranges['Z' + str(i)].value
        Relationship = sheet_ranges['AA' + str(i)].value
        ID = id_counter
        id_counter = id_counter + 1
        if re.search("\d+", str(Indep)) == None:
            continue
        Data.append({
            "Source ID" : Source_ID,
            "Hypothesis ID": H_ID,
            "Type": Type,
            "Independent": Indep,
            "Mediator/Moderator" : Mod,
            "Dependent": Dep,
            "Supported": Supported,
            "P-Value": P_Value,
            "Relationship": Relationship,
            "Relationship ID": ID


        })
keys = Data[1].keys()

with open('Hypothesis.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, keys)
    w.writeheader()
    for item in Data:
        w.writerow(item)