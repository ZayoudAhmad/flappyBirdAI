import pygame
import neat
import time
import os
import random #for randomly placing the height of the tubes

from Bird import Bird
from Pipe import Pipe
from Base import Base

#setting the dimension of my screen
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
WIN_WIDTH = 500
WIN_HEIGHT = 750

def draw_window(win, bird, pipes, base):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    base.draw(win)

    bird.draw(win)
    pygame.display.update()

def main():
    bird = Bird(WIN_WIDTH // 2 - Bird.IMGS[0].get_width() // 2, WIN_HEIGHT // 2 - Bird.IMGS[0].get_height() // 2)
    base = Base(WIN_HEIGHT-Base.IMG.get_height() // 3)
    pipes = [Pipe(WIN_WIDTH*1.5)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()
    pipe = Pipe(WIN_WIDTH)

    run = True
    while run:
        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
        #bird.move()
        base.move()
        for pipe in pipes:
            pipe.move()
        draw_window(win, bird, pipes, base)
    pygame.quit()
    quit()

main()