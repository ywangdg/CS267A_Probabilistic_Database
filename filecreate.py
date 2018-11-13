file = open('testfile.txt', 'w')
file.truncate(0)
file.write('Hello World')

file.close()

file = open('t1.txt', 'w')
file.truncate(0)
file.write('S \n')
file.write('1,1,0.6 \n')
file.write('2,1,0.4 \n')
file.write('1,2,0.8')

file.close()


file = open('t2.txt', 'w')
file.truncate(0)
file.write('S \n')
file.write('1,1,0.6 \n')
file.write('2,1,0.4 \n')
file.write('1,2,0.8')

file.close()

file = open('t3.txt', 'w')
file.truncate(0)
file.write('S \n')
file.write('1,1,0.6 \n')
file.write('2,1,0.4 \n')
file.write('1,2,0.8')

file.close()


file = open('t3.txt', 'w')
file.truncate(0)
file.write('S \n')
file.write('1,1,0.6 \n')
file.write('2,1,0.4 \n')
file.write('1,2,0.8')

file.close()


file = open('query.txt', 'w')
file.truncate(0)
file.write('R(x1),S(x1,y1) ||S(x2, y2), T(x2)')

file.close()