############  P-dispersion.py ###################################
## Goal:    Generates the LP form for a p-dispersion problem 
## Created: March 10 2015/revised October 19 2016
## Author:  eric delmelle
## Inputs:  1. coordinates of the bounding box
##             2. p (# facilities) 
##             3. interval
## Outputs: CPLEX LP file (use CPLEX or Lingo to solve)
## Particularities:
##          1. Uses Euclidean distance
#########################################################

import random, string, os, math, time, sys
import matplotlib.pyplot as plt   # only necessary if you want to plot
import numpy                          # only necessary if you want to plot

def distance(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    d = math.sqrt(dx**2 + dy**2)
    return d

## parameters
p=15            #num facilities
M=100000        # a very large number

## Generate candidate locations (uniform)
ID=[]
X=[]
Y=[]
minX=0
maxX=100
minY=0
maxY=100
interval =10

k=0
for i in range (minX, maxX, interval):
    for j in range(minY, maxY, interval):
        ID.append(k)
        X.append(i + random.random())
        Y.append(j + random.random())
        k+=1

print('there are ' + str(len(X)) + ' decision variables')
OD = []
i=0
while i<len(X):
    j=0
    while j<len(Y):
        OD.append(str(distance(X[i], Y[i], X[j], Y[j])))
        j=j+1
    i=i+1


## activate the next lines only if you want to plot the points
plt.scatter(X, Y)
plt.show()

################# WRITING L-P file ################# 

###   Objective function headings
outputFile = open('pdispersion.txt', 'w')
outputFile.write("Maximize D\n")
outputFile.write("\nSubject to")
outputFile.write("\n")

#   Constraint 2 
i=0
while i< len(X):
    j=i+1
    while j < len(X):
        Dij = OD[i*len(X) + j]
        outputFile.write('D+' + str(M - float(Dij))+ 'X' +str(i) + '+' + str(M- float(Dij)) + 'X' +str(j) +'<= ' +str((2*M) - float(Dij)) + '\n') 
        j+=1
    i+=1


#   Constraint 3- max facilities = p
outputFile.write("\n")
j=0
while j < len(ID):
    outputFile.write("+X")
    outputFile.write(str(int(ID[j])))
    j=j+1
outputFile.write("="+str(p)+"\n")

#   Constraint 4 - integer requirements
outputFile.write("\n") 
outputFile.write("Integers\n")

i=0
while i<len(X):
    outputFile.write('X' + str(i) +'\n')
    i=i+1
outputFile.write("\n")
outputFile.write("END\n")
outputFile.close()
