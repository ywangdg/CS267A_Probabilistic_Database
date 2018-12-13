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

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def is_variable(var):
    if (len(var) == 1 and var.isalpha()) or (len(var) ==2 and var[0].isalpha() and var[1].isdigit()):
        return True
    return False


def cc_loop(variables, res):
    for i in xrange(len(res)):
        for index in res[i]:
            for j in xrange(i+1, len(res)):
                for index2 in res[j]:
                    if intersection(variables[index], variables[index2]) != []:
                        res[i] = res[i] + res[j]
                        res[i].sort()
                        res.remove(res[j])
                        return res
    return res

def connected_components(variables):
    res = list()
    for i in xrange(len(variables)):
        res.append([i])

    while(True):
        old_res = copy.deepcopy(res)
        res = cc_loop(variables, res)
        if res == old_res:
            break

    return res

# def connected_components_of_cnf(variables):
#     print variables
#     res = list()
#     visited = [0] * len(variables)
#     for i in xrange(len(variables)):
#         if not visited[i]:
#             cc = list()
#             cc.append(i)
#             for j in xrange(i+1, len(variables)):
#                 for c in cc:
#                     if intersection(variables[c], variables[j]) != []:
#                         visited[j] = 1
#                         cc.append(j)
#                         break
#             res.append(cc)
#     return res

def connected_components_of_cnf_unions(variables):
    print variables
    var_list = []
    for var in variables:
        var_list += var
    # print var_list
    # print [var[0] for var in variables]
    # print connected_components_of_cnf(var_list)
    return   connected_components_of_cnf([var[0] for var in variables])



def get_grounding_for_or(variables):
    return intersection_multiple_list([var[0] for var in variables])


def get_groupby_variables(separator, mapping):
    return  [[mapping[i][var] for var in separator] for i in mapping]


def split_by_connected_components(tables, variables, connected_components):
    new_queries = list()
    new_tables = list()
    new_vars = list()
    for i in xrange(len(connected_components)):
        new_tables.append([tables[0][j] for j in connected_components[i]])
        new_vars.append([variables[0][j] for j in connected_components[i]])
    assert(len(new_tables) == len(new_vars))
    for i in xrange(len(new_tables)):
        new_queries.append(Query([new_tables[i]], [new_vars[i]]))
    return new_queries


def split_by_connected_components_union_of_cnfs(tables, variables, connected_components):
    new_queries = list()
    new_tables = list()
    new_vars = list()
    for i in xrange(len(connected_components)):
        new_tables.append([tables[j] for j in connected_components[i]])
        new_vars.append([variables[j] for j in connected_components[i]])
    assert(len(new_tables) == len(new_vars))
    for i in xrange(len(new_tables)):
        new_queries.append(Query(new_tables[i], new_vars[i]))
    return new_queries
