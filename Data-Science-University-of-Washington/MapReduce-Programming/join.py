__author__ = 'billsu'
import MapReduce

# Part 1
mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    key = record[1]
    value = record
    mr.emit_intermediate(key, value)

# Part 3
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    order = []
    item = []
    for list in list_of_values:
        if (list[0]== "line_item"):
            item.append(list)
        elif (list[0] == "order"):
            order.append(list)

    for list_o in order:
        for list_i in item:
            overall = list_o + list_i
            mr.emit(overall)


# Part 4
inputdata = open("data/records.json")
mr.execute(inputdata, mapper, reducer)