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

def get_seperator(variables):
    print variables
    sets = iter(map(set, variables))
    result = sets.next()
    for s in sets:
        result = result.intersection(s)
    return list(result)

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
        print separator
        if separator == []:
            print "Not liftable"
            sys.exit(0)
        else:
            groupby_value_list = get_groupby_variables(separator, mapping[0])

            for i in xrange(len(tables[0])):
                name = tables[0][i]
                print name
                database[name]["NegProb"]= (1-database[name]["Prob"])
                database[name]=database[name].groupby(groupby_value_list[i][0]).prod()
                database[name].index.name = 'Var1'
                database[name]["Prob"]= (1-database[name]["NegProb"])

            result = database[tables[0][0]][['Prob']]
            print result
            for i in xrange(1, len(tables[0])):
                result = result.merge(database[tables[0][i]][['Prob']],how='inner', on = 'Var1');
                print result
            result["Total_Prob"]=1
            print result
            for column in result:
                if ('Var' not in result[column].name and result[column].name!='Total_Prob'):
                    #print(result[column])
                    result["Total_Prob"]=result["Total_Prob"]*result[column]
            solution=1-(1-(result["Total_Prob"])).prod()
            return solution
        # tables1 = tables[0][0]
        # tables2 = tables[0][1]
        # var1 = variables[0][0]
        # var2 = variables[0][1]
        # print (tables1, tables2, var1, var2)
        # if intersection(var1, var2) == []:
        #     CNF1 = Query([[tables1]], [[var1]])
        #     CNF2 = Query([[tables2]], [[var2]])
        #     return get_probability(database, CNF1) * get_probability(database, CNF2)
        #
        # else:
        # # Case 3 for each independent p(x)r(x,y)
        #     separator = intersection(var1, var2)[0]
        #     groupby_value_list = [ mapping[0][tables1][separator], mapping[0][tables2][separator]]
        #
        #     database[tables1]["NegProb"]= (1-database[tables1]["Prob"])
        #     database[tables1]=database[tables1].groupby(groupby_value_list[0]).prod()
        #     database[tables1].index.name = 'Var1'
        #     database[tables1]["Prob"]= (1-database[tables1]["NegProb"])
        #     database[tables2]["NegProb"]= (1-database[tables2]["Prob"])
        #     database[tables2]=database[tables2].groupby(groupby_value_list[1]).prod()
        #     database[tables2].index.name = 'Var1'
        #     database[tables2]["Prob"]= (1-database[tables2]["NegProb"])
        #     result = pd.merge(database[tables1][['Prob']],database[tables2][['Prob']],how='inner', on = groupby_value_list[1]);
        #     result["Prob"]=1
        #     for column in result:
        #         if ('Var' not in result[column].name and result[column].name!='Prob'):
        #             #print(result[column])
        #             result["Prob"]=result["Prob"]*result[column]
        #     solution=1-(1-(result["Prob"])).prod()
        #     return solution

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
    union_tables = [query.tables[0] for yquery in cnf_queries ]
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
            variable_intersection = intersection(query.variables[0], query.variables[1])
            if table_intersection == []:
                if variable_intersection == []:
                    return 1 - (1 - lifted_algorithm(database, query1))*(1 - lifted_algorithm(database, query2))
                else:
                    conjunction_query = conjunction_of_cnf(cnf_queries)
                    return lifted_algorithm(database, query1) + lifted_algorithm(database, query2) - lifted_algorithm(database, conjunction_query)



            #case 3:
            #We have dependent union of clauses with different variables in each clause.
            if table_intersection != [] and variable_intersection == []:
                return simplify_table_intersect(query, database)
    else:
        cc = connected_components(variables[0])
        if len(cc) > 1:
            cc_tables = list()
            for i in xrange(len(cc)):
                cc_tables.append([tables[0][j] for j in cc[i]])
            if not independent(cc_tables[0], cc_tables[1]):
                new_queries = split_by_connected_components(tables, variables, cc)
                return get_probability(database, new_queries[0]) + get_probability(database, new_queries[1]) - lifted_algoritm(union_cnf_query)
            else:
                new_queries = split_by_connected_components(tables, variables, cc)
                return lifted_algorithm(database, new_queries[0]) * lifted_algorithm(database, new_queries[1])
        else:
            return get_probability(database, query)
