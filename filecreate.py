file = open('testfile.txt', 'w')
file.truncate(0)
file.write('Hello World')

file.close()

file = open('t1.txt', 'w')
file.truncate(0)
file.write('P \n')
file.write('0,0.7 \n')
file.write('1,0.8 \n')
file.write('2,0.6')

file.close()


file = open('t2.txt', 'w')
file.truncate(0)
file.write('Q \n')
file.write('0,0.7 \n')
file.write('1,0.3 \n')
file.write('2,0.5')

file.close()

file = open('t3.txt', 'w')
file.truncate(0)
file.write('R \n')
file.write('0,0,0.8 \n')
file.write('0,1,0.4 \n')
file.write('0,2,0.5 \n')
file.write('1,2,0.6 \n')
file.write('2,2,0.9')

file.close()


file = open('query1.txt', 'w')
file.truncate(0)
file.write('R(x1,y1),Q(x1)')

file.close()

file = open('query2.txt', 'w')
file.truncate(0)
file.write('R(x1,y1),P(x1),Q(x2),R(x2,y2)')

file.close()
