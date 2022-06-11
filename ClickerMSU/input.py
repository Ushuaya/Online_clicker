"""Module of registration procedure."""


import pygame as pg
from .insertion_deleting_sqlite import register, sighin
from .__init__ import Drawing, ImageUploader
from .Button import Button
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
FPS = 60
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (50, 100, 11)
pg.init()
FONT = pg.font.Font(None, 32)


class InputBox:
    """Class to create input boxes."""

    def __init__(self, x: int, y: int, w: int, h: int, text: str = '') -> None:
        """Initialize set ups.

        :param x:  x pos
        :type x: int

        :param y:  y pos
        :type y: int

        :param w:  width
        :type w: int

        :param h:  height
        :type h: int

        :param text:  user's text
        :type text: str
        
        :return: None
        """
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.print = ""
        self.password = False

    def handle_event(self, event: pg.event) -> None:
        """Toggle action of input box.
        
        :param event:  any event in game
        :type event: pg.event
        
        :return: None
        """
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    pass
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode != " ":
                        self.text += event.unicode
                self.txt_surface = FONT.render("*" * len(self.text) if self.password is True
                                               else self.text, True, self.color)

    def update(self) -> None:
        """Update input box.

        :return: None
        """
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen: pg.Surface) -> None:
        """Draw input box.
        
        :return: None
        """
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pg.draw.rect(screen, self.color, self.rect, 2)


