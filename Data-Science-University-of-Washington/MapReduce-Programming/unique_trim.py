__author__ = 'billsu'
import MapReduce
# Part 1
mr = MapReduce.MapReduce()

# Part 2
def mapper(record):
    # key: document identifier
    # value: document contents
    seq_id = record[0]
    nuc = record[1]
    tirmed = nuc[:len(nuc)-10]
    mr.emit_intermediate(tirmed, 1)

# Part 3
def reducer(key, list_of_values):
    # key: word
    # value: list of occurrence counts
    total = 0;
    for v in list_of_values:
      total += 1
    if v < 2:
        mr.emit(key)

# Part 4
inputdata = open("data/dna.json")
mr.execute(inputdata, mapper, reducer)