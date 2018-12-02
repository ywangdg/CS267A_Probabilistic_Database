import re

class Atom:
    def __init__(self, table, var):
        self.table = table
        self.var = var

class Query:
    def __init__(self,cnf_list):
        self.cnf_list = cnf_list
        self.tables = list()
        self.variables = list()
        for cnf in cnf_list:
            table_list = list()
            var_list = list()
            for atom in cnf:
                table_list.append(atom.table)
                var_list.append(atom.var)
            self.tables.append(table_list)
            self.variables.append(var_list)

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
        query_list.append(Query(cnf_list))

    return query_list
