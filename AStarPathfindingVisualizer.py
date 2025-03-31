# Pathfinding algorithm

# Libraries
import pygame
import math
from queue import PriorityQueue

# Variables to set up the display window for the program
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

# Colors to reference for the display
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255,255,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
PURPLE = (128,0,128)
ORANGE = (255,165,0)
GREY = (128,128,128)
TURQOISE = (64,224,208)

# **************************************** CLASSES ****************************************
# Class to define each spot on the grid for the visualizer
class Spot:
    # Initialization function that will instantiate each 'Spot' object with the required attributes
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    # Function to draw rectangles on the display to create a grid
    def draw(self,win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    # Function to update the location of the neighboring spots to the current one in the search algorithm
    def update_neighbors(self, grid):
        # Initialize an empty list to store the neighboring spots if they are valid options to traverse
        self.neighbors = []
        # Check that the spots with a difference in x or y value on the grid of 1 from the current spot
        # aren't barriers, then append the row and col (x and y) values to the list
        if self.row < self.total_rows -1 and not grid[self.row +1][self.col].is_barrier(): # Down
            self.neighbors.append(grid[self.row +1][self.col])
        if self.row > 0 and not grid[self.row -1][self.col].is_barrier(): # Up
            self.neighbors.append(grid[self.row -1][self.col])
        if self.col < self.total_rows -1 and not grid[self.row][self.col +1].is_barrier(): # Right
            self.neighbors.append(grid[self.row][self.col +1])
        if self.row > 0 and not grid[self.row][self.col -1].is_barrier(): # Left
            self.neighbors.append(grid[self.row][self.col -1])

    # This function will be used as a comparison operator between to spots but always returning False
    # as a less-than comparison
    def __lt__(self, other):
        return False

    # **************************************** GETTERS ****************************************
    # Functions that access the attribute values of a given 'Spot' object
    def get_position(self):
        return self.row, self.col

    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN

    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(slef):
        return self.color == TURQOISE

    # **************************************** SETTERS ****************************************
    # Functions to change a given attribute value of a 'Spot' object
    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_closed(self):
        self.color = RED

    def make_open(self):
        self.color = GREEN

    def make_barrier(self):
        self.color =   BLACK
    

    def make_end(self):
        self.color = TURQOISE

    def make_path(self):
        self.color = PURPLE

# **************************************** FUNCTIONS ****************************************
# Pathfinding algorithm that finds the 'L' distance from two points on the grid
def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)

# Function to reconstruct the best found path between the start and end points
def reconstruct_path(came_from, current, draw):
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()

# Function to handle the search algorithm of the program
# draw is passed in here as a lambda function
def algorithm(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    # Place the starting spot into the open set
    open_set.put((0, count, start))
    # Dictionary to track the previous spot to the current one
    came_from = {}
    # g score is the current shortest distance from the start node to the current node
    g_score = {spot: float("inf") for row in grid for spot in row}
    # g_score of the starting position on the grid is 0
    g_score[start] = 0
    # f score keeps track of the estimated distance between the current node and the end node
    f_score = {spot: float("inf") for row in grid for spot in row}
    # f score starts of as a guess of distance between start node and end node
    f_score[start] = h(start.get_position(), end.get_position())

    # Helps to see if something is in the open set
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # Set the current to the spot object associated with the open set
        current = open_set.get()[2]
        # Remove the current from the open set hash table
        open_set_hash.remove(current)

        # If the end has been reached, return True and exit the function
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        # Consider the neighbors of the current node and calculate their temporary g score
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1
        
            # Compare g scores and update the algorithm with the better path
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_position(), end.get_position())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.make_open()
        
        draw()

        if current != start:
            current.make_closed()

    return False


# Function to create the digital grid that the pathfinding algorithm will be operating within
def make_grid(rows, width):
    grid = []
    gap = width // rows
    # Iterate through the rows value with nested loop to create a square grid
    for i in range(rows):
        # Add an empty list to the current iteration value of rows
        grid.append([])
        for j in range(rows):
            # For each spot in the lists (within the list) initialize a 'Spot' object using the iteration
            # values to determine the x and y coordinate of the new spot
            spot = Spot(i, j, gap, rows)
            # Append the new object to the list
            grid[i].append(spot)

    return grid

# Function to draw the grid on the pygame window
def draw_grid(win, rows, width):
    gap = width // rows
    # For each row, draw a horizontal line which dimensions are connected to the iteration value
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
        # Do the same for each column by switching the order of the values and the iterator
        for j in range(rows):
            pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))

# Function to Display the program on the window
def draw(win, grid, rows, width):
    # Start by filling the window completely with one color
    win.fill(WHITE)
    # Iterate throught he 'grid' list that is passed in and call the class function of each spot to draw it
    for row in grid:
        for spot in row:
            spot.draw(win)

    # Divide the squares of the grid by drawing the grid lines between them calling draw_grid function
    draw_grid(win, rows, width)
    pygame.display.update()

# Function to detect mouse position on the display grid when the user clicks
def get_clicked_position(pos, rows, width):
    gap = width // rows
    y, x = pos

    row = y // gap
    col = x // gap

    return row, col

# **************************************** MAIN PROGRAM ****************************************
def main(win, width):
    # Variables that will be used in the main program loop
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    end = None
    run = True

    # Loop through the events of the program
    while run:
        # Call the draw function to display the program on the pygame window
        draw(win, grid, ROWS, width)
        # First event to account for is always the exit event of the program
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            # If the user clicks either mouse button while over the display
            if pygame.mouse.get_pressed()[0]: # LEFT
                # Determine the positon of the mouse cursor on the display
                pos = pygame.mouse.get_pos()
                # Extract the x and y coordinates from the position
                row, col = get_clicked_position(pos, ROWS, width)
                # Assign the spot at the correlated position to the row and column values
                spot = grid[row][col]
                # The first two clicks on the display will set the start and end of the search path
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != end and spot != start:
                    spot.make_barrier()
            # Same implementation for a mouse click but with the right mouse button and the reset function
            elif pygame.mouse.get_pressed()[2]: # RIGHT
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_position(pos, ROWS, width)
                spot = grid[row][col]
                spot.reset()
                # If the reset spot was the start or end spot, reassign the values of those spots to None
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            # If the user presses the spacebar, begin the algorithm
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)

                    # Lambda names a function as a variable so that it can be passed into another function
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)

                # Reset the game when the user presses lowercase c
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)