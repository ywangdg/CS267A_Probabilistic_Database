from query_parser import *

def is_variable(var):
    if (len(var) == 1 and var.isalpha()) or (len(var) ==2 and var[0].isalpha() and var[1].isdigit()):
        return True
    return False


def lifted_algoritm(query, database):
    #To be done
    print query
    return 0
