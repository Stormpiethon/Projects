# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
# Alexander Brittain
# Basic snake game using Tkinter and Python
# +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

from tkinter import *
import random

# Global variables that will be constant but are 
GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 25
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"


# Class to handle the snake object in the game
class Snake:
    # Initialization
    def __init__(self):
        # attributes
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Create the snake body by appending coordinates to the list
        for i in range(0,BODY_PARTS):
            self.coordinates.append([0,0])

        # Draw a square for each body part of the snake on the game window
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)


# Class to handle the food object in the game
class Food:
    # Initialization
    def __init__(self):
        # Select a random location to place the Food within the display window range as coordinates
        x = random.randint(0, (GAME_WIDTH / SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT / SPACE_SIZE) - 1) * SPACE_SIZE

        self.coordinates = [x,y]

        # Create an oval shape on the display at the random coordinates
        canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    # Create a list to hold the coordinate pairs of the snake in each element
    x, y = snake.coordinates[0]

    # Increment or decrement the x or y value in correlation to the direction of the snake
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert the changed x and y values back into the list
    snake.coordinates.insert(0, (x,y))

    # Draw the snake at the new location
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")

    # Add the other body square to the list 
    snake.squares.insert(0, square)

    # If the snake coordinates at the 0 index (head) overlap the coordinates for the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        # Update label for the game, remove the food item from the display, create a new Food object
        label.config(text="Score:{}".format(score))
        canvas.delete("food")
        food = Food()
    else:
        # Delete the last coordinate pair from the lists to show the tail of the snake
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    if check_collisions(snake):
        game_over()
    else:
        # Update function for program display to the next turn
        window.after(SPEED, next_turn, snake, food)


# Function to change the direction of the snake
def change_direction(new_direction):
    
    global direction

    # Logic checks to make sure the player cannot reverse direction
    if new_direction == 'left':
        if direction != 'right':
            direction = new_direction 
    if new_direction == 'right':
        if direction != 'left':
            direction = new_direction 
    if new_direction == 'up':
        if direction != 'down':
            direction = new_direction 
    if new_direction == 'down':
        if direction != 'up':
            direction = new_direction 

# Detect if the snake collides with a wall or itself
def check_collisions(snake):
    # Extract coordinates from the snake obejct that was passed in
    x, y = snake.coordinates[0]

    # Compare the x coordinate value to be within the boundaries of the game window width
    if x < 0 or x >= GAME_WIDTH:
        return True
    # Compare the y coordinate value with the height of the game window
    elif y < 0 or y >= GAME_HEIGHT:
        return True

    # Compare the current coordinates with any in the list of body part coordinates
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

    return False

# Function to end the game
def game_over():
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=('consolas', 70), text = "GAME OVER", fill="red", tag="game over")


# Initialize the Tkinter window
window = Tk()
window.title("Snake Game")
window.resizable(False,False)

# Label to display information to the user and update the information as the program plays
score = 0
direction = "down"
label = Label(window, text="Score:{}".format(score), font=("consolas", 40))
label.pack()

# Add attributes to the display
canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Save the pc window size information to reference for the program display window
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()

# Assign the center of the screen to coordinate values
x = int((screen_width/2) - (window_width/2))
y = int((screen_height/2) - (window_height/2))

# Place the run window of the program on the pc window
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Handle the button press events that can occur in the program
window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

# Initialize objects of the classes 
snake = Snake()
food = Food()

# Call the next turn function to begin the game loop
next_turn(snake, food)

window.mainloop()