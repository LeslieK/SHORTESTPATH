from graphLib import EdgeWeightedDigraph, EdgeWeightedGraph, DEdge, Edge
from decimal import Decimal
from priorityQueue import IndexMinPQ
from shortestPathUtils import distance

_INF = Decimal('infinity')
_SENTINEL = -1


class ShortestPathTree(object):
    Algorithms = ["astar", "dijk"]

    def __init__(self, source_init, algorithm, G, s, t=None, pos=None):
        """
        find the shortest path (in a directed graph with non-negative weights)
        from s to t using Dijkstra's alg
        """
        if algorithm not in ShortestPathTree.Algorithms:
            raise ValueError("algorithm not supported")
        else:
            self._algorithm = algorithm

        self._s = s
        if t is not None:
            self._t = t
        self._G = G
        self._distTo = [_INF] * G.V()
        self._distTo[s] = source_init

        # edgeTo[v]: last edge on shortest path from s to v
        self._edgeTo = [_SENTINEL] * G.V()
        self._pq = IndexMinPQ(G.V())
        # insert source into pq
        self._pq.insert(s, self._distTo[s])
        # list of relaxed vertices; needed for animation
        self._nextVertex = []

        # calculate data structures
        while (not self._pq.isEmpty()):
            v = self._pq.delMin()
            self._nextVertex.append(v)
            if t and v == self._t:
                break
            for edge in self._G.adj(v):
                """relaxes an edge"""
                if self._algorithm == "astar":
                    self._relaxAstar(edge, pos)
                elif self._algorithm == "dijk":
                    self._relaxDijk(edge)

    def distTo(self, v):
        "length of path from src to vertex v"
        return self._distTo[v]

    def hasPathTo(self, v):
        "checks whether path exists from src to vertex v"
        return self._edgeTo[v] != _SENTINEL

    def pathTo(self, v):
        "returns path from src to vertex v"
        if not self.hasPathTo(v):
            return
        path = []
        e = self._edgeTo[v]
        while e.src() != self._s:
            path.append(e)
            e = self._edgeTo[e.src()]
        path.append(e)
        return path[::-1]

    def getNextVertex(self, i):
        """
        return ith relaxed vertex; used for animation
        """
        return self._nextVertex[i]

    def numberExploredVertices(self):
        """returns number of relaxed vertices"""
        return len(self._nextVertex)

    def _relaxAstar(self, edge, pos):
        """uses Euclidean heuristic to relax edge"""
        v = edge.src()
        w = edge.sink()
        dist_w_t = distance(pos, w, self._t)
        dist_v_t = distance(pos, v, self._t)
        path_len_to_v = self._distTo[v] - dist_v_t
        if self._distTo[w] > path_len_to_v + edge.weight() + dist_w_t:
            # includes Euclidean heuristic
            self._distTo[w] = path_len_to_v + edge.weight() + dist_w_t
            self._edgeTo[w] = edge
            self._updatePQ(w)

    def _relaxDijk(self, edge):
        """relaxes edge without a heuristic"""
        v = edge.src()
        w = edge.sink()
        if self._distTo[w] > self._distTo[v] + edge.weight():
            self._distTo[w] = self._distTo[v] + edge.weight()
            self._edgeTo[w] = edge
            self._updatePQ(w)

    def _updatePQ(self, w):
        """
        update PQ with vertex w
        add (w, value) to PQ or
        update value for w
        """
        if not self._pq.contains(w):
            self._pq.insert(w, self._distTo[w])
        else:
            self._pq.decreaseKey(w, self._distTo[w])

    def __repr__(self):
        """print shortest path tree (spt) built by DijkSP object"""
        V = len(self._edgeTo)
        spt = GraphLib.EdgeWeightedDigraph(V)
        for i in range(V):
            if self._edgeTo[i] != _SENTINEL:
                spt.addEdge(self._edgeTo[i])
        print str(spt.edges())


def dijkstraSP(G, s, t):
    return ShortestPathTree(0, "dijk", G, s, t)


def astarSP(source_init, pos, G, s, t):
    if pos is None:
        raise ValueError("x-y coords must be provided")
    return ShortestPathTree(source_init, "astar", G, s, t, pos)
