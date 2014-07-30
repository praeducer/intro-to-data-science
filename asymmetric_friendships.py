import MapReduce
import sys
from collections import Counter

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

def mapper(persons):
    # key: document identifier
    # value: document contents
    person = persons[0]
    friend = persons[1]
    mr.emit_intermediate(person, friend)
    mr.emit_intermediate(friend, person)

def reducer(person, list_of_friends):
    count_of_friends_dict = Counter(list_of_friends)
    for friend in list_of_friends:
        if count_of_friends_dict[friend] < 2:
            mr.emit((person, friend))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
