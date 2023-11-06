from minigames.polish.polish_engine import PolishEngine
from minigames.win_lose_screen import WinPopup
from static import *
from utils import set_text 

polish_engine = PolishEngine()
win_popup = WinPopup()

class PolishScreen:
    def __init__(self) -> None:
        self.queue = [] 
        self.current_question = 1
        self.points = 0 
    
    def build_polish_screen(self, selected_class, selected_level):
        self.selected_class = selected_class
        self.selected_level = selected_level
        self.run_game()

    def run_game(self):
        polish_engine.select_class_db()
        self.questions, self.solutions = polish_engine.get_questions(self.selected_class, self.selected_level)
        self.game_btns, self.game_ids = polish_engine.create_letters()
        self.question, self.solution = polish_engine.new_question(self.current_question)
        self.build_texts()
    
    def update_game(self):
        self.queue = polish_engine.refresh_letters(self.game_btns, self.queue, self.game_ids, self.solution) 

    def select_letter(self, event_pos, from_key=False):
        self.question, self.solution, self.points, valid = polish_engine.selecting_letter(event_pos, self.question, self.solution, self.points, self.current_question, self.game_ids, from_key)
        if valid: self.current_question += 1
        if self.current_question == 10: self.end_game()
        else: self.build_texts() #If someone win the game
            
    def end_game(self):
        current_screen_val(new_val=31)
        from build_game import build_proper_widgets
        build_proper_widgets()
        win_popup.build_win_popup("Polskiego", f"{self.selected_level}", f"{self.points}")
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
    
















