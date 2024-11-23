import pandas as pd

arclist = pd.read_csv('data/arclist.txt', sep='\s+', names=['end', 'time', 'distance', 'speedlimit', 'clazz', 'flags'])
nodelist = pd.read_csv('data/nodelist.txt', sep='\s+', names=['adjacent'])
nodepl = pd.read_csv('data/nodepl.txt', sep='\s+', names=['long', 'lat'])

# our closest node is 979
start = 979

def getNeighbors(node):
    neighbors = []
    edges_node = nodelist['adjacent'][node]
    edges_next = nodelist['adjacent'][node+1]
    neighbors = []
    distances = []
    times = []
    for i in range(edges_node, edges_next):
        neighbors.append(arclist['end'][i])
        distances.append(arclist['distance'][i])
        times.append(arclist['time'][i])
    return neighbors


visited_points = []
print(nodelist['adjacent'][start])
print(nodelist['adjacent'][start+1])