def main_c(coins=None, d_w: int = 1024, d_h: int = 768) -> list:
    """Try main cycle of registration module.

    :param d_w:  width
    :type d_w: int

    :param d_h:  height
    :type d_h: int
    
    :return: list
    """
    imageSaver = ImageUploader('images')
    global DISPLAY_WIDTH
    global DISPLAY_HEIGHT
    button_1 = imageSaver.uploadImage('button_upgrade.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
    DISPLAY_WIDTH = d_w
    DISPLAY_HEIGHT = d_h

    screen = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
    pg.display.set_caption("Inputer")
    clock = pg.time.Clock()

    clock = pg.time.Clock()
    input_box1 = InputBox(DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT * 0.28, 140, 32)
    input_box1.password = False
    input_box2 = InputBox(DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT * 0.35, 140, 32)
    input_box2.password = True
    input_box3 = InputBox(DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT * 0.42, 140, 32)
    input_box3.password = True
    input_boxes = [input_box1, input_box2]
    input_boxes_registration = [input_box1, input_box2, input_box3]
    done = False
    Drawer2 = Drawing()

    Next_stage = "REG_SIGN"
    done = False
    exit_module = False
    coins_update = 0
    button_dark_blue = imageSaver.uploadImage('button_dark_blue.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))

    while not exit_module:
        if Next_stage == "REG_SIGN":
            done = not done

            REGISTRATION_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH * 0.2, DISPLAY_WIDTH * 0.1),
                                         text_input=_("Registration"), font_size=36, hovering_color=BLACK,
                                         tipper=[_("REGISTRATE TO START"), _("WITH CURRENT PLACE"), _("NEXT TIME")])
            SIGN_IN_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH * 0.6, DISPLAY_WIDTH * 0.1),
                                    tipper=[_("SIGN IN TO SAVE &"), _("CONTINUE PLAYING")],
                                    text_input=_("   Sign in   "), font_size=48, hovering_color=BLACK)
            BACK_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.8),
                                 text_input=_("BACK"), font_size=48)

            clock = pg.time.Clock()
            while not done:
                clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        exit_module = True
                        return coins, None

                    elif event.type == pg.MOUSEBUTTONDOWN:
                        mopos = pg.mouse.get_pos()

                        if REGISTRATION_BUTTON.checkForInput(mopos):
                            Next_stage = "REGISTRATION"
                            done = not done
                            break

                        elif SIGN_IN_BUTTON.checkForInput(mopos):
                            Next_stage = "SIGN_IN"
                            done = not done
                            break

                        elif BACK_BUTTON.checkForInput(mopos):
                            Next_stage = ""
                            done = not done
                            exit_module = not exit_module
                            return coins, None

                bckgrnd_im = imageSaver.uploadImage('sova.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                screen.blit(bckgrnd_im, (0, 0))
                MOUSE_POS = pg.mouse.get_pos()

                # self.gameDisplay.blit(MENU_TEXT, MENU_RECT)

                for button in [REGISTRATION_BUTTON, SIGN_IN_BUTTON, BACK_BUTTON]:
                    button.changeColor(MOUSE_POS, screen)
                    button.update(screen)

                pg.display.flip()

        if Next_stage == "REGISTRATION":
            done = not done
            wrong_inp = False
            clock = pg.time.Clock()
            while not done:
                clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        exit_module = True
                        return coins, None

                    elif event.type == pg.MOUSEBUTTONDOWN:
                        mopos = pg.mouse.get_pos()

                        if REGISTRATION_BUTTON.checkForInput(mopos):
                            if input_boxes_registration[1].text == input_boxes_registration[2].text:
                                table_10, pos = register(None, input_boxes_registration[0].text,
                                                         input_boxes_registration[1].text, coins)
                                coins_update = coins
                            else:
                                table_10 = 4

                            match table_10:
                                case 1:
                                    wrong_inp = True
                                    Error_msg = _("Username is empty")
                                case 2:
                                    wrong_inp = True
                                    Error_msg = _("Password is empty")
                                case 3:
                                    wrong_inp = True
                                    Error_msg = _("User with same already exists...")
                                case 4:
                                    wrong_inp = True
                                    Error_msg = _("Passwords don't match...")
                                case _:
                                    wrong_inp = False
                                    Error_msg = ""
                                    Next_stage = "SHOW_RESULT"
                                    done = not done

                        elif BACK_BUTTON.checkForInput(mopos):
                            done = not done
                            Next_stage = "REG_SIGN"

                    for i in range(len(input_boxes_registration)):
                        frog = input_boxes_registration[i].handle_event(event)
                        if frog is not None:
                            print(frog)

                for box in input_boxes_registration:
                    box.update()

                bckgrnd_im = imageSaver.uploadImage('sova.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                screen.blit(bckgrnd_im, (0, 0))

                for box in input_boxes_registration:
                    box.draw(screen)

                Drawer2.drawText(_("Username: "), BLACK, None,
                                 DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.3, 20, screen=screen)

                Drawer2.drawText(_("Password: "), BLACK, None,
                                 DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.37, 20, screen=screen)

                Drawer2.drawText(_("Password again: "), BLACK, None,
                                 DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.44, 20, screen=screen)

                MOUSE_POS = pg.mouse.get_pos()
                REGISTRATION_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH * 0.75, DISPLAY_HEIGHT * 0.87),
                                             text_input=_("Register"), font_size=26, hovering_color=BLACK)
                BACK_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH * 0.35, DISPLAY_HEIGHT * 0.87),
                                     text_input=_("BACK"), font_size=48)

                for button in [REGISTRATION_BUTTON, BACK_BUTTON]:
                    button.changeColor(MOUSE_POS)
                    button.update(screen)

                if wrong_inp:
                    Drawer2.drawText(Error_msg, RED, None,
                                     DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT * 0.55, 20, screen=screen)

                pg.display.flip()

        if Next_stage == "SIGN_IN":
            done = not done
            wrong_inp = False
            Error_msg = ""
            clock = pg.time.Clock()
            while not done:
                clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        exit_module = True
                        return coins, None

                    elif event.type == pg.MOUSEBUTTONDOWN:
                        mopos = pg.mouse.get_pos()

                        if SIGN_IN_BUTTON.checkForInput(mopos):
                            table_10, pos, coins_update = sighin(None, input_boxes[0].text,
                                                                 input_boxes[1].text, coins)

                            match table_10:
                                case 1:
                                    wrong_inp = True
                                    Error_msg = _("You are not registrated yet")
                                case 2:
                                    wrong_inp = True
                                    Error_msg = _("You didn't input password")
                                case 3:
                                    wrong_inp = True
                                    Error_msg = _("Wrong password")
                                case 4:
                                    wrong_inp = True
                                    Error_msg = _("You didn't specify username")
                                case _:
                                    wrong_inp = False
                                    Error_msg = ""
                                    Next_stage = "SHOW_RESULT"
                                    done = not done

                        elif BACK_BUTTON.checkForInput(mopos):
                            done = not done
                            Next_stage = "REG_SIGN"

                    elif (event.type == pg.KEYDOWN and event.key == pg.K_RETURN):
                        table_10, pos, coins_update = sighin(None, input_boxes[0].text,
                                                             input_boxes[1].text, coins)

                        match table_10:
                            case 1:
                                wrong_inp = True
                                Error_msg = _("You are not registrated yet")
                            case 2:
                                wrong_inp = True
                                Error_msg = _("You didn't input password")
                            case 3:
                                wrong_inp = True
                                Error_msg = _("Wrong password")
                            case 4:
                                wrong_inp = True
                                Error_msg = _("You didn't specify username")
                            case _:
                                wrong_inp = False
                                Error_msg = ""
                                Next_stage = "SHOW_RESULT"
                                done = not done

                    for i in range(len(input_boxes)):
                        frog = input_boxes[i].handle_event(event)
                        if frog is not None:
                            print(frog)

                for box in input_boxes:
                    box.update()

                bckgrnd_im = imageSaver.uploadImage('sova.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                screen.blit(bckgrnd_im, (0, 0))

                for box in input_boxes:
                    box.draw(screen)

                Drawer2.drawText(_("Username: "), BLACK, None,
                                 DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.3, 22, screen=screen)

                Drawer2.drawText(_("Password: "), BLACK, None,
                                 DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.37, 22, screen=screen)

                MOUSE_POS = pg.mouse.get_pos()
                SIGN_IN_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH * 0.75, DISPLAY_HEIGHT * 0.87),
                                        text_input=_("SIGN IN"), font_size=48, hovering_color=BLACK)
                BACK_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH * 0.35, DISPLAY_HEIGHT * 0.87),
                                     text_input=_("BACK"), font_size=48)

                for button in [SIGN_IN_BUTTON, BACK_BUTTON]:
                    button.changeColor(MOUSE_POS)
                    button.update(screen)

                if wrong_inp:
                    Drawer2.drawText(Error_msg, RED, None,
                                     DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT * 0.55, 20, screen=screen)

                pg.display.flip()

        if Next_stage == "SHOW_RESULT":
            done = not done
            clock = pg.time.Clock()
            while not done:
                clock.tick(FPS)
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        exit_module = True
                        return coins, None

                    elif event.type == pg.MOUSEBUTTONDOWN:
                        mopos = pg.mouse.get_pos()

                        if mopos[0] >= DISPLAY_WIDTH * 0.6 and mopos[1] >= DISPLAY_HEIGHT * 0.8 and\
                                mopos[0] <= DISPLAY_WIDTH * 0.6 + button_1.get_width() and\
                                mopos[1] <= DISPLAY_HEIGHT * 0.8 + button_1.get_height():
                            done = not done
                            exit_module = not exit_module
                            print("USER: ", input_box1.text)
                            return coins_update, input_box1.text

                bckgrnd_im = imageSaver.uploadImage('corona.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
                screen.blit(bckgrnd_im, (0, 0))
                table_10_2 = [("")]
                for i in range(len(table_10)):
                    table_10_2 += [(str(i + 1) + ". " + str(table_10[i][1]) + " -- " + str(table_10[i][0]))]
                list_to_print = [(_("Top 10 players: "))] + table_10_2 + [("")] + [(_("Your place: "))] +\
                                [(pos[0][2])] + [(_("Your score: "))] + [(pos[0][0])]
                enter = 0
                for i in list_to_print:
                    Drawer2.drawText(str(i), GREEN, None,
                                    DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 5 + enter, 25, screen=screen)
                    enter += 30

                MOUSE_POS = pg.mouse.get_pos()
                DONE_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH * 0.75, DISPLAY_HEIGHT * 0.87),
                                     text_input=_("DONE"), font_size=48, hovering_color=BLACK)

                for button in [DONE_BUTTON]:
                    button.changeColor(MOUSE_POS)
                    button.update(screen)
                pg.display.flip()


if __name__ == '__main__':
    main_c()
    pg.quit()
