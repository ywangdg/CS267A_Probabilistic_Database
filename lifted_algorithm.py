from query_parser import *

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


def simplify(query):
    CNF1 = Query([query.tables[0]],[query.variables[0]])
    CNF2 = Query([query.tables[1]],[query.variables[1]])
    intersect_table = intersection(CNF1.tables[0], CNF2.tables[0])[0]
    if intersect_table != []:
        index1 = CNF1.tables[0].index( intersect_table)
        index2 = CNF2.tables[0].index( intersect_table)
        intersect_var = CNF1.variables[0][index1]

        new_cnf_table1 = CNF1.tables[0]
        new_cnf_table1.remove(intersect_table)
        new_cnf_table2 = CNF2.tables[0]
        new_cnf_table2.remove(intersect_table)

        new_cnf_var1 = CNF1.variables[0]
        new_cnf_var1.pop(index1)
        new_cnf_var2 = CNF2.variables[0]
        new_cnf_var2.pop(index2)

        Query1 = Query([new_cnf_table1 + new_cnf_table2], [new_cnf_var1 + new_cnf_var2])

def get_probability(database, CNF_Query):
    tables = CNF_Query.tables
    variables = CNF_Query.variables

    if len(tables[0])== 1:
        name = tables[0][0]
        database[name]['NegProb'] = (1 - database[name]['Prob'])
        database['Rprod'] =  database[name].groupby('Var1').prod()

        return 1 - (1 - database['Rprod']['NegProb']).prod()

    else:
        tables1 = tables[0][0]
        tables2 = tables[0][1]
        var1 = variables[0][0]
        var2 = variables[0][1]
        print var1
        if intersection(var1, var2) == []:
            CNF1 = Query([[tables1]], [[var1]])
            CNF2 = Query([[tables2]], [[var2]])
            return get_probability(database, CNF1) * get_probability(database, CNF2)

        else:
            






def lifted_algoritm(query, database):
    #To be done
    if len(query.variables) > 1:
        simplify(query)
        print "sss"
    else:
        if len(connected_components(query.variables[0])) > 1:
            cc_tables = list()
            for i in xrange(len(connected_components(query.variables[0]))):
                cc_tables.append([ query.tables[0][j] for j in connected_components(query.variables[0])[i]])
            if not independent(cc_tables[0], cc_tables[1]):
                print "hhh"
            else:
                print "sss"
        else:
            get_probability(database, query)
