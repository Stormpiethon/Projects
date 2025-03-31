# Libraries display and physics
import pygame
import pymunk
import pymunk.pygame_util
import math

pygame.init()

WIDTH, HEIGHT = 1000, 800
window = pygame.display.set_mode((WIDTH, HEIGHT))

# Function to calculate distance between two points (pythagoras theorem)
def calculate_distance(p1, p2):
    return math.sqrt((p2[1] - p1[1])**2 + (p2[0] - p1[0])**2)

# Function to calculate angle between two points (arctangent trigonometry)
def calculate_angle(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

# Function to draw the window of the program
def draw(space, window, draw_options, line):
    window.fill((255, 255, 255))
    # Draw the line from the ball to the cursor
    if line:
        pygame.draw.line(window, "black", line[0], line[1], 3)

    space.debug_draw(draw_options)
    pygame.display.update()

# Function to create a structure
def create_structure(space, width, height):
    BROWN = (139, 69, 19, 100)
    # List of all structures to be rendered and their dimensions and colors
    rects = [
        [(600, height - 120), (40, 200), BROWN, 100],
        [(900, height - 120), (40, 200), BROWN, 100],
        [(750, height - 240), (340, 40), BROWN, 150],
    ]

    # Create the structures in the simulation
    for pos, size, color, mass in rects:
        body = pymunk.Body()
        body.position = pos
        shape = pymunk.Poly.create_box(body, size, radius=2)
        shape.color = color
        shape.mass = mass
        shape.elasticity = 0.4
        shape.friction = 0.4
        space.add(body, shape)

# Function to create a pendulum
def create_pendulum(space):
    rotation_center_body = pymunk.Body(body_type=pymunk.Body.STATIC)
    rotation_center_body.position = (300, 300)

    body = pymunk.Body()
    body.position = (300, 300)
    line = pymunk.Segment(body, (0, 0), (255, 0), 3)
    circle = pymunk.Circle(body, 40, (255, 0))
    line.friction = 1
    circle.friction = 1
    line.mass = 30
    circle.mass = 100
    line.elasticity = 0.95
    rotation_center_joint = pymunk.PinJoint(body, rotation_center_body, (0, 0), (0, 0))
    space.add(circle, line, body, rotation_center_joint)

# Add a ball to the space
def create_ball(space, radius, mass, pos):
    body = pymunk.Body(body_type=pymunk.Body.STATIC)
    body.position = pos
    shape = pymunk.Circle(body, radius)
    shape.mass = mass
    shape.elasticity = 0.9
    shape.friction = 0.5
    shape.color = (255, 0, 0, 100)
    space.add(body, shape)
    return shape

# Function to create boundaries of the screen
def create_boundaries(space, width, height):
    # Rectangles to be placed on the borders of the screen
    rects = [
        [(width / 2, height - 10), (width, 20)],
        [(width / 2, 10), (width, 20)],
        [(10, height / 2), (20, height)],
        [(width - 10, height / 2), (20, height)],
    ]

    # Create the boundaries
    for pos, size in rects:
        body = pymunk.Body(body_type=pymunk.Body.STATIC)
        body.position = pos
        shape = pymunk.Poly.create_box(body, size)
        shape.elasticity = 0.4
        shape.friction = 0.5
        space.add(body, shape)

# Run the program
def run(window, width, height):
    run = True
    clock = pygame.time.Clock()
    fps = 60
    dt = 1.0 / fps

    space = pymunk.Space()
    space.gravity = (0.0, 981.0)

    # Add the boundaries
    create_boundaries(space, width, height)
    # Add the structure
    create_structure(space, width, height)
    # Add the pendulum
    create_pendulum(space)

    draw_options = pymunk.pygame_util.DrawOptions(window)

    pressed_pos = None
    ball = None

    # Primary program loop
    while run:
        # Disable the line between the ball and the mouse
        line = None
        # Engage the line only if the mouse button is pressed
        if ball and pressed_pos:
            line = [pressed_pos, pygame.mouse.get_pos()]

        # Handle exit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break
            
            # If there is no ball on screen, when the mouse button is clicked, create one
            if event.type == pygame.MOUSEBUTTONDOWN:
                if not ball:
                    pressed_pos = pygame.mouse.get_pos()
                    ball = create_ball(space, 30, 10, pressed_pos)
                # If there is a ball on screen, when the mouse button is released, apply a force to it
                elif pressed_pos:
                    ball.body.body_type = pymunk.Body.DYNAMIC
                    angle = calculate_angle(*line)
                    force = calculate_distance(*line) * 50
                    fx = math.cos(angle) * force
                    fy = math.sin(angle) * force
                    ball.body.apply_impulse_at_local_point((fx, fy), (0, 0))
                    pressed_pos = None
                # After the ball has been launched, next click removes it from the simulation
                else:                    
                    space.remove(ball, ball.body)
                    ball = None
                                        
        draw(space, window, draw_options, line)
        space.step(dt)
        clock.tick(fps)
    
    pygame.quit()

if __name__ == "__main__":
    run(window, WIDTH, HEIGHT)