import pygame
pygame.init()

# Global constant variables for the game display
WIDTH, HEIGHT = 700, 500
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Pong")
FPS = 60
WHITE = 255,255,255
BLACK = 0,0,0
RED = 255,0,0
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
BALL_RADIUS = 7
SCORE_FONT = pygame.font.SysFont("comicsans",50)
WINNING_SCORE = 10

# Class to handle the creation and operation of the in-game paddles
class Paddle:
    # Constant attributes of a paddle object
    COLOR = WHITE
    VELOCITY = 4

    # Initialization function for Paddle objects
    def __init__(self,x,y,width,height):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.width = width
        self.height = height

    # Class function to draw the rectangle paddles on the display
    def draw(self,win):
        pygame.draw.rect(win,self.COLOR,(self.x,self.y,self.width,self.height))

    # Change the y coordinate of the paddle in order to move in on the screen
    def move(self,up=True):
        if up:
            self.y -= self.VELOCITY
        else:
            self.y += self.VELOCITY

    # Function to reset the paddle positions when a new game starts
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y

# Class to handle the ball
class Ball():
    MAX_VELOCITY = 5
    COLOR = RED

    # Initialization function for Ball object
    def __init__(self,x,y,radius):
        self.x = self.original_x = x
        self.y = self.original_y = y
        self.radius = radius
        self.x_vel = self.MAX_VELOCITY
        self.y_vel = 0

    # Function to draw the ball on screen
    def draw(self,win):
        pygame.draw.circle(win,self.COLOR,(self.x,self.y),self.radius)

    # Function to move the ball on the screen
    def move(self):
        self.x += self.x_vel
        self.y += self.y_vel

    # Function to reset the position of the ball after a player scores a point
    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.y_vel = 0
        self.x_vel *= -1

