__author__ = 'billsu'
import MapReduce
# Part 1
mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    matrix = record[0]
    i = record[1]
    j = record[2]
    value = record[3]
    if matrix == "a":
        for x in range(5):
            mr.emit_intermediate((i,x), (j, value))
    if matrix == "b":
        for x in range(5):
            mr.emit_intermediate((x,j), (i,value))
# Part 3
def reducer(key, list_of_values):
    sum = 0
    for x in range(5):
        multiple = 1
        counter = 0
        for list in list_of_values:
            if list[0] == x:
                counter += 1
        if (counter != 2):
            sum += 0
        else:
            for list in list_of_values:
                if list[0] == x:
                    multiple *= list[1]
        sum += multiple
    mr.emit((key[0], key[1], sum))


# Part 4
inputdata = open("data/matrix.json")
mr.execute(inputdata, mapper, reducer)
