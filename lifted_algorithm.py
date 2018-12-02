from query_parser import *

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

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
            cc.append(variables[i])
            for j in xrange(i+1, len(variables)):
                if intersection(variables[i], variables[j]) != []:
                    visited[j] = 1
                    cc.append(variables[j])
            res.append(cc)
    return res


def lifted_algoritm(query, database):
    #To be done
    return 0
