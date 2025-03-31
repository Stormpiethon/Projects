import curses
from curses import wrapper
import time
import random

# Function to access the terminal screen
def start_screen(stdscr):
    # Clear the terminal screen
    stdscr.clear()
    # Display text to welcome the user to the program and instruct for keypress to continue
    stdscr.addstr(" *** Welcome to the typing speed test! ***")
    stdscr.addstr("\n          Press any key to begin.")
    stdscr.refresh()
    stdscr.getkey()


# Function to handle displaying the target text and typed text
def display_text(stdscr,target,current,wpm= 0):
    stdscr.addstr(target)
    stdscr.addstr(1,0,f"WPM: {wpm}")

    # Display the current text over the target text in the terminal in a different color
    for i, char in enumerate(current):
        correct_char = target[i]
        color = curses.color_pair(1)
        if char != correct_char:
            color = curses.color_pair(2)
        stdscr.addstr(0,i,char,color)


# Function to retrieve a random sentence from a text file to display as target text for the program
def load_text():
    with open("WPMsentences.txt","r") as f:
        lines = f.readlines()
        return random.choice(lines).strip()

    
# Function to display the text that the user will be typing for the wpm test
def wpm_test(stdscr):
    # Display the text that the user will attempt to type
    target_text = load_text()
    # Save user input into a list of characters to compare to the target text
    current_text = []
    wpm = 0
    # Set a time anchor to reference as a starting point when measuring wpm
    start_time = time.time()
    # Set the program to loop even when the user isn't typing - display decreasing wpm during downtime
    stdscr.nodelay(True)

    # Loop the collection of user input and adding the character to the list of current text
    while True:
        # max function of division between start time and current time so anything less than 1 returns 1
        time_elapsed = max(time.time() - start_time,1)
        # Calculating wpm from (characters per minute) / 5 to represent the average length word
        wpm = round((len(current_text) / (time_elapsed/60))/5)

        stdscr.clear()
        # function call to display text
        display_text(stdscr,target_text,current_text,wpm)
        stdscr.refresh()

        # Combine the characters from the current_text list into a string
        if "".join(current_text) == target_text:
            stdscr.nodelay(False)
            break

        # Try block for loops when user input is not received
        try:
            key = stdscr.getkey()
        except:
            continue

        # Check if the user presses the escape key, and exit the program if they do
        # 27 is the ASCII value for the escape button on a keyboard
        if ord(key) == 27:
            break

        # Account for the backspace command so that it deletes previous text from display
        if key in ("KEY_BACKSPACE",'\b','\x7f'):
            if len(current_text) > 0:
                current_text.pop()
        # Add the entered key to the current_text list so long as there is still target text at that index
        elif len(current_text) < len(target_text):
            current_text.append(key)

        
def main(stdscr):
    # Initialize color pairs for text and background of the text
    curses.init_pair(1,curses.COLOR_GREEN,curses.COLOR_BLACK)
    curses.init_pair(2,curses.COLOR_RED,curses.COLOR_BLACK)
    curses.init_pair(3,curses.COLOR_WHITE,curses.COLOR_BLACK)

    # Main program loop
    start_screen(stdscr)
    while True:
        wpm_test(stdscr)
        stdscr.addstr(2,0,"You completed the text! Press any key to continue")
        key = stdscr.getkey()
        # Detect exit key from user after program runs
        if ord(key) == 27:
            break

wrapper(main)