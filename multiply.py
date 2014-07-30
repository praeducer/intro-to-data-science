import MapReduce
import sys
import pprint

mr = MapReduce.MapReduce()

# =============================
# Do not modify above this line

max_dimension = 5;

def mapper(record):
    # group Matrix A records together by row
    if (record[0] == "a"):
        key = record[1]
        mr.emit_intermediate(key, record)
    # give each row in Matrix A access to every record from Matrix B
    if (record[0] == "b"):
        for key in range(0, max_dimension):
            mr.emit_intermediate(key, record)

def reducer(A_row, list_of_records):
    A_dict = {}
    B_dict = {}
    # separate records by matrices
    for record in list_of_records:
        # index values from Matrix A by col since we already know the row
        if (record[0] == "a"):
            A_dict[record[2]] = record[3]
        # index values from Matrix B by row and column
        if (record[0] == "b"):
            B_dict[str(record[1]) + "," + str(record[2])] = record[3]
    # go through Matrix B column by column
    for B_col in range(0, max_dimension):
        dot_product = 0
        # go through every column of the single row we have from Matrix A
        for A_col in range(0, max_dimension):
            # for clarity's sake
            B_row = A_col
            B_key = str(B_row) + "," + str(B_col)
            # sparse matrix so default to 0
            A = 0
            B = 0
            if A_col in A_dict:
                A = A_dict[A_col]
            if B_key in B_dict:
                B = B_dict[B_key]
            dot_product += (A * B)
        mr.emit((A_row, B_col, dot_product))

# Do not modify below this line
# =============================
if __name__ == '__main__':
    inputdata = open(sys.argv[1])
    mr.execute(inputdata, mapper, reducer)
