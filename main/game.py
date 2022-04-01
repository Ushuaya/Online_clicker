from typing import Any
import pygame as pg
import time
import random


"""
                        800
    |-------------------------------------------|
    |                                           |
    |                                           |
    |                                           |
    |                                           |
600 |                main_click                 |
    |                                           |
    |                                           |
    |    b_1                             b_2    |
    |-------------------------------------------|
    
"""


class Const_Varaibles: 
    """
    Just simple class, that contains some constant values
    """
    button_1_pos = None 
    button_2_pos = None 
    button_3_pos = None 
    display_width = 800
    display_height = 600



class images_saver(Const_Varaibles):
    """
    Uploader of images
    """ 
    def upload_image(self, name: str, size: tuple) -> object:
        tmp = pg.image.load(name)
        tmp = pg.transform.scale(tmp, size)
        return tmp



class Drawing(Const_Varaibles): 

    def DrawText(self, text: str, Textcolor: tuple, Rectcolor: tuple, x: int, y: int, fsize: int , shift_1: int = 0, shift_2: int = 0, screen: object = None) -> None:
        """
        Un this function the text occurs in the main screen, so the parametres are text -- the text,
        that will be implemented to the main screen. Textcolor -- clolour of the text, Rectcolor -- ...,
        x, y -- position of the left-highest angle, fsize -- size of text, shift_1 -- shift of the text 
        window in pixels on the x axis, shift_2 -- shift of the text window in pixels on the y axis
        """
        font = pg.font.Font('freesansbold.ttf', fsize)
        text = font.render(text, True, Textcolor, Rectcolor)
        textRect = text.get_rect()
        textRect.center = (x+shift_1, y+shift_2)
        screen.blit(text, textRect)
    
    def new_image_after_click(self, screen_f: object, prev_im: object, pict_1_click: object = None, pict_2_click: object = None, pict_3_click: object = None) -> None :
        """
        Here the implementation of the changing of the main-click logo. It has the random
        of the probabilty of the changing of the screen. 
        """
        if prev_im != None:
            if prev_im%3 == 0:
                screen_f.blit(pict_1_click, (self.display_width * 0.42, self.display_height * 0.42))
            elif prev_im%3 == 1:
                screen_f.blit(pict_2_click, (self.display_width * 0.42, self.display_height * 0.42))
            else:
                screen_f.blit(pict_3_click, (self.display_width * 0.42, self.display_height * 0.42))
            return prev_im

        else:
            blaha_muha = random.randint(0, 10)
            if blaha_muha%3 == 0:
                screen_f.blit(pict_1_click, (self.display_width * 0.42, self.display_height * 0.42))
            elif blaha_muha%3 == 1:
                screen_f.blit(pict_2_click, (self.display_width * 0.42, self.display_height * 0.42))
            else:
                screen_f.blit(pict_3_click, (self.display_width * 0.42, self.display_height * 0.42))

            return blaha_muha

    def dspl_bckgrnd_bttn(self, pos: tuple , screen_f:object = None, button_f: object = None, button_bckgrnd_f: object = None) -> None:
        """
        function that creates the background of button when the cursor moves above it
        """
        if pos[0] >= 336 and pos[1] >= 252 and pos[0] <= 436 and pos[1] <= 352:
            screen_f.blit(button_bckgrnd_f, (self.display_width * 0.42 - 75, self.display_height * 0.42 - 75))

        if pos[0] >= 50 and pos[1] >= 500 and pos[0] <= 50+button_f.get_width() and pos[1] <= 500+button_f.get_height():
            screen_f.blit(button_bckgrnd_f, (50 + button_f.get_width()//2 - button_bckgrnd_f.get_width()//2, 500 + button_f.get_height()//2 - button_bckgrnd_f.get_height()//2))

        if pos[0] >= 550 and pos[1] >= 500 and pos[0] <= 550+button_f.get_width() and pos[1] <= 500+button_f.get_height():
            screen_f.blit(button_bckgrnd_f, (550 + button_f.get_width()//2 - button_bckgrnd_f.get_width()//2, 500 + button_f.get_height()//2 - button_bckgrnd_f.get_height()//2))

class Running_backgnd(Const_Varaibles): 
    """
    Class that creates background, moves it an each tick on one pixel, and other changings
    """
    cycle_back = 0 

    def running(self, screen_f: object , bckgrnd_im_f: object, im_len: int):
        """
        Main function, that implements the
        """
        screen_f.blit(bckgrnd_im_f,(0,0))
        screen_f.fill((0,0,0))
        screen_f.blit(bckgrnd_im_f,(self.cycle_back,0))
        screen_f.blit(bckgrnd_im_f,(im_len+self.cycle_back,0))
        if (self.cycle_back==-im_len):
            screen_f.blit(bckgrnd_im_f,(im_len+self.cycle_back,0))
            self.cycle_back=0
        self.cycle_back-=1


class main__(Const_Varaibles): 
    """
    Main class, that contains game logics and execution
    """
    coins = 0 
    autog = 0 
    mong = 1
    cost = 50
    cost2 = 50
    ver = "ASSS v0.1 "
    black = (0, 0, 0)
    light_blue = (173, 216, 230)

    def autominer(self):
        """
        It is auto adding of coins if corresponding upgrade has been bought
        """
        time.sleep(0.1)
        self.coins = self.coins + self.autog


    def main_loop(self):
        """
        main loop of the game
        """
        #Images
        logo_vmk = images_saver().upload_image('click_logo.png', (100, 100))
        msu_logo = images_saver().upload_image('msu_logo.png', (100, 100))
        sad_logo = images_saver().upload_image('sadovnik.png', (100, 100))
        button_1 = images_saver().upload_image('button_1.png', (200, 50))
        butn_bckrnd = images_saver().upload_image('button_back_3.png', (250, 250))
        bckgrnd_im = images_saver().upload_image('Game_back.jpeg', (self.display_width, self.display_height))
        
        #setting display
        gameDisplay = pg.display.set_mode((self.display_width, self.display_height))
        pg.display.set_caption("clicky clicks")

        #Ininial values
        game_running = True
        current_image = 0
        running_backgrnd_var = Running_backgnd() 
        Drawer = Drawing()

        #Start
        pg.init()
        clock = pg.time.Clock()

        while game_running:
            if game_running: 
                self.autominer()

            for event in pg.event.get():
                if event.type == pg.QUIT:
                    game_running = False
    
                #here we choosing the right action depending on the cursor click place 
                if event.type == pg.MOUSEBUTTONDOWN:
                    mopos = pg.mouse.get_pos()
                    if mopos[0] >= 336 and mopos[1] >= 252 and mopos[0] <= 436 and mopos[1] <= 352:
                        self.coins += self.mong
                        current_image = Drawer.new_image_after_click(gameDisplay, None, logo_vmk, sad_logo, msu_logo)

                    elif mopos[0] >= 50 and mopos[1] >= 500 and mopos[0] <= 50+button_1.get_width() and mopos[1] <= 500+button_1.get_height():
                        if self.coins >= self.cost:
                            self.coins = self.coins - self.cost
                            self.cost = self.cost * 1.5
                            self.mong = self.mong * 1.1
                            self.cost = round(self.cost, 0)

                    elif mopos[0] >= 550 and mopos[1] >= 500 and mopos[0] <= 550+button_1.get_width() and mopos[1] <= 500+button_1.get_height():
                        if self.coins >= self.cost2:
                            self.coins = self.coins - self.cost2
                            self.cost2 = self.cost2 * 1.5
                            self.autog = self.autog + 0.5
                            self.cost2 = round(self.cost2, 0)

            #Some func to create dynamic background
            running_backgrnd_var.running(gameDisplay, bckgrnd_im, self.display_width)

            Drawer.dspl_bckgrnd_bttn(pg.mouse.get_pos(), gameDisplay, button_1, butn_bckrnd)
            Drawer.DrawText("ВМИК_lif(v)e", self.black, self.light_blue, 400, 100, 50, screen = gameDisplay)
            Drawer.DrawText("you have " + str(f'{self.coins:.2f}') + " coins", self.black, self.light_blue, 100, 50, 20, screen = gameDisplay)
            Drawer.DrawText("Version: " + self.ver, self.black, self.light_blue, 650, 50, 20, screen = gameDisplay)
            current_image = Drawer.new_image_after_click(gameDisplay, current_image, logo_vmk, sad_logo, msu_logo)

            #displaying buttons
            gameDisplay.blit(button_1, (50, 500))
            Drawer.DrawText("upgrade clicker " + str(self.cost), self.black, self.light_blue, 50, 500, 20, button_1.get_width()//2, button_1.get_height()//2, gameDisplay)
            gameDisplay.blit(button_1, (550, 500))
            Drawer.DrawText("buy auto miner " + str(self.cost2), self.black, self.light_blue, 550, 500, 20, button_1.get_width()//2, button_1.get_height()//2, gameDisplay)

            #updating 
            pg.display.update()
            clock.tick(60)
 

if __name__ == "__main__":
    main__().main_loop()
    pg.quit()
    quit()