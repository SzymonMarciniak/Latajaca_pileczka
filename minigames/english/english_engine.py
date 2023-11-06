import pygame 
import json 
import time
import random
import os 

from database_actions import execute_query
from static import screen, is_fullscreen
import static

class EnglishEngine:
    def __init__(self) -> None:
        self.available_place = [x for x in range(1,11)]  
        self.questions = {}
        self.last_time = 0 
        self.class_db = None
        self.actual_question = 0
        self.solutions = [] 
        self.stop_rest = False
        self.images_amount = None
        self.choosen_lvl = None
    
    def select_class_db(self, choosen_class=None):
        if not choosen_class:
            choosen_class = execute_query("SELECT choosen_class FROM game_data WHERE id=1")[0][0]
            
        with open(f"questions/class{choosen_class}_english.json") as f:
            self.class_db = json.load(f)  
        
        
    def refresh_images(self, images_btn, queue, game_ids, solution):
        now = time.time()
        wait_time = 2 if is_fullscreen else 1 
        self.stop_rest = False

        for nr, image in enumerate(images_btn):
            image_rect = static.images_rect[nr]
            previous_x, previous_y = image_rect.center
            image_rect.center = previous_x, previous_y+3
            screen.blit(image, static.images_rect[nr])

            if str(game_ids[nr]).upper() == str(solution).upper():
                self.corr_answ = nr
                image_rect = static.images_rect[nr]
                previous_x, previous_y = image_rect.center
                if previous_y > screen.get_height()+screen.get_width()/16:
                    self.stop_rest = True
                    if abs(self.last_time-now) > wait_time:
                        previous_y = 0
                        self.set_xy_pos(image_rect)
                        self.last_time = time.time()
                        queue.append(image)
                        if len(queue) == self.images_amount:
                            queue = []


        for nr, image in enumerate(images_btn):
            if str(game_ids[nr]).upper() != str(solution).upper():
                if not self.stop_rest:
                    image_rect = static.images_rect[nr-1]
                    previous_x, previous_y = image_rect.center
                    if previous_y > screen.get_height()+screen.get_width()/16:
                        if abs(self.last_time-now) > wait_time:
                            if image not in queue:
                                previous_y = 0
                                self.set_xy_pos(image_rect)
                                self.last_time = time.time()
                                if static.images_id[nr].lower() in self.solutions:
                                    queue.insert(0, image)
                                else:
                                    queue.append(image)
                                if len(queue) == self.images_amount:
                                    queue = []
        if queue == None: queue = []
        return queue
    
    def set_images_to_default_pos(self, images_btn, queue):
        for nr, image in enumerate(images_btn):
            image_rect = static.images_rect[nr-1]
            self.set_xy_pos(image_rect)
            queue.append(image)
            if len(queue) == self.images_amount:
                queue = []
    
    def set_xy_pos(self, image_rect, y=-(screen.get_width()/10)):
        x_pos = random.choice(self.available_place)
        idx = self.available_place.index(x_pos)
        self.available_place.pop(idx)
        x_space = 180 if is_fullscreen() else 75
        image_rect.center = x_space*x_pos, y
       
        if len(self.available_place) == 0:
            self.available_place = [x for x in range(1,11)] 

    def selecting_image(self, event_pos, question_text, solution: str, points, current_question, game_ids,from_key):

        if from_key:
            points += 1
            new_question, solution = self.new_question(current_question+1)

            for nr, image in enumerate(static.images_rect):
                if str(game_ids[nr]).upper() == solution.upper():
                    image.center = 0, screen.get_height() + (screen.get_width()/10) + 100
                    
            return new_question, solution, points, True
        
        x, y = event_pos
        ball_det = False
        my_y = 10000
        if x == 10000:
            XList = [x for x in range(0, screen.get_width(), 20)]
            ball_det = True
            my_y = y

        for nr, image in enumerate(static.images_rect):
            if x != 10000:
                if image.collidepoint(event_pos): 
                    print(f"You clicked image: {game_ids[nr]}")
                    image.center = 0, screen.get_height() + (screen.get_width()/10) + 100
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
                        if (image.collidepoint((my_x, my_y2)) and ball_det): 
                            try:
                                print(f"You clicked image: {game_ids[nr]}")
                                image.center = 0, screen.get_height() + (screen.get_width()/10) + 100
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
        self.select_class_db()
        level_data = self.class_db["english"][f"class_{choosen_class}"][f"level_{choosen_lvl}"]["settings"]["vocabulary"]

        self.choosen_lvl = choosen_lvl
        path = f"images/english/Lvl_{choosen_lvl}"
        images = os.listdir(path)
        self.images_amount = len(images)

        self.questions.clear()
        self.solutions.clear()

        self.questions, self.solutions = self.generate_qestions(level_data)
        return self.questions, self.solutions

    def generate_qestions(self, level_data):
        for i in range(0,(self.images_amount)):
            question = level_data[i]
            answer = level_data[i]
            self.questions.update({i: [f"{question}", answer]})
            self.solutions.append(answer)
        print(self.solutions, self.questions)
        return self.questions, self.solutions

    def create_images(self):
        static.images_rect = []
        static.images_id = []

        path = f"images/english/Lvl_{self.choosen_lvl}"
        images = os.listdir(path)
        
        images_btn = []
        for image in images:           
            ID = str(image[:-4])
            ID = [l for l in ID]
            ID = "".join(ID)
            image_img = pygame.image.load(f"{path}/{image}")
            image_img = pygame.transform.scale(image_img, ((screen.get_width()/10), (screen.get_width()/10)))
            images_btn.append(image_img)
            image_rect = image_img.get_rect()
            static.images_rect.append(image_rect)
            static.images_id.append(ID)
            self.set_xy_pos(image_rect, y=screen.get_height()+(screen.get_height()/10)+100)
        return images_btn, static.images_id, self.images_amount
        