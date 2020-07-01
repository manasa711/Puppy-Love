import pygame
from pygame import mixer
import random
import math

# Initializing pygame
pygame.init()

# Display screen
screen = pygame.display.set_mode((800,600))

#Background Image
background = pygame.image.load('./Backgrounds/Background.png')

# Score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

#Gameover Background and Font
gameover_bg = pygame.image.load('./Backgrounds/Background_Heart.png')
game_over_font = pygame.font.Font('freesansbold.ttf', 72)

#Background Music
mixer.music.load("./Music/bensound-jazzyfrenchy.wav")
mixer.music.play(-1)

# Caption and icon
pygame.display.set_caption("Puppy Love")
icon = pygame.image.load('./Original_Images_512px/Icon_Puppy.PNG')
pygame.display.set_icon(icon)

# Player Puppy
puppy_image = pygame.image.load('./Icons/player_puppy_128.png')
puppy_x = 350
puppy_y = 450
puppy_x_change = 0

# Heart
heart_image = pygame.image.load('./Icons/Heart_70.png')
heart_x = 0
heart_y = 450
heart_x_change = 0
heart_y_change = 10
heart_state = "ready"

# Things dogs love
ball = pygame.image.load('./Icons/Ball_100.png')
dog_bone = pygame.image.load('./Icons/dog_bone_100.png')
dog_food = pygame.image.load('./Icons/dog_food_100.png')

# Things dogs hate
cat = pygame.image.load('./Icons/Cat_100.png')
noise = pygame.image.load('./Icons/noise_100.png')

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

def displayText(surface, text, size, x, y, color):
    font_name = pygame.font.match_font('arial')
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

def displayScore(x,y):
    score = font.render("SCORE: "+str(score_value), True, (0,0,0))
    screen.blit(score, (x,y))

def show_go_screen(screen,score_value):

    displayText(screen, "PUPPY LOVE", 72, 200, 280, (255,255,255))
    displayText(screen, "Use right and left arrow keys to move \n Use Space to give love", 36, 200, 350, (255,255,255))
    displayText(screen, "Press any KEY to begin", 36, 200, 400, (255,255,255))
    pygame.display.flip()
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.QUIT()
            elif event.type == pygame.KEYDOWN:
                waiting = False

def game_over_text():
    global game_over_font
    over_text = game_over_font.render("GAME OVER", True, (0, 0, 0))
    screen.blit(over_text, (200, 250))


#Game Loop
game_over = False
running = True
while running:

    if game_over:
        for j in range(num_things):
            thing_y[j] = 2000
        puppy_y = 2000
        game_over_text()
        pygame.time.wait(5000)
        break

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
                    bark = mixer.Sound('./Music/bark.wav')
                    bark.play()
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
                score_sound = mixer.Sound('./Music/shooting_star.wav')
                score_sound.play()
                score_value += 1
            elif love_hate_list[i] == noise:
                loud_sound = mixer.Sound('./Music/Loud_Bang.wav')
                loud_sound.play()
                game_over = True
            elif love_hate_list[i] == cat:
                cat_sound = mixer.Sound('./Music/Cat.wav')
                cat_sound.play()
                game_over = True
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
