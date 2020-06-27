import pygame
from pygame import mixer
import random
import math

# Initializing pygame
pygame.init()

# Display screen
screen = pygame.display.set_mode((800,600))

#Background Image
background = pygame.image.load('Background.png')

#Background Music

# Caption and icon
pygame.display.set_caption("Puppy Love")
icon = pygame.image.load('Icon_Puppy.PNG')
pygame.display.set_icon(icon)

# Player Puppy
puppy_image = pygame.image.load('player_puppy_128.png')
puppy_x = 350
puppy_y = 450
puppy_x_change = 0

# Heart
heart_image = pygame.image.load('Heart_70.png')
heart_x = 0
heart_y = 450
heart_x_change = 0
heart_y_change = 10
heart_state = "ready"

# Things dogs love
ball = pygame.image.load('Ball_100.png')
dog_bone = pygame.image.load('dog_bone_100.png')
dog_food = pygame.image.load('dog_food_100.png')

# Things dogs hate
cat = pygame.image.load('Cat_100.png')
noise = pygame.image.load('noise_100.png')

love_hate_list = [ball,dog_bone,dog_food,cat,noise]
thing_x = []
thing_y = []
thing_x_change = []
thing_y_change = []
num_things = len(love_hate_list)

for i in range(num_things):
    thing_x.append(random.randint(0,736))
    thing_y.append(random.randint(50, 150))
    thing_x_change.append(random.randint(5,15))
    thing_y_change.append(40)

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

game_over_font = pygame.font.Font('freesansbold.ttf', 64)

def player_puppy(x,y):
    screen.blit(puppy_image,(x,y))

def thing(x,y,i):
    screen.blit(love_hate_list[i],(x,y))

def give_heart(x,y):
    global heart_state
    heart_state = "fire"
    screen.blit(heart_image,(x + 25, y + 10))

def collide(thing_x, thing_y, heart_x, heart_y):
    distance = math.sqrt(math.pow(thing_x - heart_x,2) + (math.pow(thing_y - heart_y,2)))
    if distance < 30:
        return True
    else:
        return False

def displayScore(x,y):
    score = font.render("SCORE: "+str(score_value), True, (0,0,0))
    screen.blit(score, (x,y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (200, 250))

# Game Loop
running = True
while running:

    screen.fill((0, 0, 0)) #black
    screen.blit(background,(0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keystrokes
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_LEFT:
            puppy_x_change = -5
        if event.key == pygame.K_RIGHT:
            puppy_x_change = 5
        if event.key == pygame.K_SPACE:
            if heart_state is "ready":
                heart_x = puppy_x
                give_heart(heart_x,heart_y)

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
            puppy_x_change = 0

    # Puppy Movement
    puppy_x += puppy_x_change
    if puppy_x <= 0:
        puppy_x = 0
    elif puppy_x >= 736:
        puppy_x = 736

    # Love Hate Things

    for i in range(num_things):

        thing_x[i] += thing_x_change[i]
        if thing_x[i] <= 0:
            thing_x_change[i] = 8
            thing_y[i] += thing_y_change[i]
        elif thing_x[i] >= 736:
            thing_x_change[i] = -4
            thing_y[i] += thing_y_change[i]

        # determining the collision:
        collision = collide(thing_x[i], thing_y[i], heart_x, heart_y)
        if collision:
            heart_y = 450
            heart_state = "ready"

            if love_hate_list[i] == ball or love_hate_list[i] == dog_bone or love_hate_list[i] == dog_food:
                #play sound woof
                score_value += 1
            elif love_hate_list == noise or love_hate_list == cat:
                game_over_text()
                break
            thing_x[i] = random.randint(0,736)
            thing_y[i] = random.randint(50,150)

        thing(thing_x[i],thing_y[i],i)

    # Heart Movement
    if heart_y <= 0:
        heart_y = 450
        heart_state = "ready"

    if heart_state is 'fire':
        give_heart(heart_x,heart_y)
        heart_y -= heart_y_change

    player_puppy(puppy_x,puppy_y)
    displayScore(10,10)
    pygame.display.update()
