from query_parser import *
import pandas as pd
import sys
import numpy as np
import query

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
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

# When simplify is called, we know we have a disjunction in our query with a shared table such as:
# [T(x1),Q(x1,y1)]||[S(x2),Q(x2,y2)]
# Let query_1 = [T(x1),Q(x1,y1)] and query_2 = [S(x2),Q(x2,y2)] and query_3 = query_1 * query_2
# We perform inclusion exclusion and get query_1 + query_2 - query_3
# query_1 and query_2 are easy to compute with a call to get_probability.
# query_3 = T(x1),Q(x1,y1),S(x2),Q(x2,y2), which is solved with a recurive call to lifted_algorithm.
def simplify_table_intersect(query, database):
    query_1 = Query([query.tables[0]], [query.variables[0]])
    query_2 = Query([query.tables[1]], [query.variables[1]])

    query_3 = Query([query.tables[0]+query.tables[1]], [query.variables[0]+query.variables[1]])

    print query_1.tables
    print query_1.variables

    print ""

    print query_2.tables
    print query_2.variables

    print ""

    print query_3.tables
    print query_3.variables

    return get_probability(database, query_1) + get_probability(database, query_1) - lifted_algorithm(database, query_3)

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
        tables1 = tables[0][0]
        tables2 = tables[0][1]
        var1 = variables[0][0]
        var2 = variables[0][1]
        if intersection(var1, var2) == []:
            CNF1 = Query([[tables1]], [[var1]])
            CNF2 = Query([[tables2]], [[var2]])
            return get_probability(database, CNF1) * get_probability(database, CNF2)

        else:
        # Case 3 for each independent p(x)r(x,y)
            separator = intersection(var1, var2)[0]
            groupby_value_list = [ mapping[0][tables1][separator], mapping[0][tables2][separator]]

            database[tables1]["NegProb"]= (1-database[tables1]["Prob"])
            database[tables1]=database[tables1].groupby(groupby_value_list[0]).prod()
            database[tables1].index.name = 'Var1'
            database[tables1]["Prob"]= (1-database[tables1]["NegProb"])
            database[tables2]["NegProb"]= (1-database[tables2]["Prob"])
            database[tables2]=database[tables2].groupby(groupby_value_list[1]).prod()
            database[tables2].index.name = 'Var1'
            database[tables2]["Prob"]= (1-database[tables2]["NegProb"])
            result = pd.merge(database[tables1][['Prob']],database[tables2][['Prob']],how='inner', on = groupby_value_list[1]);
            result["Prob"]=1
            for column in result:
                if ('Var' not in result[column].name and result[column].name!='Prob'):
                    #print(result[column])
                    result["Prob"]=result["Prob"]*result[column]
            solution=1-(1-(result["Prob"])).prod()
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

def lifted_algorithm(database, query):
    tables = query.tables
    variables = query.variables
    #To be done
    if len(variables) > 1:
        simplify(query)
        print "sss"
    else:
        cc = connected_components(variables[0])
        if len(cc) > 1:
            cc_tables = list()
            for i in xrange(len(cc)):
                cc_tables.append([tables[0][j] for j in cc[i]])
            if not independent(cc_tables[0], cc_tables[1]):
                new_queries = split_by_connected_components(tables, variables, cc)
                union_cnf_query = union_of_cnf(new_queries)
                print get_probability(database, new_queries[0]) + get_probability(database, new_queries[1])
                return get_probability(database, new_queries[0]) + get_probability(database, new_queries[1])
            else:
                new_queries = split_by_connected_components(tables, variables, cc)
                print lifted_algorithm(database, new_queries[0])
                print lifted_algorithm(database, new_queries[1])
                print lifted_algorithm(database, new_queries[0]) * lifted_algorithm(database, new_queries[1])
                return lifted_algorithm(database, new_queries[0]) * lifted_algorithm(database, new_queries[1])
        else:
            return get_probability(database, query)
