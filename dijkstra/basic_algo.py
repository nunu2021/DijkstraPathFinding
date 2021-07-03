import pygame

graph = {
    'a': {'b': 1, 'c': 1, 'd': 1},
    'b': {'c': 1, 'f': 1},
    'c': {'f': 1, 'd': 1},
    'd': {'e': 1, 'g': 1},
    'e': {'g': 1, 'h': 1},
    'f': {'e': 1, 'h': 1},
    'g': {'h': 1},
    'h': {'g': 1},
}


def dijkstra(graph, start,goal):
    shortest_distance ={} # records the cost to reach to that node
    track_predecessor = {} # keep track of the path that has led us to this node
    unseenNodes = graph # to iterate through the entire graph
    infinity = 9999999999 # infinity can basically be considered a very large number

    track_path = [] # going to trace out journey back to the source node, which is the optimal route

    for node in unseenNodes:
        shortest_distance[node] = infinity
    shortest_distance[start] = 0

    while unseenNodes:

        min_distance_node = None

        for node in unseenNodes:
            if min_distance_node == None:
                min_distance_node = node
            elif shortest_distance[node] < shortest_distance[min_distance_node]:
                min_distance_node = node

        path_options= graph[min_distance_node].items()

        for child_node, weight in path_options: # checks if the path to
            if weight + shortest_distance[min_distance_node] < shortest_distance[child_node]:
                shortest_distance[child_node] = weight + shortest_distance[min_distance_node]
                track_predecessor[child_node] = min_distance_node

        # since dijkstra's algo does not allow back tracking, we will not be able to visit the nodes we have already gone through
        unseenNodes.pop(min_distance_node)


        # vvv before this code, the program has the shortest path from anywhere to anywhere.

    currentNode = goal

    while currentNode != start:
        try:
            track_path.insert(0, currentNode)
            currentNode = track_predecessor[currentNode]
        except KeyError:
            print('Path is not reachable')
            break;

    track_path.insert(0, start)

    if shortest_distance != infinity:
        print("Shortest Distance is " + str(shortest_distance[goal]))
        print("Optimal path is: " + str(track_path))





dijkstra(graph, 'a', 'h')
