import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    order_id = record[1]
    mr.emit_intermediate(order_id, record)

def reducer(key, list_of_records):
    order_record = []
    # is there a faster way for finding the order record without looping over everything twice? Pattern matching...
    for record in list_of_records:
        if record[0] == "order":
            order_record = record
    for record in list_of_records:
        if record[0] != "order":
            mr.emit(order_record + record)

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
