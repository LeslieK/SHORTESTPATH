program: sptAnimation.py

usage: python sptAnimation.py -h
usage: python sptAnimation.py -f "input6.txt" -s 0 -t 6 -m -a

What it does:
It finds the shortest path between 2 US cities, using only US roads.
(No traveling through Canada!)
The graph consists of 87575 nodes and 121961 edges (see usa.txt).
The result is an animation of the search process. The program searches
for the path and if it reaches a dead end, it tries another path. The animation
is displayed over the graph over which it is searching; i.e., a map of the US.

By default, the program uses Dijkstra's algorithm without a Euclidean heuristic.
To enable the Euclidean heuristic in the search, the user uses the -a switch
(which enables A* search).
