import pygame as pg
from .__init__ import Game

if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    FONT = pg.font.Font(None, 32)
    Game()
    pg.quit()
