__author__ = 'billsu'
__author__ = 'billsu'
import openpyxl as xl
import csv
import re
wb = xl.load_workbook(filename  = "Annotation Spreadsheet.xlsx")
sheet_ranges = wb['Hypothesis']


Data = []
id_counter = 1
Instance_set = set()
for i in range(3, 5461):
     if sheet_ranges['R' + str(i)].value != None and sheet_ranges['S' + str(i)].value != None and sheet_ranges['T' + str(i)].value != 0:
        # Let's first lock in source IDs, which is column B
        Source_ID = sheet_ranges['B' + str(i)].value
        if Source_ID == None:
            for j in range(1,30):
                Source_ID = sheet_ranges['B' + str(i-j)].value
                if Source_ID != None:
                    break


        V_ID = sheet_ranges['R' + str(i)].value
        V_Instance = sheet_ranges['T' + str(i)].value.encode("UTF-8")
        Instance_set.add(V_Instance)
        ID = id_counter
        id_counter = id_counter + 1

        Data.append({
            "SourceId" : Source_ID,
            "VariableId": V_ID,
            "NLPVariableName": V_Instance
        })
instances = list(Instance_set)
for item in Data:
    for i in range(0, len(instances)):
        if item["NLPVariableName"] == instances[i]:
            item["NLPVariableId"] = i

keys = Data[1].keys()

with open('NLP.csv', 'wb') as f:  # Just use 'w' mode in 3.x
    w = csv.DictWriter(f, keys)
    w.writeheader()
    for item in Data:
        w.writerow(item)