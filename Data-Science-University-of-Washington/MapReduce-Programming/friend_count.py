__author__ = 'billsu'
__author__ = 'billsu'
import MapReduce

# Part 1
mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    personA = record[0]
    personB = record[1]
    mr.emit_intermediate(personA, 1)

# Part 3
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0;
    for v in list_of_values:
      total += 1
    mr.emit((key, total))

# Part 4
inputdata = open("data/friends.json")
mr.execute(inputdata, mapper, reducer)