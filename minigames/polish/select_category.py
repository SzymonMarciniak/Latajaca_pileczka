from pygame_gui.core import ObjectID
import pygame_gui
import pygame

from screens.play_screen import StartScreen
from static import screen, is_fullscreen, manager_getter, game_buttons
from database_actions import execute_query


class SelectPolishCategory:

    category_buttons = []

    def build_category_screen(self):
        SelectPolishCategory.build_images_texts()
        SelectPolishCategory.build_buttons()

    @staticmethod
    def build_images_texts():
        StartScreen.build_images_texts(back_img=True) 

    @staticmethod
    def build_buttons():
        selected_class = execute_query("SELECT choosen_class FROM game_data WHERE id=1")[0][0]

        if selected_class == 1:
            SelectPolishCategory.build_1_class()
        elif selected_class == 2:
            SelectPolishCategory.build_2_class()
        elif selected_class == 3:
            SelectPolishCategory.build_3_class()

    @staticmethod
    def build_1_class(): 
        screen_w, screen_h = screen.get_width(), screen.get_height()
        button_w, button_h = (screen.get_height()/4) ,(screen.get_height()/4)

        button_style = '#button_fullscreen' if is_fullscreen() else '#button_notfullscreen'

        manager = manager_getter() 

        SelectPolishCategory.u_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2.1)-(button_w*1.25), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='Ó / U',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue'))

        SelectPolishCategory.rz_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2.1)+(button_w/1.75), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='RZ / Ż',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue'))

        SelectPolishCategory.ch_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)+(button_h/2)), (button_w, button_h)),
                                                    text='CH / H',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue')) 
        
        
        
        SelectPolishCategory.category_buttons.extend((SelectPolishCategory.u_button, SelectPolishCategory.rz_button, SelectPolishCategory.ch_button))
        game_buttons.extend((SelectPolishCategory.u_button, SelectPolishCategory.rz_button, SelectPolishCategory.ch_button)) 

    @staticmethod
    def build_2_class(): 
        screen_w, screen_h = screen.get_width(), screen.get_height()
        button_w, button_h = (screen.get_height()/4) ,(screen.get_height()/4)

        button_style = '#button_fullscreen' if is_fullscreen() else '#button_notfullscreen'

        manager = manager_getter() 

        SelectPolishCategory.u_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2.1)-(button_w*1.25), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='Ó / U',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue'))

        SelectPolishCategory.rz_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2.1)+(button_w/1.75), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='RZ / Ż',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue'))

        SelectPolishCategory.ch_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)+(button_h/2)), (button_w, button_h)),
                                                    text='CH / H',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue')) 
        
        
        
        SelectPolishCategory.category_buttons.extend((SelectPolishCategory.u_button, SelectPolishCategory.rz_button, SelectPolishCategory.ch_button))
        game_buttons.extend((SelectPolishCategory.u_button, SelectPolishCategory.rz_button, SelectPolishCategory.ch_button))  

    @staticmethod
    def build_3_class(): 
        screen_w, screen_h = screen.get_width(), screen.get_height()
        button_w, button_h = (screen.get_height()/4) ,(screen.get_height()/4)

        button_style = '#button_fullscreen' if is_fullscreen() else '#button_notfullscreen'

        manager = manager_getter() 

        SelectPolishCategory.u_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2.1)-(button_w*1.25), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='Ó / U',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue'))

        SelectPolishCategory.rz_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2.1)+(button_w/1.75), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='RZ / Ż',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue'))

        SelectPolishCategory.ch_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2.1)-(button_w*1.25), (screen_h/2)+(button_h/2)), (button_w, button_h)),
                                                    text='CH / H',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue')) 
        
        SelectPolishCategory.no_less = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2.1)+(button_w/1.75), (screen_h/2)+(button_h/2)), (button_w, button_h)),
                                                    text='Nie / Nie',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue')) 
        
        
        
        SelectPolishCategory.category_buttons.extend((SelectPolishCategory.u_button, SelectPolishCategory.rz_button, SelectPolishCategory.ch_button, SelectPolishCategory.no_less))
        game_buttons.extend((SelectPolishCategory.u_button, SelectPolishCategory.rz_button, SelectPolishCategory.ch_button, SelectPolishCategory.no_less))  










