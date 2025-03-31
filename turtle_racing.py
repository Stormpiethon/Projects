# 'turtle' module allows for simple 2D graphical animations
import turtle
import time
import random

# Setting up the turtle screen to display our program
WIDTH, HEIGHT = 700, 600
# Possible colors of the turtles that will be racing on the visualizer
COLORS = ['red','green','blue','orange','yellow','black','purple','pink','brown','cyan']

# Function that asks the user how many racers they want to have and checks user input for validity
def get_number_of_racers():
    # Set the initial value of the 'racers' variable to 0
    racers = 0
    # Using a while loop to continue asking the user until given valid input
    while True:
        racers = input("Enter the number of racers (2-10): ")
        # Check to see that the user input was a numerical digit
        if racers.isdigit():
            # Case the user string input into an integer value
            racers = int(racers)
        else:
            # Message to the user that their input was not correct
            print("Input is not numeric... Try Again!")
            # continue will send the program back to the beginning of the while loop
            continue
        # Check to see if the user input is within the range of acceptable values
        if 2 <= racers <= 10:
            return racers
        else:
            # Display message to enter a different value
            # 'continue' is not used here because the loop will already start over if this block executes
            print("Number is not in range (2-10). Try Again")

# function to move the turtles on the screen
def race(colors):
    # Call the 'create_turtles' function and pass the list of colors that was sliced from 'COLORS'
    turtles = create_turtles(colors)

    # Loop moving the turtles on the screen until on of them crosses the finish line
    while True:
        # Iterate through the list of turtles and assign distance to move from a range of random numbers
        for racer in turtles:
            distance = random.randrange(1,20)
            racer.forward(distance)

            # Get the racer position
            x, y = racer.pos()
            # Check if the racer has reached the finish line (Max Y value)
            if y >= (HEIGHT//2) - 10:
                # Use the index value of the current racer to return the color stored at the same index value of the 'colors' list
                return colors[turtles.index(racer)]

# Function to place/position turtles on the screen
def create_turtles(colors):
    # Declare an empty list to store whatever amount of turtles the user has selected
    turtles = []

    # Setting the spacing for the turtles on the screen
    # the X position is calculated by dividing the screen width by the number of turtles, plus one
    # --- so the turtles are evenly displayed between the screen edges and each other
    spacingx = WIDTH // (len(colors) + 1)

    # Iterate through the list of colors that was passed in and create a turtle for each one
    # 'enumerate' returns the index position and the value at that index position
    for i, color in enumerate(colors):
        # Create a turtle object 
        racer = turtle.Turtle()
        # Assign the color that is being iterated over as the color value of the new turtle object
        racer.color(color)
        # Set the shape of the object
        racer.shape('turtle')
        racer.left(90)
        racer.penup()
        # i+1 is so the first turtle doesn't spawn at X position 0, Height is just above the bottom of the screen
        racer.setpos(-WIDTH//2 + (i + 1) * spacingx, -HEIGHT//2 + 20)
        racer.pendown()
        # Add the new object to the list
        turtles.append(racer)

    # return the list of racer objects
    return turtles

# function to initalize the visualer for the program
def init_turtle():
    # Initialize the screen
    screen = turtle.Screen()
    screen.setup(WIDTH, HEIGHT)
    screen.title("Turtle Racing!")

# Call function and store return in the 'racers' variable
racers = get_number_of_racers()
init_turtle()
# Randomize the order of the elements of the 'COLORS' list
random.shuffle(COLORS)
# Create a list that contains the same number of elements from the COLORS list as there are racers
colors = COLORS[:racers]

winner = race(colors)
print(f"The winner is the {winner} turtle.")
time.sleep(5)