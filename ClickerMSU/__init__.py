"""Main module."""


import pygame as pg
import random
import time
from .Button import Button
from . import input
from . import insertion_deleting_sqlite
from .Option import Option_switchable, Option_slider
from os import path, listdir
import threading
import sys
import gettext


# Costyl variant
lang_def = gettext.translation("Clicker", path.dirname(__file__), fallback=True)
lang_ru = gettext.translation("Clicker", path.dirname(__file__), languages=["ru"], fallback=True)
lang_eng = gettext.translation("Clicker", path.dirname(__file__), languages=["en"], fallback=True)


def set_default_language() -> None:
    """Set language to default."""
    global lang_def
    lang_def.install()


def set_ru_language() -> None:
    """Set language to Russian."""
    global lang_ru
    lang_ru.install()


def set_eng_language() -> None:
    """Set language to English."""
    global lang_eng
    lang_eng.install()


""" Play screen:
                        DISPLAY WIDTH
        |-------------------------------------------|
        |   coins         TITLE            home_b   |
        |                                           |
        |                                           |
        |                                           |
DISPLAY |               main_click                  |
 HEIGHT |                                           |
        |                                           |
        |                                           |
        |    b_1                             b_2    |
        |-------------------------------------------|

"""

DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768
FPS = 60
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)
BLUE_GRAY = (115, 147, 179)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_YELLOW = (150, 150, 30)
GOLD = (230, 190, 85)
f_stop = None

LANGUAGES = ["Default", "English", "Russian", ]
RESOLUTIONS = ["1024x768", "640x480", "1280x720", "1920x1080", ]


LANG_TO_LOC = {"English": set_eng_language,
               "Russian": set_ru_language,
               "Default": set_default_language, }


class ImageUploader():
    """I Image uploader."""

    def __init__(self, dir: str) -> None:
        """Try Init image uploader associated with the <dir> directiry.

        :param dir: image size to scale to
        :type dir: str

        :return: None
        """
        self.img_dir = path.join(path.dirname(__file__), dir)

    def uploadImage(self, name: str, size: tuple) -> pg.Surface:
        """Try Upload image from self.img_dir folder.

        :param name: image name
        :type name: str

        :param size: image size to scale to
        :type size: tuple

        :return: pg.Surface
        """
        if name.find(".png") == -1:
            tmp = pg.image.load(path.join(self.img_dir, name)).convert()          # if not png
        else:
            tmp = pg.image.load(path.join(self.img_dir, name)).convert_alpha()    # if png
        tmp = pg.transform.scale(tmp, size)
        return tmp


class MusicUploader():
    """Try Image uploader."""

    SONG_END = pg.USEREVENT + 1

    def __init__(self, dir) -> None:
        """Init music uploader associated with <dir> directiry.
        
        :param name: name of music, that will be implemented on next step.
        :type name: str

        :return: None
        """        
        self.sound_dir = path.join(path.dirname(__file__), dir)

    def uploadMusic(self, name: str) -> None:
        """Upload music from self.sound_dir folder.

        :param name: name of music, that will be implemented on next step.
        :type name: str

        :return: None
        """
        pg.mixer.music.load(path.join(self.sound_dir, name))
        return None

    def playRandomMusic(self) -> None:
        """Play random music from self.sound_dir folder."""
        song_name = random.choice(listdir(self.sound_dir))
        self.uploadMusic(song_name)
        pg.mixer.music.set_volume(0.5)
        pg.mixer.music.play(fade_ms=5000)
        pg.mixer.music.set_endevent(self.SONG_END)

    def setVolume(self, v: float) -> None:
        """Set music volume to v."""
        if 0 < v <= 1:
            pg.mixer.music.set_volume(v)
        elif v <= 0:
            pg.mixer.music.set_volume(0)
        elif v > 1:
            pg.mixer.music.set_volume(1)
        return

    def getVolume(self) -> float:
        """Try Get current volume."""
        return pg.mixer.music.get_volume()


