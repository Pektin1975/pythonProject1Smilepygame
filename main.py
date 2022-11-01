import pygame
from pygame.draw import *

pygame.init()

FPS = 30
screen = pygame.display.set_mode((400, 400))
y1=150
circle(screen, (255,255,153), (200, 175), 70)
rect(screen,(100,0,0),(165,210,70,10),5 )
circle(screen,(255,0,0),(220,150),13)
circle(screen,(255,0,0),(180,150),13)
circle(screen,(0,0,0),(220,150),5)
circle(screen,(0,0,0),(180,150),5)
line(screen,(0,0,0) , (220+20, y1-40+15), (180+20, y1-20+15),7)
line(screen,(0,0,0) , (180-20-10, y1-40+15-2), (220-20-10, y1-20+15-2),7)
pygame.display.update()
clock = pygame.time.Clock()
finished = False

while not finished:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True

pygame.quit()