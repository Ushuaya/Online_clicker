"""Main module."""

from typing import Any
import pygame as pg
import time
import random
from .Button import Button
from . import input
from . import insertion_deleting_sqlite
from .Option import Option_switchable, Option_slider
from os import path, listdir
import threading
import asyncio


""" Play screen:
                        DISPLAY WIDTH
        |-------------------------------------------|
        |                                           |
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
WHITE = (255,255,255)
RED = (255,0,0)
DARK_YELLOW = (150, 150, 30)
GOLD = (230, 190, 85)
f_stop = None


class ImageUploader():
    """Image uploader.""" 
    def __init__(self, dir):
        """Init image uploader associated with the <dir> directiry"""
        self.img_dir = path.join(path.dirname(__file__), dir)

    def uploadImage(self, name: str, size: tuple) -> pg.Surface:
        """ Upload image from self.img_dir folder.

        params:
            name - image name
            size - image size to scale to
        returns:
            pg.Surface object - loaded and scaled image
        """
        if name.find(".png") == -1:
            tmp = pg.image.load(path.join(self.img_dir, name)).convert()          # if not png
        else:
            tmp = pg.image.load(path.join(self.img_dir, name)).convert_alpha()    # if png
        tmp = pg.transform.scale(tmp, size)
        return tmp


class MusicUploader():
    """
    Image uploader.
    """ 
    SONG_END = pg.USEREVENT + 1
    def __init__(self, dir):
        """Init music uploader associated with <dir> directiry."""
        self.sound_dir = path.join(path.dirname(__file__), dir)

    def uploadMusic(self, name: str):
        """Upload music from self.sound_dir folder.

        params:
            name - music name
        returns:
            None
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


class Drawing(): 

    def drawText(self, text: str, textColor: tuple, rectColor: tuple, 
                 x: int, y: int, fsize: int, shift_1: int = 0, shift_2: int = 0, 
                 screen: object = None, font_name: str = "freesansbold.ttf") -> None:
        """
        Draw text on the main screen.

        params: 
            text - the text, that will be implemented to the main screen. 
            textColor - colour of the text, 
            rectColor - ...,
            x, y - position of the left-highest angle, 
            fsize - size of text, 
            shift_1 -- shift of the text window in pixels on the x axis, 
            shift_2 -- shift of the text window in pixels on the y axis
            font_name - str, text font to use
        returns:
            None
        """
        font = pg.font.Font(font_name, fsize)
        text = font.render(text, True, textColor, rectColor)
        textRect = text.get_rect()
        textRect.center = (x + shift_1, y + shift_2)
        screen.blit(text, textRect)
        return
    
    def newImageAfterClick(self, logos: tuple) -> None:
        """Change of the main-click logo. There is random probabilty of changing the logo."""
        pict = random.choice(logos)
        #screen_f.blit(pict, (DISPLAY_WIDTH * 0.42, DISPLAY_HEIGHT * 0.42))
        return pict
        
    def dispaylBackgroundButton(self, pos: tuple , screen_f:object = None, 
                                button_f: object = None, button_bckgrnd_f: object = None) -> None:
        """Create the background of button when the cursor moves above it."""
        if pos[0] >= DISPLAY_WIDTH * 0.42 and pos[1] >= DISPLAY_HEIGHT * 0.42 and\
           pos[0] <= DISPLAY_WIDTH * 0.545 and pos[1] <= DISPLAY_HEIGHT * 0.59:
            screen_f.blit(button_bckgrnd_f, (DISPLAY_WIDTH * (0.42 - 0.1), DISPLAY_HEIGHT * (0.42 - 0.125)))


