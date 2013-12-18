import argparse
from search import astarSP, dijkstraSP
import shortestPathUtils
import matplotlib.pyplot as plt
from matplotlib import animation


def init():
    """set initial value of line"""
    line.set_data([], [])
    return line,


def animate(i):
    """draws path to ith vertex visited"""
    resize = False
    # set line to new data
    n = spt.getNextVertex(i)
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


def createFigure(pos):
    """initializes base figure"""
    fig = plt.figure()
    fig.hold(True)
    ax = fig.add_subplot(111, aspect=True, autoscale_on=True)
    ax.set_xlim(pos[:, 0].min() * -1.1, pos[:, 0].max() * 1.1)
    ax.set_ylim(pos[:, 1].min() * -1.1, pos[:, 1].max() * 1.1)
    line, = ax.plot([], [], linewidth=2, color='red', marker='.')
    return fig, ax, line


def plotMap(args, ax, pos):
    """plot map on base figure"""
    if args.map:
        print "beginning to plot map"
        for e in usamap_UN.edges():
            v = e.either()
            w = e.other(v)
            ax.plot([pos[v, 0], pos[w, 0]], [pos[v, 1], pos[w, 1]],
                ls='-', color='gray', alpha=.2)
        print "map plot done"

##############################################################
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--filename", "-f", default="usa.txt",
        help="filename of network", type=str)
    parser.add_argument("--source_vertex", "-s", default=83494, 
        help="a vertex number: 0 to 87574", type=int)
    parser.add_argument("--target_vertex", "-t", default=35075, 
        help="a vertex number: 0 to 87574", type=int)
    parser.add_argument("--map", "-m", action="store_true", 
        help="plot network")
    parser.add_argument("--astar", "-a", action="store_true", 
        help="do A-Star search with Euclidean heuristic")
    args = parser.parse_args()

    with open(args.filename) as f:
        V = int(f.readline().strip())
        E = int(f.readline().strip())
        text = f.read()

    source = args.source_vertex
    target = args.target_vertex
    if source < 0 or source > V-1 or target < 0 or target > V-1:
        raise ValueError("source or target value out of range")

    lines = text.split('\n')
    # build 2 maps: 1 with directed edges; 
    # 1 with undirected edges (used for plotting)
    usamap, usamap_UN, pos = shortestPathUtils.buildMap(lines, V)

    # find shortest path
    if args.astar:
        source_init = shortestPathUtils.distance(pos, source, target)
        spt = astarSP(source_init, pos, usamap, source, target)
    else:
        spt = dijkstraSP(usamap, source, target)

    fig, ax, line = createFigure(pos)
    plotMap(args, ax, pos)

    ani = animation.FuncAnimation(fig, animate, init_func=init, 
        frames=spt.numberExploredVertices(), repeat=False, interval=10, 
                        blit=True)

    plt.show()
