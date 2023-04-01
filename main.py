import turtle
import os
import random
import time
import winsound

# Set up the screen
wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")

# Draw the border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("white")
border_pen.penup()
border_pen.setposition(-300, -300)
border_pen.pendown()
border_pen.pensize(3)
for side in range(4):
    border_pen.fd(600)
    border_pen.lt(90)
border_pen.hideturtle()

# Create the player turtle
player = turtle.Turtle()
player.color("blue")
player.shape("triangle")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)

# Set the player speed
playerspeed = 15

# Set maximum bullets, initialt speed, and score
MAX_BULLETS = 10
bullet_count = 0
BULLET_SPEED = 10
score = 0
player_bullets = []

# Define the score pen
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("red")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(-240, 250)
score_pen.write("Score:", align="center")

# Create the aliens
alien_list = []
position = (250, 250)
for i in range(0,24):
    enemy = turtle.Turtle()
    enemy.color("green")
    enemy.penup()

    enemy.setposition(position)
    enemy.speed(0)
    enemy.setheading(-90)
    alien_list.append(enemy)
    position = (position[0] - 30, position[1])
    if i == 11:
        position = (250, 230)
print(alien_list)

# Set the alien speed
alien_speed = 15


def update_score():
    score_pen.clear()
    score_pen.write(f"Score: {score}", align="center")

update_score()
# Move the player left and right
def move_left():
    x = player.xcor()
    x -= playerspeed
    if x < -280:
        x = -280
    player.setx(x)

def move_right():
    x = player.xcor()
    x += playerspeed
    if x > 280:
        x = 280
    player.setx(x)

def player_shoot():
    if len(player_bullets) >= MAX_BULLETS:
        return
    bullet = turtle.Turtle()
    bullet.hideturtle()
    bullet.color("red")
    bullet.shape("square")
    bullet.penup()
    bullet.speed(0)
    bullet.setposition(player.xcor(), player.ycor())
    bullet.setheading(90)
    bullet.showturtle()
    player_bullets.append(bullet)

    def move_bullet():
        global score
        bullet.sety(bullet.ycor() + 10)

        # check for collision with enemy ships
        for enemy in alien_list:
            if bullet.distance(enemy) < 20:
                enemy.hideturtle()
                bullet.hideturtle()
                alien_list.remove(enemy)
                # increase score
                score += 10
                score_pen.clear()
                score_pen.write(f"Score: {score}", align="center")

        if bullet.ycor() < 300:
            # schedule the next movement of the bullet
            turtle.ontimer(move_bullet, 10)
        else:
            # hide the bullet when it goes off-screen
            bullet.hideturtle()
            player_bullets.remove(bullet)

    # start the bullet movement
    move_bullet()


def alien_shoot():
    global bullet_count

    # limit the number of bullets that an alien can shoot
    if bullet_count >= MAX_BULLETS:
        return

    bullet = turtle.Turtle()
    bullet.hideturtle()
    bullet.color("red")
    bullet.shape("square")
    bullet.penup()
    bullet.speed(0)

    # choose a random alien to shoot
    shooting_alien = random.choice(alien_list)

    # set the bullet's position and direction
    bullet.setposition(shooting_alien.xcor(), shooting_alien.ycor())
    bullet.setheading(-90)
    bullet.showturtle()

    # move the bullet downwards
    while bullet.ycor() > -300:
        bullet.sety(bullet.ycor() - BULLET_SPEED)

        # check for collision with the player
        if bullet.distance(player) < 20:
            player.hideturtle()
            bullet.hideturtle()
            print("Game Over")
            break

        time.sleep(0.01)

    # hide the bullet and update the bullet count
    bullet.hideturtle()
    bullet_count += 1

    # play a sound effect
    winsound.PlaySound("shoot.wav", winsound.SND_ASYNC)



def alien_move():
    global alien_speed
    for alien in alien_list:
        x = alien.xcor()
        x = x + alien_speed
        alien.setx(x)

    if max([alien.xcor() for alien in alien_list]) > 280 or min([alien.xcor() for alien in alien_list]) < -280:
        alien_speed = alien_speed * -1
        for alien in alien_list:
            alien.sety(alien.ycor() - 30)


def game_over():
    for alien in alien_list:
        if alien.ycor() < player.ycor() + 20:
            return True
    return False

def detect_hit():
    pass





# Create keyboard bindings
turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(player_shoot, "space")

# Main game loop
while True:

    #Move alien
    alien_move()
    alien_shoot()
    if game_over():
        print("Game Over")
        break

    # Update the screen
    wn.update()
