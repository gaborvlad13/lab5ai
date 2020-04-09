from random import random
from Graph import Graph
from ACO import ACO


class Ant(object):
    def __init__(self, colony:ACO, graph: Graph):
        self.colony = colony
        self.graph = graph
        self.totalDistance = 0
        self.solution = []
        self.pheromoneDelta = []
        self.allowed = [i for i in range(graph.n)]
        self.eta = [[0 if i == j else 1 / graph.matDistance[i][j] for j in range(graph.n)] for i in
                    range(graph.n)]
        start = random.randint(0, graph.n-1)
        self.solution.append(start)
        self.current = start
        self.allowed.remove(start)

    def selectNext(self):
        denominator=0
        for i in self.allowed:
            """suma dintre feromon * 1/distanta"""
            denominator+=self.graph.matPheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][i] ** self.colony.beta
        probabilities = [0 for i in range(self.graph.n)]
        for i in range(self.graph.n):
            try:
                self.allowed.index(i)  # test if allowed list contains i
                probabilities[i] = self.graph.matPheromone[self.current][i] ** self.colony.alpha * \
                                   self.eta[self.current][i] ** self.colony.beta / denominator
            except ValueError:
                pass  # do nothing
            selected = 0
            rand = random.random()
            for i, probability in enumerate(probabilities):
                rand-=probability
                if rand <= 0:
                    selected = i
                    break
            self.allowed.remove(selected)
            self.solution.append(selected)
            self.totalDistance+=self.graph.matDistance[self.current][selected]
            self.current = selected

    def updatePheromoneDelta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.n)] for i in range(self.graph.n)]
        for _ in range (1, len(self.solution)):
            i = self.solution[_ - 1]
            j = self.solution[_]
            self.pheromone_delta[i][j] = self.colony.p / self.totalDistance

