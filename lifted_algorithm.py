from query_parser import *
import pandas as pd
import sys
import numpy as np
import copy
from utils import *
import itertools
import functools


def get_probability(database, CNF_Query):
    tables = CNF_Query.tables
    variables = CNF_Query.variables
    mapping = CNF_Query.variable_column_mapping_list
    separator = intersection_multiple_list(variables[0])
    if separator == []:
        print ("Not liftable")
        sys.exit(0)
    else:
        groupby_value_list = get_groupby_variables(separator, mapping[0])
        for i in range(len(tables[0])):
            name = tables[0][i]
            database[name]["NegProb"]= (1-database[name]["Prob"])
            database[name]=database[name].groupby(groupby_value_list[i][0]).prod()
            database[name].index.name = 'Var1'
            database[name]["Prob"]= (1-database[name]["NegProb"])

        data_frames = [database[tables[0][i]][['Prob']].add_suffix(str(i)) for i in range(len(tables[0]))]
        result = functools.reduce(lambda  left,right: pd.merge(left,right,on=['Var1'],   how='inner'), data_frames)

        result["Total_Prob"]=1
        for column in result:
            if ('Var' not in result[column].name and result[column].name!='Total_Prob'):
                #print(result[column])
                result["Total_Prob"]=result["Total_Prob"]*result[column]

        solution=1-(1-(result["Total_Prob"])).prod()
        return result[["Total_Prob"]] ,solution


def inclusion_exclusion(query):
    tables = [q.tables for q in query]
    variables = [q.variables for q in query]
    new_query_family = list()

    for i in range(len(query)):
        new_query_family.append([union_of_cnf(pair) for pair in itertools.combinations(query, i+1)])
    return new_query_family

def get_independent_query_from_cc(query, connected_components):
    rest_queries = list()
    tables_list = [q.tables[0] for q in query]

    independent_queries = list()
    for i in range(len(connected_components)):
        intersection_list = list()
        for j in range(len(tables_list)):
            if intersection(query[i].tables[0], tables_list[j]) != [] and i != j:
                intersection_list.append(j)
        if len(intersection_list) == 0:
            independent_queries.append(query[i])
        else:
            rest_queries.append(query[i])

    return independent_queries, rest_queries


def get_independent_query_from_cc_for_unions(query, connected_components):
    tables_list = [q.tables for q in query]
    independent_queries = list()
    rest_queries = list()
    for i in range(len(connected_components)):
        intersection_list = list()
        for j in range(len(tables_list)):
            if not completely_independent(tables_list[i], tables_list[j]) and i!=j:
                intersection_list.append(j)
        if len(intersection_list) == 0:
            independent_queries.append(query[i])
        else:
            rest_queries.append(query[i])


    return independent_queries, rest_queries

def get_df_for_unions(database, query):
    tables = query.tables
    variables = query.variables
    cnf_list = decompose_or(query)
    data_frames = list()
    for i in range(len(cnf_list)):
        df = get_probability(database,cnf_list[i])[0]
        df = df.rename(index=str, columns={"Total_Prob": str(i)})
        data_frames.append(df)
    # data_frames = [get_probability(database,cnf)[0] for cnf in cnf_list]
    result = functools.reduce(lambda  left,right: pd.merge(left,right,on=['Var1'],   how='outer'), data_frames)
    result = result.fillna(0)
    product = 1
    for col in list(result.columns):
            product = product * (1-result[col])
    orfunct= 1- product
    return orfunct


def get_probability_for_unions(database, query):
    tables = query.tables
    variables = query.variables
    variable_column_mapping_list = query.variable_column_mapping_list

    if len(query.tables) == 1:
        df, prob = get_probability(database, query)
        return prob
    else:
        separator = intersection_multiple_list(tables)
        if separator == []:
            print ("Not liftable")
            sys.exit(0)
        else:
            seperator_var = [[var for var in query.variable_column_mapping_list[0][table].keys()] for table in separator]
            seperator_query = Query([separator], [seperator_var])
            rest_query_tables = copy.deepcopy(tables)
            for cnf_tables in rest_query_tables:
                for table in separator:
                    cnf_tables.remove(table)

            rest_variable_index_list = list()
            for i in range(len(query.variables)):
                cnf_intersection_index_list = list()
                for table in query.tables[i]:
                    if not table in separator:
                        intersect_index = index_of_intersection(list(query.variable_column_mapping_list[i][table].keys()), list(query.variable_column_mapping_list[i][table].keys()))
                        cnf_intersection_index_list.append(intersect_index)
                rest_variable_index_list.append(cnf_intersection_index_list)

            rest_variable_list = list()
            for i in range(len(rest_variable_index_list)):
                index_list = list()
                for j in range(len(rest_variable_index_list[i])):
                    index_list.append(variables[i][j])
                rest_variable_list.append(index_list)
                #rest_variable_list.append([[variables[i][index] for index in index_list]  for index_list in rest_variable_index_list[i]])

            rest_query = Query(rest_query_tables, rest_variable_list)
            seperator_df, prob = get_probability(database, seperator_query)
            rest_df = get_df_for_unions(database, rest_query)
            return 1 - (1 - rest_df * seperator_df['Total_Prob']).prod()

def lifted_algorithm(database, query):
    tables = query.tables
    variables = query.variables
    #To be done
    if len(variables) > 1:
        cc_of_cnf_unions =  connected_components(tables)
        new_queries = split_by_connected_components_union_of_cnfs(tables, variables, cc_of_cnf_unions)


        prod = 1
        for union_query in new_queries:
            prod *= (1 - get_probability_for_unions(database, union_query))

        return 1 - prod

    else:
        cc = connected_components(variables[0])
        if len(cc) > 1:
            cc_tables = list()
            new_queries = split_by_connected_components(tables, variables, cc)
            independent_queries, rest_queries = get_independent_query_from_cc(new_queries, cc)
            new_query_family = inclusion_exclusion(rest_queries)
            print (len(new_query_family))
            #
            independent_prod = 1
            for query in independent_queries:
                prob = lifted_algorithm(database, query)
                independent_prod *= prob

            if len(rest_queries) == 0:
                return independent_prod

            else:
                inclusion_exclusion_result = 0
                for i in range(len(new_query_family)):
                    for query in new_query_family[i]:
                        res = lifted_algorithm(database, query)
                        inclusion_exclusion_result += res* np.power(-1,i)
                return inclusion_exclusion_result * independent_prod

        else:
            _, prob = get_probability(database, query)
            return prob
