import getopt
import sys

import numpy as np
import pandas as pd
from query_parser import *
from lifted_algorithm import *

database = dict()

def read_table(table):
    file = open(table, "r")
    lines = file.readlines()
    lines = [line.replace("\n", "") for line in lines]
    lines = [line.strip() for line in lines]
    lines = [line.split(',') for line in lines]
    table_name = lines[0][0]
    data = np.array(lines[1:])
    columns = []
    for i in range(data.shape[1] - 1):
        columns.append('Var' + str(i+1))
    columns.append('Prob')
    df = pd.DataFrame(data = data, columns = columns, dtype = float)
    database[table_name] = df


def main(argv):
    queries = []
    tables = []
    try:
        opts, args = getopt.getopt(argv,"hq:t:",["query=","table="])
    except getopt.GetoptError:
        print ('qeval.py -q <query files> -t <table files>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print ('qeval.py -q <query files> -t <table files>')
            sys.exit()
        elif opt in ("-q", "--query"):
            queries.append(arg)
        elif opt in ("-t", "--table"):
            tables.append(arg)
    print ('Input query file is', queries)
    print ('Input table file is', tables)
    for table in tables:
        read_table(table)

    query_list = convert_query_to_class(queries)

    #check single ground atom
    res = [0] * len(query_list)
    print ("-------")
    for query in query_list:
        #To be done:
        print (lifted_algorithm(database, query))



if __name__ == "__main__":
    main(sys.argv[1:])
