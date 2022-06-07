import pygame as pg
from . import Game

if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    Game()
    pg.quit()
