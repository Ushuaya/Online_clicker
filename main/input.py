from unittest import result
import pygame as pg
from insertion_deleting_sqlite import register, sighin
from __init__ import Drawing, ImageUploader
DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480






pg.init()
screen = pg.display.set_mode((640, 480))
pg.display.set_caption("Inputer")
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

imageSaver = ImageUploader('images')
button_1 = imageSaver.uploadImage('button_1.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.print = ""

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.print = self.text
                    self.text = ''
                    self.txt_surface = FONT.render(self.text, True, self.color)
                    return self.print
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, self.color)
        

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)








def main():
    print("ok")
    clock = pg.time.Clock()
    input_box1 = InputBox(100, 100, 140, 32)
    input_box2 = InputBox(100, 300, 140, 32)
    input_boxes = [input_box1, input_box2]
    done = False
    Drawer2 = Drawing()

    # step one 
    Next_stage = ""
    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True

            elif event.type == pg.MOUSEBUTTONDOWN:
                    mopos = pg.mouse.get_pos()

                    if  mopos[0] >= DISPLAY_WIDTH * 0.1 and mopos[1] >= DISPLAY_HEIGHT * 0.1 and\
                        mopos[0] <= DISPLAY_WIDTH * 0.1 + button_1.get_width() and\
                        mopos[1] <= DISPLAY_HEIGHT * 0.1 + button_1.get_height():
                        Next_stage = "REGISTRATION"
                        done = not done

                    elif mopos[0] >= DISPLAY_WIDTH * 0.6 and mopos[1] >= DISPLAY_HEIGHT * 0.1 and\
                        mopos[0] <= DISPLAY_WIDTH * 0.6 + button_1.get_width() and\
                        mopos[1] <= DISPLAY_HEIGHT * 0.1 + button_1.get_height():
                        Next_stage = "SIGN_IN"
                        done = not done

            
        screen.fill((30, 30, 30))
        screen.blit(button_1, (DISPLAY_WIDTH*0.1, 0.1 * DISPLAY_HEIGHT))
        Drawer2.drawText("Registration" , (0, 0, 0), None, 
                            DISPLAY_WIDTH*0.25, 0.16 * DISPLAY_HEIGHT, 20, screen = screen)
        screen.blit(button_1, (DISPLAY_WIDTH*0.6, 0.1 * DISPLAY_HEIGHT))
        Drawer2.drawText("Sign in" , (0, 0, 0), None, 
                            DISPLAY_WIDTH*0.75, 0.16 * DISPLAY_HEIGHT, 20, screen = screen)

        pg.display.flip()

    done = not done
    if Next_stage == "REGISTRATION":
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

                elif event.type == pg.MOUSEBUTTONDOWN:
                    mopos = pg.mouse.get_pos()

                    if  mopos[0] >= DISPLAY_WIDTH * 0.6 and mopos[1] >= DISPLAY_HEIGHT * 0.8 and\
                        mopos[0] <= DISPLAY_WIDTH * 0.6 + button_1.get_width() and\
                        mopos[1] <= DISPLAY_HEIGHT * 0.8 + button_1.get_height():
                        Next_stage = "REGISTRATION"
                        #done = not done
                        #print("There ate not empty: ", input_boxes[0].text, input_boxes[1].text)
                        table_10, pos = register(None, input_boxes[0].text, input_boxes[1].text)
                        #print(table_10, "\n", pos[0])
                        Next_stage = "SHOW_RESULT"
                        done = not done 

                for i in range(len(input_boxes)):
                    frog = input_boxes[i].handle_event(event)
                    if frog != None: 
                        print(frog)

            for box in input_boxes:
                box.update()

            screen.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(screen)

            Drawer2.drawText("Username: " , (0, 0, 0), (100, 110, 110), 
                                60, 105, 20, screen = screen)
            
            Drawer2.drawText("Password: " , (0, 0, 0), (100, 110, 110), 
                                60, 150, 20, screen = screen)


            screen.blit(button_1, (DISPLAY_WIDTH * 0.6, DISPLAY_HEIGHT * 0.8))
            Drawer2.drawText("Register" , (0, 0, 0), None, 
                            DISPLAY_WIDTH * 0.75, DISPLAY_HEIGHT * 0.87, 20, screen = screen)



            pg.display.flip()
            #clock.tick(30)

    if Next_stage == "SIGN_IN":
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True
                for box in input_boxes:
                    frog = box.handle_event(event)
                    if frog != None: 
                        print(frog)

            for box in input_boxes:
                box.update()

            screen.fill((30, 30, 30))
            for box in input_boxes:
                box.draw(screen)

            Drawer2.drawText("Username: " , (0, 0, 0), (100, 110, 110), 
                                60, 105, 20, screen = screen)
            
            Drawer2.drawText("Password: " , (0, 0, 0), (100, 110, 110), 
                                60, 150, 20, screen = screen)

            pg.display.flip()
            #clock.tick(30)

    done = not done        
    if Next_stage == "SHOW_RESULT":
        while not done:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    done = True

            Drawer2.drawText("Top 10 players: " + str(table_10) , (0, 0, 0), (100, 110, 110), 
                                60, 105, 20, screen = screen)
            
            Drawer2.drawText("Your place: " + str(pos) , (0, 0, 0), (100, 110, 110), 
                                60, 150, 20, screen = screen)

            pg.display.flip()
            #clock.tick(30)

        

    


if __name__ == '__main__':
    main()
    pg.quit()

