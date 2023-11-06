import pygame 
import json 
import time
import random
import os
import re


from database_actions import execute_query
from static import screen, is_fullscreen
import static

class Mathematic:
    def __init__(self) -> None:
        self.available_place = [x for x in range(2,10)]  
        self.questions = {}
        self.last_time = 0 
        self.class_db = None
        self.actual_question = 0
        self.solutions = []
        self.corr_answ = None
        self.stop_rest = False

    def select_class_db(self, choosen_class=None):
        if not choosen_class:
            choosen_class = execute_query("SELECT choosen_class FROM game_data WHERE id=1")[0][0]
            
        with open(f"questions/class{choosen_class}_math.json") as f:
            self.class_db = json.load(f) 
    
    def refresh_digits(self, digits_btn, queue, game_ids, solution):
        now = time.time()
        wait_time = 2.8 if is_fullscreen else 1 
        self.stop_rest = False
        for nr, digit in enumerate(digits_btn):
            digit_rect = static.digits_rect[nr]
            previous_x, previous_y = digit_rect.center
            digit_rect.center = previous_x, previous_y+3
            screen.blit(digit, static.digits_rect[nr])


            if int(game_ids[nr]) == int(solution):
                self.corr_answ = nr
                digit_rect = static.digits_rect[nr]
                previous_x, previous_y = digit_rect.center
                if previous_y > screen.get_height()+screen.get_width()/16:
                    self.stop_rest = True
                    if abs(self.last_time-now) > wait_time:
                        previous_y = 0
                        self.set_xy_pos(digit_rect)
                        self.last_time = time.time()
                        queue.append(digit)
                        if len(queue) == 10:
                            queue = []
             
        for nr, digit in enumerate(digits_btn):
            if int(game_ids[nr]) != int(solution):
                if not self.stop_rest:
                    digit_rect = static.digits_rect[nr]
                    previous_x, previous_y = digit_rect.center
                    if previous_y > screen.get_height()+screen.get_width()/16:
                        if abs(self.last_time-now) > wait_time:
                            if digit not in queue:
                                previous_y = 0
                                self.set_xy_pos(digit_rect)
                                self.last_time = time.time()
                                queue.append(digit)
                                if len(queue) == 10:
                                    queue = []
            
        if queue == None: queue = []
        return queue
    
    def set_numbers_to_default_pos(self, digits_btn, queue):
        for nr, digit in enumerate(digits_btn):
            digit_rect = static.digits_rect[nr-1]
            self.set_xy_pos(digit_rect)
            queue.append(digit)
            if len(queue) == 10:
                queue = []
    
    def create_digits(self):
        static.digits_id = []
        static.digits_rect = []

        path = "images/set1"
        digits = os.listdir(path)
        digits_name = "number"
        digits = [digit for digit in digits if digits_name in digit]
        p = re.compile(r'\d+')
        digits = sorted(digits, key=lambda s: int(p.search(s).group()))
        digits_btn = []
        for digit in digits:           
            ID = ''.join(filter(lambda i: i.isdigit(), digit))
            if_one = 2 if int(ID) < 10 else 1 
            digit_img = pygame.image.load(f"{path}/{digit}")
            digit_img = pygame.transform.scale(digit_img, ((screen.get_width()/10/if_one), (screen.get_width()/10)))
            digit_rect = digit_img.get_rect()
            digits_btn.append(digit_img)
            static.digits_rect.append(digit_rect)
            static.digits_id.append(ID)
            self.set_xy_pos(digit_rect, y=screen.get_height()+(screen.get_height()/10)+100)
        return digits_btn
    
    def set_xy_pos(self, digit_rect, y=-(screen.get_width()/16)):
        x_pos = random.choice(self.available_place)
        idx = self.available_place.index(x_pos)
        self.available_place.pop(idx)
        x_space = 180 if is_fullscreen() else 75
        digit_rect.center = x_space*x_pos, y
       
        if len(self.available_place) == 0:
            self.available_place = [x for x in range(1,11)] 
    
    def selecting_digit(self, event_pos, question_text, solution, points, current_question, game_ids, from_key):

        if from_key:
            points += 1
            new_question, solution = self.new_question(current_question+1)
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
        for nr, digit in enumerate(static.digits_rect):
            if x != 10000: 
                if digit.collidepoint((x-screen.get_width()/10/2,y)) or digit.collidepoint(event_pos): 
                    print(f"You clicked digit: {game_ids[nr]}")
                    digit.center = 0, screen.get_height() + (screen.get_width()/16) + 1
                    if str(game_ids[nr]) == solution:
                        points += 1
                        new_question, solution = self.new_question(current_question+1)
                        return new_question, solution, points, True
                    else:
                        if points > 0:
                            points -= 0
            else:
                for my_x in XList:
                    for my_y2 in [my_y-80,my_y-40, my_y, my_y+40, my_y+80]:
                        if (digit.collidepoint((my_x, my_y2)) and ball_det): 
                            try:
                                print(f"You clicked digit: {game_ids[nr]}")
                                digit.center = 0, screen.get_height() + (screen.get_width()/16) + 1
                                if str(game_ids[nr]) == solution:
                                    points += 1
                                    new_question, solution = self.new_question(current_question+1)
                                    return new_question, solution, points, True
                                else:
                                    if points > 0:
                                        points -= 1
                            except: pass

        return question_text, solution, points, False
    
    def select_game_numbers(self, solutions, digits):
        game_digits = []
        game_ids = []
        for nr, digit in enumerate(digits):
            if int(static.digits_id[nr]) in solutions:
                 print(nr)
                 game_digits.append(digit)
                 game_ids.append(nr)
        
        other = []
        while len(game_digits) != 10:
            nr = random.randint(0,99)
            if (nr not in solutions) and (nr not in other):
                other.append(nr)
                digit = digits[nr]
                game_digits.append(digit)
                game_ids.append(nr)
        
        lists = list(zip(game_digits, game_ids))
        random.shuffle(lists)
        game_digits, game_ids = zip(*lists)
        game_digits, game_ids = list(game_digits), list(game_ids)
        
        return game_digits, game_ids

        
    def get_questions(self, choosen_class, choosen_lvl):
        # section = "sum" # substract / multiplication / less_more_the_same / days_weak1
        section = execute_query("SELECT sub_category FROM game_data WHERE id=1")[0][0]

        if section == "Dodawanie": section = "sum"
        elif section == "Odejmowanie": section = "substract"
        elif section == "Mnożenie": section = "multiplication"

        self.select_class_db()
        level_data = self.class_db["math"][f"class_{choosen_class}"][section][f"level_{choosen_lvl}"]["settings"]
        max_num = level_data["max_num"]
        min_num = level_data["min_num"]
        max_equal = level_data["max_equal"]

        self.questions.clear()
        self.solutions.clear()

        if section == "sum":
            self.generate_sum_questions(min_num, max_equal)
        elif section == "substract":
            self.generate_sub_questions(min_num, max_num)
        

        print(self.questions)
        return self.questions, self.solutions
    
    def generate_sum_questions(self, min_num, max_equal):
        for i in range(1, 11):
            equal = random.randint(min_num+3, max_equal)
            digit_a = random.randint(min_num, equal-3)
            digit_b = equal - digit_a
            self.questions.update({i: [f"{digit_a} + {digit_b}", equal]})
            self.solutions.append(equal)
    
    def generate_sub_questions(self, min_num, max_num):
        for i in range(1, 11):
               
            digit_a = random.randint(min_num, max_num-3)
            digit_b = random.randint(min_num, max_num)
            if digit_a == digit_b: 
                digit_b = random.randint(min_num, max_num) #small probability to equal == 0
            (digit_b, digit_a) = (digit_a, digit_b) if digit_b > digit_a else (digit_b, digit_a) # a > b
            equal = digit_a - digit_b
            self.questions.update({i: [f"{digit_a} - {digit_b}", equal]})
            self.solutions.append(equal)

    def new_question(self, current_question):
        a = 1 if current_question == 10 else 0 
        current_question -= a
        my_set = self.questions[current_question]
        quest, answer = my_set[0], my_set[1]
        solution = str(answer)
        
        return quest, solution
    
    