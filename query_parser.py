import re


class Query:
    def __init__(self,tables, variables):
        self.tables = tables
        self.variables = variables
        # Create a list of mappings for each clause.
        # Each mapping is of the form:
        # {
        #     table_name : {
        #         var_name : column_name
        #     }
        # }
        # table_name is the name of the table in our database.
        # var_name is the name of the variable in our query (self.variables)
        # column_name is the column name that the variable refers to.
        self.variable_column_mapping_list = []
        for clause_num in range(len(self.tables)):
            table_to_mapping = {}
            for table_num in range(len(self.tables[clause_num])):
                table_name = self.tables[clause_num][table_num]
                variable_to_column_mapping = {}
                for variable_num in range(len(self.variables[clause_num][table_num])):
                    variable_name = self.variables[clause_num][table_num][variable_num]
                    variable_to_column_mapping[variable_name] = "var{}".format(variable_num + 1)
                table_to_mapping[table_name] = variable_to_column_mapping
            self.variable_column_mapping_list.append(table_to_mapping)

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
