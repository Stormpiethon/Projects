import pygame
import random
import math
pygame.init()

# **************************************** Display visualizer ****************************************
# Class that contains the display details of the program
class DrawInformation:
    # Colors, in RGB value, defined for use in the display
    BLACK = 0,0,0
    WHITE = 255,255,255
    GREEN = 0,255,0
    RED = 255,0,0
    BACKGROUND_COLOR = WHITE

    # 3 Different shades of gray to be used when displaying the different columns
    GRADIENTS = [(128,128,128),(160,160,160),(192,192,192)]

    # Set the fonts for the display window
    FONT = pygame.font.SysFont('comicsans', 20)
    LARGE_FONT = pygame.font.SysFont('comicsans', 30)

    # Padding on the display window from the edge to allow room for text etc.
    SIDE_PAD = 100
    TOP_PAD = 150

# Initialization function to set up the window that will be showing the visualizer
    def __init__(self,width,height,lst):
        self.width = width
        self.height = height
        self.window = pygame.display.set_mode((width,height))
        pygame.display.set_caption("Sorting Algorithm Visualizer")
        self.set_list(lst)

# Function to display the list of numbers that will be sorted
    def set_list(self,lst):
        self.lst = lst
        self.min_val = min(lst)
        self.max_val = max(lst)

        # Setting the width and height of each column on the visualizer based on the number of items in
        # the list, and the value of each item.
        self.block_width = round((self.width - self.SIDE_PAD) / len(lst))
        self.block_height = math.floor((self.height - self.TOP_PAD) / (self.max_val - self.min_val))
        self.start_x = self.SIDE_PAD//2

# **************************************** Draw on the window ****************************************
# Function to draw and create the base window that will be used for the visualizer
def draw(draw_info, algo_name, ascending):
    # fill the window with one color to reset it
    draw_info.window.fill(draw_info.BACKGROUND_COLOR)

    # Text to display the controls of the program
    # Center the text location horizontally by subtracing half the length of the 'controls' text from the width of the window, the y value is hard coded
    title = draw_info.FONT.render(f"{algo_name} - {'Ascending' if ascending else 'Descending'}", 1, draw_info.BLACK)
    draw_info.window.blit(title, (draw_info.width/2 - title.get_width()/2, 5))
    controls = draw_info.FONT.render("R - Reset | SPACE - Start Sorting | A - Ascending | D - Descending", 1, draw_info.BLACK)
    draw_info.window.blit(controls, (draw_info.width/2 - controls.get_width()/2, 40))
    sorting = draw_info.FONT.render("I - Insertion Sort | B - Bubble Sort", 1, draw_info.BLACK)
    draw_info.window.blit(sorting, (draw_info.width/2 - sorting.get_width()/2, 65))

    draw_list(draw_info)
    pygame.display.update()

