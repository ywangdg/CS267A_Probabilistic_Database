import sys, getopt


database = dict()
#
# def generate_table(tables):
#     for table in tables:
#

def read_table(table):
    fd = open(table, "r")
    table_name = fd[0]
    print table_name


def main(argv):
    queries = []
    tables = []
    try:
        opts, args = getopt.getopt(argv,"hq:t:",["query=","table="])
    except getopt.GetoptError:
        print 'qeval.py -q <query files> -t <table files>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == "-h":
            print 'qeval.py -q <query files> -t <table files>'
            sys.exit()
        elif opt in ("-q", "--query"):
            queries.append(arg)
        elif opt in ("-t", "--table"):
            tables.append(arg)
    print 'Input query file is', queries
    print 'Input table file is', tables

    read_table(tables[0])

if __name__ == "__main__":
   main(sys.argv[1:])
