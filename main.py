import turtle
import random
import csv

# Set up the screen
screen = turtle.Screen()
screen.title("Breakout")
screen.bgcolor("black")
screen.setup(width=800, height=600)
screen.tracer(0)

# Create the paddle
paddle = turtle.Turtle()
paddle.shape("square")
paddle.color("white")
paddle.shapesize(stretch_wid=1, stretch_len=5)
paddle.penup()
paddle.goto(0, -250)

# Create the ball
ball = turtle.Turtle()
ball.shape("circle")
ball.color("white")
ball.penup()
ball.goto(0, 0)
ball.dx = 0
ball.dy = 0

# Create bricks
bricks = []
brick_colors = ["red", "orange", "yellow", "green", "blue"]
for row in range(5):
    for col in range(10):
        brick = turtle.Turtle()
        brick.shape("square")
        brick.color(brick_colors[row])
        brick.shapesize(stretch_wid=1, stretch_len=2)
        brick.penup()
        brick.goto(-370 + col * 80, 250 - row * 25)
        bricks.append(brick)

# Set up the score
score = 0
high_score = 0

# Load high score from CSV
try:
    with open("high_score.csv", "r") as file:
        reader = csv.reader(file)
        for row in reader:
            high_score = int(row[0])
except FileNotFoundError:
    # If the file doesn't exist, start with high score of 0
    high_score = 0

score_display = turtle.Turtle()
score_display.color("white")
score_display.penup()
score_display.goto(-390, 270)
score_display.write("Score: 0  High Score: {}".format(high_score), align="left", font=("Courier", 16, "normal"))

# Set up the game over text
game_over_text = turtle.Turtle()
game_over_text.color("white")
game_over_text.penup()
game_over_text.goto(0, 0)
game_over_text.hideturtle()

# Function to start the game
def start_game(x, y):
    global score
    global high_score

    if ball.dx == 0 and ball.dy == 0:
        # Reset the score
        score = 0

        # Hide the game over text
        game_over_text.clear()
        game_over_text.hideturtle()

        # Reset the ball position
        ball.goto(0, 0)

        # Set the ball's initial direction
        ball.dx = random.choice([-2, 2]) * 0.5  # Decrease the speed by 50%
        ball.dy = -2 * 0.5  # Decrease the speed by 50%

# Mouse button event listener
screen.onscreenclick(start_game, 1)  # Left mouse button

# Function to update the score display
def update_score():
    score_display.clear()
    score_display.write("Score: {}  High Score: {}".format(score, high_score), align="left", font=("Courier", 16, "normal"))

# Functions to move the paddle
def move_paddle_left():
    x = paddle.xcor()
    if x > -350:
        x -= 100
    paddle.setx(x)

def move_paddle_right():
    x = paddle.xcor()
    if x < 350:
        x += 100
    paddle.setx(x)

# Keyboard bindings
screen.listen()
screen.onkeypress(move_paddle_left, "Left")
screen.onkeypress(move_paddle_right, "Right")

# Main game loop
while True:
    screen.update()

    # Move the ball
    ball.setx(ball.xcor() + ball.dx)
    ball.sety(ball.ycor() + ball.dy)

    # Check for ball collision with walls
    if ball.xcor() > 390:
        ball.setx(390)
        ball.dx *= -1
    elif ball.xcor() < -390:
        ball.setx(-390)
        ball.dx *= -1
    if ball.ycor() > 290:
        ball.sety(290)
        ball.dy *= -1

    # Check for ball collision with paddle
    if (ball.ycor() < -240) and (paddle.xcor() - 50 < ball.xcor() < paddle.xcor() + 50):
        ball.sety(-240)
        ball.dy *= -1

    # Check for ball collision with bricks
    for brick in bricks:
        if brick.distance(ball) < 30:
            brick.goto(1000, 1000)
            ball.dy *= -1
            score += 10

            if score > high_score:
                # Update the high score
                high_score = score

                # Save high score to CSV
                with open("high_score.csv", "w", newline="") as file:
                    writer = csv.writer(file)
                    writer.writerow([high_score])

            update_score()

    # Check for game over
    if ball.ycor() < -290:
        game_over_text.write("Game Over", align="center", font=("Courier", 24, "normal"))
        ball.dx = 0
        ball.dy = 0

# Keep the screen open until it is manually closed
turtle.done()
