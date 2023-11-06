import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from static import *
from screens.start_screen import StartScreen

class PlayScreen:
    math_button = None
    polish_button = None
    english_button = None
    
    def build_play_screen(self):
        PlayScreen.build_images_texts()
        PlayScreen.build_buttons()

    @staticmethod
    def build_images_texts():
        StartScreen.build_images_texts(back_img=True)

    @staticmethod
    def build_buttons():
        screen_w, screen_h = screen.get_width(), screen.get_height()
        button_w, button_h = (screen.get_width()/3) ,(screen.get_height()/11)

        button_style = '#button_fullscreen' if is_fullscreen() else '#button_notfullscreen'

        manager = manager_getter()

        PlayScreen.math_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='Matematyka',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@orange'))

        PlayScreen.polish_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)+(button_h/2)), (button_w, button_h)),
                                                    text='Polski',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@green'))

        PlayScreen.english_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)+(button_h*2)), (button_w, button_h)),
                                                    text='Angielski',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue')) 
        game_buttons.extend((PlayScreen.math_button, PlayScreen.polish_button, PlayScreen.english_button))