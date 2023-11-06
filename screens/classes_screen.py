import pygame
import pygame_gui
from pygame_gui.core import ObjectID

from static import *
from screens.start_screen import StartScreen

class ClassesScreen:
    class1_button = None
    class2_button = None
    class3_button = None

    def build_classes_screen(self):
        ClassesScreen.build_images_texts()
        ClassesScreen.build_buttons()
    
    @staticmethod
    def build_images_texts():
        StartScreen.build_images_texts(back_img=True)

    @staticmethod
    def build_buttons():
        screen_w, screen_h = screen.get_width(), screen.get_height()
        button_w, button_h = (screen.get_width()/3) ,(screen.get_height()/11)

        button_style = '#button_fullscreen' if is_fullscreen() else '#button_notfullscreen'

        manager = manager_getter()

        ClassesScreen.class1_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='Klasa 1',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@green'))

        ClassesScreen.class2_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)+(button_h/2)), (button_w, button_h)),
                                                    text='Klasa 2',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@orange'))

        ClassesScreen.class3_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)+(button_h*2)), (button_w, button_h)),
                                                    text='Klasa 3', 
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@red')) 
        game_buttons.extend((ClassesScreen.class1_button, ClassesScreen.class2_button, ClassesScreen.class3_button))