class ShiftingBackgoungnd(): 
    """Create background, move it an each tick on one pixel, and other changes."""
    cycleBack = 0 

    def shift(self, screen_f: object, bckgrnd_im_f: object, im_len: int):
        """
        Main function
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
    """Main class, that contains game logics and execution."""
    coins = 0 
    autog = 0 
    mong = 1
    costUpgrade = 50
    costAutominer = 50
    ver = "0.1"
    User = None

    def autominer(self):
        """Auto adding coins if corresponding upgrade has been bought."""
        time.sleep(0.1)
        self.coins = self.coins + self.autog

    def play(self) -> None:
        """Play loop of the game."""
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
        menu_bitton = imageSaver.uploadImage('button_dark_blue.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))


        UPGRADE_BUTTON = Button(button_1, pos=(0.20 * DISPLAY_WIDTH, 0.85 * DISPLAY_HEIGHT), 
                                text_input="Upgrade clicker: {}".format(self.costUpgrade), font_size=20, 
                                hovering_color=GREEN)
        AUTOMINER_BUTTON = Button(button_1, pos=(0.80 * DISPLAY_WIDTH, 0.85 * DISPLAY_HEIGHT), 
                                  text_input="Upgrade autominer: {}".format(self.costAutominer), font_size=20, 
                                  hovering_color=GREEN)

        MENU_BUTTON = Button(menu_bitton, pos=(0.5 * DISPLAY_WIDTH, 0.2 * DISPLAY_HEIGHT), 
                                  text_input="MENU", font_size=30, 
                                  hovering_color=GREEN)
        
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
                    #MOUSE_POS = pg.mouse.get_pos()
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
                            UPGRADE_BUTTON.changeText("Upgrade clicker: {}".format(self.costUpgrade))

                    # if click for autominer
                    elif AUTOMINER_BUTTON.checkForInput(MOUSE_POS):
                        if self.coins >= self.costAutominer:
                            self.coins = self.coins - self.costAutominer
                            self.autog = self.autog + 0.5
                            self.costAutominer = round(self.costAutominer * 1.5, 0)
                            AUTOMINER_BUTTON.changeText("Upgrade autominer: {}".format(self.costAutominer))

                    # if click for menu
                    elif MENU_BUTTON.checkForInput(MOUSE_POS):
                        return


            # Func to create dynamic background
            shiftBackgoungnd.shift(self.gameDisplay, bckgrnd_im, DISPLAY_WIDTH)

            for button in [UPGRADE_BUTTON, AUTOMINER_BUTTON, MENU_BUTTON]:
                button.changeColor(MOUSE_POS, self.gameDisplay)
                button.update(self.gameDisplay)

            Drawer.dispaylBackgroundButton(pg.mouse.get_pos(), self.gameDisplay, button_1, butn_bckrnd)
            self.gameDisplay.blit(currLogo, (DISPLAY_WIDTH * 0.42, DISPLAY_HEIGHT * 0.42))

            Drawer.drawText("ВМИК lif(v)e", BLACK, LIGHT_BLUE, 
                            0.5 * DISPLAY_WIDTH, 0.12 * DISPLAY_HEIGHT, 50, screen = self.gameDisplay)
            Drawer.drawText("You have: " + str(f'{self.coins:.2f}') + " coins", BLACK, LIGHT_BLUE, 
                            0.15 * DISPLAY_WIDTH, 0.06 * DISPLAY_HEIGHT, 20, screen = self.gameDisplay)
            Drawer.drawText("Version: " + self.ver, BLACK, LIGHT_BLUE, 
                            0.85 * DISPLAY_WIDTH, 0.06 * DISPLAY_HEIGHT, 20, screen = self.gameDisplay)

            #updating 
            pg.display.flip()
        return
    
    def apply_changes(self) -> None:
        """Apply changes in options."""
        print("!!!TEST SUCCESS!!!")
        return

    def options(self) -> None:
        """Options menu."""
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
        OPT_TEXT = pg.font.Font(font_name, font_size).render("Options", True, BLACK)
        OPT_RECT = OPT_TEXT.get_rect(center=(DISPLAY_WIDTH // 2, DISPLAY_HEIGHT * 0.08))

        LANGUAGES = ["English", "Russian", ]
        RESOLUTIONS = ["1024x768", "640x480", "1280x720", "1920x1080", ]
        LANGUAGE_OPTION = Option_switchable("Language", (0.05 * DISPLAY_WIDTH, 0.30 * DISPLAY_HEIGHT), 
                                            panel_green, panel_yellow, button_prev, button_next, 
                                 variants=LANGUAGES)
        RESOLUTION_OPTION = Option_switchable("Resolution", (0.05 * DISPLAY_WIDTH, 0.50 * DISPLAY_HEIGHT), 
                                              panel_green, panel_yellow, button_prev, button_next, 
                                              variants=RESOLUTIONS)
        VOLUME_OPTION = Option_slider(self.gameDisplay, "Volume", 
                                      (0.05 * DISPLAY_WIDTH, 0.70 * DISPLAY_HEIGHT), panel_green,
                                      0, 100, 1, slider_colour=DARK_YELLOW, handle_colour=GOLD)

        APPLY_BUTTON = Button(button_apply, (0.30 * DISPLAY_WIDTH, 0.85 * DISPLAY_HEIGHT), "Apply",
                              font_size=46, hovering_color=LIGHT_BLUE)
        BACK_BUTTON = Button(button_back, (0.70 * DISPLAY_WIDTH, 0.85 * DISPLAY_HEIGHT), "Esc: back",
                              font_size=46, hovering_color=BLUE_GRAY)        

        clock = pg.time.Clock()
        while self.running:
            clock.tick(FPS)
            self.gameDisplay.blit(bckgrnd_im, (0, 0))

            self.gameDisplay.blit(OPT_TEXT, OPT_RECT)
            for option in [LANGUAGE_OPTION, RESOLUTION_OPTION, VOLUME_OPTION, ]:
                option.update(self.gameDisplay)

            for button in [APPLY_BUTTON, BACK_BUTTON]:
                button.changeColor(pg.mouse.get_pos())
                button.update(self.gameDisplay)

            events = pg.event.get()
            for event in events:
                MOUSE_POS = pg.mouse.get_pos()
                if event.type == pg.QUIT:
                    self.running = False
                    continue
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        return
                if event.type == pg.MOUSEBUTTONDOWN:
                    LANGUAGE_OPTION.switch_mb(MOUSE_POS)
                    RESOLUTION_OPTION.switch_mb(MOUSE_POS)
                    if BACK_BUTTON.checkForInput(MOUSE_POS):
                        return
                    if APPLY_BUTTON.checkForInput(MOUSE_POS):
                        self.apply_changes()

                # If current music ends
                elif event.type == self.musicPlayer.SONG_END:
                    self.musicPlayer.playRandomMusic()
            
            VOLUME_OPTION.update_slider(events)
            pg.display.flip()
        return


    def main_menu(self) -> None:
        """Main menu screen."""
        pg.display.set_caption("Main menu")
        global f_stop

        imageSaver = ImageUploader('images')
        button_dark_blue = imageSaver.uploadImage('button_dark_blue.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        button_red = imageSaver.uploadImage('button_red.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        bckgrnd_im = imageSaver.uploadImage('Game_back.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))

        font_name = "freesansbold.ttf" 
        font_size = 80
        MENU_TEXT = pg.font.Font(font_name, font_size).render("Clicker: MSU edition", True, BLACK)
        MENU_RECT = MENU_TEXT.get_rect(center=(DISPLAY_WIDTH // 2, 0.12 * DISPLAY_HEIGHT))
        
        PLAY_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH // 2, 0.33 * DISPLAY_HEIGHT), 
                             text_input="PLAY", font_size=48)
        OPTIONS_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH // 2, 0.48 * DISPLAY_HEIGHT), 
                                text_input="OPTIONS", font_size=48)
        RATING_BUTTON = Button(button_dark_blue, pos=(DISPLAY_WIDTH // 2, 0.63 * DISPLAY_HEIGHT), 
                             text_input="SAVE & RATING", font_size=36)
        QUIT_BUTTON = Button(button_red, pos=(DISPLAY_WIDTH //2, 0.78 * DISPLAY_HEIGHT), 
                             text_input="QUIT", font_size=48, hovering_color=BLACK)
        
        clock = pg.time.Clock()
        while self.running:
            clock.tick(FPS)

            self.gameDisplay.blit(bckgrnd_im, (0, 0))
            MENU_MOUSE_POS = pg.mouse.get_pos()
            self.gameDisplay.blit(MENU_TEXT, MENU_RECT)
            
            if self.User != None: 
                USER_TEXT = pg.font.Font(font_name, 40).render("СURRENT USER: " + self.User, True, WHITE)
                USER_RECT = USER_TEXT.get_rect(center=(DISPLAY_WIDTH // 2, 0.9 * DISPLAY_HEIGHT))
                self.gameDisplay.blit(USER_TEXT, USER_RECT)
                if f_stop == None:
                    f_stop = threading.Event()
                    self.updation_of_cur_user_data(f_stop, self.User, self.coins)

            for button in [PLAY_BUTTON, OPTIONS_BUTTON, QUIT_BUTTON, RATING_BUTTON]:
                button.changeColor(MENU_MOUSE_POS, self.gameDisplay)
                button.update(self.gameDisplay)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    continue
                elif event.type == pg.MOUSEBUTTONDOWN:
                    if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.play()
                    if OPTIONS_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.options()
                    if RATING_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.coins, self.User = input.main_c(self.coins)
                        #stopping previous thread
                        if self.User != None: 
                            if f_stop != None:
                                f_stop.set()
                                f_stop = None
                    if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                        self.running = False
                        continue
                # If current music ends
                elif event.type == self.musicPlayer.SONG_END:
                    self.musicPlayer.playRandomMusic()

            pg.display.flip()
        return

    def updation_of_cur_user_data(self, f_stop, username_, coins):
        print("Updation")
        insertion_deleting_sqlite.update_signed(None, username_, self.coins) 
        if not f_stop.is_set():
            # call f() again in 10 seconds
            threading.Timer(10, self.updation_of_cur_user_data, [f_stop , username_, self.coins]).start()

    def __init__(self) -> None:
        """Start the game."""
        # Setting display
        self.gameDisplay = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        FONT = pg.font.Font(None, 32)
        
        # Music
        self.musicPlayer = MusicUploader('music')
        self.musicPlayer.playRandomMusic()

        # Ininial values
        self.running = True

        self.main_menu()

        global f_stop
        if f_stop != None:
            f_stop.set()
            f_stop = None
        return
