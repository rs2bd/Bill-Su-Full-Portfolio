__author__ = 'billsu'
import csv
from collections import defaultdict
import json
import re
filename = 'Hypothesis.csv'

def __unicode__(self):
    return '%s' % self.id

def data_cleaning(file):
    data = []

    with open(file, 'rU') as f:
        reader = csv.DictReader(f)
        for rows in reader:
            data.append(rows)

    #Cleaning of Result Section
    positive_dict = ["Positive", "positive", "Positive ", "positive ",  "Positve"]
    negative_dict = ["Negative", "negative", "Negative "]
    effect_dict = ["has effect", "Has effect", "Has another effect (u-shaped)",
                    "effect", "Effect", 'Has a relationship', "has a difference", "Has affect","Has a difference",
                   "Has an effect","Has Effect", "Has effect ", "Effect ", "Has effect ",]
    noeffect_dict = ["no effect", "No effect", "no relationship", "No relationship", "No relationship "]


    for item in data:
        if item['Relationship'] in positive_dict:
            item['Relationship'] = "Positive Effect"
        elif item['Relationship'] in negative_dict:
            item['Relationship'] = "Negative Effect"
        elif item['Relationship'] in effect_dict:
            item['Relationship'] = "Effect"
        elif item['Relationship'] in noeffect_dict:
            item['Relationship'] = "No Effect"
        else: item['Relationship'] = None

    #Cleaning of Type Section
        if item["Type"] == '0' or item["Type"] == "regular" or item["Type"] == "Regular":
            item["Type"] = "Regular"
        elif item["Type"] == '1' or item["Type"] == "Mediating" or item["Type"] == "mediating" or item["Type"] == "Mediator" \
                or item["Type"] == 'mediator':
            item["Type"] = "Mediator"
        elif item["Type"] == '2' or item["Type"] == "Moderating" or item["Type"] == "moderating" or item["Type"] == "Moderator" \
                or item["Type"] == "Moderate" or item["Type"] == "Mediated moderation" or item['Type'] == 'moderator'\
                or item["Type"] == "Moderating?":
            item["Type"] = "Moderator"
        else: item["Type"] = None

        if re.search(".*(0*.0*[1-9]).*",item["P-Value"]) == None:
            item["P-Value"] = None
        else: item["P-Value"] = re.search(".*(0*\.0*[1-9]).*",item["P-Value"]).group(1)


    #Cleaning of Mediator Section:
        if item["Mediator/Moderator"] == "NULL":
            item["Mediator/Moderator"] = None

    #Cleaning of p-value:
        if item["P-Value"] == "NULL":
            item["P-Value"] = None

        if item["Supported"] == "TRUE" or "Partial" or "TRUE - Partial":
            item["Supported"] = 1
        elif item["Supported"] == "FALSE":
            item["Supported"] = 0



    return data

Data = data_cleaning(filename)

#
#     # fieldnames = ["Source ID", "Hypothesis ID", "Relationship ID", "Type", "Independent", "Dependent", "Mediator/Moderator",
#     #                   "Supported", "P-Value", "Relationship", "Indep_Coord", "Dep_Coord", "Med_Coord", "Mod_Coord", "Mid_Node_Coord"
#     #                   , "Color"]
#     # # writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
#     # # writer.writeheader()
#     # #Where the fun stuff starts.
SID = set()
for item in Data:
    SID.add(item["Source ID"])
# nodes = []
# edges = []
mod = []
mod_list = []
med = []
med_list = []
inter = []
inter_list = []
indep = []
indep_list = []
dep = []
dep_list = []

for ID in SID:

    Source_ID = ID
    selected = []

    for items in Data:
        if items["Source ID"] == ID:
            selected.append(items)


    for item in selected:
        if item["Independent"] not in indep_list:
            indep_list.append(item["Independent"])

        if item["Dependent"] not in dep_list:
            dep_list.append(item["Dependent"])

        if item['Type'] == "Mediator":

            if item["Mediator/Moderator"] not in med_list:
                med_list.append(item["Mediator/Moderator"])

            if (item["Relationship ID"]) not in med_list:
                med_list.append("r" + item["Relationship ID"])

        elif item['Type'] == "Moderator":
            if item["Mediator/Moderator"] not in mod_list:
                mod_list.append(item["Mediator/Moderator"])

            if (item["Relationship ID"]) not in mod_list:
                mod_list.append("r" + item["Relationship ID"])


already = []
for item in mod_list:
    already.append(item)

for item in med_list:
    if item not in already:
        already.append(item)

for item in dep:
    if item not in already:
        already.append(item)

for item in indep:
    if item["id"] not in already:
        already.append(item)
pos = {}
for ID in SID:
    indep_counter = 0
    dep_counter = 0
    mod_counter = 0
    med_counter = 0
    indep_pos = 0
    dep_pos = 0
    mod_pos = 0
    med_pos = 0
    inter_pos = 0
    indep_y = []
    inter_y = []
    selected = []
    dep_y = []
    mod_y = []
    med_y = []
    inter_counter = 0

    for item in Data:
        if item["Source ID"] == ID:
            pos[item["Independent"]] = {"x": -300, "y": None}
            indep_counter = indep_counter + 1
            pos[item["Dependent"]] = {"x": 300, "y": None}
            dep_counter = dep_counter + 1
            if item["Type"] == "Moderator":
                pos[item["Mediator/Moderator"]] = {"x": -200, "y": None}
                mod_counter = mod_counter + 1
            if item["Type"] == "Mediator":
                pos[item["Mediator/Moderator"]] = {"x": 200, "y": None}
                med_counter = med_counter + 1

        for i in range(0,indep_counter):
            tier = 500/indep_counter
            indep_y.append(-250+i*tier)

        for i in range(0,dep_counter):

            tier = 500/dep_counter
            dep_y.append(-250+i*tier)

        if mod_counter!= 0:
            for i in range(0,mod_counter):
                tier = 500/mod_counter
                mod_y.append(-350+i*tier)


        if med_counter != 0:
            for i in range(0,med_counter):
                tier = 500/med_counter
                med_y.append(-350+i*tier)

    for item in Data:
        if item["Source ID"] == ID:
            if item["Source ID"] == ID:
                pos[item["Independent"]]["y"]  = indep_y[indep_pos]
                indep_pos = indep_pos + 1
                pos[item["Dependent"]]["y"] = dep_y[dep_pos]
                dep_pos = dep_pos + 1

                if item["Type"] == "Moderator":
                    if mod_counter != 0:
                        pos[item["Mediator/Moderator"]]["y"] = mod_y[mod_pos]
                        mod_pos = mod_pos + 1
                if item["Type"] == "Mediator":
                    if med_counter != 0:
                        pos[item["Mediator/Moderator"]]["y"] = med_y[med_pos]
                        med_pos = med_pos + 1
for item in Data:
    for var in pos:
        if item["Independent"] == var:
            item["IndPos"] = (pos[var]["x"], pos[var]["y"])
        elif item["Dependent"] == var:
            item["DepPos"] = (pos[var]["x"], pos[var]["y"])
        if item["Type"] != "Regular":
            if item["Mediator/Moderator"] == var:
                item["MidPos"] = (pos[var]["x"], pos[var]["y"])

with open("cleaning.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames = Data[1].keys())
    writer.writeheader()
    for item in Data:
        writer.writerow(item)
