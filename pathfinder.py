# This program executes an algorithm that will search for possible paths through a maze in a breadth
# first formula
import curses
from curses import wrapper
import queue
import time


# Hard coded maze for the program to find the shortest path through
# 'O' is the starting point and 'X' is the end
maze = [
    ["#", "#", "#", "#", "#", "O", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]
]

# Function to display the maze to the curses terminal
def print_maze(maze,stdscr,path=[]):
    GREEN = curses.color_pair(1)
    RED = curses.color_pair(2)

    # Nested for loops to iterate through the 2D list that is stored in the 'maze' variable
    for i, row in enumerate(maze):
        for j, value in enumerate(row):
            if (i,j) in path:
                stdscr.addstr(i,j*2,"X",RED)
            else:
                stdscr.addstr(i,j*2,value,GREEN)

# Function to iterate through the maze and search for the symbol that indicates the starting position
def find_start(maze,start):
    for i, row in enumerate(maze):
        for j,value in enumerate(row):
            if value == start:
                return i,j
    return None

# Algorithm function that will find the shortest possible path through the maze
def find_path(maze,stdscr):
    start = "O"
    end = "X"
    start_pos = find_start(maze,start)

    # Initialize a queue data structure for processing possible paths through the maze
    q = queue.Queue()
    # Storing the next node to process, as well as a list of previously examined nodes in the queue
    q.put((start_pos, [start_pos]))

    # Empty set to store all of the visited positions of a given path
    visited = set()

    # As long as the queue has something in it, get the information stored and store it in variables
    while not q.empty():
        # Extract the value from the queue and store the path, and coordinates
        current_pos, path = q.get()
        row, col = current_pos

        # Refresh the curses display during each iteration
        stdscr.clear()
        print_maze(maze,stdscr,path)
        time.sleep(0.2)
        stdscr.refresh()

        # If the algorithm finds the end of the maze, return the path that was taken to get there
        if maze[row][col] == end:
            return path

        # Function call to 'find_neighbors' and storing return in the local 'neighbors' variable
        neighbors = find_neighbors(maze,row,col)
        # Check if the neighbor value is also in the 'visited' set
        for neighbor in neighbors:
            if neighbor in visited:
                continue
            
            # Store the row and column values of the neighboring position, check for obstacle symbol
            r,c = neighbor
            if maze[r][c] == '#':
                continue

            # The new path is the current one plus whatever neighboring space is being considered
            new_path = path + [neighbor]
            q.put((neighbor,new_path))
            visited.add(neighbor)

# Function to identify the 4 directions are possible from the current position
def find_neighbors(maze,row,col):
    neighbors = []

    if row > 0: # UP
        neighbors.append((row - 1,col))
    if row + 1 < len(maze): # DOWN
        neighbors.append((row + 1,col))
    if col > 0: # LEFT
        neighbors.append((row,col - 1))
    if col + 1 < len(maze[0]): # RIGHT
        neighbors.append((row,col + 1))

    return neighbors

# 'stdscr' stands for standard output screen for the curses module
def main(stdscr):
    # Initialize text color combinations for the maze on the curses display
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)

    # Function call to find a path through the maze and display the maze with the path highighted
    find_path(maze,stdscr)
    stdscr.getch()

# Initializes the curses module on the main function
wrapper(main)