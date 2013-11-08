import argparse

from GraphLib import EdgeWeightedDigraph, EdgeWeightedGraph
from DirectedEdge import DEdge 		# directed, weighted edge
from WeightedEdge import Edge
from decimal import Decimal
from PQ import IndexMinPQ

import matplotlib.pyplot as plt
from matplotlib import animation
import numpy as np
import math	

from time import time

_INF = Decimal('infinity')
_SENTINEL = -1

parser = argparse.ArgumentParser()
parser.add_argument("--filename", "-f", default="usa.txt", help="filename of network", type=str)
parser.add_argument("--source_vertex", "-s", default=83494, help="a vertex number: 0 thru 87574", type=int)
parser.add_argument("--target_vertex", "-t", default=35075, help="a vertex number: 0 thru 87574", type=int)
parser.add_argument("--map", "-m", action="store_true", help="plot network")
args = parser.parse_args()

with open(args.filename) as f:
	V = int(f.readline().strip())
	E = int(f.readline().strip())
	text = f.read()

source = args.source_vertex
target = args.target_vertex
if source < 0 or source > V-1 or target < 0 or target > V-1:
	raise ValueError, "bad input"

# with open("usa.txt", 'r') as f:
# 	V = int(f.readline().strip())
# 	E = int(f.readline().strip())
# 	text = f.read()

# long path
#source = 83494
#target = 35075

# short path
#source = 0
#target = 69383

#input6.txt
#source = 0
#target = 5

def distance(pos, v, w):
	'''returns straight-line distance between 2 vertices

	pos: a numpy array of xcoord ycoord for each row'''
	vx = pos[v][0]
	vy = pos[v][1]
	wx = pos[w][0]
	wy = pos[w][1]
	d = math.sqrt((vx - wx) ** 2 + (vy - wy) ** 2)
	return d

usamap = EdgeWeightedDigraph(V)
usamap_UN = EdgeWeightedGraph(V)  # undirected graph used for drawing the network (digraph is needed to find shortest path)

pos = np.zeros((V, 2))
lines = text.split('\n')
for position in lines[:V]:		# v x-coord y-coord
	l = position.strip().split()
	v = int(l[0])
	pos[v, 0] = int(l[1])
	pos[v, 1] = int(l[2])
# now parse the edges from the lines
for edge in lines[V:-1]:			# v w 
	l = edge.strip().split()
	v = int(l[0])
	w = int(l[1])
	weight = distance(pos, v, w)
	# add directed edge to map for running the algorithm
	usamap.addEdge(DEdge(v, w, weight))
	usamap.addEdge(DEdge(w, v, weight))
	# add undirected edge to map for drawing purposes (only need to draw 1 undirected edge)
	usamap_UN.addEdge(Edge(v, w, weight))


class DijkSP(object):
	def __init__(self, G, s, t=None):
		"find the shortest path (in a directed graph with non-negative weights) from s to t using Dijkstra's alg"
		self._s = s
		if t is not None:
			self._t = t
		self._G = G
		self._distTo = [_INF] * G.V()
		self._distTo[s] = distance(pos, s, t) 				# for A*
		#self._distTo[s] = 0 								# for pure Dijkstra
		self._edgeTo = [_SENTINEL] * G.V() 					# edgeTo[v]: last edge on shortest path from s to v
		self._pq = IndexMinPQ(G.V())
		self._pq.insert(s, self._distTo[s])                 # insert source into pq
		self.nextVertex = []
		
		# calculate data structures
		while (not self._pq.isEmpty()):
			v = self._pq.delMin()
			self.nextVertex.append(v)
			if t and v == self._t: 
				#self.nextVertex.append(v)	# only draws the final path
				break
			for e in self._G.adj(v):
				self._relax(e)

		# while (not self._pq.isEmpty()):
		# 	v = self._pq.delMin() 			# add closest vertex to source to Tree
		# 	if t and v == t: break
		# 	for e in G.adj(v):
		# 		self._relax(e) 				# relax(e) updates the distTo and edgeTo data structures					

	def distTo(self, v):
		"length of path from src to vertex v"
		return self._distTo[v]

	def hasPathTo(self, v):
		"checks whether path exists from src to vertex v"
		return self._edgeTo[v] != _SENTINEL

	def pathTo(self, v):
		"returns path from src to vertex v"
		if not self.hasPathTo(v): return
		path = []
		e = self._edgeTo[v] 				# last edge of path
		while e.src() != self._s:
			path.append(e)
			e = self._edgeTo[e.src()]
		path.append(e)
		return path[::-1]

	def _relax(self, edge):
		"relaxes an edge by updating data structures with that edge"
		v = edge.src()
		w = edge.sink()
		# priority of edge v-w: 
		# (length of path from s to v) + e.weight() + distance(w, t)
		# (length of path from s to v) = distTo[v] - distance(v, t)
		dist_w_t = distance(pos, w, self._t)
		dist_v_t = distance(pos, v, self._t)
		path_len_to_v = self._distTo[v] - dist_v_t
		if self._distTo[w] > path_len_to_v + edge.weight() + dist_w_t:
			self._distTo[w] = path_len_to_v + edge.weight() + dist_w_t  	# includes Euclidean heuristic
			self._edgeTo[w] = edge
			if not self._pq.contains(w):
					self._pq.insert(w, self._distTo[w])
			else: 
					self._pq.decreaseKey(w, self._distTo[w])

	# def _relax(self, edge):
	# 	"relaxes an edge by updating data structures with that edge"
	# 	v = edge.src()
	# 	w = edge.sink()
	# 	if self._distTo[w] > self._distTo[v] + edge.weight():
	# 		self._distTo[w] = self._distTo[v] + edge.weight() 				# does not include Euclidean heuristic
	# 		self._edgeTo[w] = edge
	# 		if not self._pq.contains(w):
	# 				self._pq.insert(w, self._distTo[w])
	# 		else: 
	# 				self._pq.decreaseKey(w, self._distTo[w])

	def __repr__(self):
		"print spt built by Dijkstra object"
		V = len(self._edgeTo)
		spt = GraphLib.EdgeWeightedDigraph(V)
		for i in range(V):
			if self._edgeTo[i] != _SENTINEL:
				spt.addEdge(self._edgeTo[i])
		print str(spt.edges())

