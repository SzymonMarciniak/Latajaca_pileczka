import pygame 
import pygame_gui
from pygame_gui.core import ObjectID

from static import *
import static
from utils import *


class StartScreen:    
    def build_start_screen(self):
        StartScreen.build_images_texts()
        StartScreen.build_buttons()
       

    @staticmethod
    def build_images_texts(back_img=False):
        print(screen)
        screen_w, screen_h = screen.get_width(), screen.get_height()
        vw = screen_w/100
        
        new_background = pygame.transform.scale(background, (screen_w, screen_h))
        static.background = new_background
        
        main_text_size = 50 if not is_fullscreen() else 100
        main_text = set_text("Dwa ognie", (screen_w/2), screen_h/9, main_text_size)

        if back_img:
            exit_image = pygame.image.load("images/return_button.png")
        else:   
            exit_image = pygame.image.load("images/exit_button.png")
        
        settings_image = pygame.image.load("images/settings_button.png")

        btns_pos = 4
        if not is_fullscreen():
            exit_image = pygame.transform.scale(exit_image, (8*vw, 8*vw))
            settings_image = pygame.transform.scale(settings_image, (8*vw, 8*vw))
            btns_pos = 6
        
        exit_image_rect = exit_image.get_rect()
        exit_image_rect.center = btns_pos*vw, screen_h - btns_pos*vw
        StartScreen.exit_image_rect = exit_image_rect

        settings_image_rect = settings_image.get_rect()
        settings_image_rect.center = screen_w - btns_pos*vw, screen_h - btns_pos*vw
        StartScreen.settings_image_rect = settings_image_rect
        to_blit.clear()
        to_blit.extend(([main_text[0], main_text[1]],[exit_image, exit_image_rect],[settings_image, settings_image_rect]))

    @staticmethod
    def build_buttons():
        screen_w, screen_h = screen.get_width(), screen.get_height()
        button_w, button_h = (screen.get_width()/3) ,(screen.get_height()/11)

        button_style = '#button_fullscreen' if is_fullscreen() else '#button_notfullscreen'

        manager = manager_getter()
        StartScreen.play_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)-(button_h)), (button_w, button_h)),
                                                    text='GRAJ',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@blue'))

        StartScreen.camera_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)+(button_h/2)), (button_w, button_h)),
                                                    text='USTAWIENIA KAMERY',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@green'))

        StartScreen.leaderboard_button = pygame_gui.elements.UIButton(relative_rect=pygame.Rect(((screen_w/2)-(button_w/2), (screen_h/2)+(button_h*2)), (button_w, button_h)),
                                                    text='RANKING',
                                                    manager=manager,
                                                    object_id=ObjectID(class_id=button_style,object_id='@yellow'))
        
        game_buttons.extend((StartScreen.play_button, StartScreen.camera_button, StartScreen.leaderboard_button))

     