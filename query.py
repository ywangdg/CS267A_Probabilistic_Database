class Query:
    def __init__(self, table, var):
        self.table = table
        self.var = var

class CNF:
    def __init__(self, queries):
        self.queries = queries

class UCQ:
    def __init__(self, CNFs):
        self.CNFs = CNFs
