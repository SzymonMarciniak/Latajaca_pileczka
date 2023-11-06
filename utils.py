import pygame
import static
from static import game_buttons, menu_manager

def scale_to(object, new_size=(800,600)):
    object = pygame.transform.scale(object, new_size)
    return object

def set_text(string, coordx, coordy, fontSize, color=(0,0,0)): 
    font = pygame.font.Font('fonts/bungee-regular.ttf', fontSize) 
    text = font.render(string, True, color) 
    textRect = text.get_rect()
    textRect.center = (coordx, coordy) 
    return (text, textRect)

def clear_front(object):
    object.kill()

def quick_clear_front():
    for button in game_buttons:
        try:
            clear_front(button)
        except: print(button) 
    game_buttons.clear()

def show_menu(menu):
    static.popup_open = True
    if menu_manager.active_menu is not None:
        if menu_manager.active_menu.identifier == menu.identifier:
            print("Given menu is already opened")
            return
        else:
            menu_manager.close_active_menu()
    menu_manager.open_menu(menu)

def close_popup(identifier: str):
    menu_manager.close_given_menu(identifier)
    static.popup_open = False