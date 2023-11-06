import pygamepopup
from pygamepopup.components import Button, InfoBox, TextElement
from pygamepopup.constants import CLOSE_BUTTON_MARGIN_TOP, BLACK, WHITE
from static import screen
import utils

pygamepopup.init()

class WinPopup:
    def __init__(self) -> None:
        pass 
    
    @staticmethod
    def win_popup_getter(category, level, points):
        points = int(points)
        points += 1
        points = str(points)
        win_popup = InfoBox(
        "Wygrałeś!",
        [
            [
            TextElement(
                text=f"Gratulacje,",
                text_color=BLACK,   
                
            )
            ],
            [
            TextElement(
                text=f"ukończyłeś poziom {level} {category}",
                text_color=BLACK,
                
            )
            ],
            [
            TextElement(
                text= f"Twój wynik to: {points}",
                text_color=BLACK,
                
            )
            ],
            [
            TextElement(
                text="Trzymaj tak dalej!",
                text_color=BLACK,
                
            )
            ],
            [
                Button(
                    size=(screen.get_width()/5, screen.get_height()/14),
                    title="Świetnie",
                    margin=(CLOSE_BUTTON_MARGIN_TOP, 0, 0, 0),
                    background_path="images/btn_bg_0.png",
                    background_hover_path="images/btn_bg_0.png",
                    text_color=BLACK,
                    text_hover_color=WHITE,
                    callback=lambda: utils.close_popup("win_popup"),
                )
            ]
        ],
        width=screen.get_width()/1.44,
        identifier="win_popup",
        has_close_button=False,
        background_path="images/end_game_popup_img.png",
        title_color=BLACK
        )
        
        return win_popup
    
    def build_win_popup(self, category, level, points):
        win_popup = WinPopup.win_popup_getter(category, level, points)
        utils.show_menu(win_popup)
    
    



        