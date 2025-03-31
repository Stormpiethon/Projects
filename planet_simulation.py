# This program will display a simulation of the orbit of the 4 closest planets to Sol
import pygame
import math
pygame.init()

# Set up the pygame window
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet Simulation")

# Global constant variables to be used throughout the program
WHITE = (255,255,255)
YELLOW = (255,255,0)
BLUE = (100,149,237)
RED = (188,39,50)
DARK_GREY = (80,78,81)

FONT = pygame.font.SysFont("comicsans", 16)

# Class to define the attributes of a Planet within the simulation
class Planet:
    # Global variable of one Astronomical Unit (distance between Earth and Sol) multiplied by 1k for meters
    AU = 149.6e6 * 1000
    # Gravitational constant
    G = 6.67428e-11
    # Relational scale of distances between Sol and planets for the pixel range of display window
    SCALE = 250 / AU
    # Setting an amount of simulated time to be passed with each cycle of the program loop
    TIMESTEP = 3600 * 24

    def __init__(self,x,y,radius,color,mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        # Boolean to store wether the object is the sun, which will have no orbit
        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        # Velocity associated with the change in x and y position to make a circle
        self.x_vel = 0
        self.y_vel = 0

    # Function to draw the planets on the screen
    def draw(self,win):
        # Scale the x and y values down to fit in the display window
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        if len(self.orbit) > 2:
        # Use each point saved into the 'orbit' list attribute to draw the planet orbit
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                updated_points.append((x,y))

            pygame.draw.lines(win,self.color,False,updated_points)

        pygame.draw.circle(win,self.color,(x,y),self.radius)

        # If the object is not the sun itself, display the distance to the sun in .km
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000,1)}km",1,WHITE)
            win.blit(distance_text,(x-distance_text.get_width()/2,y-distance_text.get_width()/2))

    # Class function that will calculate the attractive force between to planets/objects
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    # Class function that will update the display as the planets orbit the sun
    # Get the total force being exerted on the passed in planet by all planets that are not itself
    def update_position(self,planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            # Calculate the force over x and y using a call to the attraction() function of the given planet
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        # Calculating acceleration of the planet
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Incrementing the x and y velocity
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x,self.y))

# Main function of the program
def main():
    # Event loop for the main portion of the program
    run = True
    # Clock variable to regulate the speed of the program as it loops
    clock = pygame.time.Clock()

    # Initialize the sun
    sun = Planet(0,0,30,YELLOW,1.98892 * 10**30)
    sun.sun = True

    # Initialize 4 planet objects and set the initial velocity of each so they will orbit
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 * 1000 
    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = -47.4 * 1000
    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000

    # Put all planet objects into a single list
    planets = [sun,earth,mars,mercury,venus]

    # Main program loop
    while run:
        clock.tick(60)
        WIN.fill((0,0,0))

        # If the user clicks the exit button change the 'run' variable to False, which will exit the loop
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Iterate through the list of planets and draw each one on the display
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        # Update the simulation display
        pygame.display.update()

    # Close the window and exit the program
    pygame.quit()

main()