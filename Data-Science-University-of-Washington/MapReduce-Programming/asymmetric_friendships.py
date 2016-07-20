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
    total = personA + personB
    mr.emit_intermediate(personA, record)

# Part 3
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    for lista in list_of_values:
        if (lista[1] not in mr.intermediate):
            mr.emit(lista)
            mr.emit((lista[1], lista[0]))
        else:
            if set(lista) not in mr.intermediate [lista[1]]:
                    mr.emit(lista)
                    mr.emit((lista[1], lista[0]))
# Part 4
inputdata = open("data/friends.json")
mr.execute(inputdata, mapper, reducer)