class Drawing():
    """Try Class to draw elements on screen."""

    def drawText(self, text: str, textColor: tuple, rectColor: tuple,
                 x: int, y: int, fsize: int, shift_1: int = 0, shift_2: int = 0,
                 screen: object = None, font_name: str = "freesansbold.ttf") -> None:
        """
        Draw text on the main screen.

        :param text: the text, that will be implemented to the main screen.
        :type text: str

        :param textColor:  colour of the text
        :type textColor:  tuple

        :param rectColor:  rectangle color
        :type rectColor: tuple

        :param x: position of the leftangle
        :type x: int

        :param y: position of the right angle
        :type y: int

        :param fsize:  size of text
        :type fsize:  int

        :param shift_1:  shift of the text window in pixels on the x axis
        :type shift_1: int

        :param shift_2:  shift of the text window in pixels on the y axis
        :type shift_2: int

        :param font_name:  text font to use
        :type font_name: str

        :return: None
        """
        font = pg.font.Font(font_name, fsize)
        text = font.render(text, True, textColor, rectColor)
        textRect = text.get_rect()
        textRect.center = (x + shift_1, y + shift_2)
        screen.blit(text, textRect)
        return

    def newImageAfterClick(self, logos: tuple) -> None:
        """Change of the main-click logo. There is random probabilty of changing the logo.
        
        :param logos:  new logo to show
        :type logos: tuple

        :return: None
        """
        pict = random.choice(logos)
        return pict

    def dispaylBackgroundButton(self, pos: tuple, screen_f: object = None,
                                button_bckgrnd_f: object = None) -> None:
        """Create the background of button when the cursor moves above it.

        :param pos: position of button.
        :type pos: tuple

        :param screen_f:  screen where to draw
        :type screen_f:  pg.Surface

        :param button_bckgrnd_f: button background to draw
        :type button_bckgrnd_f: pg.Surface

        :return: None
        """
        if pos[0] >= DISPLAY_WIDTH * 0.42 and pos[1] >= DISPLAY_HEIGHT * 0.42 and\
           pos[0] <= DISPLAY_WIDTH * 0.545 and pos[1] <= DISPLAY_HEIGHT * 0.59:
            screen_f.blit(button_bckgrnd_f, (DISPLAY_WIDTH * (0.42 - 0.1),
                          DISPLAY_HEIGHT * (0.42 - 0.125)))


class ShiftingBackgoungnd():
    """Create background, move it an each tick on one pixel, and other changes."""
    

    cycleBack = 0

    def shift(self, screen_f: object, bckgrnd_im_f: object, im_len: int):
        """Try Main function.

        :param screen_f: screen where to draw.
        :type screen_f: pg.Surface

        :param bckgrnd_im_f: button background to draw
        :type bckgrnd_im_f: pg.Surface

        :param im_len:  imge length
        :type im_len:  int

        :return: None
        """
        screen_f.blit(bckgrnd_im_f, (0, 0))
        screen_f.fill((0, 0, 0))
        screen_f.blit(bckgrnd_im_f, (self.cycleBack, 0))
        screen_f.blit(bckgrnd_im_f, (im_len + self.cycleBack, 0))
        if (self.cycleBack == -im_len):
            screen_f.blit(bckgrnd_im_f, (im_len + self.cycleBack, 0))
            self.cycleBack = 0
        self.cycleBack -= 1


