import networkx as nx
import tsplib95 as tsp
import numpy as np


def readTSP(file_name_input):
    tsp_problem = tsp.load_problem(file_name_input)
    G = tsp_problem.get_graph()
    n = len(G.nodes())
    net = {}
    net['noNodes'] = n
    matrix = nx.to_numpy_matrix(G)
    net['mat'] = matrix
    return net

def read(file_name_input):
    net = {}
    f = open(file_name_input, "r")
    n = int(f.readline())
    net['noNodes'] = n
    matrix = [[0 for i in range(n)] for j in range(n)]
    matrixAux = [[0 for i in range(n)] for j in range(n)]
    for i in range(0, n):
        line = f.readline()
        line = line.strip()
        vec = line.split(",")
        for j in range(0, len(vec)):
            matrix[i][j] = int(vec[j])
            if (int(vec[j]) == 0):
                matrixAux[i][j] = 0
    net['mat'] = matrix
    return net

