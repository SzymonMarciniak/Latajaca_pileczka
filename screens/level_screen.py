import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from screens.start_screen import StartScreen
from database_actions import execute_query
from static import *

class LevelScreen:
    level_buttons = []
    def build_level_screen(self):
        LevelScreen.build_images_texts()
        LevelScreen.build_buttons() 

    @staticmethod
    def build_images_texts():
        StartScreen.build_images_texts(back_img=True)

    @staticmethod
    def build_buttons():
        screen_w, screen_h = screen.get_width(), screen.get_height()
        button_w, button_h = (screen.get_width()/15) ,(screen.get_width()/15)
        vw = screen_w/100
        vh = screen_h/100

        manager = manager_getter()

        entire_width = screen_w-(24*vw)
        free_width = entire_width - 8*button_w
        space_x = free_width/7

        entire_heigth = screen_h - screen_h/3 - 15*vh
        free_height = entire_heigth - 4*button_h
        space_y = free_height/3

        w = -1
        pos_y = screen_h/3

        levels_amount = 32

        sub_category = execute_query("SELECT sub_category FROM game_data")[0][0]

        if sub_category == "Mnożenie": levels_amount = 15
        elif sub_category == "Ó / U" or sub_category == "RZ / Ż" or \
            sub_category == "CH / H" or sub_category == "Event":
            levels_amount = 16
        elif sub_category == "english":
            levels_amount = 17
        

        for i in range(1,levels_amount+1):
            w += 1
            if ((i-1) % 8 == 0) and (i-1!=0):
                pos_y += button_h + space_y
                w = 0

            button_style = '#level_button_fullscreen' if is_fullscreen() else '#level_button_notfullscreen'

            pos_x = (12*vw + w*(button_w+space_x))
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((pos_x, pos_y)), (button_w, button_h)),
                                                    text=str(i),manager=manager,object_id=ObjectID(class_id=button_style))
            LevelScreen.level_buttons.append(button)

        if sub_category == "Event":
            pos_x = (12*vw + 1.25*(button_w+space_x))
            pos_y = 5*(button_h + space_y)
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((pos_x, pos_y)), ((button_w+space_x)*2.5, button_h)),
                                                    text="Czy awansujesz do",manager=manager,object_id=ObjectID(class_id=button_style))
            LevelScreen.level_buttons.append(button)

            pos_x = (12*vw + 3.9*(button_w+space_x))
            button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((pos_x, pos_y)), ((button_w+space_x)*2.5, button_h)),
                                                    text="4 klasy podstawowej?",manager=manager,object_id=ObjectID(class_id=button_style))
            LevelScreen.level_buttons.append(button)

        game_buttons.extend(LevelScreen.level_buttons)
