import pygamepopup
from pygamepopup.components import Button, InfoBox
from pygamepopup.constants import BUTTON_SIZE, CLOSE_BUTTON_SIZE, CLOSE_BUTTON_MARGIN_TOP, BLACK, WHITE

from static import *
import static, utils
pygamepopup.init()

def close_popup():
    current_screen_val(static.last_screen)
    utils.close_popup("settings_menu")

def settings_menu_getter():
    
    settings_menu = InfoBox(
        "Ustawienia",
        [
            [
                Button(
                    title="Język: Polski",
                    size=(320, BUTTON_SIZE[1]),
                    background_path="images/btn_bg_1.png",
                    background_hover_path="images/btn_bg_1.png",
                    text_color=BLACK,
                    text_hover_color=WHITE,
                )
            ],
            [
                Button(
                    title="FPS: 60" if static.FPS == 60 else "FPS: 120",
                    size=(320, BUTTON_SIZE[1]),
                    callback=lambda: change_max_fps(120) if static.FPS == 60 else change_max_fps(60),
                    background_path="images/btn_bg_1.png",
                    background_hover_path="images/btn_bg_1.png",
                    text_color=BLACK,
                    text_hover_color=WHITE,
                )
            ],
            [
                Button(
                    title="Głos: Wył",
                    size=(320, BUTTON_SIZE[1]),
                    background_path="images/btn_bg_1.png",
                    background_hover_path="images/btn_bg_1.png",
                    text_color=BLACK,
                    text_hover_color=WHITE,
                )
            ],
            [
                Button(
                    title="Tryb pełnoekranowy: Wł" if is_fullscreen() else "Tryb pełnoekranowy: Wył",
                    size=(320, BUTTON_SIZE[1]),
                    # callback=lambda: change_fullscreen(),
                    background_path="images/btn_bg_1.png",
                    background_hover_path="images/btn_bg_1.png",
                    text_color=BLACK,
                    text_hover_color=WHITE,
                )
            ],       
            [
                Button(
                    size=CLOSE_BUTTON_SIZE,
                    title="Wyjdź",
                    margin=(CLOSE_BUTTON_MARGIN_TOP, 0, 0, 0),
                    background_path="images/btn_bg_1.png",
                    background_hover_path="images/btn_bg_1.png",
                    text_color=BLACK,
                    text_hover_color=WHITE,
                    callback=lambda: close_popup()
                )
            ]
        ],
        width=420,
        identifier="settings_menu",
        has_close_button=False
    )
    return settings_menu

def change_fullscreen():
    #Function responsible for changing screen size
    from build_game import build_proper_widgets
    to_blit.clear()
    change_fullscreen_var() 
    build_proper_widgets()


class SettingsScreen:

    def build_settings_popup(self):
        current_screen_val(100)
        settings_menu = settings_menu_getter()
        utils.show_menu(settings_menu)
    
    