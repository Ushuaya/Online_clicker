import pygame as pg
from .insertion_deleting_sqlite import register, sighin
from .__init__ import Drawing, ImageUploader
DISPLAY_WIDTH = 1024
DISPLAY_HEIGHT = 768




pg.init()
screen = pg.display.set_mode((1024, 768))
pg.display.set_caption("Inputer")
COLOR_INACTIVE = pg.Color('lightskyblue3')
COLOR_ACTIVE = pg.Color('dodgerblue2')
FONT = pg.font.Font(None, 32)

imageSaver = ImageUploader('images')
button_1 = imageSaver.uploadImage('button_upgrade.png', (0.30 * DISPLAY_WIDTH, 0.125 * DISPLAY_HEIGHT))


class InputBox:

    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = COLOR_INACTIVE
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.print = ""
        self.password = False

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
                    self.txt_surface = FONT.render("*"*len(self.text) if self.password == True else self.text, True, self.color)  
                    return self.print
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if event.unicode != " ":
                        self.text += event.unicode
                # Re-render the text.
                self.txt_surface = FONT.render("*"*len(self.text) if self.password == True else self.text, True, self.color)
        

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y+5))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)




def main_c(coins = None):
    FONT = pg.font.Font(None, 32)
    print("ok")
    clock = pg.time.Clock()
    input_box1 = InputBox(DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT*0.28, 140, 32)
    input_box2 = InputBox(DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT*0.48, 140, 32)
    input_box2.password = True
    input_box3 = InputBox(DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT*0.68, 140, 32)
    input_box3.password = True
    input_boxes = [input_box1, input_box2]
    input_boxes_registration = [input_box1, input_box2, input_box3]
    done = False
    Drawer2 = Drawing()

    # step one 
    Next_stage = "REG_SIGN"
    done = False
    exit_module = False
    coins_update = 0

    while not exit_module:
        if Next_stage == "REG_SIGN":
            done = not done 
            while not done:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        exit_module = True

                    elif event.type == pg.MOUSEBUTTONDOWN:
                            mopos = pg.mouse.get_pos()

                            if  mopos[0] >= DISPLAY_WIDTH * 0.1 and mopos[1] >= DISPLAY_HEIGHT * 0.1 and\
                                mopos[0] <= DISPLAY_WIDTH * 0.1 + button_1.get_width() and\
                                mopos[1] <= DISPLAY_HEIGHT * 0.1 + button_1.get_height():
                                Next_stage = "REGISTRATION"
                                done = not done
                                break

                            elif mopos[0] >= DISPLAY_WIDTH * 0.6 and mopos[1] >= DISPLAY_HEIGHT * 0.1 and\
                                mopos[0] <= DISPLAY_WIDTH * 0.6 + button_1.get_width() and\
                                mopos[1] <= DISPLAY_HEIGHT * 0.1 + button_1.get_height():
                                Next_stage = "SIGN_IN"
                                done = not done
                                break

                            elif mopos[0] >= DISPLAY_WIDTH * 0.2 and mopos[1] >= DISPLAY_HEIGHT * 0.8 and\
                                mopos[0] <= DISPLAY_WIDTH * 0.2 + button_1.get_width() and\
                                mopos[1] <= DISPLAY_HEIGHT * 0.8 + button_1.get_height():
                                Next_stage = ""
                                done = not done
                                exit_module = not exit_module
                                return coins

                    
                screen.fill((30, 30, 30))
                screen.blit(button_1, (DISPLAY_WIDTH*0.1, 0.1 * DISPLAY_HEIGHT))
                Drawer2.drawText("Registration" , (0, 0, 0), None, 
                                    DISPLAY_WIDTH*0.25, 0.16 * DISPLAY_HEIGHT, 20, screen = screen)
                screen.blit(button_1, (DISPLAY_WIDTH*0.6, 0.1 * DISPLAY_HEIGHT))
                Drawer2.drawText("Sign in" , (0, 0, 0), None, 
                                    DISPLAY_WIDTH*0.75, 0.16 * DISPLAY_HEIGHT, 20, screen = screen)

                screen.blit(button_1, (DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.8))
                Drawer2.drawText("BACK" , (0, 0, 0), None, 
                                DISPLAY_WIDTH * 0.35, DISPLAY_HEIGHT * 0.87, 20, screen = screen)

                pg.display.flip()


        if Next_stage == "REGISTRATION":
            done = not done
            wrong_inp = False
            while not done:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        exit_module = True

                    elif event.type == pg.MOUSEBUTTONDOWN:
                        mopos = pg.mouse.get_pos()

                        if  mopos[0] >= DISPLAY_WIDTH * 0.6 and mopos[1] >= DISPLAY_HEIGHT * 0.8 and\
                            mopos[0] <= DISPLAY_WIDTH * 0.6 + button_1.get_width() and\
                            mopos[1] <= DISPLAY_HEIGHT * 0.8 + button_1.get_height():
                            #done = not done
                            #print("There ate not empty: ", input_boxes[0].text, input_boxes[1].text)
                            if input_boxes_registration[1].text == input_boxes_registration[2].text:
                                table_10, pos = register(None, input_boxes_registration[0].text, input_boxes_registration[1].text, coins)
                                coins_update = coins
                            else:
                                table_10 = 4
                            #print(table_10, "\n", pos[0])
                            


                            match table_10: 
                                case 1: 
                                    wrong_inp = True
                                    Error_msg = "Username is empty"
                                case 2: 
                                    wrong_inp = True
                                    Error_msg = "Password is empty"
                                case 3: 
                                    wrong_inp = True
                                    Error_msg = "User with same also exists..."
                                case 4: 
                                    wrong_inp = True
                                    Error_msg = "Passwords are not equaol..."
                                case _: 
                                    wrong_inp = False
                                    Error_msg = ""
                                    Next_stage = "SHOW_RESULT"
                                    done = not done

                        elif mopos[0] >= DISPLAY_WIDTH * 0.2 and mopos[1] >= DISPLAY_HEIGHT * 0.8 and\
                            mopos[0] <= DISPLAY_WIDTH * 0.2 + button_1.get_width() and\
                            mopos[1] <= DISPLAY_HEIGHT * 0.8 + button_1.get_height():
                            done = not done 
                            Next_stage = "REG_SIGN"

                    for i in range(len(input_boxes_registration)):
                        frog = input_boxes_registration[i].handle_event(event)
                        if frog != None: 
                            print(frog)

                for box in input_boxes_registration:
                    box.update()

                screen.fill((30, 30, 30))
                for box in input_boxes_registration:
                    box.draw(screen)

                Drawer2.drawText("Username: " , (0, 0, 0), (100, 110, 110), 
                                    DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.3, 20, screen = screen)
                
                Drawer2.drawText("Password: " , (0, 0, 0), (100, 110, 110), 
                                    DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.5, 20, screen = screen)
                
                Drawer2.drawText("Password again: " , (0, 0, 0), (100, 110, 110), 
                                    DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.7, 20, screen = screen)


                screen.blit(button_1, (DISPLAY_WIDTH * 0.6, DISPLAY_HEIGHT * 0.8))
                Drawer2.drawText("Register" , (0, 0, 0), None, 
                                DISPLAY_WIDTH * 0.75, DISPLAY_HEIGHT * 0.87, 20, screen = screen)

                screen.blit(button_1, (DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.8))
                Drawer2.drawText("BACK" , (0, 0, 0), None, 
                                DISPLAY_WIDTH * 0.35, DISPLAY_HEIGHT * 0.87, 20, screen = screen)

                if wrong_inp: 
                    Drawer2.drawText(Error_msg , (255, 0, 0), None, 
                                DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT * 0.4, 20, screen = screen)



                pg.display.flip()
                #clock.tick(30)

        if Next_stage == "SIGN_IN":
            done = not done
            wrong_inp = False
            Error_msg = ""
            while not done:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        exit_module = True

                    elif event.type == pg.MOUSEBUTTONDOWN:
                        mopos = pg.mouse.get_pos()

                        if  mopos[0] >= DISPLAY_WIDTH * 0.6 and mopos[1] >= DISPLAY_HEIGHT * 0.8 and\
                            mopos[0] <= DISPLAY_WIDTH * 0.6 + button_1.get_width() and\
                            mopos[1] <= DISPLAY_HEIGHT * 0.8 + button_1.get_height():
                            #done = not done
                            #print("There ate not empty: ", input_boxes[0].text, input_boxes[1].text)
                            table_10, pos, coins_update = sighin(None, input_boxes[0].text, input_boxes[1].text, coins)
                            #print(table_10, "\n", pos[0])
                            match table_10: 
                                case 1: 
                                    wrong_inp = True
                                    Error_msg = "You are not registrated yet"
                                case 2: 
                                    wrong_inp = True
                                    Error_msg = "You didn't input password"
                                case 3: 
                                    wrong_inp = True
                                    Error_msg = "Wrong password"
                                case 4: 
                                    wrong_inp = True
                                    Error_msg = "You didn't specify username"
                                case _: 
                                    wrong_inp = False
                                    Error_msg = ""
                                    Next_stage = "SHOW_RESULT"
                                    done = not done

                        elif mopos[0] >= DISPLAY_WIDTH * 0.2 and mopos[1] >= DISPLAY_HEIGHT * 0.8 and\
                            mopos[0] <= DISPLAY_WIDTH * 0.2 + button_1.get_width() and\
                            mopos[1] <= DISPLAY_HEIGHT * 0.8 + button_1.get_height():
                            done = not done 
                            Next_stage = "REG_SIGN"


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
                                    DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.3, 20, screen = screen)
                
                Drawer2.drawText("Password: " , (0, 0, 0), (100, 110, 110), 
                                    DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.5, 20, screen = screen)


                screen.blit(button_1, (DISPLAY_WIDTH * 0.6, DISPLAY_HEIGHT * 0.8))
                Drawer2.drawText("Sign in" , (0, 0, 0), None, 
                                DISPLAY_WIDTH * 0.75, DISPLAY_HEIGHT * 0.87, 20, screen = screen)

                screen.blit(button_1, (DISPLAY_WIDTH * 0.2, DISPLAY_HEIGHT * 0.8))
                Drawer2.drawText("BACK" , (0, 0, 0), None, 
                                DISPLAY_WIDTH * 0.35, DISPLAY_HEIGHT * 0.87, 20, screen = screen)

                if wrong_inp: 
                    Drawer2.drawText(Error_msg , (255, 0, 0), None, 
                                DISPLAY_WIDTH * 0.3, DISPLAY_HEIGHT * 0.4, 20, screen = screen)



                pg.display.flip()
                #clock.tick(30)


            
        if Next_stage == "SHOW_RESULT":
            done = not done 
            while not done:
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        done = True
                        exit_module = True
                    
                    elif event.type == pg.MOUSEBUTTONDOWN:
                        mopos = pg.mouse.get_pos()

                        if  mopos[0] >= DISPLAY_WIDTH * 0.6 and mopos[1] >= DISPLAY_HEIGHT * 0.8 and\
                            mopos[0] <= DISPLAY_WIDTH * 0.6 + button_1.get_width() and\
                            mopos[1] <= DISPLAY_HEIGHT * 0.8 + button_1.get_height():
                            done = not done 
                            #Next_stage = "REG_SIGN"
                            exit_module = not exit_module
                            return coins_update

                screen.fill((30, 30, 30))
                #table_10 = eval(table_10)
                
                list_to_print = [("Top 10 players: ")] + table_10 + [("")] + [("Your place: ")] + [(pos[0][2])]
                enter = 0 
                for i in list_to_print: 
                    Drawer2.drawText(str(i)  , (50, 100, 11), None, 
                                    DISPLAY_WIDTH//2, DISPLAY_HEIGHT//5 + enter, 20, screen = screen)
                    enter += 25


                screen.blit(button_1, (DISPLAY_WIDTH * 0.6, DISPLAY_HEIGHT * 0.8))
                Drawer2.drawText("DONE" , (0, 0, 0), None, 
                                DISPLAY_WIDTH * 0.75, DISPLAY_HEIGHT * 0.87, 20, screen = screen)
                
                
                pg.display.flip()
                #clock.tick(30)

            

    


if __name__ == '__main__':
    main()
    pg.quit()

