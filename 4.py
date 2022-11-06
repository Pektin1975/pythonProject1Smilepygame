import pygame
from pygame.draw import *
from random import randint
pygame.init()


smile_x=0
smile_y=0
smile_speed=10
FPS = 10
screen = pygame.display.set_mode((800, 600))
scores = 0
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]
speed_x=[]
speed_y=[]
balls=[]
r=[]
smile=pygame.image.load('smile.png').convert()
smile_box=smile.get_rect()
def new_balls():             #zdes sozdaytsya balls i dvigayutsya
    global x, y, r,speed_x,speed_y,balls
    for i in range(5):
        x = randint(100, 700)
        y = randint(100, 500)
        r.append(randint(30, 50))
        speed_x.append(randint(20,30))
        speed_y.append(randint(20,30))
        balls.append([x, y])
        color = COLORS[randint(0, 5)]
        circle(screen, COLORS[i], (balls[i]), r[i])
        balls[i][1]+=speed_y[i]
        balls[i][0] += speed_x[i]
        if balls[i][0]+r[i]>=800:
            speed_x[i]=speed_x[i]*(-1)
        if balls[i][0]-r[i]<=0:
            speed_x[i]=speed_x[i]*(-1)
        if balls[i][1]-r[i]<=0:
            speed_y[i]=speed_y[i]*(-1)
        if balls[i][1]+r[i]>=600:
            speed_y[i]=speed_y[i]*(-1)
def Smile():#risuem smilij s ego dvizh
    global smile,smile_x,smile_y,smile_speed
    screen.blit(smile, (smile_x, smile_y))
    smile_y += smile_speed * 3 / 5
    smile_x += smile_speed
    if smile_x + 190 >= 800:
        smile_speed = smile_speed * (-1)
    if smile_x <= 0:
        smile_speed = smile_speed * (-1)
def SmileClick(event):
    global scores
    if (abs(event.pos[0]-smile_x)<=smile_box[2]) and (abs(event.pos[1]-smile_y)<=smile_box[3]):
        scores+=2
        print("popal po smilik")
        return scores

def click(event): #podschet ochkov
    global scores

    for i in range(5):
        if((balls[i][0]-event.pos[0])**2+(balls[i][1]-event.pos[1])**2)<=r[i]**2:
            scores += 1
            return scores
def click2(event): # usloviye na popdanyie po figure
    for i in range(5):
        if((balls[i][0]-event.pos[0])**2+(balls[i][1]-event.pos[1])**2)<=r[i]**2:
            return True

pygame.display.update()
clock = pygame.time.Clock()

finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:

            print('Click!', 'scores=', scores)
            click(event)  #podschet ochkov po click
            SmileClick(event)# podschet ochkov po smile
            if click2(event)==True:  #esli popal chto-to sdelat
                new_balls()

                print("popal po sharik")
                pygame.display.update()
    new_balls()
    Smile()


    pygame.display.update()

    screen.fill(BLACK)
pygame.quit()