import heapq

import pandas as pd
import folium

# read in the files and prepare them as dataframes
arclist = pd.read_csv('data/arclist.txt', sep='\\s+', names=['end', 'time', 'distance', 'speedlimit', 'clazz', 'flags'])
nodelist = pd.read_csv('data/nodelist.txt', sep='\\s+', names=['adjacent'])
nodepl = pd.read_csv('data/nodepl.txt', sep='\\s+', names=['long', 'lat'])
dummy_arclist = pd.DataFrame({'end': [0], 'time': [0], 'distance': [0], 'speedlimit': [0], 'clazz': [0], 'flags': [0]})
dummy_nodelist = pd.DataFrame({'adjacent': [0]})
dummy_nodepl = pd.DataFrame({'long': [0.0], 'lat': [0.0]})
arclist = pd.concat([dummy_arclist, arclist], ignore_index=True)
nodelist = pd.concat([dummy_nodelist, nodelist], ignore_index=True)
nodepl = pd.concat([dummy_nodepl, nodepl], ignore_index=True)

# our closest node to our home is 979
start = 979
# the user chooses the type of cost function
choice = 0


def init_graph():
    graph = []
    for i in range(len(nodelist) - 1):
        graph.append({"node": i, "cost": float('inf'), "predecessor": None, "visited": False})
    graph[start]['cost'] = 0
    # We added a dummy line at the top such that all indices align
    graph[0]['visited'] = True

    return graph


def distance_update(i, neighbor, node_min_cost, graph, cost):
    # for pedestrians try to not use roads with more than 50 km/h (don't use highways)
    # and only use roads with the flag classification "pedestrian"
    if choice == 3:
        if arclist.loc[neighbor, 'flags'] < 4 or arclist.loc[neighbor, 'speedlimit'] > 50:
            cost[i] = cost[i] + 10000
    # cars try not to drive on pedestrian and/or bike streets and try to drive not on "small" streets
    if choice == 4:
        if arclist.loc[neighbor, 'flags'] == 2 or arclist.loc[neighbor, 'flags'] == 4 or arclist.loc[
            neighbor, 'flags'] == 6 or arclist.loc[neighbor, 'clazz'] == 31 or arclist.loc[neighbor, 'clazz'] == 41 or \
                arclist.loc[neighbor, 'clazz'] == 43:
            cost[i] = cost[i] + 10000

    alternative_distance = graph[node_min_cost]['cost'] + cost[i]
    if alternative_distance < graph[neighbor]['cost']:
        graph[neighbor]['cost'] = alternative_distance
        graph[neighbor]['predecessor'] = node_min_cost
    return graph


def dijkstra():
    # init graph
    graph = init_graph()
    #start at 1 because of the dummy line
    iterations = 1
    # as long as we have not visited all nodes
    while iterations != len(graph):
        not_visited_nodes = [node for node in graph if not node['visited']]
        not_visited_node_ids = [node['node'] for node in not_visited_nodes]
        # get node with the currently min cost
        node_min_cost = min(not_visited_nodes, key=lambda x: x['cost'])["node"]
        # set visited flag
        graph[node_min_cost]['visited'] = True
        # get the neighbours and the edges (the cost) of the node
        neighbors, cost = getNeighbors(node_min_cost)
        # update path of all neighbours
        for i, neighbor in enumerate(neighbors):
            if neighbor in not_visited_node_ids:
                graph = distance_update(i, neighbor, node_min_cost, graph, cost)
        iterations += 1
    return graph


def getNeighbors(node):
    # do the calculation from the adjacency list
    edges_node = nodelist['adjacent'][node]
    edges_next = nodelist['adjacent'][node + 1]
    neighbors = []
    distances = []
    times = []
    # store the costs / neighbours
    for i in range(edges_node, edges_next):
        neighbors.append(arclist['end'][i])
        distances.append(arclist['distance'][i])
        times.append(arclist['time'][i])

    # return different cost function based on the user input
    if choice == 1 or choice == 3 or choice == 4:
        return neighbors, times
    else:
        return neighbors, distances


def find_path(graph, end):
    # just go from the end node back to the start node
    path = []
    cost = []
    current_node = end
    while current_node is not None:
        path.append(current_node)
        cost.append(graph[current_node]['cost'])
        current_node = graph[current_node]['predecessor']
    # We get our path from the start node
    path.reverse()
    return path, cost


def main():
    global choice
    while True:
        print(30 * "-")
        print("Choose the Task:")
        print("Task 1-1: - time:      1")
        print("Task 1-2: - distance:  2")
        print("Task 2-1: - pedestrian 3")
        print("Task 2-2: - car        4")
        print("Exit    :              5")
        print(30 * "-")
        while True:
            # Read input and convert to integer
            choice = str(input("Enter a number (1-5): "))
            if choice in ["1", "2", "3", "4", "5"]:
                choice = int(choice)
                if choice != 5:
                    print("Calculating the dijkstra algorithm for option ", choice)
                break
            else:
                print("Enter a number between 1 and 5")
        if choice == 5:
            break

        graph = dijkstra()
        best_paths = []
        best_paths.append(find_path(graph, 9328))
        best_paths.append(find_path(graph, 6031))
        best_paths.append(find_path(graph, 8543))


        m = folium.Map(location=(nodepl.loc[start, "long"], nodepl.loc[start, "lat"]), zoom_start=15)
        for best_path in best_paths:
            print(f"Best path from {start} to {best_path[0][-1]}: {best_path[0]}")
            coordinates = [(nodepl.loc[i, "long"], nodepl.loc[i, "lat"]) for i in best_path[0]]
            folium.PolyLine(coordinates, color="blue", weight=2.5, opacity=1).add_to(m)
        m.save("map.html")


if __name__ == "__main__":
    main()
