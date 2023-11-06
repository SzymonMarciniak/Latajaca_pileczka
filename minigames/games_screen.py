from database_actions import execute_query
from minigames.math.math_screen import MathScreen
from minigames.polish.polish_screen import PolishScreen
from minigames.english.english_screen import EnglishScreen


math_screen = MathScreen()
polish_sceen = PolishScreen()
english_screen = EnglishScreen()

class GamesScreen:
    def __init__(self) -> None:
        pass 

    def select_game(self):
        GamesScreen.selected_category = execute_query("SELECT choosen_category FROM game_data WHERE id=1")[0][0]
        selected_class = execute_query("SELECT choosen_class FROM game_data WHERE id=1")[0][0]
        selected_level = execute_query("SELECT choosen_lvl FROM game_data WHERE id=1")[0][0]

        if GamesScreen.selected_category == "math":
            math_screen.build_math_screen(selected_class, selected_level)
        
        elif GamesScreen.selected_category == "polish":
            polish_sceen.build_polish_screen(selected_class, selected_level)
        
        elif GamesScreen.selected_category == "english":
            english_screen.build_english_screen(selected_class, selected_level)

    def update_game(self):
        if GamesScreen.selected_category == "math":
            math_screen.update_game()
        
        elif GamesScreen.selected_category == "polish":
            polish_sceen.update_game()
        
        elif GamesScreen.selected_category == "english":
            english_screen.update_game()
    
    def select_answer(self, event_pos, from_key=False):
        if GamesScreen.selected_category == "math":
            math_screen.select_digit(event_pos)
            if from_key:
                math_screen.select_digit(event_pos, True)
        
        elif GamesScreen.selected_category == "polish":
            polish_sceen.select_letter(event_pos)
            if from_key:
                polish_sceen.select_letter(event_pos, True)
        
        elif GamesScreen.selected_category == "english":
            english_screen.select_image(event_pos, from_key)





