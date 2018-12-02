import getopt
import sys
import re
import numpy as np
import pandas as pd
from query import Atom
import inspect

database = dict()

def parse_query(query):
    file = open(query, "r")
    lines = file.readlines()
    sentence = lines[0]
    return sentence.strip().split("||")

def read_table(table):
    file = open(table, "r")
    lines = file.readlines()
    lines = [line.replace("\n", "") for line in lines]
    lines = [line.strip() for line in lines]
    lines = [line.split(',') for line in lines]
    table_name = lines[0][0]
    data = np.array(lines[1:])
    columns = []
    for i in xrange(data.shape[1] - 1):
        columns.append('Var' + str(i+1))
    columns.append('Prob')
    df = pd.DataFrame(data = data, columns = columns)
    database[table_name] = df


def main(argv):
    queries = []
    tables = []
    try:
        opts, args = getopt.getopt(argv,"hq:t:",["query=","table="])
    except getopt.GetoptError:
        print 'qeval.py -q <query files> -t <table files>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print 'qeval.py -q <query files> -t <table files>'
            sys.exit()
        elif opt in ("-q", "--query"):
            queries.append(arg)
        elif opt in ("-t", "--table"):
            tables.append(arg)
    print 'Input query file is', queries
    print 'Input table file is', tables
    for table in tables:
        read_table(table)

    query_list = list()
    for query in queries:
        query_raw = parse_query(query)
        cnf_list = list()
        for cnf in query_raw:
            atom_raw = cnf.strip().split(")")
            atom_list = list()
            for atom in atom_raw:
                res = re.split("\(|,| ", atom)
                res = filter(None, res)
                if res:
                    atom_list.append(Atom(res[0], res[1:]))
            cnf_list.append(atom_list)
        query_list.append(cnf_list)









if __name__ == "__main__":
   main(sys.argv[1:])
