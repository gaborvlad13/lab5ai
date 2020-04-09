from ACO import ACO
from Graph import Graph
from Read import read, readTSP
from random import seed
from random import randint

net = read('data/easy.txt')
graph = Graph(net['mat'], net['noNodes'])
aco = ACO(100, 150, 1, 1, 0.5, 5)
bestSolution, bestDistance = aco.solve(graph)
print(str(bestDistance)+": ")
for i in range(len(bestSolution)):
    print(str(bestSolution[i])+" ")




