import pygame
import os
from grid import Grid

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (100,50)
surface = pygame.display.set_mode((1200,810))
pygame.display.set_caption("Sodoku")

pygame.font.init()
game_font = pygame.font.SysFont('comicsans', 40)
restart_font = pygame.font.SysFont('comicsans', 20)

grid = Grid(pygame,game_font)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and not grid.win:
            if pygame.mouse.get_pressed()[0]:
                position = pygame.mouse.get_pos()
                grid.get_mouse_click(position[0],position[1])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and grid.win:
                grid.restart()
    surface.fill((0, 0, 0))

    grid.draw_all(pygame,surface)
    if grid.win:
        won_surface = game_font.render("You Win!",False,(0,255,0))
        surface.blit(won_surface,(900,650))
        press_supace_text = restart_font.render("Press SPACE to restart",False,(0,255,200))
        surface.blit(press_supace_text,(900,700))
    
    pygame.display.flip()