# Function to handle on the screen display mechanics
def draw(win,paddles,ball,left_score,right_score):
    win.fill(BLACK)

    # Display the score on the background of the window for the game
    left_score_text = SCORE_FONT.render(f"{left_score}",1,WHITE)
    right_score_text = SCORE_FONT.render(f"{right_score}",1,WHITE)
    win.blit(left_score_text,(WIDTH//4 - left_score_text.get_width()//2,20))
    win.blit(right_score_text,(WIDTH * (3/4) - right_score_text.get_width()//2,20))

    # Display the paddles calling the Paddle class function
    for paddle in paddles:
        paddle.draw(win)

    # Drawing a dashed line across the middle of the screen
    for i in range(10,HEIGHT,HEIGHT//20):
        if i % 2 == 1:
            continue
        pygame.draw.rect(win,WHITE,(WIDTH//2-2,i,4,HEIGHT//20))

    # Display the ball calling the Ball class function
    ball.draw(win)
    pygame.display.update()

# Function that will handle all types of collision between the ball and the game environment
def handle_collision(ball,left_paddle,right_paddle):
    # Reverse the direction of y value of the ball for wall collision
    if ball.y + ball.radius >= HEIGHT:
        ball.y_vel *= -1
    elif ball.y - ball.radius <= 0:
        ball.y_vel *= -1

    # Detect collision with the paddle and reverse the x velocity
    if ball.x_vel < 0: # LEFT
        if ball.y >= left_paddle.y and ball.y <= left_paddle.y + left_paddle.height:
            if ball.x - ball.radius <= left_paddle.x + left_paddle.width:
                ball.x_vel *= -1

                # Detect location of collision with paddle from the center of the paddle rectangle
                middle_y = left_paddle.y + left_paddle.height/2
                difference_in_y = middle_y - ball.y
                # Reduction factor used to get the Y velocity according to collision location with paddle
                reduction_factor = (left_paddle.height/2)/ball.MAX_VELOCITY
                y_vel = difference_in_y/reduction_factor
                ball.y_vel = y_vel * -1

    else: # RIGHT
        if ball.y >= right_paddle.y and ball.y <= right_paddle.y + right_paddle.height:
            if ball.x + ball.radius >= right_paddle.x:
                ball.x_vel *= -1

                # Detect location of collision with paddle from the center of the paddle rectangle
                middle_y = right_paddle.y + right_paddle.height/2
                difference_in_y = middle_y - ball.y
                # Reduction factor used to get the Y velocity according to collision location with paddle
                reduction_factor = (right_paddle.height/2)/ball.MAX_VELOCITY
                y_vel = difference_in_y/reduction_factor
                ball.y_vel = y_vel * -1

# Function to move the paddles depending on the key that is pressed and stops them at screen edge
def paddle_movement(keys,left_paddle,right_paddle):
    # If the key is pressed and the top-left coordinate of the paddle rectangle stays on screen, move up
    if keys[pygame.K_w] and (left_paddle.y-left_paddle.VELOCITY) >= 0:
        left_paddle.move(up=True)
    # Have to consider the paddle's height after starting coordinate to stay on screen moving down
    if keys[pygame.K_s] and (left_paddle.y+left_paddle.VELOCITY+left_paddle.height) <= HEIGHT:
        left_paddle.move(up=False)

    # Right paddle controls and edge detection
    if keys[pygame.K_UP] and (right_paddle.y-right_paddle.VELOCITY) >= 0:
        right_paddle.move(up=True)
    if keys[pygame.K_DOWN] and (right_paddle.y+right_paddle.VELOCITY+right_paddle.height) <= HEIGHT:
        right_paddle.move(up=False)

# Main function of the program
def main():
    # Main while loop that will handle the events from user interaction
    run = True
    clock = pygame.time.Clock()
    # Initialize paddle objects at the center point of the screen with a small adjustment so the middle
    # of the paddle lines up with the middle of the screen with the y value argument passed in
    left_paddle = Paddle(10,HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = Paddle(WIDTH-10-PADDLE_WIDTH ,HEIGHT//2-PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)

    # Initialize the Ball object
    ball = Ball(WIDTH//2,HEIGHT//2,BALL_RADIUS)

    # Variables to use for the scoring system
    left_score, right_score = 0, 0

    # Main loop of the program
    while run:
        # Display FPS to cap program at a certain run speed
        clock.tick(FPS)
        # Call draw function and pass all items that need to be visualized
        draw(WIN,[left_paddle,right_paddle],ball,left_score,right_score)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        # Track the buttons that are pressed while the program is running
        keys = pygame.key.get_pressed()
        # Call function to handle movement of the paddle when coorelated keys are pressed
        paddle_movement(keys, left_paddle, right_paddle)
        # Call the Class function to move the ball at the beginning of the game
        ball.move()
        # call function to detect collision with walls or paddles and redirect the ball
        handle_collision(ball,left_paddle,right_paddle)

        # Detect ball position on the edge of the screen and give a point to the opposite side
        if ball.x < 0:
            right_score += 1
            ball.reset()
        elif ball.x > WIDTH:
            left_score += 1
            ball.reset()

        # When a player wins, change boolean value to True and execute reset block
        won = False
        # Compare score to the WINNING_SCORE
        if left_score >= WINNING_SCORE:
            won = True
            win_text = "*** Left Player Won! ***"
        elif right_score >= WINNING_SCORE:
            won = True
            win_text = "*** Right Player Won! ***"

        # Display text to the screen of the winning side
        if won:
            # Render a drawable object to display text of winning side
            text = SCORE_FONT.render(win_text,1,RED)
            # Display text in the middle of the screen for 5 seconds
            WIN.blit(text,(WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
            pygame.display.update()
            pygame.time.delay(5000)
            # Reset the game
            ball.reset()
            left_paddle.reset()
            right_paddle.reset()
            left_score = 0
            right_score = 0

    pygame.quit()

# Make this program run when called directly from this module
if __name__ == '__main__':
    main()