# Function to draw the columns in correlation to the values that they represent from the list
def draw_list(draw_info, color_positions={}, clear_bg=False):
    # Shorten the representation of the list attribute of the draw_info object
    lst = draw_info.lst

    # Clearing the area of the columns to prepare for new display during sort
    if clear_bg:
        clear_rect = (draw_info.SIDE_PAD//2, draw_info.TOP_PAD, draw_info.width - draw_info.SIDE_PAD, draw_info.height - draw_info.TOP_PAD)
        pygame.draw.rect(draw_info.window, draw_info.BACKGROUND_COLOR, clear_rect)

    # Loop that will access the index as well as the value stored within that index of the list
    for i, val in enumerate(lst):
        # Designate the starting x coordinate of the space to draw the list columns
        # Each time the loop iterates the x value will increase to wherever the next column starts
        x = draw_info.start_x + i * draw_info.block_width

        # The y-coordinate depends on the value of the element that it represents
        # Subtracting the minimum value from the actual value of the element will show how much larger the current value is
        y = draw_info.height - (val - draw_info.min_val) * draw_info.block_height

        # Selecting column color with 1 mod 3 return for each value
        color = draw_info.GRADIENTS[1 % 3]

        # Change the color of the values that are being swapped:
        if i in color_positions:
            color = color_positions[i]

        # Create the rectangle to represent the value on screen at the x and y coordinate
        pygame.draw.rect(draw_info.window, color, (x, y, draw_info.block_width, draw_info.height))

    if clear_bg:
        pygame.display.update()

# **************************************** Generate starting list ****************************************
# Function to generate random values within a given range and append them to the list to be sorted
def generate_starting_list(n,min_val,max_val):
    lst = []
    # Iterate through the list a given number of times to generate random numbers
    for _ in range(n):
        val = random.randint(min_val,max_val)
        lst.append(val)
    return lst

# Sorting algorithm that is also a generator due the the 'yield' keyword within it
def bubble_sort(draw_info, ascending=True):
    lst = draw_info.lst

    # Iterate through the length of the list and store 2 numbers to be compared through each iteration
    for i in range(len(lst)-1):
        for j in range(len(lst) - 1 - i):
            num1 = lst[j]
            num2 = lst[j + 1]

            # Conditions in which the sorting algorithm will execute and the action to execute
            if (num1 > num2 and ascending) or (num1 < num2 and not ascending):
                lst[j], lst[j+1] = lst[j+1], lst[j]
                draw_list(draw_info, {j:draw_info.GREEN, j+1:draw_info.RED}, True)

                # Yielding allows the execution of this function to be paused in case the user pushes a button
                # Without yielding, the function would keep complete control of the program during runtime
                yield True
    return lst

# Insertion sort function
def insertion_sort(draw_info, ascending=True):
    lst = draw_info.lst

    for i in range(1, len(lst)):
        current = lst[i]

        # Setting conditions for the sorting algorithm based on wether it is ascending or descending
        while True:
            ascending_sort = i > 0 and lst[i-1] > current and ascending
            descending_sort = i > 0 and lst[i-1] < current and not ascending

            if not ascending_sort and not descending_sort:
                break
            
            # Move the iterator over one space in the list and assign the new value to the 'current' variable
            lst[i] = lst[i - 1]
            i = i - 1
            lst[i] = current
            draw_list(draw_info, {i - 1: draw_info.GREEN, i: draw_info.RED}, True)
            yield True
    return lst
        
# **************************************** Main function ****************************************
def main():
    run = True
    clock = pygame.time.Clock()

    # Variables holding values for the list generation function
    n = 50
    min_val = 1
    max_val = 100

    # Generate the starting list
    lst = generate_starting_list(n, min_val, max_val)
    # Generate the display window with height and width parameters
    draw_info = DrawInformation(800,600,lst)
    sorting = False
    ascending = True

    # Variables to store information about the sorting algorithm that is being used
    sorting_algorithm = bubble_sort
    sorting_algo_name = "Bubble Sort"
    sorting_algo_generator = None

    while run:
        clock.tick(45)

        # Try to iterate the sorting function again until the next() function returns an exeption
        if sorting:
            try:
                next(sorting_algo_generator)
            except StopIteration:
                sorting = False
        else:
            draw(draw_info, sorting_algo_name, ascending)

        pygame.display.update()

        # Track all the events that occur and implement a loop break if the program is exited or quit
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type != pygame.KEYDOWN:
                continue
            if event.key == pygame.K_r:
                lst = generate_starting_list(n, min_val, max_val)
                draw_info.set_list(lst)
            elif event.key == pygame.K_SPACE and sorting == False:
                sorting = True
                sorting_algo_generator = sorting_algorithm(draw_info, ascending)
            elif event.key == pygame.K_a and not sorting:
                ascending = True
            elif event.key == pygame.K_d and not sorting:
                ascending = False
            elif event.key == pygame.K_i and not sorting:
                sorting_algorithm = insertion_sort
                sorting_algo_name = "Insertion Sort"
            elif event.key == pygame.K_b and not sorting:
                sorting_algorithm = bubble_sort
                sorting_algo_name = "Bubble Sort"

    pygame.quit()

if __name__ == "__main__":
    main()
