"""Class for creating and placing options."""

import pygame as pg
import pygame_widgets

from .Button import Button
from collections import deque
from pygame_widgets.slider import Slider
from pygame_widgets.textbox import TextBox

WHITE = (255,255,255)


class Option:
    """Base class for options."""
    font_name = "freesansbold.ttf"
    font_size = 32

    _COEF_SPACE_AFTER_NAME = 0.20  

    def __init__(self, option_name: str, pos: tuple[int], name_pic: pg.Surface):
        """Create an object.
        
        params:
            option_name - str, name of the option
            pos - tuple[int], position for start of option (bottomleft of name_pic)
            name_pic - pg.Surface, picture for pannel with option_name
        """
        self.x_pos = pos[0]
        self.y_pos = pos[1]

        self.opt_name = option_name
        self.font = pg.font.Font(self.font_name, self.font_size)
        self.opt_name_text = self.font.render(self.opt_name, True, WHITE)
        self.name_pic = name_pic

    def change_font(self, font_name: str = None, font_size: int = None) -> None:
        """Change font and/or font_size for option's text.
        
        params:
            font_name - str, name of new font, if None - remains the same
            font_size - int, new size, if None - remains the same
        """
        if font_name:
            self.font_name = font_name
        if font_size:
            self.font_size = font_size
        self.font = pg.font.Font(self.font_name, self.font_size)
        self.text = self.font.render(self.opt_name, True)
        return


class Option_switchable(Option):
    """Class for creating switchable option."""
    
    _COEF_SPACE_BETWEEN_SWITCH_AND_VAR = 0.07

    def _make_rectangles(self) -> None:
        """Make rectangles for options."""
        self.rect_name_pic = self.name_pic.get_rect(bottomleft=(self.x_pos, self.y_pos))
        self.rect_opt_name_text = self.opt_name_text.get_rect(center=self.rect_name_pic.center)

        # Space between opt name panel and switch previous button
        shift1 = self.rect_name_pic.width * self._COEF_SPACE_AFTER_NAME  
        # Space between switch buttons and current variant  
        shift2 = self.rect_name_pic.width * self._COEF_SPACE_BETWEEN_SWITCH_AND_VAR

        switch_prev_pos = (self.rect_name_pic.right + shift1, self.y_pos)
        #self.rect_switch_prev = self.switch_prev.get_rect(bottomleft=switch_prev_pos)
        self.switch_prev_button = Button(self.switch_prev_pic, switch_prev_pos, "")
        self.switch_prev_button.set_pos(bottomleft=switch_prev_pos)

        curr_var_pos = (self.switch_prev_button.get_rect().right + shift2, self.y_pos)
        self.rect_curr_var_pic = self.curr_var_pic.get_rect(bottomleft=curr_var_pos)
        self.rect_curr_var_text = self.curr_var_text.get_rect(center=self.rect_curr_var_pic.center)

        switch_next_pos = (self.rect_curr_var_pic.right + shift2, self.y_pos)
        self.switch_next_button = Button(self.switch_next_pic, switch_next_pos, "")
        self.switch_next_button.set_pos(bottomleft=switch_next_pos)

        return

    def __init__(self, option_name: str, pos: tuple[int], name_pic: pg.Surface, 
                 current_var_pic: pg.Surface, switch_prev_pic: pg.Surface, 
                 switch_next_pic: pg.Surface, variants: tuple[str] = None):
        """Create an object.
        
        params:
            option_name - str, name of the option
            pos - tuple[int], position for start of option (bottomleft of name_pic)
            name_pic - pg.Surface, picture for pannel with option_name
            current_var_pic - pg.Surface, picture for pannel with current (selected) variant
            switch_prev_pic - pg.Surface, picture for button for switching to previous variant
            switch_prev_pic - pg.Surface, picture for button for switching to next variant
            variants - tuple[str], possible values
        """
        super().__init__(option_name, pos, name_pic)
        self.switch_prev_pic = switch_prev_pic
        self.curr_var_pic = current_var_pic
        self.switch_next_pic = switch_next_pic

        self.variants = deque(variants) if variants else None
        self.curr_var = self.variants[0] if variants else None
        self.curr_var_text = self.font.render(self.curr_var, True, WHITE)

        self._make_rectangles()
        
    def update(self, screen: pg.Surface) -> None:
        """Update options images on screen."""
        screen.blit(self.name_pic, self.rect_name_pic)
        screen.blit(self.opt_name_text, self.rect_opt_name_text)

        self.switch_prev_button.update(screen)
        self.switch_next_button.update(screen)

        screen.blit(self.curr_var_pic, self.rect_curr_var_pic)
        screen.blit(self.curr_var_text, self.rect_curr_var_text)

    def check_for_switch_prev(self, position: tuple[int]) -> bool:
        """Check if possition corresponds to switch prev button."""
        return self.switch_prev_button.checkForInput(position)

    def check_for_switch_next(self, position: tuple[int]) -> bool:
        """Check if possition corresponds to switch next button."""
        return self.switch_next_button.checkForInput(position)
    
    def switch_next(self) -> None:
        """Switch current variant to next."""
        self.variants.rotate(-1)
        self.curr_var = self.variants[0]
        self.curr_var_text = self.font.render(self.curr_var, True, WHITE)

    def switch_prev(self) -> None:
        """Switch current variant to previous."""
        self.variants.rotate(1)
        self.curr_var = self.variants[0]
        self.curr_var_text = self.font.render(self.curr_var, True, WHITE)

    def switch_mb(self, position: tuple[int]) -> None:
        """Check if position corresponds to switch buttons and if it is then switch."""
        if self.check_for_switch_prev(position):
            self.switch_prev()
            return
        if self.check_for_switch_next(position):
            self.switch_next()
            return
        return
