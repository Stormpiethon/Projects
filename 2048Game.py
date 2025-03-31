# *******************************************************************************************
# Alexander Brittain
# 2048 is a 4x4 grid based math game
# ******************************************************************************************* 

# Import libraries
import pygame
import random
import math

# Initialize the pygame library
pygame.init()

# **************************************** CONSTANTS ****************************************
FPS = 60
WIDTH, HEIGHT = 800, 800
ROWS, COLS = 4, 4
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS
OUTLINE_COLOR = (187,173,160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205,192,180)
FONT_COLOR = (119,110,101)
FONT = pygame.font.SysFont('comicsans', 60, bold=True)
MOVE_VELOCITY = 20

# Create the window that will be used in the game
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")

# **************************************** CLASSES ****************************************
# Defining a class for a tile on the board
class Tile:
    # All of the colors that are used for the number tiles in the game
    COLORS = [
        (237,229,218),
        (238,225,201),
        (243,178,122),
        (246,150,101),
        (247,124,95),
        (247,95,59),
        (237,208,115),
        (237,204,99),
        (236,202,80),
    ]

    # Constructor for the tile
    def __init__(self, value, row, col):
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH
        self.y = row * RECT_HEIGHT

    # Method to get the color of the tile
    def get_color(self):
        # Choose the color index value using a log base 2 equation, minus one for computer 0 indexing
        color_index = int(math.log2(self.value)) -1 
        color = self.COLORS[color_index]
        return color

    # Method to draw the tile
    def draw(self, window):
        color = self.get_color()
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    # Method to set the position of the tile
    def set_pos(self, ceil=False):
        if ceil:
            # Calculate which row and column the tile is in by dividing current x and y values by tile
            # dimensions - then rounding the values to the nearest integer
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    # Method to move the tile
    def move(self, delta):
        self.x += delta[0]
        self.y += delta[1]

# **************************************** FUNCTIONS ****************************************

# Function to draw the grid on the game screen
def draw_grid(window):
    # Loop through all the rows and columns and draw the grid lines
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    # Draw the border of the game
    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)

# Function to draw the game board
def draw(window, tiles):
    # Draw the background
    window.fill(BACKGROUND_COLOR)

    # Draw all the tiles on the board
    for tile in tiles.values():
        tile.draw(window)

    # Draw the grid
    draw_grid(window)

    # Update the display
    pygame.display.update()

# Function to get a random row and column position that is not currently occupied by a tile
def get_random_pos(tiles):
    row = None
    col = None
    # Loop through all the tiles on the board
    while True:
        # Generate random row and column values
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        # Check if the tile is already in the dictionary of tiles and break the loop if it isn't
        if f"{row}{col}" not in tiles:
            break

    return row, col

# Function to move tiles, merge tiles, and handle the movement animation
def move_tiles(window, tiles, clock, direction):
    updated = True
    blocks = set()

    # Conditions for each direction of movement that the user can choose
    # Declare all of the lambda functions specifically for each direction and set the variable values for
    # each direction - these will all plug into the while loop below
    # Moving left or right will check and work with x values
    # Moving up or down will check and work with y values

    # Move tiles left
    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VELOCITY, 0) # Negative move velocity for left direction
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VELOCITY
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VELOCITY
        ceil = True # Rounding up when moving left

    # Move tiles right
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VELOCITY, 0) # Positive move velocity for right direction
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VELOCITY
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VELOCITY < next_tile.x
        ceil = False # Rounding down when moving right
        
    # Move tiles up
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0,-MOVE_VELOCITY) # Negative move velocity for up direction
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VELOCITY
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VELOCITY
        ceil = True # Rounding up when moving up

    # Move tiles down
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0,MOVE_VELOCITY) # Poitive move velocity for up direction
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VELOCITY
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VELOCITY < next_tile.y 
        ceil = False # Rounding down when moving down

    # While the tiles are 
    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        # Loop through all the tiles on the board after they have been sorted
        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            # Get the next tile in the direction that we are moving
            next_tile = get_next_tile(tile)
            # If there is no tile we simply move
            if not next_tile:
                tile.move(delta)
            # If there is a next tile and value is the same and it isn't already in the blocks set
            elif tile.value == next_tile.value and tile not in blocks and next_tile not in blocks:
                # Move the tile to the next tile and overlap it
                if merge_check(tile, next_tile):
                    tile.move(delta)            
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            
            # Call the move check function to see when the block has reached a boundary
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            # Set the position of the tile to the row and column it is in
            tile.set_pos(ceil)
            
            # Set the updated boolean to true so that the while loop continues
            updated = True

        # Update the tiles on the board to match the sorted tiles from within the while loop
        update_tiles(window, tiles, sorted_tiles)

    # End the current move and return the state of the game board
    return end_move(tiles)

# Check to see if the game is over
def end_move(tiles):
    # If every block on the board has a tile in it at the current state of the game
    if len(tiles) == 16:
        return "lost"

    # Get a random block brough into the game in order to continue playing
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"

# Function to update the tiles on the board to match the sorted tiles from the move tiles function
def update_tiles(window, tiles, sorted_tiles):
    # Clear the dictionary of the old tiles
    tiles.clear()
    # Loop through the given list of sorted tiles and add them to the dictionary of tiles
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    # Draw the tiles on the board
    draw(window, tiles)

# Function to generate random tiles for the start of the game
def generate_tiles():
    tiles = {}
    for _ in range(2):
        # Generate a random row and column to place tiles inside of then instantiate a tile with value 2
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles

# Main function of the program
def main(window):
    clock = pygame.time.Clock()
    run = True

    # Create a dictionary of tiles and set the key to the x and y values for the tile's location
    tiles = generate_tiles()

    # Main program loop that will constantly update as the game runs
    while run:
        clock.tick(FPS)

        # Loop through all the events that occur, check the event, and handle it
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Check for different key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                move_tiles(window, tiles, clock, "left")
            elif event.key == pygame.K_RIGHT:
                move_tiles(window, tiles, clock, "right")
            elif event.key == pygame.K_UP:
                move_tiles(window, tiles, clock, "up")
            elif event.key == pygame.K_DOWN:
                move_tiles(window, tiles, clock, "down")
        
        # Create the game window using the draw() function
        draw(window, tiles)
    
    # Exit the program
    pygame.quit()

if __name__ == '__main__':
	main(WINDOW)
