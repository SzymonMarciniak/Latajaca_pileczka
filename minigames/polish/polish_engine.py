import pygame 
import json 
import time
import random
import os 

from database_actions import execute_query
from static import screen, is_fullscreen
import static

class PolishEngine:
    def __init__(self) -> None:
        self.available_place = [x for x in range(1,11)]  
        self.questions = {}
        self.last_time = 0 
        self.class_db = None
        self.actual_question = 0
        self.solutions = [] 
        self.stop_rest = False

    def select_class_db(self, choosen_class=None):
        if not choosen_class:
            choosen_class = execute_query("SELECT choosen_class FROM game_data WHERE id=1")[0][0]
            
        with open(f"questions/class{choosen_class}_polish.json") as f:
            self.class_db = json.load(f)  

    def refresh_letters(self, letters_btn, queue, game_ids, solution):
        now = time.time()
        wait_time = 2 if is_fullscreen else 1 
        self.stop_rest = False

        for nr, letter in enumerate(letters_btn):
            letter_rect = static.letters_rect[nr]
            previous_x, previous_y = letter_rect.center
            letter_rect.center = previous_x, previous_y+3
            screen.blit(letter, static.letters_rect[nr])

            if str(game_ids[nr]).upper() == str(solution).upper():
                self.corr_answ = nr
                letter_rect = static.letters_rect[nr]
                previous_x, previous_y = letter_rect.center
                if previous_y > screen.get_height()+screen.get_width()/16:
                    self.stop_rest = True
                    if abs(self.last_time-now) > wait_time:
                        previous_y = 0
                        self.set_xy_pos(letter_rect)
                        self.last_time = time.time()
                        queue.append(letter)
                        if len(queue) == 6:
                            queue = []


        for nr, letter in enumerate(letters_btn):
            if str(game_ids[nr]).upper() != str(solution).upper():
                if not self.stop_rest:
                    letter_rect = static.letters_rect[nr-1]
                    previous_x, previous_y = letter_rect.center
                    if previous_y > screen.get_height()+screen.get_width()/16:
                        if abs(self.last_time-now) > wait_time:
                            if letter not in queue:
                                previous_y = 0
                                self.set_xy_pos(letter_rect)
                                self.last_time = time.time()
                                if static.letters_id[nr].lower() in self.solutions:
                                    queue.insert(0, letter)
                                else:
                                    queue.append(letter)
                                if len(queue) == 6:
                                    queue = []
        if queue == None: queue = []
        return queue
    
    def set_letters_to_default_pos(self, letters_btn, queue):
        for nr, letter in enumerate(letters_btn):
            letter_rect = static.letters_rect[nr-1]
            self.set_xy_pos(letter_rect)
            queue.append(letter)
            if len(queue) == 6:
                queue = []
    
    def set_xy_pos(self, letter_rect, y=-(screen.get_width()/10)):
        x_pos = random.choice(self.available_place)
        idx = self.available_place.index(x_pos)
        self.available_place.pop(idx)
        x_space = 180 if is_fullscreen() else 75
        letter_rect.center = x_space*x_pos, y
       
        if len(self.available_place) == 0:
            self.available_place = [x for x in range(1,11)] 

    def selecting_letter(self, event_pos, question_text, solution: str, points, current_question, game_ids,from_key):

        if from_key:
            points += 1
            new_question, solution = self.new_question(current_question+1)

            for nr, letter in enumerate(static.letters_rect):
                if str(game_ids[nr]).upper() == solution.upper():
                    letter.center = 0, screen.get_height() + (screen.get_width()/10) + 100
                    
            return new_question, solution, points, True
        

        x, y = event_pos
        ball_det = False
        my_y = 10000
        if x == 10000:
            XList = [x for x in range(0, screen.get_width(), 20)]
            print(len(XList))
            ball_det = True
            my_y = y
        
        print(f"MY YYYYY {my_y}")
        for nr, letter in enumerate(static.letters_rect):
            if x != 10000:
                if letter.collidepoint(event_pos): 
                    print(f"You clicked letter: {game_ids[nr]}")
                    letter.center = 0, screen.get_height() + (screen.get_width()/10) + 100
                    print(str(game_ids[nr]).upper(),  solution.upper())
                    if str(game_ids[nr]).upper() == solution.upper():
                        points += 1
                        new_question, solution = self.new_question(current_question+1)
                        return new_question, solution, points, True
                    else:
                        if points != -9:
                            points -= 0
            else:
                for my_x in XList:
                    for my_y2 in [my_y-80,my_y-40, my_y, my_y+40, my_y+80, my_y+120, my_y+160, my_y+200]:
                        if (letter.collidepoint((my_x, my_y2)) and ball_det): 
                            try:
                                print(f"You clicked letter: {game_ids[nr]}")
                                letter.center = 0, screen.get_height() + (screen.get_width()/10) + 100
                                print(str(game_ids[nr]).upper(),  solution.upper())
                                if str(game_ids[nr]).upper() == solution.upper():
                                    points += 1
                                    new_question, solution = self.new_question(current_question+1)
                                    return new_question, solution, points, True
                                else:
                                    if points != -9:
                                        points -= 0
                            except: pass
        return question_text, solution, points, False

    def new_question(self, current_question):
        my_set = self.questions[current_question]
        quest, answer = my_set[0], my_set[1]
        solution = str(answer)
        
        return quest, solution
    
    def get_questions(self, choosen_class, choosen_lvl):
        section = execute_query("SELECT sub_category FROM game_data WHERE id=1")[0][0]

        if section == "Ó / U": section = "u_ó"
        elif section == "RZ / Ż": section = "rz_ż"
        elif section == "CH / H": section = "ch_h"
        elif section == "nie": section = "Nie"

        self.select_class_db()
        level_data = self.class_db["polish"][f"class_{choosen_class}"][section][f"level_{choosen_lvl}"]["settings"]

        self.questions.clear()
        self.solutions.clear()

        self.questions, self.solutions = self.generate_qestions(level_data)
        return self.questions, self.solutions

    def generate_qestions(self, level_data):
        for i in range(1,11):
            question = level_data[f"{i}"][0]
            answer = level_data[f"{i}"][1]
            self.questions.update({i: [f"{question}", answer]})
            self.solutions.append(answer)
        print(self.solutions, self.questions)
        return self.questions, self.solutions

    def create_letters(self):
        static.letters_rect = []
        static.letters_id = []

        path = "images/set2"
        letters = os.listdir(path)
        letters_name = "pol"
        letters = [letter for letter in letters if letters_name in letter]
        
        letters_btn = []
        for letter in letters:           
            ID = str(letter[3:-4])
            ID = [l for l in ID]
            if_one = 2 if len(ID) < 2 else 1 
            ID = "".join(ID)
            letter_img = pygame.image.load(f"{path}/{letter}")
            letter_img = pygame.transform.scale(letter_img, ((screen.get_width()/10/if_one), (screen.get_width()/10)))
            letters_btn.append(letter_img)
            letter_rect = letter_img.get_rect()
            static.letters_rect.append(letter_rect)
            static.letters_id.append(ID)
            self.set_xy_pos(letter_rect, y=screen.get_height()+(screen.get_height()/10)+100)
        return letters_btn, static.letters_id
