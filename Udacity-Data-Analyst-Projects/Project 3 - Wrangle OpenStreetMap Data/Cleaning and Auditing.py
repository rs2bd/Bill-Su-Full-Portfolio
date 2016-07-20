__author__ = 'billsu'

from pymongo import MongoClient
import gridfs
import xml.etree.ElementTree as ET
import re
from collections import defaultdict

# Open Files and open MongoDB connections
f = open('/Users/billsu/Downloads/oxford_england.xml', 'r')
client = MongoClient()
db = client.udacity_database

#Initalizing Variables
counter = 0
cafe_counter = 0
shop_counter = 0
unique_users = set()
street_types = defaultdict(set)

#Keys for created
created_keys = ["version", "changeset", "timestamp", "user", "uid"]

#Initalize Variable for Auditing of Streets
expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road",
            "Trail", "Parkway", "Commons"]
keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}

#Update mapping and expected after auditing
mapping = { "St": "Street",
            "St.": "Street",
            "Rd.": "Road",
            "Rd" : "Road",
            "Ave" : "Avenue",
            "road": "Road",
            "Giles'": "Giles",
            "Way?" : "Way",
            "Way," : "Way",
            "road" : "Road",
            "way" : "Way"
            }
expected.append(["Way", "Hill", "Crescent", "Close"])


#Three Types of Anomoly to Look At
lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

#Reg.ex for street names
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


def update_name(name, mapping):
    splited = name.split(" ")
    if splited[-1] in mapping.keys():
        splited[-1] = mapping[splited[-1]]
        name = " ".join(splited)

    return name

for event, elem in ET.iterparse(f):

    #Initalize Variable for Node
    node = {}
    created = {}
    pos = []
    address = {}
    lat = 0
    lon = 0


    if event == "end":


        if elem.tag == "node" or elem.tag == "way":


            #enter type in node
            node["type"] = elem.tag


            firstdict = elem.attrib

            #node_refs entry
            node_refs = []
            if elem.tag == "way":
                for child in elem:
                    if child.tag == "nd":
                        node_refs.append(child.attrib["ref"])
            if node_refs != []:
                node['node_refs'] = node_refs

            #Dig Deeper into Childs, see if anything can be added
            for child in elem:
                seconddict = child.attrib
                if "k" in child.attrib.keys() and "v" in child.attrib.keys():

                    #skip if key have probs
                    if re.match(problemchars, child.attrib["k"]):
                        continue

                    #append address only when in specific format, else just append
                    else:
                        splited = seconddict["k"].split(":")
                        if splited[0] == "addr" and len(splited) > 2:
                            continue
                        elif splited[0] == "addr" and len(splited) == 2:
                            word = seconddict["v"]
                            if re.search("[^a-zA-Z0-9]$", seconddict["v"]):
                                word = re.search("[^a-z]$", seconddict["v"]).group(0)
                            address[splited[1]] = update_name(word,mapping)
                        else: node[seconddict["k"]] = seconddict["v"]

            #add address
            if address != None and address != {}:
                node["address"] = address

            #add created key field and manipulate lat and long
            for key in firstdict:
                if key in created_keys:
                    created[key] = firstdict[key]
                elif (key == "lat"):
                    lat = float(firstdict[key])
                elif (key == "lon"):
                    lon = float(firstdict[key])
                else: node[key] = firstdict[key]

            pos.append(lat)
            pos.append(lon)
            if created != None:
                node["created"] = created
            if pos != None:
                node["pos"] = pos



        #count node and unique users
        if elem.tag == "node":
            counter = counter + 1
            if "uid" in elem.attrib.keys():
                unique_users.add(elem.attrib["uid"])


        #audit addresses
        if elem.tag == "tag":
            if re.search(lower,elem.attrib["k"]) != None:
                keys["lower"] = keys["lower"]+1
            elif re.search(lower_colon,elem.attrib["k"]) != None:
                keys["lower_colon"] = keys["lower_colon"] + 1
            elif re.search(problemchars,elem.attrib["k"]) != None:
                keys["problemchars"] = keys["problemchars"]+1
            else: keys["other"] = keys["other"]+1

    #Audit Postal Address and address, this is done post-conversion due to simplicity
        for key in node:
            if key == "postal_code":
                new = node["postal_code"].split(" ")[0]
                node["postal_code"] = new
                print node["postal_code"]
            # if key == "address":
            #     for item in node["address"]:
            #         temp = node["address"][item]
            #         m = re.search(street_type_re, temp)
            #         if m:
            #             street_type = m.group()
            #             if street_type not in expected:
            #                 street_types[street_type].add(temp)

    db.udacity_database.insert_one(node)

#Print out street_types after repairation.
# output = []
# for keys in street_types:
#     if len(street_types[keys]) >= 2:
#         output.append(keys)
#         print street_types[keys]
# print output

        #Insert items into MongoDB






