from query_parser import *
import pandas as pd
import sys
import numpy as np
import query
import copy

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

def index_of_intersection(lst1, lst2):
    lst3 = [lst1.index(value) for value in lst1 if value in lst2]
    return lst3

def union(a, b):
    """ return the union of two lists """
    return list(set(a) | set(b))

def is_variable(var):
    if (len(var) == 1 and var.isalpha()) or (len(var) ==2 and var[0].isalpha() and var[1].isdigit()):
        return True
    return False

def independent(table1, table2):
    if intersection(table1, table2) == []:
        return True
    return False

def connected_components(variables):
    res = list()
    visited = [0] * len(variables)
    for i in xrange(len(variables)):
        if not visited[i]:
            cc = list()
            cc.append(i)
            for j in xrange(i+1, len(variables)):
                for c in cc:
                    if intersection(variables[c], variables[j]) != []:
                        visited[j] = 1
                        cc.append(j)
                        break
            res.append(cc)
    return res

def get_seperator(variables):
    sets = iter(map(set, variables))
    result = sets.next()
    for s in sets:
        result = result.intersection(s)
    return list(result)

def get_grounding_for_or(variables):
    return get_seperator([var[0] for var in variables])

# When simplify is called, we know we have a disjunction in our query with a shared table such as:
# [T(x1),Q(x1,y1)]||[S(x2),Q(x2,y2)]
# Let query_1 = [T(x1),Q(x1,y1)] and query_2 = [S(x2),Q(x2,y2)] and query_3 = query_1 * query_2
# We perform inclusion exclusion and get query_1 + query_2 - query_3
# query_1 and query_2 are easy to compute with a call to get_probability.
# query_3 = T(x1),Q(x1,y1),S(x2),Q(x2,y2), which is solved with a recurive call to lifted_algorithm.
def simplify_table_intersect(database, query):
    table_intersection =  intersection(query.tables[0], query.tables[1])[0]
    seperator_var = [var for var in query.variable_column_mapping_list[0][table_intersection].keys()]
    seperator_query = Query([[table_intersection]], [[seperator_var]])

    query_tables = copy.deepcopy(query.tables)

    for cnf_tables in query_tables:
        cnf_tables.remove(table_intersection)

    rest_query_tables = query_tables

    rest_variable_index_list = list()
    for i in xrange(len(query.variables)):
        cnf_intersection_index_list = list()
        for table in query.tables[i]:
            if table != table_intersection:
                intersect_index = index_of_intersection(query.variable_column_mapping_list[i][table_intersection].keys(), query.variable_column_mapping_list[i][table].keys())
                cnf_intersection_index_list.append(intersect_index)
        rest_variable_index_list.append(cnf_intersection_index_list)


    rest_variable_list = list()
    for i in xrange(len(rest_variable_index_list)):
        rest_variable_list.append([[seperator_var[index] for index in index_list]  for index_list in rest_variable_index_list[i]])

    rest_query = Query(rest_query_tables, rest_variable_list)
    print seperator_query.tables, seperator_query.variables
    print rest_query.tables, rest_query.variables


    # return lifted_algorithm(database, query_1) + lifted_algorithm(database, query_1) - lifted_algorithm(database, query_3)

def get_groupby_variables(separator, mapping):
    return  [[mapping[i][var] for var in separator] for i in mapping]


def get_probability(database, CNF_Query):
    tables = CNF_Query.tables
    variables = CNF_Query.variables
    mapping = CNF_Query.variable_column_mapping_list

    # Base Case
    if len(tables[0])== 1:
        name = tables[0][0]
        database[name]['NegProb'] = (1 - database[name]['Prob'])
        database['Rprod'] =  database[name].groupby('Var1').prod()
        database['Rprod']['Prob'] =  1-database['Rprod']['NegProb']
        result = 1 - (1 - database['Rprod']['Prob']).prod()
        return result

    else:
        separator = get_seperator(variables[0])
        if separator == []:
            print "Not liftable"
            sys.exit(0)
        else:
            groupby_value_list = get_groupby_variables(separator, mapping[0])
            print mapping
            print groupby_value_list
            for i in xrange(len(tables[0])):
                name = tables[0][i]
                print name
                database[name]["NegProb"]= (1-database[name]["Prob"])
                database[name]=database[name].groupby(groupby_value_list[i][0]).prod()
                database[name].index.name = 'Var1'
                database[name]["Prob"]= (1-database[name]["NegProb"])

            data_frames = [database[tables[0][i]][['Prob']].add_suffix(str(i)) for i in xrange(len(tables[0])) ]
            print data_frames

            result = reduce(lambda  left,right: pd.merge(left,right,on=['Var1'],   how='inner'), data_frames)
            result["Total_Prob"]=1
            for column in result:
                if ('Var' not in result[column].name and result[column].name!='Total_Prob'):
                    #print(result[column])
                    result["Total_Prob"]=result["Total_Prob"]*result[column]

            solution=1-(1-(result["Total_Prob"])).prod()
            return solution

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

