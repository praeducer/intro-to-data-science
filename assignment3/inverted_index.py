import MapReduce
import sys

mr = MapReduce.MapReduce()

def mapper(record):
    # doc_id: document identifier
    # text: document contents
    doc_id = record[0]
    text = record[1]
    words = text.split()
    for word in words:
        mr.emit_intermediate(word, doc_id)

def reducer(key, list_of_doc_ids):
    # key: word
    # value: list of document identifiers
    mr.emit((key, list(set(list_of_doc_ids))))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
