import pygame
from pygame.constants import MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT

pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

ball = pygame.image.load("ball.gif")
ballrect = ball.get_rect()
speed = [1, 1]

while True:
    screen.fill((0, 0, 0))
    ballrect = ballrect.move(speed)

    if ballrect.left < 0 or ballrect.right > width:
        speed[0] = -speed[0]
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]

    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            print("Mouse down! vvvvv")
        elif event.type == MOUSEBUTTONUP:
            print("Mouse wheel!  ^^^ ")
        elif event.type == QUIT:
            pygame.quit()

    screen.blit(ball, ballrect)
    pygame.display.flip()
