
import itertools
import numpy as np
import random



dict = {}
dict['T'] = 0
dict['F'] = 0


def draw_sample(a):
    a = 0.2 * 1000
    b = 0.1 * 1000
    c = 0.8 * 1000
    d = 0.3 * 1000
    e = 0.5 * 1000
    ares = 0
    bres = 0
    cres = 0
    dres = 0
    eres = 0

    ar = random.randint(1, 1000)
    br = random.randint(1, 1000)
    cr = random.randint(1, 1000)
    dr = random.randint(1, 1000)
    er = random.randint(1, 1000)

    # print (ar,br,cr,dr,er)
    if ar < a:
        ares = 1
    else:
        ares = -1
    if br < b:
        bres = 1
    else:
        bres = -1
    if cr < c:
        cres = 1
    else:
        cres = -1
    if dr < d:
        dres = 1
    else:
        dres = -1
    if er < e:
        eres = 1
    else:
        eres = -1
    return [[ares, bres, cres, dres, eres]]


def sat_count(clause, var):
    # clause=[[-1,-2],[1,-2]]
    # var=[1,2]

    # initialize your variables here
    init = [1, -1]
    varcount = len(var)
    x = init * varcount
    satcase = 0

    # this gives all of the distinct combinations of positives and negatives for all of the iterals in a set
    # impl=set((list(itertools.combinations(x, varcount))))
    impl = draw_sample(1)
    # print (impl)
    start = list(impl)
    # print(start)
    # Do array multiplication for each combination vs each entry in your clause
    for pindex in range(len(start)):
        errors = 0
        for cindex in range(len(clause)):
            elements = [a * b for a, b in zip(start[pindex], clause[cindex])]
            for eindex in range(len(elements)):
                # print ('element '     ,elements[eindex],'multi',elements,'clause',clause[cindex],'start', start[pindex])
                if elements[eindex] > 0:
                    break
                if eindex == len(elements) - 1:
                    errors += 1
        # If there are no errors, print Sat and the successful combination
        if errors == 0:
            # print('SAT',[a*b for a,b in zip(start[pindex],var)])
            satcase += 1
            dict['T'] += 1
    # If no cominations work, print UNSAT
    if satcase == 0:
        # print('UNSAT')
        dict['F'] += 1


count = 0
while count < 1000:
    # sat_count ([[1,2,-3,0,0],[0,2,3,4,-5],[0,-2,0,-4,5],[-1,-2,0,0,0]], [1,2,3,4,5])

    sat_count([[-1, 0, 3, 4, 0], [0, 2, 3, -4, 5], [0, 0, -3, 4, -5]], [1, 2, 3, 4, 5])
    count += 1

# sat_count ([[1,2,3],[1,2,-3],[1,-2,3],[1,-2,-3],[-1,2,3],[-1,2,-3],[-1,-2,3],[-1,-2,-3]],   [1,2,3])

print(dict)


