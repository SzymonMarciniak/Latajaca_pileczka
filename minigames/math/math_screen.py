from minigames.math.basic import Mathematic
from minigames.win_lose_screen import WinPopup
from static import *
from utils import set_text 

mathematic = Mathematic()
win_popup = WinPopup()

class MathScreen:
    def __init__(self) -> None:
        self.queue = [] 
        self.current_question = 1
        self.points = 0


    def build_math_screen(self, selected_class, selected_level):
        self.selected_class = selected_class
        self.selected_level = selected_level
        self.run_game()
        
    
    def run_game(self):
        mathematic.select_class_db(self.selected_class)
        self.questions, self.solutions = mathematic.get_questions(self.selected_class, self.selected_level)
        self.digits_btn = mathematic.create_digits()
        self.game_btns, self.game_ids = mathematic.select_game_numbers(self.solutions, self.digits_btn)
        self.question, self.solution = mathematic.new_question(self.current_question)
        self.build_texts()

    def update_game(self):
        self.queue = mathematic.refresh_digits(self.game_btns, self.queue, self.game_ids, self.solution)
    
    
    def select_digit(self, event_pos, from_key=False):
        if self.current_question != 10: #11 to proper work
            self.question, self.solution, self.points, valid = mathematic.selecting_digit(event_pos, self.question, self.solution, self.points, self.current_question, self.game_ids, from_key)
            if valid: self.current_question += 1
            if self.current_question == 11: self.end_game()
            else:self.build_texts()
        else: #If someone win the game
            self.end_game()

    def end_game(self):
        current_screen_val(new_val=31)
        from build_game import build_proper_widgets
        build_proper_widgets()
        win_popup.build_win_popup("Matematyki", f"{self.selected_level}", f"{self.points}")
        self.current_question = 1
        self.points = 0
        

    def end_game(self):
        current_screen_val(new_val=31)
        from build_game import build_proper_widgets
        build_proper_widgets()
        win_popup.build_win_popup("Matematyki", f"{self.selected_level}", f"{self.points}")
        self.current_question = 1
        self.points = 0
        

    def build_texts(self):
        screen_w, screen_h = screen.get_width(), screen.get_height()

        question_text_size = 50 if not is_fullscreen() else 100
        question_text = set_text(str(self.question), (screen_w/2), screen_h/9, question_text_size)

        points_text_size = 50 if not is_fullscreen() else 100
        points_text = set_text(str(self.points), (screen_w/9), screen_h/9, points_text_size)
        
        to_blit.clear()
        to_blit.extend(([question_text[0], question_text[1]], [points_text[0], points_text[1]]))