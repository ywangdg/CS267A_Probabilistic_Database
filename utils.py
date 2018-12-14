from query_parser import *
import itertools
import copy

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def index_of_intersection(lst1, lst2):
    lst3 = [lst1.index(value) for value in lst1 if value in lst2]
    return lst3

def intersection_multiple_list(lst_of_list):
    result = lst_of_list[0]
    for lst in lst_of_list:
        result = intersection(result, lst)
    return result


def independent(table1, table2):
    if intersection(table1, table2) == []:
        return True
    return False

def completely_independent(table_list1, table_list2):
    for table1 in table_list1:
        for table2 in table_list2:
            if not independent(table1, table2):
                return False
    return True

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def is_variable(var):
    if (len(var) == 1 and var.isalpha()) or (len(var) ==2 and var[0].isalpha() and var[1].isdigit()):
        return True
    return False


def cc_loop(variables, res):
    for i in range(len(res)):
        for index in res[i]:
            for j in range(i+1, len(res)):
                for index2 in res[j]:
                    if intersection(variables[index], variables[index2]) != []:
                        res[i] = res[i] + res[j]
                        res[i].sort()
                        res.remove(res[j])
                        return res
    return res

def connected_components(variables):
    res = list()
    for i in range(len(variables)):
        res.append([i])

    while(True):
        old_res = copy.deepcopy(res)
        res = cc_loop(variables, res)
        if res == old_res:
            break

    return res

def connected_components_of_cnf_unions(variables):
    var_list = []
    for var in variables:
        var_list += var
    return   connected_components_of_cnf([var[0] for var in variables])

def get_grounding_for_or(variables):
    return intersection_multiple_list([var[0] for var in variables])


def get_groupby_variables(separator, mapping):
    return  [[mapping[i][var] for var in separator] for i in mapping]


def split_by_connected_components(tables, variables, connected_components):
    new_queries = list()
    new_tables = list()
    new_vars = list()
    for i in range(len(connected_components)):
        new_tables.append([tables[0][j] for j in connected_components[i]])
        new_vars.append([variables[0][j] for j in connected_components[i]])
    assert(len(new_tables) == len(new_vars))
    for i in range(len(new_tables)):
        new_queries.append(Query([new_tables[i]], [new_vars[i]]))
    return new_queries


def split_by_connected_components_union_of_cnfs(tables, variables, connected_components):
    new_queries = list()
    new_tables = list()
    new_vars = list()
    for i in range(len(connected_components)):
        new_tables.append([tables[j] for j in connected_components[i]])
        new_vars.append([variables[j] for j in connected_components[i]])
    assert(len(new_tables) == len(new_vars))
    for i in range(len(new_tables)):
        new_queries.append(Query(new_tables[i], new_vars[i]))
    return new_queries

def decompose_or(union_cnf_query):
    cnf_tables = [[table] for table in union_cnf_query.tables]
    cnf_variables = [[variables] for variables in union_cnf_query.variables]
    assert(len(cnf_tables) == len(cnf_variables))
    cnf_queries = list()
    for i in range(len(cnf_tables)):
        cnf_queries.append(Query(cnf_tables[i], cnf_variables[i]))
    return cnf_queries

def conjunction_of_cnf(cnf_queries):
    cnf_tables = list()
    cnf_variables = list()
    for query in cnf_queries:
        cnf_tables += query.tables[0]
        cnf_variables += query.variables[0]
    return Query([cnf_tables], [cnf_variables])

def union_of_cnf(cnf_queries):
    union_tables = [query.tables[0] for query in cnf_queries ]
    union_variables = [query.variables[0] for query in cnf_queries ]
    return Query(union_tables, union_variables)
