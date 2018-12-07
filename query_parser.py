import re


class Query:
    def __init__(self,tables, variables):
        self.tables = tables
        self.variables = variables

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
        full_table_list = list()
        full_var_list = list()
        for cnf in query_raw:
            atom_raw = cnf.strip().split(")")
            table_list = list()
            var_list = list()
            for atom in atom_raw:
                res = re.split("\(|,| ", atom)
                res = filter(None, res)
                if res:
                    table_list.append(res[0])
                    var_list.append(res[1:])
            full_table_list.append(table_list)
            full_var_list.append(var_list)

        query_list.append(Query(full_table_list, full_var_list))

    return query_list
