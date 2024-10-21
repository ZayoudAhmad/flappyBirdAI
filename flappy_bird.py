import pygame
import neat
import time
import os
import random #for randomly placing the height of the tubes

from Bird import Bird
from Pipe import Pipe
from Base import Base
pygame.font.init()

#setting the dimension of my screen
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs", "bg.png")))
WIN_WIDTH = 500
WIN_HEIGHT = 750

STAT_FONT = pygame.font.SysFont("comicsans", 50)

def draw_window(win, bird, pipes, base, score):
    win.blit(BG_IMG, (0,0))

    for pipe in pipes:
        pipe.draw(win)

    text = STAT_FONT.render("Score: " + str(score), 1, (255,255,255))
    win.blit(text, (WIN_WIDTH-10-text.get_width(),10))

    base.draw(win)

    bird.draw(win)
    pygame.display.update()

def draw_text(win, text, font, size, x, y, color):
    font = pygame.font.Font(font, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    win.blit(text_surface, text_rect)

def main():
    bird = Bird(WIN_WIDTH // 2 - Bird.IMGS[0].get_width() // 2, WIN_HEIGHT // 2 - Bird.IMGS[0].get_height() // 2)
    base = Base(WIN_HEIGHT-Base.IMG.get_height() // 3)
    pipes = [Pipe(WIN_WIDTH*1.5)]
    win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    clock = pygame.time.Clock()

    score = 0

    game_state = "waiting"
    run = True
    while run:
        clock.tick(25)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

            if game_state in ["waiting", "game_over"]:
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    if game_state == "waiting":
                        game_state = "playing"
                    elif game_state == "game_over":
                        # Reset the game elements
                        bird = Bird(WIN_WIDTH // 2 - Bird.IMGS[0].get_width() // 2, WIN_HEIGHT // 2 - Bird.IMGS[0].get_height() // 2)
                        pipes = [Pipe(WIN_WIDTH*1.5)]
                        score = 0
                        game_state = "waiting"

            if game_state == "playing" and event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        if game_state == "waiting":
            win.fill((0, 0, 0))  # Clear the screen
            draw_text(win, "Press SPACE to Start", None, 50, WIN_WIDTH // 2, WIN_HEIGHT // 2, (255, 255, 255))
            pygame.display.update()
            continue

        if game_state == "game_over":
            draw_text(win, f"You Lost! Score: {score}", None, 50, WIN_WIDTH // 2, WIN_HEIGHT // 2, (255, 0, 0))
            draw_text(win, "Press SPACE to Restart", None, 30, WIN_WIDTH // 2, WIN_HEIGHT // 2 + 50, (255, 255, 255))
            pygame.display.update()
            continue

        bird.move()
        base.move()

        add_pipe = False
        rem = []
        for pipe in pipes:
            if pipe.collide(bird):
                game_state = "game_over"

            if pipe.x + pipe.PIPE_TOP.get_width() < 0:
                rem.append(pipe)

            if not pipe.passed and pipe.x < bird.x:
                pipe.passed = True
                add_pipe = True

            pipe.move()

        if add_pipe:
            score += 1
            pipes.append(Pipe(WIN_WIDTH*1.25))

        for r in rem:
            pipes.remove(r)

        if bird.y + bird.img.get_height() >= (WIN_HEIGHT-Base.IMG.get_height() // 3):
            game_state = "game_over"

        draw_window(win, bird, pipes, base, score)

main()