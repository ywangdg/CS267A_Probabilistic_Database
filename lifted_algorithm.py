from query_parser import *
import pandas as pd
import sys
import numpy as np
import query
import copy
from utils import *
import itertools


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
    rest_result_df, x = get_probability_union_of_cnfs(database, rest_query)
    seperator_df, prob = get_probability(database, seperator_query)

    return 1 - (1 - rest_result_df * seperator_df).prod()

    # return lifted_algorithm(database, query_1) + lifted_algorithm(database, query_1) - lifted_algorithm(database, query_3)


def get_probability(database, CNF_Query):
    tables = CNF_Query.tables
    variables = CNF_Query.variables
    mapping = CNF_Query.variable_column_mapping_list
    separator = intersection_multiple_list(variables[0])
    if separator == []:
        print "Not liftable"
        sys.exit(0)
    else:
        groupby_value_list = get_groupby_variables(separator, mapping[0])
        for i in xrange(len(tables[0])):
            name = tables[0][i]
            database[name]["NegProb"]= (1-database[name]["Prob"])
            database[name]=database[name].groupby(groupby_value_list[i][0]).prod()
            database[name].index.name = 'Var1'
            database[name]["Prob"]= (1-database[name]["NegProb"])

        data_frames = [database[tables[0][i]][['Prob']].add_suffix(str(i)) for i in xrange(len(tables[0])) ]

        result = reduce(lambda  left,right: pd.merge(left,right,on=['Var1'],   how='inner'), data_frames)
        result["Total_Prob"]=1
        for column in result:
            if ('Var' not in result[column].name and result[column].name!='Total_Prob'):
                #print(result[column])
                result["Total_Prob"]=result["Total_Prob"]*result[column]

        solution=1-(1-(result["Total_Prob"])).prod()
        return result["Total_Prob"] ,solution


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

def get_probability_union_of_cnfs(database, query):
    tables = query.tables
    assert (len(tables)==2)
    assert (len(tables[0])==1)
    assert (len(tables[1])==1)

    variables = query.variables
    mapping = query.variable_column_mapping_list
    grounding = get_grounding_for_or(variables)
    grounding_var_list = list()
    for i in xrange(len(mapping)):
        grounding_var_list.append([mapping[i][key][grounding[0]] for key in mapping[i].keys()])

    for i in xrange(len(tables)):
        for j in  xrange(len(tables[i])):
            table = tables[i][j]
            database[table]["NegProb"]= (1-database[table]["Prob"])
            #
            database[table]=database[table].groupby(grounding_var_list[i][j]).prod()
            database[table].index.name = 'Var1'
            database[table]["Prob"]= (1-database[table]["NegProb"])

    data_frames = [database[tables[i][j]][['Prob']].add_suffix(str(tables[i][j])) for j in xrange(len(tables[i])) for i in xrange(len(tables)) ]
    result = reduce(lambda  left,right: pd.merge(left,right,on=['Var1'],   how='outer'), data_frames)

    product = 1
    for col in list(result.columns):
            product = product * (1-result[col])

    orfunct= 1- product
    solution = 1-(1-orfunct).prod()
    return orfunct, solution

def inclusion_exclusion(query):
    tables = [q.tables for q in query]
    variables = [q.variables for q in query]
    new_query_family = list()

    for i in xrange(len(query)):
        new_query_family.append([union_of_cnf(pair) for pair in itertools.combinations(query, i+1)])
    return new_query_family

def get_independent_query_from_cc(query, connected_components):
    rest_queries = list()
    tables_list = [q.tables[0] for q in query]

    independent_queries = list()
    for i in xrange(len(connected_components)):
        intersection_list = list()
        for j in xrange(len(tables_list)):
            if intersection(query[i].tables[0], tables_list[j]) != [] and i != j:
                intersection_list.append(j)
        if len(intersection_list) == 0:
            independent_queries.append(query[i])
        else:
            rest_queries.append(query[i])

    return independent_queries, rest_queries

def completely_independent(table_list1, table_list2):
    for table1 in table_list1:
        for table2 in table_list2:
            if not independent(table1, table2):
                return False
    return True

def get_independent_query_from_cc_for_unions(query, connected_components):
    tables_list = [q.tables for q in query]
    independent_queries = list()
    rest_queries = list()
    for i in xrange(len(connected_components)):
        intersection_list = list()
        for j in xrange(len(tables_list)):
            if not completely_independent(tables_list[i], tables_list[j]) and i!=j:
                intersection_list.append(j)
        if len(intersection_list) == 0:
            independent_queries.append(query[i])
        else:
            rest_queries.append(query[i])


    return independent_queries, rest_queries

def get_probability_unions(database, query):
    tables = query.tables
    variables = query.variables
    print get_grounding_for_or(variables)

    for i in xrange(len(query.tables)):
        print query.tables[i], query.variables[i]


def lifted_algorithm(database, query):
    tables = query.tables
    variables = query.variables
    #To be done
    if len(variables) > 1:
        cc_of_cnf_unions =  connected_components_of_cnf_unions(variables)
        print cc_of_cnf_unions
        new_queries = split_by_connected_components_union_of_cnfs(tables, variables, cc_of_cnf_unions)
        independent_queries, rest_queries = get_independent_query_from_cc_for_unions(new_queries,cc_of_cnf_unions)

        independent_prod = 1
        for query in independent_queries:
            get_probability_unions(database, query)


        if len(cc_of_cnf_unions) == 1:
            print 1
        else:
            print 2


            #solve_unions_query(databse, new_queries)
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
                    _, prob = get_probability_union_of_cnfs(database, query)
                    return prob
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
        cc = connected_components_of_cnf(variables[0])
        print cc
        if len(cc) > 1:
            cc_tables = list()
            new_queries = split_by_connected_components(tables, variables, cc)
            independent_queries, rest_queries = get_independent_query_from_cc(new_queries, cc)
            new_query_family = inclusion_exclusion(rest_queries)
            print len(new_query_family)
            #
            independent_prod = 1
            for query in independent_queries:
                prob = lifted_algorithm(database, query)
                independent_prod *= prob

            if len(rest_queries) == 0:
                return independent_prod

            else:
                inclusion_exclusion_result = 0
                for i in xrange(len(new_query_family)):
                    for query in new_query_family[i]:
                        res = lifted_algorithm(database, query)
                        inclusion_exclusion_result += res* np.power(-1,i)
                return inclusion_exclusion_result * independent_prod

            #solve_cnf_query(database, new_queries)
            # for i in xrange(len(cc)):
            #     cc_tables.append([tables[0][j] for j in cc[i]])
            # if not independent(cc_tables[0], cc_tables[1]):
            #     # return lifted_algorithm(database, union_of_cnf(new_queries))
            #     return lifted_algorithm(database, new_queries[0]) + lifted_algorithm(database, new_queries[1]) - lifted_algorithm(database, union_of_cnf(new_queries))
            # else:
            #
            #     return lifted_algorithm(database, new_queries[0]) * lifted_algorithm(database, new_queries[1])
        else:
            _, prob = get_probability(database, query)
            return prob
