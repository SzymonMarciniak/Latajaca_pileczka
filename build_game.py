import pygame
import pygame_gui

pygame.init()
pygame.font.init()
pygame.display.set_caption('Education Game')

from static import * 
import static
from utils import *
from user_events import UserEvents
from screens.start_screen import StartScreen
from screens.play_screen import PlayScreen
from screens.classes_screen import ClassesScreen
from screens.level_screen import LevelScreen
from minigames.games_screen import GamesScreen
from minigames.math.seclect_category import SelectMathCategory 
from minigames.polish.select_category import SelectPolishCategory
from minigames.english.select_category import SelectEnglishCategory
from database_actions import set_default_values, execute_query


start_screen = StartScreen()
play_screen = PlayScreen()
level_screen = LevelScreen()
classes_screen = ClassesScreen()
games_screen = GamesScreen()


math_category = SelectMathCategory()
polish_category = SelectPolishCategory()
english_category = SelectEnglishCategory() 

user_events = UserEvents()


start_screen.build_start_screen()
def start_game():
    global running
    while running_val():
        manager = manager_getter()
        build_proper_images()
        time_delta = clock.tick(static.FPS)/1000.0

        #EVENTS
        for event in pygame.event.get():      
            if event.type == pygame.QUIT:
                set_default_values()
                running_val(close=True)
            if event.type == pygame.KEYDOWN: #On key down
                if event.key == pygame.K_f: #Change fullscreen
                    change_fullscreen()
                if event.key == pygame.K_m:
                    user_events.game_event(my_y, True)
            
            if event.type == pygame.USEREVENT: #On user event
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                    user_events.buttons_events(event.ui_element)
                                         
            if event.type == pygame.MOUSEBUTTONDOWN: #If clicked on image
                user_events.images_events(event.pos)
            
            if event.type == pygame.MOUSEMOTION:
                menu_manager.motion(event.pos)  # Highlight buttons upon hover
            
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    menu_manager.click(event.button, event.pos)
            
            my_y = execute_query("SELECT pos_y FROM mouse_data WHERE id=0")[0][0]
            if my_y != 10000:
                user_events.game_event(my_y)

            manager.process_events(event)

        current_screen = current_screen_val()
        if current_screen_dict[current_screen] == "game_screen":
            games_screen.update_game()

        manager.update(time_delta)
        manager.draw_ui(screen)
        menu_manager.display()
        pygame.display.update()

    pygame.quit()

def build_proper_images():
    screen.blit(static.background, (0,0))
    for build_set in to_blit:
        screen.blit(build_set[0], build_set[1])

def build_proper_widgets():
    #Function responsible for build buttons, images and texts depends on choosen screen
    quick_clear_front()

    current_screen = current_screen_val()
    if current_screen_dict[current_screen] == "start_screen":
       start_screen.build_start_screen()
    elif current_screen_dict[current_screen] == "play_screen":
        play_screen.build_play_screen()
    elif current_screen_dict[current_screen] == "classes_screen":
        classes_screen.build_classes_screen()
    elif current_screen_dict[current_screen] == "category_screen":
        build_proper_category()
    elif current_screen_dict[current_screen] == "levels_screen":
        level_screen.build_level_screen()
    elif current_screen_dict[current_screen] == "game_screen":
        games_screen.select_game()

def change_fullscreen():
    #Function responsible for changing screen size
    to_blit.clear()
    change_fullscreen_var() 
    build_proper_widgets()

def build_proper_category():
    minigame = execute_query("SELECT choosen_category FROM game_data")[0][0]
    if minigame == "math":
        math_category.build_category_screen()

    elif minigame == "polish":
        polish_category.build_category_screen() 

    elif minigame == "english":
        english_category.build_category_screen()
    
start_game()

