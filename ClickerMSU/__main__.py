"""__main__..."""

import pygame as pg
from .__init__ import Game
import sys


def main() -> None:
    """Start the game."""
    pg.init()
    pg.mixer.init()
    Game()
    pg.quit()


if __name__ == "__main__":
    main()
    sys.exit(0)
