from screens.play_screen import StartScreen
from static import current_screen_val
from database_actions import update_db


class SelectEnglishCategory:

    category_buttons = []

    def build_category_screen(self):
        SelectEnglishCategory.build_images_texts()
        SelectEnglishCategory.build_buttons()

    @staticmethod
    def build_images_texts():
        StartScreen.build_images_texts(back_img=True) 

    @staticmethod
    def build_buttons():
        
        update_db(f"UPDATE game_data SET sub_category = 'english'")
        current_screen_val(new_val=41) 
        from build_game import build_proper_widgets
        build_proper_widgets()