class Game():
    """Try main class, that contains game logics and execution."""

    coins = 0
    autog = 0
    mong = 1
    costUpgrade = 50
    costAutominer = 50
    ver = "0.1"
    User = None
    f_stop = None
    tmp = None

    def autominer(self) -> None:
        """Auto adding coins if corresponding upgrade has been bought.

        :return: None
        """
        time.sleep(0.1)
        self.coins = self.coins + self.autog

    def play(self) -> None:
        """Play loop of the game.

        :return: None
        """
        pg.display.set_caption("Play")

        # Images
        imageSaver = ImageUploader('images')
        vmkLogo = imageSaver.uploadImage('click_logo.png', (0.125 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        msuLogo = imageSaver.uploadImage('msu_logo.png', (0.125 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        sadLogo = imageSaver.uploadImage('sadovnik.png', (0.125 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        clickImages = (vmkLogo, msuLogo, sadLogo)
        currLogo = msuLogo

        button_1 = imageSaver.uploadImage('button_upgrade.png', (0.33 * DISPLAY_WIDTH, 0.13 * DISPLAY_HEIGHT))
        butn_bckrnd = imageSaver.uploadImage('button_back.png', (0.32 * DISPLAY_WIDTH, 0.42 * DISPLAY_HEIGHT))
        bckgrnd_im = imageSaver.uploadImage('Game_back.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        button_home = imageSaver.uploadImage("home_button.png", (0.10 * DISPLAY_WIDTH, 0.10 * DISPLAY_HEIGHT))

        UPGRADE_BUTTON = Button(button_1, pos=(0.20 * DISPLAY_WIDTH, 0.85 * DISPLAY_HEIGHT),
                                text_input=_("Upgrade clicker: {}").format(self.costUpgrade), font_size=20,
                                hovering_color=GREEN)
        AUTOMINER_BUTTON = Button(button_1, pos=(0.80 * DISPLAY_WIDTH, 0.85 * DISPLAY_HEIGHT),
                                  text_input=_("Upgrade autominer: {}").format(self.costAutominer), font_size=20,
                                  hovering_color=GREEN)
        HOME_BUTTON = Button(button_home, (0.85 * DISPLAY_WIDTH, 0.10 * DISPLAY_HEIGHT), "")

        # Ininial values
        shiftBackgoungnd = ShiftingBackgoungnd()
        Drawer = Drawing()

        # Start
        clock = pg.time.Clock()
        while self.running:
            clock.tick(FPS)
            self.autominer()

            MOUSE_POS = pg.mouse.get_pos()
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    self.running = False
                    continue

                # If current music ends
                elif event.type == self.musicPlayer.SONG_END:
                    self.musicPlayer.playRandomMusic()

                # Here we choose the right action depending on the cursor click place
                elif event.type == pg.MOUSEBUTTONDOWN:
                    # if click for score
                    if MOUSE_POS[0] >= DISPLAY_WIDTH * 0.42 and MOUSE_POS[1] >= DISPLAY_HEIGHT * 0.42 and\
                       MOUSE_POS[0] <= DISPLAY_WIDTH * 0.545 and MOUSE_POS[1] <= DISPLAY_HEIGHT * 0.59:
                        self.coins += self.mong
                        currLogo = Drawer.newImageAfterClick(clickImages)

                    # if click for upgrade
                    elif UPGRADE_BUTTON.checkForInput(MOUSE_POS):
                        if self.coins >= self.costUpgrade:
                            self.coins = self.coins - self.costUpgrade
                            self.mong = self.mong * 1.1
                            self.costUpgrade = round(self.costUpgrade * 1.5, 0)
                            UPGRADE_BUTTON.changeText(_("Upgrade clicker: {}").format(self.costUpgrade))

                    # if click for autominer
                    elif AUTOMINER_BUTTON.checkForInput(MOUSE_POS):
                        if self.coins >= self.costAutominer:
                            self.coins = self.coins - self.costAutominer
                            self.autog = self.autog + 0.5
                            self.costAutominer = round(self.costAutominer * 1.5, 0)
                            AUTOMINER_BUTTON.changeText(_("Upgrade autominer: {}").format(self.costAutominer))

                    # if click for home
                    elif HOME_BUTTON.checkForInput(MOUSE_POS):
                        return

            # Func to create dynamic background
            shiftBackgoungnd.shift(self.gameDisplay, bckgrnd_im, DISPLAY_WIDTH)

            for button in [UPGRADE_BUTTON, AUTOMINER_BUTTON, HOME_BUTTON]:
                button.changeColor(MOUSE_POS)
                button.update(self.gameDisplay)

            Drawer.dispaylBackgroundButton(pg.mouse.get_pos(), self.gameDisplay, butn_bckrnd)
            self.gameDisplay.blit(currLogo, (DISPLAY_WIDTH * 0.42, DISPLAY_HEIGHT * 0.42))

            Drawer.drawText("ВМИК lif(v)e", BLACK, LIGHT_BLUE,
                            0.5 * DISPLAY_WIDTH, 0.12 * DISPLAY_HEIGHT, 50, screen=self.gameDisplay)
            Drawer.drawText(_("You have {:.2f} coins").format(self.coins), BLACK, LIGHT_BLUE,
                            0.15 * DISPLAY_WIDTH, 0.10 * DISPLAY_HEIGHT, 20, screen=self.gameDisplay)

            # updating
            pg.display.flip()
        return

    def update_locale(self) -> None:
        """Update current locale depending on self.language.

        :return: None
        """

        LANG_TO_LOC[self.language]()
        return


    def apply_changes(self, **kwargs) -> bool:
        """Apply changes in options.

        :return: bool
        """
        # restart = False
        restart = True
        if "new_volume" in kwargs:
            self.musicPlayer.setVolume(kwargs["new_volume"] / 100)
            self.volume = kwargs["new_volume"]
        if "new_language" in kwargs:
            self.language = kwargs["new_language"]
            self.update_locale()
        if "new_resolution" in kwargs:
            global DISPLAY_HEIGHT, DISPLAY_WIDTH
            self.resolution = self.resolution_to_str(kwargs["new_resolution"])
            DISPLAY_WIDTH = kwargs["new_resolution"][0]
            DISPLAY_HEIGHT = kwargs["new_resolution"][1]
            self.gameDisplay = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        return restart

    @staticmethod
    def resolution_to_tuple(resol: str) -> tuple[int]:
        """Cast resolution in format 'AxB' to (A, B).

        :param resol: resloution type.
        :type resol: str

        :return: tuple[int]
        """
        if not isinstance(resol, str):
            raise TypeError("Wrong resol type")
        A, x, B = resol.partition('x')
        A = int(A)
        B = int(B)
        if x == '':
            raise ValueError("Wrong resolution format")
        return (A, B)

    @staticmethod
    def resolution_to_str(resol: tuple[int, int]) -> str:
        """Cast resolution in format (A, B) to 'AxB'.

        :param resol: resloution type.
        :type resol: tuple[int, int]

        :return: str
        """
        if not (isinstance(resol, tuple) or isinstance(resol, list)) or len(resol) == 0\
           or not isinstance(resol[0], int):
            raise TypeError("Wrong resol type")
        return str(resol[0]) + "x" + str(resol[1])

    @staticmethod
    def get_new_resolution(resol_opt: Option_switchable) -> tuple[int]:
        """Cast resolution in format (A, B) to 'AxB'.

        :param resol_opt: resloution type.
        :type resol_opt: Option_switchable

        :return: tuple[int]
        """
        resol = resol_opt.curr_var
        return Game.resolution_to_tuple(resol)

    def options(self) -> None:
        """Options menu.

        :return: None
        """
        pg.display.set_caption("Options")

        imageSaver = ImageUploader('images')
        bckgrnd_im = imageSaver.uploadImage('Game_back.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        panel_green = imageSaver.uploadImage('button_green.png',
                                             (0.30 * DISPLAY_WIDTH, 0.15 * DISPLAY_HEIGHT))
        panel_yellow = imageSaver.uploadImage('button_yellow.png',
                                              (0.30 * DISPLAY_WIDTH, 0.15 * DISPLAY_HEIGHT))
        button_prev = imageSaver.uploadImage('arrow-left.png',
                                             (0.10 * DISPLAY_WIDTH, 0.15 * DISPLAY_HEIGHT))
        button_next = imageSaver.uploadImage('arrow-right.png',
                                             (0.10 * DISPLAY_WIDTH, 0.15 * DISPLAY_HEIGHT))
        button_apply = imageSaver.uploadImage('button_light_green.png',
                                              (0.35 * DISPLAY_WIDTH, 0.175 * DISPLAY_HEIGHT))
        button_back = imageSaver.uploadImage('button_violet.png',
                                             (0.35 * DISPLAY_WIDTH, 0.175 * DISPLAY_HEIGHT))

        font_name = "freesansbold.ttf"
        font_size = 56
        OPT_TEXT = pg.font.Font(font_name, font_size).render(_("Options"), True, BLACK)
        OPT_RECT = OPT_TEXT.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 0.08))

        LANGUAGE_OPTION = Option_switchable(_("Language"), (0.05 * DISPLAY_WIDTH, 0.30 * DISPLAY_HEIGHT),
                                            panel_green, panel_yellow, button_prev, button_next,
                                            variants=LANGUAGES)
        LANGUAGE_OPTION.set_curr_value(self.language)

        RESOLUTION_OPTION = Option_switchable(_("Resolution"), (0.05 * DISPLAY_WIDTH, 0.50 * DISPLAY_HEIGHT),
                                              panel_green, panel_yellow, button_prev, button_next,
                                              variants=RESOLUTIONS)
        RESOLUTION_OPTION.set_curr_value(self.resolution)

        VOLUME_OPTION = Option_slider(self.gameDisplay, _("Volume"),
                                      (0.05 * DISPLAY_WIDTH, 0.70 * DISPLAY_HEIGHT), panel_green,
                                      0, 100, 1, slider_colour=DARK_YELLOW, handle_colour=GOLD,
                                      initial_value=self.volume)

        APPLY_BUTTON = Button(button_apply, (0.30 * DISPLAY_WIDTH, 0.85 * DISPLAY_HEIGHT), _("Apply"),
                              font_size=46, hovering_color=LIGHT_BLUE)
        BACK_BUTTON = Button(button_back, (0.70 * DISPLAY_WIDTH, 0.85 * DISPLAY_HEIGHT), _("Esc: back"),
                             font_size=46, hovering_color=BLUE_GRAY)

        clock = pg.time.Clock()
        changes = dict()
        while self.running and not self._changes_applied:
            clock.tick(FPS)
            self.gameDisplay.blit(bckgrnd_im, (0, 0))

            self.gameDisplay.blit(OPT_TEXT, OPT_RECT)
            for option in [LANGUAGE_OPTION, RESOLUTION_OPTION, VOLUME_OPTION, ]:
                option.update(self.gameDisplay)

            for button in [APPLY_BUTTON, BACK_BUTTON]:
                button.changeColor(pg.mouse.get_pos())
                button.update(self.gameDisplay)

            events = pg.event.get()
            VOLUME_OPTION.update_slider(events)
            for event in events:
                MOUSE_POS = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    self.running = False
                    continue
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                if event.type == pg.MOUSEBUTTONDOWN:
                    if LANGUAGE_OPTION.switch_mb(MOUSE_POS):
                        changes["new_language"] = LANGUAGE_OPTION.curr_var
                    if RESOLUTION_OPTION.switch_mb(MOUSE_POS):
                        changes["new_resolution"] = self.get_new_resolution(RESOLUTION_OPTION)
                    if BACK_BUTTON.checkForInput(MOUSE_POS):
                        return
                    if APPLY_BUTTON.checkForInput(MOUSE_POS):
                        changes["new_volume"] = VOLUME_OPTION.get_value()
                        # Bug in pygame-widgets: old Sliders and TextBoxes are not removed from screen
                        VOLUME_OPTION.slider.hide()
                        VOLUME_OPTION.output.hide()
                        self._changes_applied = self.apply_changes(**changes)
                # If current music ends
                elif event.type == self.musicPlayer.SONG_END:
                    self.musicPlayer.playRandomMusic()

            pg.display.flip()
        return

    def main_menu(self) -> None:
        """Try Main menu screen.

        :return: None

        """
        pg.display.set_caption("Main menu")

        imageSaver = ImageUploader('images')
        button_dark_blue = imageSaver.uploadImage('button_dark_blue.png',
                                                  (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        button_red = imageSaver.uploadImage('button_red.png',
                                            (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        bckgrnd_im = imageSaver.uploadImage('Game_back.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))

        font_name = "freesansbold.ttf"
        font_size = 80
        MENU_TEXT = pg.font.Font(font_name, font_size).render(_("Clicker: MSU edition"), True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(DISPLAY_WIDTH // 2, 0.12 * DISPLAY_HEIGHT))

        PLAY_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH // 2, 0.33 * DISPLAY_HEIGHT),
                             text_input=_("PLAY"), font_size=48)
        OPTIONS_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH // 2, 0.48 * DISPLAY_HEIGHT),
                                text_input=_("OPTIONS"), font_size=48)
        RATING_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH // 2, 0.63 * DISPLAY_HEIGHT),
                             text_input=_("SAVE & RATING"), font_size=28)
        QUIT_BUTTON = Button(button_red, pos=(DISPLAY_WIDTH // 2, 0.78 * DISPLAY_HEIGHT),
                             text_input=_("QUIT"), font_size=48, hovering_color=BLACK)

        clock = pg.time.Clock()
        while self.running and not self._reset_screen:
            clock.tick(FPS)

            self.gameDisplay.blit(bckgrnd_im, (0, 0))
            MENU_MOUSE_POS = pg.mouse.get_pos()
            self.gameDisplay.blit(MENU_TEXT, MENU_RECT)

            if self.User is not None:
                USER_TEXT = pg.font.Font(font_name, 40).render(_("СURRENT USER: {}").format(self.User), True, WHITE)
                USER_RECT = USER_TEXT.get_rect(center=(DISPLAY_WIDTH // 2, 0.9 * DISPLAY_HEIGHT))
                self.gameDisplay.blit(USER_TEXT, USER_RECT)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, RATING_BUTTON]:
                button.changeColor(MENU_MOUSE_POS, self.gameDisplay)
                button.update(self.gameDisplay)

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    continue
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        # starting updatign of coins with server
                        if self.User is not None:
                            if self.f_stop is None:
                                print("NEW THREAD")
                                self.f_stop = threading.Event()
                                print("New: ", self.f_stop)
                                self.updation_of_cur_user_data(self.User)
                        self.play()
                        # killing thread
                        try:
                            self.f_stop.set()
                            print("3:THREAD STOPPED: ", self.f_stop)
                            self.f_stop = None
                            self.tmp.join()
                        except Exception:
                            pass

                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                        if self._changes_applied:
                            self._changes_applied = False
                            self._reset_screen = True

                    if RATING_BUTTON.checkForInput(MENU_MOUSE_POS):
                        print("1:THREAD STOPPED: ", self.f_stop)
                        try:
                            self.f_stop.set()
                            self.f_stop = None
                            self.tmp.join()
                        except Exception:
                            pass
                        self.coins, self.User = input.main_c(self.coins, d_w=DISPLAY_WIDTH, d_h=DISPLAY_HEIGHT)

                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.running = False
                        try:
                            self.f_stop.set()
                            self.f_stop = None
                            self.tmp.join()
                            print("3:THREAD STOPPED: ", self.f_stop)
                        except Exception:
                            pass
                        continue
                # If current music ends
                elif event.type == self.musicPlayer.SONG_END:
                    self.musicPlayer.playRandomMusic()

            pg.display.flip()
        return

    def updation_of_cur_user_data(self, username_: str):
        """Try to update current logged in user.

        :param username_: user's name.
        :type username_: str
       
        :return: None

        """
        if self.User is not None:
            print("Updation")
            insertion_deleting_sqlite.update_signed(None, username_, self.coins)
            try:
                if not self.f_stop.is_set():
                    # update each 5 seconds
                    self.tmp = threading.Timer(5, self.updation_of_cur_user_data, [username_])
                    self.tmp.start()
            except Exception:
                sys.exit(0)
        else:
            if self.f_stop is not None:
                print("2:THREAD STOPPED: ", self.f_stop)
                self.f_stop.set()
                self.f_stop = None

    def internet_error(self) -> None:
        """Screen for displaying Internet connection error."""
        gameDisplay = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))

        pg.display.set_caption("Main menu")
        imageSaver = ImageUploader('images')
        button_red = imageSaver.uploadImage('button_red.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))

        QUIT_BUTTON = Button(button_red, pos=(DISPLAY_WIDTH // 2, 0.78 * DISPLAY_HEIGHT),
                             text_input=_("QUIT"), font_size=48, hovering_color=BLACK)

        font_name = "freesansbold.ttf"
        font_size = 30
        MENU_TEXT = pg.font.Font(font_name, font_size).render(_("NO INTERNET! TURN IT ON, THEN RESTART"), True, RED)
        MENU_RECT = MENU_TEXT.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT // 2))
        clock = pg.time.Clock()
        running = True
        while running:
            clock.tick(FPS)
            gameDisplay.blit(MENU_TEXT, MENU_RECT)
            MOUSE_POS = pg.mouse.get_pos()

            for button in [QUIT_BUTTON]:
                button.changeColor(MOUSE_POS, gameDisplay)
                button.update(gameDisplay)

            for event in pg.event.get():

                if event.type == pg.QUIT:
                    running = False
                    continue

                if event.type == pg.MOUSEBUTTONDOWN:
                    if QUIT_BUTTON.checkForInput(MOUSE_POS):
                        running = False
                        continue

            pg.display.flip()

    def __init__(self) -> None:
        """Start the game."""
        # Setting display
        self.gameDisplay = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        # Music
        self.musicPlayer = MusicUploader('music')
        self.musicPlayer.playRandomMusic()

        # Ininial values
        self.running = True

        # Ininial values and default values
        self.running = True
        self._changes_applied = False
        self._reset_screen = True   # initially True but set to False during launch
        self.language = LANGUAGES[0]
        self.update_locale()
        self.resolution = RESOLUTIONS[0]
        self.volume = int(self.musicPlayer.getVolume() * 100)

        # Check Internet connection
        import urllib
        try:
            urllib.request.urlopen("http://google.com")
        except IOError:
            "Google is not available! Internet is broken!"
            self.internet_error()
            return
        else:
            while self._reset_screen:
                self._reset_screen = False
                self.main_menu()

            if self.f_stop is not None:
                self.f_stop.set()
                self.f_stop = None
            return

