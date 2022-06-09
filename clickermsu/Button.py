"""Module containing Button class.
source: https://github.com/baraltech/Menu-System-PyGame/blob/main/button.pyS
"""
import pygame.font
from pygame import Surface

WHITE = (255,255,255)
RED = (255,0,0)

class Button():
    def __init__(self, image: Surface, pos: tuple[int], text_input: str, 
                 font_name: str = "freesansbold.ttf", font_size: int = 20,
                 base_color: tuple[int] = WHITE, hovering_color: tuple[int] = RED, tipper: list = None):
        """Create a button."""
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
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        self.tip = tipper

    def update(self, screen: Surface) -> None:
        """Update button image."""
        if self.image is not None:
            screen.blit(self.image, self.rect)
        screen.blit(self.text, self.text_rect)

    def checkForInput(self, position: tuple[int]) -> bool:
        """Check if possition corresponds to button."""
        return self.rect.left <= position[0] <= self.rect.right and\
               self.rect.top <= position[1] <= self.rect.bottom

    def changeText(self, new_text: str) -> None:
        self.text_input = new_text
        self.text = self.font.render(self.text_input, True, self.base_color)
        self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

    def changeColor(self, position: tuple[int], screen: Surface = None) -> None:
        """Change button's text color if position in button's range."""
        if self.checkForInput(position):
            self.text = self.font.render(self.text_input, True, self.hovering_color)
            if self.tip != None: 
                step = 0
                for i in self.tip:
                    text = pygame.font.Font("freesansbold.ttf", 25).render(i, True, (0,0,0), None)
                    screen.blit(text, self.text.get_rect(center=((self.rect.left + self.rect.right)/2, self.y_pos + 80 + step)))
                    step += abs(self.text_rect.top - self.text_rect.bottom)
        else:
            self.text = self.font.render(self.text_input, True, self.base_color)

        