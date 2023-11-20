import turtle
import os
import math
import random

def menu():
     option = input('''--Selecione a dificuldade--
     [1] Fácil
     [2] Médio
     [3] Difícil
     ''')

     global PLAYER_SPEED
     global NUMBER_OF_ENEMIES
     global ENEMY_SPEED
     global BULLET_SPEED
     global ENEMY_BULLET_SPEED
     global ENEMY_BULLETSPEED

     if option == "1":
          PLAYER_SPEED = 20
          NUMBER_OF_ENEMIES = 5
          ENEMY_SPEED = 2
          BULLET_SPEED = 30
          ENEMY_BULLETSPEED = 20
     elif option == "2":
          PLAYER_SPEED = 19
          NUMBER_OF_ENEMIES = 5
          ENEMY_SPEED = 5
          BULLET_SPEED = 28
          ENEMY_BULLETSPEED = 50
     elif option == "3":
          PLAYER_SPEED = 18
          NUMBER_OF_ENEMIES = 5
          ENEMY_SPEED = 30
          BULLET_SPEED = 101
          ENEMY_BULLETSPEED = 70

menu()

wn = turtle.Screen()
wn.bgcolor("black")
wn.title("Space Invaders")

turtle.register_shape("invader.gif")
turtle.register_shape("player.gif")

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

score = 0
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("white")
score_pen.penup()
score_pen.setposition(-290, 280)
scorestring = "Score: %s" % score
score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))
score_pen.hideturtle()

player = turtle.Turtle()
player.color("blue")
player.shape("player.gif")
player.penup()
player.speed(0)
player.setposition(0, -250)
player.setheading(90)
playerspeed = PLAYER_SPEED

number_of_enemies = NUMBER_OF_ENEMIES
enemies = []
for _ in range(number_of_enemies):
    enemies.append(turtle.Turtle())

for enemy in enemies:
     enemy.color("red")
     enemy.shape("invader.gif")
     enemy.penup()
     enemy.speed(0)
     x = random.randint(-200, 200)
     y = random.randint(100, 250)
     enemy.setposition(x, y)

enemyspeed = ENEMY_SPEED

# Create the player's bullet
bullet = turtle.Turtle()
bullet.color("yellow")
bullet.shape("triangle")
bullet.penup()
bullet.speed(0)
bullet.setheading(90)
bullet.shapesize(0.5, 0.5)
bullet.hideturtle()

bulletspeed = BULLET_SPEED
bulletstate = "ready"

# Create the enemy bullets
enemy_bullets = []
for _ in range(number_of_enemies):
     eb = turtle.Turtle()
     eb.color("red")
     eb.shape("triangle")
     eb.penup()
     eb.speed(0)
     eb.setheading(270)
     eb.shapesize(0.5, 0.5)
     eb.hideturtle()
     enemy_bullets.append(eb)

enemy_bullet_speed = ENEMY_BULLETSPEED


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

def move_up():
     y = player.ycor()
     y += playerspeed
     if y > -25:
          y = -25
     player.sety(y)

def move_down():
     y = player.ycor()
     y -= playerspeed
     if y < -280:
          y = -280
     player.sety(y)

def fire_bullet():
     global bulletstate
     if bulletstate == "ready":
          bulletstate = "fire"
          x = player.xcor()
          y = player.ycor() + 10
          bullet.setposition(x, y)
          bullet.showturtle()

def enemy_fire_bullet(enemy):
     global enemy_bullet_speed
     for eb in enemy_bullets:
          if not eb.isvisible():
               x = enemy.xcor()
               y = enemy.ycor()
               eb.setposition(x, y)
               eb.showturtle()
               break


# Check for a collision between two turtles
def is_collision(t1, t2):
     distance = math.sqrt(math.pow(t1.xcor() - t2.xcor(), 2) + math.pow(t1.ycor() - t2.ycor(), 2))
     return distance < 15

turtle.listen()
turtle.onkey(move_left, "Left")
turtle.onkey(move_right, "Right")
turtle.onkey(move_up, "Up")
turtle.onkey(move_down, "Down")
turtle.onkey(fire_bullet, "space")

condition = True
while condition:
     for enemy in enemies:
          x = enemy.xcor()
          x += enemyspeed
          enemy.setx(x)

          if enemy.xcor() > 280 or enemy.xcor() < -280:
               for e in enemies:
                    y = e.ycor()
                    y -= 40
                    e.sety(y)
               enemyspeed *= -1

          if is_collision(bullet, enemy):
               bullet.hideturtle()
               bulletstate = "ready"
               bullet.setposition(0, -400)
               x = random.randint(-200, 200)
               y = random.randint(100, 250)
               enemy.setposition(x, y)
               score += 10
               scorestring = "Score: %s" % score
               score_pen.clear()
               score_pen.write(scorestring, False, align="left", font=("Arial", 14, "normal"))

          if is_collision(player, enemy):
               enemyspeed = 0
               playerspeed = 0
               game_over = turtle.Turtle()
               game_over.speed(0)
               game_over.color("white")
               game_over.penup()
               game_over.setposition(0, 0)
               gameover = "Game Over"
               game_over.write(gameover, False, align="center", font=("Arial", 30, "normal"))
               game_over.hideturtle()
               condition = False
               turtle.done()

          if enemy.ycor() <= -280:
               enemyspeed = 0
               playerspeed = 0
               game_over = turtle.Turtle()
               game_over.speed(0)
               game_over.color("white")
               game_over.penup()
               game_over.setposition(0, 0)
               gameover = "Game Over"
               game_over.write(gameover, True, align="center", font=("Arial", 30, "normal"))
               game_over.hideturtle()
               condition = False
               turtle.done()

          if random.randint(1, 100) == 1:
               enemy_fire_bullet(enemy)
          
              # Verifica a colisão entre o tiro do inimigo e o jogador
          for eb in enemy_bullets:
               if eb.isvisible() and is_collision(player, eb):
                    enemyspeed = 0
                    playerspeed = 0
                    game_over = turtle.Turtle()
                    game_over.speed(0)
                    game_over.color("white")
                    game_over.penup()
                    game_over.setposition(0, 0)
                    gameover = "Game Over"
                    game_over.write(gameover, True, align="center", font=("Arial", 30, "normal"))
                    game_over.hideturtle()
                    condition = False
                    turtle.done()

          if random.randint(1, 100) == 1:
               enemy_fire_bullet(enemy)

     if bulletstate == "fire":
          y = bullet.ycor()
          y += bulletspeed
          bullet.sety(y)

     if bullet.ycor() > 275:
          bullet.hideturtle()
          bulletstate = "ready"

     for eb in enemy_bullets:
          if eb.isvisible():
               y = eb.ycor()
               y -= enemy_bullet_speed
               eb.sety(y)

          if is_collision(player, eb):
               enemyspeed = 0
               playerspeed = 0
               game_over = turtle.Turtle()
               game_over.speed(0)
               game_over.color("white")
               game_over.penup()
               game_over.setposition(0, 0)
               gameover = "Game Over"
               game_over.write(gameover, True, align="center", font=("Arial", 30, "normal"))
               game_over.hideturtle()
               condition = False
               turtle.done()

          if eb.ycor() < -275:
               eb.hideturtle()

# End of the game loop