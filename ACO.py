from Graph import Graph
import random


class ACO(object):
    def __init__(self, antCount: int, generations: int, alpha: float, beta: float, e: float, p: int):
        self.antCount = antCount
        self.generations = generations
        self.alpha = alpha
        self.beta = beta
        self.e = e
        self.p = p

    def updatePheromone(self, graph: Graph, ants: list):
        for i in range(graph.n):
            for j in range(graph.n):
                """ il evapor pe cel actual"""
                graph.matPheromone[i][j] *= self.e
                for ant in ants:
                    """actualizez noul feromon"""
                    graph.matPheromone[i][j] += ant.pheromone_delta[i][j]

    def solve(self, graph: Graph):
        bestDistance = float('inf')
        bestSolution = []
        for gen in range(self.generations):
            """ creez cate o furnica pt nr de furnici dat si le bag intr o lista"""
            ants = [Ant(self, graph) for i in range(self.antCount)]
            for ant in ants:
                for i in range(graph.n - 1):
                    """ creez drumul furnicii"""
                    ant.selectNext()
                    """calculez distanta parcursa"""
                ant.totalDistance += graph.matDistance[ant.solution[-1]][ant.solution[0]]
                if (ant.totalDistance < bestDistance):
                    """ actualizez cea mai buna distanta si cea mai buna solutie"""
                    bestDistance = ant.totalDistance
                    bestSolution = [] + ant.solution
                """actualizez feromonul in functie de drumul parcurs de furnica (cantitate feromon / drum total)"""
                ant.updatePheromoneDelta()
            """actualizez feromonul general"""
            self.updatePheromone(graph, ants)
        return bestSolution, bestDistance


class Ant(object):
    def __init__(self, colony: ACO, graph: Graph):
        self.colony = colony
        self.graph = graph
        self.totalDistance = 0
        self.solution = []
        self.pheromoneDelta = []
        self.allowed = [i for i in range(graph.n)]
        self.eta = [[0 if i == j else 1 / graph.matDistance[i][j] for j in range(graph.n)] for i in
                    range(graph.n)]
        start = random.randint(0, graph.n - 1)
        self.solution.append(start)
        self.current = start
        self.allowed.remove(start)

    def selectNext(self):
        denominator = 0
        for i in self.allowed:
            """suma dintre feromon * 1/distanta"""
            denominator += self.graph.matPheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][
                i] ** self.colony.beta
        probabilities = [0 for i in range(self.graph.n)]
        for i in range(self.graph.n):
            try:
                self.allowed.index(i)  # test if allowed list contains i
                probabilities[i] = (self.graph.matPheromone[self.current][i] ** self.colony.alpha * self.eta[self.current][i] ** self.colony.beta) / denominator
            except ValueError:
                pass  # do nothing
        selected = 0
        rand = random.random()
        for i, probability in enumerate(probabilities):
            rand -= probability
            if rand <= 0:
                selected = i
                break
        self.allowed.remove(selected)
        self.solution.append(selected)
        self.totalDistance += self.graph.matDistance[self.current][selected]
        self.current = selected

    def updatePheromoneDelta(self):
        self.pheromone_delta = [[0 for j in range(self.graph.n)] for i in range(self.graph.n)]
        for _ in range(1, len(self.solution)):
            i = self.solution[_ - 1]
            j = self.solution[_]
            self.pheromone_delta[i][j] = self.colony.p / self.totalDistance
