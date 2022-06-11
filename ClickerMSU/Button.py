"""Module containing Button class.

Original source: https://github.com/baraltech/Menu-System-PyGame/blob/main/button.pyS
"""
from typing import Any
import pygame.font
from pygame import Surface, Rect

WHITE = (255, 255, 255)
RED = (255, 0, 0)


class Button:
    """Class to create Buttons."""

    def __init__(self, image: Surface, pos: tuple[int], text_input: str,
                 font_name: str = "freesansbold.ttf", font_size: int = 20,
                 base_color: tuple[int] = WHITE, hovering_color: tuple[int] = RED,
                 tipper: list = None):
        """Create a button.

        params:
            image - pg.Surface,
            pos - tuple[int], center's position
            text_input - str,
            font_name - str,
        """
        self.image = image
        self.x_pos = pos[0]
        self.y_pos = pos[1]
        self.font = pygame.font.Font(font_name, font_size)
        self.base_color, self.hovering_color = base_color, hovering_color
        self.text_input = text_input
        self.text = self.font.render(self.text_input, True, self.base_color)
        if self.image is None:
            self.image = self.text
        self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
        self.text_rect = self.text.get_rect(center=self.rect.center)
        self.tip = tipper

    def update(self, screen: Surface) -> None:
        """Update button image.

        params:
            screen -- pg.Surface, main screen of game
        """
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position: tuple[int]) -> bool:
        """Check if possition corresponds to button.

        params:
            position - int, position of mouse
        """
        return self.rect.collidepoint(position)

    def changeText(self, new_text: str) -> None:
        """Change the text of button.

        params:
            new_text - new text to write on button
        """
        self.text_input = new_text
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=self.rect.center)

    def changeColor(self, position: tuple[int], screen: Surface = None) -> None:
        """Change button's text color if position in button's range."""
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            if self.tip is not None:
                step = 0
                for i in self.tip:
                    text = pygame.font.Font("freesansbold.ttf", 25).render(i, True, (0, 0, 0), None)
                    screen.blit(text, self.text.get_rect(center=((self.rect.left + self.rect.right) / 2,
                                self.y_pos + 80 + step)))
                    step += abs(self.text_rect.top - self.text_rect.bottom)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

    def get_rect(self) -> Rect:
        """Try Returns rectangle square of Button."""
        return self.rect

    def set_pos(self, **kwargs: Any) -> None:
        """Set new position for image.

        params:
            kwargs from Surface.get_rect
        """
        self.rect = self.image.get_rect(**kwargs)
        self.text_rect.center = self.rect.center
        self.x_pos, self.y_pos = self.rect.center
