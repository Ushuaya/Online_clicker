import pygame as pg
from .__init__ import Game
import sys

if __name__ == "__main__":
    pg.init()
    pg.mixer.init()
    
    Game()
    pg.quit()
    sys.exit(0)
