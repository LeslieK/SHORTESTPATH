from graphLib import EdgeWeightedDigraph, EdgeWeightedGraph, DEdge, Edge
import numpy as np
import math


def distance(pos, v, w):
    """returns Euclidean distance between 2 vertices"""

    vx = pos[v][0]
    vy = pos[v][1]
    wx = pos[w][0]
    wy = pos[w][1]
    d = math.sqrt((vx - wx) ** 2 + (vy - wy) ** 2)
    return d


def buildMap(lines, V):
    """
    returns 2 maps: 1 with and 1 without directed edges
    returns pos: an array; rows = vertices col 0: x coord col 1: y coord

    V: number of vertices
    lines: each line is a vertex or an edge (from input file)
    """
    pos = np.zeros((V, 2))
    vertices = lines[:V]
    edges = lines[V:]
    usamap = EdgeWeightedDigraph(V)
    usamap_UN = EdgeWeightedGraph(V)

    for vertex in vertices:            # v x-coord y-coord
        line = vertex.strip().split()
        v = int(line[0])
        pos[v, 0] = int(line[1])
        pos[v, 1] = int(line[2])

    for edge in edges:
        line = edge.strip().split()
        v = int(line[0])
        w = int(line[1])
        weight = distance(pos, v, w)
        # add directed edge to map for running the algorithm
        usamap.addEdge(DEdge(v, w, weight))
        usamap.addEdge(DEdge(w, v, weight))
        # usamap_UN is used for plotting
        usamap_UN.addEdge(Edge(v, w, weight))
    return usamap, usamap_UN, pos
