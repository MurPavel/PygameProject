from levels import *
import pygame


pygame.init()
pygame.display.set_caption("Spase Adventure")
pygame.display.set_icon(pygame.transform.scale(pygame.image.load("data/icon.ico"), (5, 5)))
WIDTH = 800
HEIGHT = 600
FPS = 30
screen = pygame.display.set_mode((WIDTH, HEIGHT))


if __name__ == "__main__":
    main_menu(screen)
