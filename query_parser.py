import re

class Atom:
    def __init__(self, table, var):
        self.table = table
        self.var = var

def parse_query(query):
    file = open(query, "r")
    lines = file.readlines()
    sentence = lines[0]
    return sentence.strip().split("||")

def convert_query_to_class(queries):
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

    return query_list
