import subprocess

from database_actions import update_db, set_default_values, execute_query
from screens.settings_screen import SettingsScreen
from screens.start_screen import StartScreen
from screens.play_screen import PlayScreen
from screens.classes_screen import ClassesScreen
from screens.level_screen import LevelScreen
from minigames.games_screen import GamesScreen
from minigames.math.seclect_category import SelectMathCategory
from minigames.polish.select_category import SelectPolishCategory

import static
from static import *

game_screen = GamesScreen()
settings_screen = SettingsScreen()

class UserEvents:
    camera_setup_open = False
    
    def buttons_events(self, event_elem):
        current_screen = current_screen_val()
        if current_screen >= 100: return #Settings open
        if static.popup_open == True: return

        elif event_elem == StartScreen.play_button: 
            current_screen_val(new_val=11)

        elif event_elem == StartScreen.camera_button: 
            if not UserEvents.camera_setup_open:
                subprocess.Popen(["python", "camera_setup/camera.py", "1"])
                UserEvents.camera_setup_open = True
        elif event_elem == StartScreen.leaderboard_button: print("LEADERBOARD")

        elif event_elem == PlayScreen.math_button: 
            update_db("UPDATE game_data SET choosen_category = 'math'")
            current_screen_val(new_val=21)

        elif event_elem == PlayScreen.polish_button: 
            update_db("UPDATE game_data SET choosen_category = 'polish'")
            current_screen_val(new_val=21)

        elif event_elem == PlayScreen.english_button: 
            update_db("UPDATE game_data SET choosen_category = 'english'")
            current_screen_val(new_val=21)

        elif event_elem == ClassesScreen.class1_button: 
            update_db("UPDATE game_data SET choosen_class = 1")
            current_screen_val(new_val=31)

        elif event_elem == ClassesScreen.class2_button: 
            update_db("UPDATE game_data SET choosen_class = 2")
            current_screen_val(new_val=31)

        elif event_elem == ClassesScreen.class3_button: 
            update_db("UPDATE game_data SET choosen_class = 3")
            current_screen_val(new_val=31)
        
        elif event_elem in SelectMathCategory.category_buttons:
            sub_category = event_elem.text
            update_db(f"UPDATE game_data SET sub_category = '{sub_category}'")
            current_screen_val(new_val=41)
        
        elif event_elem in SelectPolishCategory.category_buttons:
            sub_category = event_elem.text
            update_db(f"UPDATE game_data SET sub_category = '{sub_category}'")
            current_screen_val(new_val=41)

        elif event_elem in LevelScreen.level_buttons: 
            choosen_lvl = event_elem.text
            update_db(f"UPDATE game_data SET choosen_lvl = {choosen_lvl}")
            current_screen_val(new_val=51)
            
        from build_game import build_proper_widgets
        build_proper_widgets()
        

    def images_events(self, event_pos):
        global running
        current_screen = current_screen_val()
        sub_category = execute_query("SELECT sub_category FROM game_data")[0][0]
        if StartScreen.exit_image_rect.collidepoint(event_pos): 
            if current_screen_dict[current_screen] == "start_screen":
                set_default_values()
                running_val(close=True)
            else:
                if current_screen_dict[current_screen] != "game_screen":
                    if sub_category == "english" and current_screen==41:
                        current_screen_val(current_screen-20)
                    else:
                        current_screen_val(current_screen-10)
                    from build_game import build_proper_widgets
                    build_proper_widgets()

        elif StartScreen.settings_image_rect.collidepoint(event_pos): 
            if current_screen_dict[current_screen] != "game_screen":
                settings_screen.build_settings_popup()

        if current_screen_dict[current_screen] == "game_screen":
            game_screen.select_answer(event_pos)
    
    def game_event(self, my_y, from_key=False):
        current_screen = current_screen_val()
        if current_screen_dict[current_screen] == "game_screen":
            game_screen.select_answer((10000, my_y))
            update_db(f"UPDATE mouse_data SET pos_y = 10000")
        if from_key and current_screen_dict[current_screen] == "game_screen":
            game_screen.select_answer((10000, my_y), True)
            
                