# plot vertices
#plt.scatter(pos[:, 0], pos[:, 1], color='gray', marker='.', alpha=.4)
#plt.show()

# initialize spt object
#time0 = time()
spt = DijkSP(usamap, source, target)
#time1 = time()
#print time1 - time0
#spt = DijkSP(usamap, source)

# initialize base figure
fig = plt.figure()
fig.hold(True)
ax = fig.add_subplot(111, aspect=True, autoscale_on=True)
ax.set_xlim(pos[:, 0].min() * -1.1, pos[:, 0].max() * 1.1)
ax.set_ylim(pos[:, 1].min() * -1.1, pos[:, 1].max() * 1.1)
#ax.set_xlim(min(pos[source, 0], pos[target, 0])*.5, max(pos[source, 0], pos[target, 0])*1.5)
#ax.set_ylim(min(pos[source, 1], pos[target, 1])*.5, max(pos[source, 1], pos[target, 1])*1.5)
line, = ax.plot([], [], linewidth=2, color='red', marker='.')  # creates a Line2D object

#draw map on canvas: this takes ~5 minutes!
if args.map:
	for e in usamap_UN.edges():
		v = e.either()
		w = e.other(v)
		ax.plot([pos[v, 0], pos[w, 0]], [pos[v, 1], pos[w, 1]], ls='-', color='gray', alpha=.2)

# xmin, xmax = ax.get_xlim()
# ymin, ymax = ax.get_ylim()
# for e in usamap_UN.edges():
# 	v = e.either()
# 	w = e.other(v)
# 	if (pos[[v, w], 0] < xmax).all() and (pos[[v, w], 1] > xmin).all():
# 		if ((pos[[v, w], 1]) < ymax).all() and ((pos[[v, w], 1] > ymin).all()):
# 			ax.plot([pos[v, 0], pos[w, 0]], [pos[v, 1], pos[w, 1]], ls='-', color='gray', alpha=.2)

def init():
	line.set_data([], [])  						# sets the initial value of the line
	return line,

def animate(i):
	resize=False
	# set line to new data
	n = spt.nextVertex[i]
	x = []
	y = []
	edges = spt.pathTo(n)
	if spt.hasPathTo(n):
		for e in edges:
			v = e.src()
			w = e.sink()
			vx = pos[v][0]
			vy = pos[v][1]
			wx = pos[w][0]
			wy = pos[w][1]
			x.append(vx)
			x.append(wx)
			y.append(vy)
			y.append(wy)
	line.set_data(x, y)
	return line,

ani = animation.FuncAnimation(fig, animate, init_func=init, frames=len(spt.nextVertex),
                               repeat=False, interval=10, blit=True)

#ani.save('dijkstra.mp4', writer='ffmpeg', extra_args=['-vcodec', 'libx264'])

plt.show()







