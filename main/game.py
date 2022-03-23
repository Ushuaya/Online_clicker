# importing stuff
 
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
600 |                                           |
    |                                           |
    |                                           |
    |                                           |
    |-------------------------------------------|
    
 
"""
pg.init()

clock = pg.time.Clock()
ver = "ASSS v0.1 "
autog = 0
coins = 0
display_width = 800
display_height = 600
white = (255, 255, 255)
black = (0, 0, 0)
grey = (128, 128, 128)
light_grey = (224, 224, 224)
light_blue = (173, 216, 230)
grey = (128, 128, 128)
blue = (0, 100, 250)

logo_vmk = pg.image.load('click_logo.png')
logo_vmk = pg.transform.scale(logo_vmk, (100, 100))

msu_logo = pg.image.load('msu_logo.png')
msu_logo = pg.transform.scale(msu_logo, (100, 100))

sad_logo = pg.image.load('sadovnik.png')
sad_logo = pg.transform.scale(sad_logo, (100, 100))

button_1 = pg.image.load('button_1.png')
button_1 = pg.transform.scale(button_1, (200, 50))

butn_bckrnd = pg.image.load('button_back_3.png')
butn_bckrnd = pg.transform.scale(butn_bckrnd, (250, 250))
 
bckgrnd_im = pg.image.load('Game_back.jpeg')
bckgrnd_im = pg.transform.scale(bckgrnd_im, (display_width, display_height))
 
gameDisplay = pg.display.set_mode((display_width, display_height))
pg.display.set_caption("clicky clicks")


 
 
# def circle(display, color, x, y, radius):
#     pg.draw.circle(display, color, [x, y], radius)
 
def autominer():
    global coins
    global autog
    time.sleep(0.1)
    coins = coins + autog
 
 
def DrawText(text, Textcolor, Rectcolor, x, y, fsize, shift_1 = 0, shift_2 = 0):
    font = pg.font.Font('freesansbold.ttf', fsize)
    text = font.render(text, True, Textcolor, Rectcolor)
    textRect = text.get_rect()
    textRect.center = (x+shift_1, y+shift_2)
    gameDisplay.blit(text, textRect)
 
 
def rectangle(display, color, x, y, w, h):
    pg.draw.rect(display, color, (x, y, w, h))

def new_image_after_click(screen_f, prev_im = None):
    if prev_im != None:
        if prev_im%3 == 0:
            screen_f.blit(logo_vmk, (display_width*0.42, display_height*0.42))
        elif prev_im%3 == 1:
            screen_f.blit(sad_logo, (display_width*0.42, display_height*0.42))
        else:
            screen_f.blit(msu_logo, (display_width*0.42, display_height*0.42))
        return prev_im

    else:
        blaha_muha = random.randint(0, 10)
        if blaha_muha%3 == 0:
            screen_f.blit(logo_vmk, (display_width*0.42, display_height*0.42))
        elif blaha_muha%3 == 1:
            screen_f.blit(sad_logo, (display_width*0.42, display_height*0.42))
        else:
            screen_f.blit(msu_logo, (display_width*0.42, display_height*0.42))

        return blaha_muha


def dspl_bckgrnd_bttn(pos):
    if pos[0] >= 336 and pos[1] >= 252 and pos[0] <= 436 and pos[1] <= 352:
            gameDisplay.blit(butn_bckrnd, (display_width*0.42 - 75, display_height*0.42 - 75))

    if pos[0] >= 50 and pos[1] >= 500 and pos[0] <= 50+button_1.get_width() and pos[1] <= 500+button_1.get_height():
        gameDisplay.blit(butn_bckrnd, (50 + button_1.get_width()//2 - butn_bckrnd.get_width()//2, 500 + button_1.get_height()//2 - butn_bckrnd.get_height()//2))

    if pos[0] >= 550 and pos[1] >= 500 and pos[0] <= 550+button_1.get_width() and pos[1] <= 500+button_1.get_height():
        gameDisplay.blit(butn_bckrnd, (550 + button_1.get_width()//2 - butn_bckrnd.get_width()//2, 500 + button_1.get_height()//2 - butn_bckrnd.get_height()//2))


 
 
def main_loop():
    global clock
    global autog
    global ver
    global color1
    global color2
    global color3
    mong = 1
    cost = 50
    cost2 = 50
    global coins
    game_running = True
    current_image = 0
    cycle_back = 0 


    while game_running:
        if game_running: 
            autominer()

        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_running = False
 
            if event.type == pg.MOUSEBUTTONDOWN:
                mopos = pg.mouse.get_pos()
                if mopos[0] >= 336 and mopos[1] >= 252 and mopos[0] <= 436 and mopos[1] <= 352:
                    coins += mong
                    current_image = new_image_after_click(gameDisplay)



                elif mopos[0] >= 50 and mopos[1] >= 500 and mopos[0] <= 50+button_1.get_width() and mopos[1] <= 500+button_1.get_height():
                    if coins >= cost:
                        coins = coins - cost
                        cost = cost * 1.5
                        mong = mong * 1.1
                        cost = round(cost, 0)
                

                elif mopos[0] >= 550 and mopos[1] >= 500 and mopos[0] <= 550+button_1.get_width() and mopos[1] <= 500+button_1.get_height():
                    if coins >= cost2:
                        coins = coins - cost2
                        cost2 = cost2 * 1.5
                        autog = autog + 0.5
                        cost2 = round(cost2, 0)
                # if mopos >= (50, 0):
                #     if mopos <= (245, 0):
                #         if coins >= cost2:
                #             coins = coins - cost2
                #             cost2 = cost2 * 1.5
                #             autog = autog + 0.5
                #             cost2 = round(cost2, 0)

            
        
 
 
 
        gameDisplay.blit(bckgrnd_im,(0,0))
        gameDisplay.fill((0,0,0))
        gameDisplay.blit(bckgrnd_im,(cycle_back,0))
        gameDisplay.blit(bckgrnd_im,(display_width+cycle_back,0))
        if (cycle_back==-display_width):
            gameDisplay.blit(bckgrnd_im,(display_width+cycle_back,0))
            cycle_back=0
        cycle_back-=1

        
        dspl_bckgrnd_bttn(pg.mouse.get_pos())

        
        #gameDisplay.fill(light_blue)
        DrawText("ВМИК_lif(v)e", black, light_blue, 400, 100, 50)
        DrawText("you have " + str(f'{coins:.2f}') + " coins", black, light_blue, 100, 50, 20)
        #DrawText("upgrade clicker " + str(cost), black, light_blue, 700, 300, 20)
        #DrawText("buy auto miner " + str(cost2), black, light_blue, 150, 370, 20)
        DrawText("Version: " + ver, black, light_blue, 650, 50, 20)

        current_image = new_image_after_click(gameDisplay, current_image)

        # rectangle(gameDisplay, blue, 50, 400, 200, 300)
        # rectangle(gameDisplay, blue, 600, 317, 200, 300)

        gameDisplay.blit(button_1, (50, 500))
        DrawText("upgrade clicker " + str(cost), black, light_blue, 50, 500, 20, button_1.get_width()//2, button_1.get_height()//2)

        gameDisplay.blit(button_1, (550, 500))
        DrawText("buy auto miner " + str(cost2), black, light_blue, 550, 500, 20, button_1.get_width()//2, button_1.get_height()//2)


        

        pg.display.update()
        clock.tick(60)
 
main_loop()
pg.quit()
quit()