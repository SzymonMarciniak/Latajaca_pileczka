import pygame
import pygame_gui

from pygamepopup.menu_manager import MenuManager

screen = pygame.display.set_mode((800,600))
clock = pygame.time.Clock()
keys = pygame.key.get_pressed()

FULLSCREEN = False
FPS = 60

BLACK = 0,0,0
ORANGE = 255,127,0
RED = 255,0,0
GREEN = 0,255,0

background = pygame.image.load("images/background.png")
exit_image = pygame.image.load("images/exit_button.png")
settings_image = pygame.image.load("images/settings_button.png")

running = True
def running_val(close = False):
    global running
    if close:
        running = False
    return running 

last_screen = 1
current_screen = 1
def current_screen_val(new_val: int = None):
    global current_screen, last_screen
    if new_val:
        last_screen = current_screen
        current_screen = new_val
    else:
        return current_screen
    
current_screen_dict ={ #if you substract key-10 you go to the previous screen
    1: "start_screen",
    11: "play_screen",
    12: "camera_setup_screen",
    13: "leaderboard_screen",
    21: "classes_screen",
    31: "category_screen",
    41: "levels_screen",
    51: "game_screen",
    100: "settings_screen" #exception
}

def change_fullscreen_var():
    global FULLSCREEN, screen
    FULLSCREEN = not FULLSCREEN
    if FULLSCREEN:
        screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    else:
        screen = pygame.display.set_mode((800,600), pygame.RESIZABLE)

def is_fullscreen():
    return FULLSCREEN

manager_base = pygame_gui.UIManager((screen.get_width(), screen.get_height()), 'style/menu_screen.json')
manager_levels = pygame_gui.UIManager((screen.get_width(), screen.get_height()), 'style/levels_screen.json')

def manager_getter(my_type="base"):
    screen_w, screen_h = screen.get_width(), screen.get_height()

    if my_type == "base":
        manager_base.set_window_resolution((screen_w, screen_h))
        return manager_base
    
    elif my_type == "levels": #to fix
        manager_levels.set_window_resolution((screen_w, screen_h))
        return manager_levels

def change_max_fps(new_val):
    global FPS 
    FPS = new_val

menu_manager = MenuManager(screen)
popup_open = False

#GLOBAL VARIABLES
game_buttons = []
to_blit = []

digits_rect = []
digits_id = []

letters_rect = []
letters_id = []

images_rect = []
images_id = []

