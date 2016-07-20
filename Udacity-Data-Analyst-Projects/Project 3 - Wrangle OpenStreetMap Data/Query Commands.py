#!/usr/bin/env python
# -*- coding: utf-8 -*-

from pymongo import MongoClient

client = MongoClient()
db = client.udacity_database
cursor = db.udacity_database.count()
total_count = 0
unique_users = 0


find_unique_users = db.udacity_database.distinct("created.uid")

count_node = db.udacity_database.count({"type" : "node"})
count_way = db.udacity_database.count({
        "type" : "way"
    })
count_cafe =  db.udacity_database.count({"amenity" : "cafe"})

return_universities = db.udacity_database.find({"amenity" : "university"})
university_coord = {}

for document in return_universities:
    ref = []
    coord = []
    if "name" in document.keys() and "node_refs" in document.keys():
        ref = document["node_refs"]
        for item in ref:
            return_coord = db.udacity_database.find({"id" : item})
            for cord in return_coord:
                coord.append(cord["pos"])
        university_coord[document["name"]] = coord

print "Total Size in MegaBytes: "  + str(db.command("collstats", "udacity_database")["storageSize"]/1024/1024)
print "Total Number of Entries: " + str(cursor)
print "Total Unique Users: " + str(len(find_unique_users))
print "Total Number of Nodes: " + str(count_node)
print "Total Number of Ways: " + str(count_way)
print "Total Number of Cafes: " + str(count_cafe)
print university_coord["University College"]