def union_of_cnf(cnf_queries):
    union_tables = [query.tables[0] for query in cnf_queries ]
    union_variables = [query.variables[0] for query in cnf_queries ]
    return Query(union_tables, union_variables)


def decompose_or(union_cnf_query):
    cnf_tables = [[table] for table in union_cnf_query.tables]
    cnf_variables = [[variables] for variables in union_cnf_query.variables]
    assert(len(cnf_tables) == len(cnf_variables))
    cnf_queries = list()
    for i in xrange(len(cnf_tables)):
        cnf_queries.append(Query(cnf_tables[i], cnf_variables[i]))
    return cnf_queries

def conjunction_of_cnf(cnf_queries):
    cnf_tables = list()
    cnf_variables = list()
    for query in cnf_queries:
        cnf_tables += query.tables[0]
        cnf_variables += query.variables[0]
    return Query([cnf_tables], [cnf_variables])

def px_or_qx(database, query):

#     orfunct=(1-(1-df_final["Prob_x"])*(1-df_final["Prob_y"])) #replace this with table 1, table 2
#     xyfunct=(1-(df_final["NegProb"])) #replace this with prob(r)
# #.prod()
#     solution=1-(1-orfunct*xyfunct).vprod()
#     print(orfunct,xyfunct,solution)
    tables = query.tables
    print tables
    variables = query.variables
    mapping = query.variable_column_mapping_list
    grounding = get_grounding_for_or(variables)

    grounding_var_list = list()
    for i in xrange(len(mapping)):
        grounding_var_list.append([mapping[i][key][grounding[0]] for key in mapping[i].keys()])

    print grounding_var_list

    for i in xrange(len(tables)):
        for j in  xrange(len(tables[i])):
            table = tables[i][j]
            database[table]["NegProb"]= (1-database[table]["Prob"])
            #
            database[table]=database[table].groupby(grounding_var_list[i][j]).prod()
            database[table].index.name = 'Var1'
            database[table]["Prob"]= (1-database[table]["NegProb"])

    data_frames = [database[tables[i][j]][['Prob']].add_suffix(str(tables[i][j])) for j in xrange(len(tables[i])) for i in xrange(len(tables)) ]
    print data_frames
    result = reduce(lambda  left,right: pd.merge(left,right,on=['Var1'],   how='outer'), data_frames)
    result["Total_Prob"]=1
    print result
    orfunct=(1-(1-result["ProbP"])*(1-result["ProbQ"]))
    print 1-(1-orfunct).prod()

def lifted_algorithm(database, query):
    tables = query.tables
    variables = query.variables
    #To be done
    if len(variables) > 1:
        # Special case for now when we have 2 clauses
        if len(variables) == 2:
            #case 1:
            cnf_queries = decompose_or(query)
            query1 = cnf_queries[0]
            query2 = cnf_queries[1]
            table_intersection =  intersection(query1.tables[0], query2.tables[0])
            variable_intersection = intersection(query1.variables[0][0], query2.variables[0][0])
            if table_intersection == []:
                if variable_intersection == []:
                    return 1 - (1 - lifted_algorithm(database, query1))*(1 - lifted_algorithm(database, query2))
                else:
                    px_or_qx(database, query)
            #case 3:
            #We have dependent union of clauses with different variables in each clause.
            #table_intersection != [] and variable_intersection == []:
            else:
                print "simplify"
                return simplify_table_intersect(database, query)
        else:
            print "Not liftable for more than 2 cnf clauses right now"
            sys.exit(0)
    else:
        cc = connected_components(variables[0])
        if len(cc) > 1:
            cc_tables = list()
            for i in xrange(len(cc)):
                cc_tables.append([tables[0][j] for j in cc[i]])
            if not independent(cc_tables[0], cc_tables[1]):
                new_queries = split_by_connected_components(tables, variables, cc)
                print lifted_algorithm(database, union_of_cnf(new_queries))
                # return lifted_algorithm(database, new_queries[0]) + lifted_algorithm(database, new_queries[1]) - lifted_algorithm(database, union_of_cnf(new_queries))
            else:
                new_queries = split_by_connected_components(tables, variables, cc)
                return lifted_algorithm(database, new_queries[0]) * lifted_algorithm(database, new_queries[1])
        else:
            return get_probability(database, query)
