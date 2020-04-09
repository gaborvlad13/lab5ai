class Graph(object):
    def __init__(self, matDistance:list, n:int):
        self.matDistance = matDistance
        self.n = n
        self.matPheromone =[[1 / (n * n) for j in range(n)] for i in range(n)]


