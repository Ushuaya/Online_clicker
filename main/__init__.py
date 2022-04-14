from typing import Any
import pygame as pg
import time
import random
from os import path


"""
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


button_1_pos = None 
button_2_pos = None 
button_3_pos = None 
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
FPS = 60
BLACK = (0, 0, 0)
LIGHT_BLUE = (173, 216, 230)


class ImageUploader():
    """
    Image uploader.
    """ 
    def __init__(self, dir):
        """ SUS.
        """
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


class Drawing(): 

    def drawText(self, text: str, textColor: tuple, rectColor: tuple, x: int, y: int, fsize: int , shift_1: int = 0, shift_2: int = 0, screen: object = None) -> None:
        """
        In this function the text occurs in the main screen.

        params: 
            text - the text, that will be implemented to the main screen. 
            textColor - clolour of the text, 
            rectColor - ...,
            x, y - position of the left-highest angle, 
            fsize - size of text, 
            shift_1 -- shift of the text window in pixels on the x axis, 
            shift_2 -- shift of the text window in pixels on the y axis
        returns:
            None
        """
        font = pg.font.Font('freesansbold.ttf', fsize)
        text = font.render(text, True, textColor, rectColor)
        textRect = text.get_rect()
        textRect.center = (x + shift_1, y + shift_2)
        screen.blit(text, textRect)
    
    def newImageAfterClick(self, logos: tuple) -> None:
        """
        Change of the main-click logo. There is random probabilty of changing the logo. 
        """
        pict = random.choice(logos)
        #screen_f.blit(pict, (DISPLAY_WIDTH * 0.42, DISPLAY_HEIGHT * 0.42))
        return pict
        

    def dispaylBackgroundButton(self, pos: tuple , screen_f:object = None, button_f: object = None, button_bckgrnd_f: object = None) -> None:
        """
        Create the background of button when the cursor moves above it.
        """
        if pos[0] >= DISPLAY_WIDTH * 0.42 and pos[1] >= DISPLAY_HEIGHT * 0.42 and\
           pos[0] <= DISPLAY_WIDTH * 0.545 and pos[1] <= DISPLAY_HEIGHT * 0.59:
            screen_f.blit(button_bckgrnd_f, (DISPLAY_WIDTH * (0.42 - 0.1), DISPLAY_HEIGHT * (0.42 - 0.125)))

        if pos[0] >= DISPLAY_WIDTH * 0.0625 and pos[1] >= DISPLAY_HEIGHT * 0.84 and\
           pos[0] <= DISPLAY_WIDTH * 0.0625 + button_f.get_width() and pos[1] <= DISPLAY_HEIGHT * 0.84 + button_f.get_height():
            screen_f.blit(button_bckgrnd_f, (DISPLAY_WIDTH * 0.0625 + button_f.get_width() // 2 - button_bckgrnd_f.get_width() // 2, 
                                             DISPLAY_HEIGHT * 0.82 + button_f.get_height() // 2 - button_bckgrnd_f.get_height() // 2))

        if pos[0] >= DISPLAY_WIDTH * 0.6875 and pos[1] >= DISPLAY_HEIGHT * 0.84 and\
           pos[0] <= DISPLAY_WIDTH * 0.6875 + button_f.get_width() and pos[1] <= DISPLAY_HEIGHT * 0.84 + button_f.get_height():
            screen_f.blit(button_bckgrnd_f, (DISPLAY_WIDTH * 0.6875 + button_f.get_width() // 2 - button_bckgrnd_f.get_width() // 2,
                          DISPLAY_HEIGHT * 0.82 + button_f.get_height() // 2 - button_bckgrnd_f.get_height() // 2))


class ShiftingBackgoungnd(): 
    """
    Create background, move it an each tick on one pixel, and other changes.
    """
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
    """
    Main class, that contains game logics and execution
    """
    coins = 0 
    autog = 0 
    mong = 1
    costUpgrade = 50
    costAutominer = 50
    ver = "v0.1"

    def autominer(self):
        """
        It is auto adding of coins if corresponding upgrade has been bought
        """
        time.sleep(0.1)
        self.coins = self.coins + self.autog

    def main_loop(self):
        """
        Main loop of the game.
        """
        #setting display
        gameDisplay = pg.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
        pg.display.set_caption("Clicky Clicks")

        #Images
        imageSaver = ImageUploader('images')
        vmkLogo = imageSaver.uploadImage('click_logo.png', (0.125 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        msuLogo = imageSaver.uploadImage('msu_logo.png', (0.125 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        sadLogo = imageSaver.uploadImage('sadovnik.png', (0.125 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        clickImages = (vmkLogo, msuLogo, sadLogo)
        currLogo = msuLogo

        button_1 = imageSaver.uploadImage('button_1.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))
        butn_bckrnd = imageSaver.uploadImage('button_back_3.png', (0.32 * DISPLAY_WIDTH, 0.42 * DISPLAY_HEIGHT))
        bckgrnd_im = imageSaver.uploadImage('Game_back.jpeg', (DISPLAY_WIDTH, DISPLAY_HEIGHT))
        
        #Ininial values
        running = True
        shiftBackgoungnd = ShiftingBackgoungnd() 
        Drawer = Drawing()

        #Start
        
        clock = pg.time.Clock()

        while running:
            clock.tick(FPS)
            self.autominer()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running = False
    
                # Here we choose the right action depending on the cursor click place 
                if event.type == pg.MOUSEBUTTONDOWN:
                    mopos = pg.mouse.get_pos()
                    # if click for score
                    if mopos[0] >= DISPLAY_WIDTH * 0.42 and mopos[1] >= DISPLAY_HEIGHT * 0.42 and\
                       mopos[0] <= DISPLAY_WIDTH * 0.545 and mopos[1] <= DISPLAY_HEIGHT * 0.59:
                        self.coins += self.mong
                        currLogo = Drawer.newImageAfterClick(clickImages)

                    # if click for upgrade
                    elif mopos[0] >= DISPLAY_WIDTH * 0.0625 and DISPLAY_HEIGHT * 0.84 and\
                         mopos[0] <= DISPLAY_WIDTH * 0.42 + button_1.get_width() and\
                         mopos[1] <= DISPLAY_HEIGHT * 0.84 + button_1.get_height():
                        if self.coins >= self.costUpgrade:
                            self.coins = self.coins - self.costUpgrade
                            self.mong = self.mong * 1.1
                            self.costUpgrade = round(self.costUpgrade * 1.5, 0)

                    # if click for autominer
                    elif mopos[0] >= DISPLAY_WIDTH * 0.6875 and mopos[1] >= DISPLAY_HEIGHT * 0.84 and\
                         mopos[0] <= DISPLAY_WIDTH * 0.6875 + button_1.get_width() and\
                         mopos[1] <= DISPLAY_HEIGHT * 0.84 + button_1.get_height():
                        if self.coins >= self.costAutominer:
                            self.coins = self.coins - self.costAutominer
                            self.autog = self.autog + 0.5
                            self.costAutominer = round(self.costAutominer * 1.5, 0)

            # Func to create dynamic background
            shiftBackgoungnd.shift(gameDisplay, bckgrnd_im, DISPLAY_WIDTH)

            Drawer.dispaylBackgroundButton(pg.mouse.get_pos(), gameDisplay, button_1, butn_bckrnd)
            gameDisplay.blit(currLogo, (DISPLAY_WIDTH * 0.42, DISPLAY_HEIGHT * 0.42))

            Drawer.drawText("ВМИК lif(v)e", BLACK, LIGHT_BLUE, 
                            0.5 * DISPLAY_WIDTH, 0.12 * DISPLAY_HEIGHT, 50, screen = gameDisplay)
            Drawer.drawText("You have: " + str(f'{self.coins:.2f}') + " coins", BLACK, LIGHT_BLUE, 
                            0.15 * DISPLAY_WIDTH, 0.06 * DISPLAY_HEIGHT, 20, screen = gameDisplay)
            Drawer.drawText("Version: " + self.ver, BLACK, LIGHT_BLUE, 
                            0.85 * DISPLAY_WIDTH, 0.06 * DISPLAY_HEIGHT, 20, screen = gameDisplay)

            #displaying buttons
            gameDisplay.blit(button_1, (0.065 * DISPLAY_WIDTH, 0.80 * DISPLAY_HEIGHT))
            Drawer.drawText("Upgrade clicker: " + str(self.costUpgrade), BLACK, LIGHT_BLUE, 
                            0.065 * DISPLAY_WIDTH, 0.80 * DISPLAY_HEIGHT, 20, 
                            button_1.get_width() // 2, button_1.get_height() // 2, gameDisplay)
            gameDisplay.blit(button_1, (0.69 * DISPLAY_WIDTH, 0.80 * DISPLAY_HEIGHT))
            Drawer.drawText("Buy auto miner: " + str(self.costAutominer), BLACK, LIGHT_BLUE, 
                            0.69 * DISPLAY_WIDTH, 0.80 * DISPLAY_HEIGHT, 20, 
                            button_1.get_width() // 2, button_1.get_height() // 2, gameDisplay)

            #updating 
            pg.display.flip()
            
 
