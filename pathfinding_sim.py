import pygame
import time
from priority_queue import PrioritySet, PriorityQueue, AStarQueue
from math import inf
import random
from collections import deque

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
LIGHT_BLUE = (0, 111, 255)
ORANGE = (255, 128, 0)
PURPLE = (128, 0, 255)
YELLOW = (255, 255, 0)
GREY = (143, 143, 143)
BROWN = (186, 127, 50)
DARK_GREEN = (0, 128, 0)
DARKER_GREEN = (0, 50, 0)
DARK_BLUE = (0, 0, 128)


# For creating Buttons
class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = int(x)
        self.y = int(y)
        self.width = int(width)
        self.height = int(height)
        self.text = text

    def draw(self, win, outline=None):
        # Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x, self.y, self.width, self.height), 0)

        pygame.draw.rect(win, self.color, (self.x + 1, self.y + 1, self.width - 1, self.height - 1), 0)

        if self.text != '':
            font = pygame.font.SysFont('arial', 12)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + int(self.width / 2 - text.get_width() / 2), self.y + int(self.height / 2 - text.get_height() / 2)))

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


# Make it easier to add different node types
class Node():
    nodetypes = ['blank', 'start', 'end', 'wall', 'mud', 'dormant']

    colors = {
        'regular': {'blank': WHITE, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': BROWN, 'dormant': GREY},
        'visited': {'blank': GREEN, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': DARK_GREEN, 'dormant': GREY},
        'path': {'blank': BLUE, 'start': RED, 'end': LIGHT_BLUE, 'wall': BLACK, 'mud': DARK_BLUE, 'dormant': GREY}
        }

    distance_modifiers = {'blank': 1, 'start': 1, 'end': 1, 'wall': inf, 'mud': 3, 'dormant': inf}

    def __init__(self, nodetype, text='', colors=colors, dmf=distance_modifiers):
        self.nodetype = nodetype
        self.rcolor = colors['regular'][self.nodetype]
        self.vcolor = colors['visited'][self.nodetype]
        self.pcolor = colors['path'][self.nodetype]
        self.is_visited = True if nodetype == 'start' else True if nodetype == 'end' else False
        self.is_path = True if nodetype == 'start' else True if nodetype == 'end' else False
        self.distance_modifier = dmf[self.nodetype]
        self.color = self.pcolor if self.is_path else self.vcolor if self.is_visited else self.rcolor

    def update(self, nodetype=False, is_visited='unchanged', is_path='unchanged', colors=colors, dmf=distance_modifiers,
               nodetypes=nodetypes):
        if nodetype:
            assert nodetype in nodetypes, f"nodetype must be one of: {nodetypes}"
            if (self.nodetype == ('start' or 'end')) and (nodetype == ('wall' or 'mud')):
                pass
            else:
                self.nodetype = nodetype

        if is_visited != 'unchanged':
            assert type(is_visited) == bool, "'is_visited' must be boolean: True or False"
            self.is_visited = is_visited

        if is_path != 'unchanged':
            assert type(is_path) == bool, "'is_path' must be boolean: True or False"
            self.is_path = is_path

        self.rcolor = colors['regular'][self.nodetype]
        self.vcolor = colors['visited'][self.nodetype]
        self.pcolor = colors['path'][self.nodetype]
        self.distance_modifier = dmf[self.nodetype]
        self.color = self.pcolor if self.is_path else self.vcolor if self.is_visited else self.rcolor


# This sets the WIDTH and HEIGHT of each grid location
WIDTH = 7
HEIGHT = WIDTH  # so they are squares
BUTTON_HEIGHT = 50

# This sets the margin between each cell
MARGIN = 0

# Create a 2 dimensional array (a list of lists)
grid = []
ROWS = 95
# Iterate through every row and column, adding blank nodes
for row in range(ROWS):
    grid.append([])
    for column in range(ROWS):
        grid[row].append(Node('blank'))

    # Set start and end points for the pathfinder
START_POINT = (random.randrange(2, ROWS - 1, 2) - 1, random.randrange(2, ROWS - 1, 2) - 1)
END_POINT = (random.randrange(2, ROWS - 1, 2), random.randrange(2, ROWS - 1, 2))

grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
grid[END_POINT[0]][END_POINT[1]].update(nodetype='end')

DIAGONALS = False
VISUALIZE = True

# Used for handling click & drag
mouse_drag = False
drag_start_point = False
drag_end_point = False

# Used for deciding what to do in different situations
path_found = False
algorithm_run = False

pygame.init()

# Set default font for nodes
FONT = pygame.font.SysFont('arial', 6)

# Set the width and height of the screen [width, height]
SCREEN_WIDTH = ROWS * (WIDTH + MARGIN) + MARGIN * 2
SCREEN_HEIGHT = SCREEN_WIDTH + BUTTON_HEIGHT * 3
WINDOW_SIZE = (SCREEN_WIDTH, SCREEN_HEIGHT)
screen = pygame.display.set_mode(WINDOW_SIZE)

#Make some buttons
dijkstraButton = Button(GREY, 0, SCREEN_WIDTH, SCREEN_HEIGHT/3, BUTTON_HEIGHT, "Dijkstra Algo")

# MAKE THEM HERE

pygame.display.set_caption('Labdhi\'s Algorithm Visualization')

# Loop until the user clicks the close button
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()


'''This next part the the main program loop. This is the main game code. Have fun!!!'''
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()

            # Find out which keys have been pressed
            pressed = pygame.key.get_pressed()

            # If click is inside the gird
            if pos[1] <= SCREEN_WIDTH -1:
                # Change the x/y screen coordinates to grid coordinates
                column = pos[0] // (WIDTH + MARGIN)
                row = pos[1] //(HEIGHT + MARGIN)

                if (row, column) == START_POINT:
                    drag_start_point = True
                elif (row, column) == END_POINT:
                    drag_end_point = True
                else:
                    cell_updated = grid[row][column]
                    if pressed[pygame.K_LCTRL]: # this is when the left CTRL button is clicked in windows
                        update_cell_to = 'mud'
                    else:
                        update_cell_to = 'wall'
                    cell_updated.update(nodetype = update_cell_to)
                    mouse_drag = True
                    if algorithm_run and cell_updated.is_path == True:
                        path_found = update_path()


            # The following code is for all of the Button onClicks
            elif dijkstraButton.isOver(pos):
                clear_visited()
                update_gui(draw_background=False, draw_buttons=False)
                if VISUALIZE:
                    pygame.display.flip()
                path_found = dijkstra(grid, START_POINT, END_POINT)
                grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
                algorithm_run = 'dijkstra'


                # Move the start point
            elif drag_start_point == True:
                if grid[row][column].nodetype == "blank":
                    grid[START_POINT[0]][START_POINT[1]].update(nodetype='blank', is_path=False, is_visited=False)
                    START_POINT = (row, column)
                    grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
                    # If we have already run the algorithm, update it as the point is moved
                    if algorithm_run:
                        path_found = update_path()
                        grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')

                        # Move the end point
            elif drag_end_point == True:
                if grid[row][column].nodetype == "blank":
                    grid[END_POINT[0]][END_POINT[1]].update(nodetype='blank', is_path=False, is_visited=False)
                    END_POINT = (row, column)
                    grid[END_POINT[0]][END_POINT[1]].update(nodetype='end')
                    # If we have already run the algorithm, update it as the point is moved
                    if algorithm_run:
                        path_found = update_path()
                        grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')

            pygame.display.flip()


    # Main Game Logic
    def clear_visited():
        excluded_nodetypes = ['start', 'end', 'wall' , 'mud']
        for row in range(ROWS):
            for column in range(ROWS):
                if grid[row][column].nodetype not in excluded_nodetypes:
                    grid[row][column].update(nodetype = 'blank', is_visited=False, is_path=False)
                else:
                    grid[row][column].update(is_visited=False, is_path=False)

    def update_path(algorith_run =algorithm_run):
        clear_visited()
        valid_algorithms = ['dijkstra']

        assert algorithm_run in valid_algorithms, f"last algo used({algorithm_run}) is not in valid algorithms: {valid_algorithms})"

        if algorithm_run == 'dijkstra':
            path_found = dijkstra(grid, START_POINT, END_POINT, visualise=False)
        else:
            path_found = False

        return path_found


    # Function for moving an item between dictionaries
    def dict_move(from_dict, to_dict, item):
        to_dict[item] = from_dict[item]
        from_dict.pop(item)
        return from_dict, to_dict

    # + means non-diagonal neighbors and x means diagonal neighbors
    def get_neighbors(node, max_width=ROWS-1, diagonals=DIAGONALS):
        if not diagonals:
            neighbours = (
                ((min(max_width, node[0] + 1), node[1]), "+"),
                ((max(0, node[0] - 1), node[1]), "+"),
                ((node[0], min(max_width, node[1] + 1)), "+"),
                ((node[0], max(0, node[1] - 1)), "+")
            )
        else:
            neighbours = (
                ((min(max_width, node[0] + 1), node[1]), "+"),
                ((max(0, node[0] - 1), node[1]), "+"),
                ((node[0], min(max_width, node[1] + 1)), "+"),
                ((node[0], max(0, node[1] - 1)), "+"),
                ((min(max_width, node[0] + 1), min(max_width, node[1] + 1)), "x"),
                ((min(max_width, node[0] + 1), max(0, node[1] - 1)), "x"),
                ((max(0, node[0] - 1), min(max_width, node[1] + 1)), "x"),
                ((max(0, node[0] - 1), max(0, node[1] - 1)), "x")
            )

            # return neighbours
        return (neighbour for neighbour in neighbours if neighbour[0] != node)





# draw the square in a given location
    def draw_square(row, column, grid=grid):
        pygame.draw.rect(
            screen,
            grid[row][column].color,
            [
                (MARGIN + HEIGHT) * column + MARGIN,
                (MARGIN + HEIGHT) * row + MARGIN,
                WIDTH,
                HEIGHT
            ]
        )
        pygame.event.pump()



    # updates a single square
    def update_square(row, column):
        pygame.display.update(
            (MARGIN + HEIGHT) * column + MARGIN,
            (MARGIN + HEIGHT) * row + MARGIN,
            WIDTH,
            HEIGHT
        )
        pygame.event.pump()

    def neighbors_loop(neighbor, maze_arr, visited_nodes, unvisited_nodes, queue, v_distance, current_node, current_distance, diags=DIAGONALS, astar=False):
        neighbor, ntype = neighbor

        heuristic = 0

        if astar:
            heuristic += abs(END_POINT[0] - neighbor[0]) + abs(END_POINT[1] - neighbor[1])
            heuristic *= 1  # if this goes above 1 then the shortest path is not guaranteed, but the attempted route becomes more direct

        # If the neighbour has already been visited
        if neighbor in visited_nodes:
            pass
        elif maze_arr[neighbor[0]][neighbor[1]].nodetype == 'wall':
            visited_nodes.add(neighbor)
            unvisited_nodes.discard(neighbor)
        else:
            modifier = maze_arr[neighbor[0]][neighbor[1]].distance_modifier
            if ntype == "+":
                queue.push(current_distance + (1 * modifier) + heuristic, current_distance + (1 * modifier), neighbor)
            elif ntype == "x":
                queue.push(current_distance + ((2 ** 0.5) * modifier) + heuristic,
                           current_distance + ((2 ** 0.5) * modifier), neighbor)

    def trace_back(goal_node, start_node, v_distances, visited_nodes, n, maze_arr, diags=False, visualize=VISUALIZE):
        # begin the list of nodes which will represent the path back, starting with the end node
        path = [goal_node]

        current_node = goal_node

        # Set the loop in  motion until we get back to the start
        while current_node != start_node:
            neighbor_distances= PriorityQueue()
            neighbors = get_neighbors(current_node, n, diags)

            try:
                distance = v_distances[current_node]
            except Exception as e:
                print(e)

            # for each neighbor of the current node, add its location and distance to a priority queue

            for neighbor, ntype in neighbors:
                if neighbor in v_distances:
                    distance = v_distances[neighbor]
                    neighbor_distances.push(distance, neighbor)

            distance, smallest_neighbor = neighbor_distances.pop()
            maze_arr[smallest_neighbor[0]][smallest_neighbor[1]].update(is_path=True)

            # update pygame display
            draw_square(smallest_neighbor[0], smallest_neighbor[1], grid=maze_arr)

            path.append(smallest_neighbor)

            current_node = smallest_neighbor
        pygame.display.flip()
        maze_arr[start_node[0]][start_node[1]].update(is_path=True)





    # DIJKSTRAS ALGORITHM CODE
    def dijkstra(maze_array, start_point=(0,0), goal_node=False, display=pygame.display, visualize=VISUALIZE, diagonals=DIAGONALS, astar=False):

        heuristic = 0
        distance = 0

        # Get the dimensions of the square maze
        n = len(maze_array) - 1

        # Create the various data structures with speed in mind
        visited_nodes = set()
        unvisited_nodes = set([(x,y) for x in range(n+1) for y in range(n+1)])
        queue = AStarQueue()

        queue.push(distance+heuristic, distance, start_point)
        v_distance ={}

        # If goal_node in not set, put it in the bottom right (1 square away from either edge)
        if not goal_node:
            goal_node=(n,n)
        priority, current_distance, current_node = queue.pop()
        start = time.perf_counter()

        #Main algo loop
        while current_node!= goal_node and len(unvisited_nodes) > 0:
            if current_node in visited_nodes:
                if len(queue.show()) == 0:
                    return False
                else:
                    priority, current_distance, current_node = queue.pop()
                    continue

            # Call to check neighbors of the current node
            for neigbor in get_neighbors(current_node, n, diagonals=diagonals):
                neighbors_loop(
                    neigbor,
                    maze_arr=maze_array,
                    visited_nodes=visited_nodes,
                    unvisited_nodes=unvisited_nodes,
                    queue=queue,
                    v_distance=v_distance,
                current_node=current_node,
                    current_distance=current_distance,
                    astar=astar

                )

            # When we have checked the current node, add and remove appropriately
            visited_nodes.add(current_node)
            unvisited_nodes.discard(current_node)

            # Add the distance to the visited distances dictionary (used for traceback)
            v_distance[current_node] = current_distance

            # Pygame part: visited nodes mark visited nodes as green
            if (current_node[0], current_node[1]) != start_point:
                maze_array[current_node[0]][current_node[1]].update(is_visited=True)
                draw_square(current_node[0], current_node[1], grid=maze_array)

                # If I want to visualize it rather than run instantly, then we update the grid with each iteration of this loop
                if visualize:
                    update_square(current_node[0], current_node[1])
                    time.sleep(0.000001)

                if len(queue.show()) == 0:
                    return False
                # Otherwise we take the minimum distance as the new current node
                else:
                    priority, current_distance, current_node = queue.pop()



        v_distance[goal_node] = current_distance + (1 if not diagonals else (2**0.5))
        visited_nodes.add(goal_node)

        # Draw the path back from the goal node to the start node
        trace_back(goal_node, start_point, v_distance, visited_nodes, n, maze_array, diags=diagonals, visualize=visualize)

        end = time.perf_counter()
        num_visited = len(visited_nodes)
        time_taken = (end-start)

        print(f"Congrats Labdhi, your program finished in {time_taken: .4f} seconds after checking {num_visited} nodes. That is {time_taken/num_visited: .8f} seconds per node!")

        return False if v_distance[goal_node] == float('inf') else True

    grid[START_POINT[0]][START_POINT[1]].update(nodetype='start')
    grid[END_POINT[0]][END_POINT[1]].update(nodetype='end')
    def update_gui(draw_background = True, draw_buttons=True, draw_grid=True):
        if draw_background:
            # It should be obvious , I draw the background here, and set everything on it
            screen.fill(BLACK)
            pass

        if draw_buttons:
            visToggleButton = Button(GREY, SCREEN_WIDTH/3, SCREEN_WIDTH + BUTTON_HEIGHT*2, SCREEN_WIDTH/3, BUTTON_HEIGHT, f"Visualize:{str(VISUALIZE)}")
            # draw the button below the grid

            dijkstraButton.draw(screen, (0,0,0))
            visToggleButton.draw(screen, (0,0,0))

        if draw_grid:
            # Draw the grid
            for row in range(ROWS):
                for column in range(ROWS):
                    color = grid[row][column].color
                    draw_square(row,column)

    update_gui()

    pygame.display.flip() # updates the entire screen

    clock.tick(100)





'''This is where the main loop ends. I hope you had fun!!!'''

#Close the window and quit
pygame.quit()







