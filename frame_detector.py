import cv2
import numpy as np
import time
import json
import yaml

from database_actions import update_db

#Camera setup
with open('camera_setup/config.yaml', "r") as config_file:
    data = yaml.safe_load(config_file)
if data["camera_rstp_adress"] and data['use_rstp_camera']: 
    camera = data["camera_rstp_adress"]
else:
    camera = 0

cap = cv2.VideoCapture(camera)
szerokosc_ekranu = cap.get(3)
wysokosc_ekranu = cap.get(4)


#Read values from db
with open("camera_setup/pos_data.json", "r") as f:
    camera_data = json.load(f)
    wall_side = camera_data["wall"]["side"]
    ball_color = camera_data["ball"]["color"]
    start_kx = camera_data["cameras"][str(camera)]["left"] 
    stop_kx = 1 - camera_data["cameras"][str(camera)]["right"] 
    start_ky = camera_data["cameras"][str(camera)]["top"] 
    stop_ky = 1 - camera_data["cameras"][str(camera)]["bottom"]

poczatek_wykrywania = int(szerokosc_ekranu * start_kx)
koniec_wykrywania = int(szerokosc_ekranu * stop_kx)

gorny_zakres = int(wysokosc_ekranu - wysokosc_ekranu * start_ky)
dolny_zakres = int(wysokosc_ekranu - wysokosc_ekranu * stop_ky)

punkt_udezenia = 20 if wall_side == "right" else -20
green_color = True if ball_color == "green" else False

ilosc_pilek_do_wykrycia = 2 #TODO magic num

#Default values
XList = [item for item in range(koniec_wykrywania, poczatek_wykrywania, -1)]
posList = []
YList = []
posListX = []
posListY = []
true_x, true_y = None, None
no_ball = 0
prev_x = 0
prev_time = 0

#COLOR FINDER
# from cvzone.ColorModule import ColorFinder
# myclolor = ColorFinder(True)

#Start read images from camera
while True:
    ret, frame = cap.read()
    #               YYY  ,  XX 
    # frame = frame[550:1400,:] #To crop image
    
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    
    if green_color:
        lower_green = np.array([38, 76, 78])
        upper_green = np.array([90, 252, 223])
        
        mask = cv2.inRange(hsv, lower_green, upper_green)

    else:
        #HINT - Red color has 2 ranges in hsv model
        lower_red = np.array([0, 70, 20])
        upper_red = np.array([9, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        
        lower_red = np.array([160, 70, 20])
        upper_red = np.array([180, 255, 255])
        mask2 = cv2.inRange(hsv, lower_red, upper_red)
        
        mask = cv2.add(mask1, mask2)

    #Detect proper colors 
    kernel = np.ones((5, 5), np.uint8)
    mask = cv2.erode(mask, kernel)
    mask = cv2.dilate(mask, kernel)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #ROI lines
    cv2.line(frame, (poczatek_wykrywania,0), (poczatek_wykrywania, 1000), (0,255,0), 3)
    cv2.line(frame, (koniec_wykrywania,0), (koniec_wykrywania, 1000), (0,255,0), 3)

    cv2.line(frame, (0,gorny_zakres), (2000, gorny_zakres), (0,255,0), 3)
    cv2.line(frame, (0,dolny_zakres), (2000, dolny_zakres), (0,255,0), 3)

    nr = None
    can_detect = False
    if len(contours) > 0: #If ball detect
        ball_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(ball_contour)
        
        #If ball is in ROI
        if (radius > 5) and (koniec_wykrywania > x > poczatek_wykrywania) and (dolny_zakres < y < gorny_zakres):
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
            cv2.circle(frame, (int(x), int(y)), 5, (0, 0, 255), -1)
            no_ball = 0
           
            #If the ball goes towards the wall 
            if prev_x > x:
                posList.append((int(x), int(y)))
                posListX.append(int(x))
                posListY.append(int(y))
                A, B, C  = np.polyfit(posListX, posListY, 2)                    


            else: #If the ball bounced off the wall
                if len(posListX) >= ilosc_pilek_do_wykrycia:
                    posList.pop()
                    posListX.pop()
                    posListY.pop()
                    A, B, C  = np.polyfit(posListX, posListY, 2)
                    can_detect = True
            prev_x = x
            
        else:
            no_ball += 1
            if no_ball >= 40: #Prepare to next throw
                no_ball = 0
                posList = []
                YList = []
                posListX = []
                posListY = []


    #If the ball bounced off the wall 
    if can_detect:

        #Visualization
        for line_x in XList:
            if len(posList) >= ilosc_pilek_do_wykrycia-1:
                line_y = int(A*line_x**2 + B*line_x + C) 
                YList.append(line_y)

        for id, position in enumerate(posList):
            cv2.circle(frame, position, 8, (0,255,0), cv2.FILLED)
            if id == 0:
                cv2.line(frame, position, position, (0,255,0), 4)
            else:
                cv2.line(frame, position, posList[id-1], (0,255,0), 2)
        for (x,y) in zip(XList, YList):
                cv2.circle(frame, (x,y), 3, (255,0,255), cv2.FILLED)
        
        #Analise y point and move coursor if valid y
        now = time.time()
        if now - prev_time > 1:
            prev_time = now
            last_polynomial_X = poczatek_wykrywania if wall_side == "left" else koniec_wykrywania
            true_y = int(A*(last_polynomial_X)**2 + B*(last_polynomial_X) + C) 
            cv2.circle(frame, (last_polynomial_X+punkt_udezenia,true_y), 10, (255,0,0), cv2.FILLED )
        
            if dolny_zakres > true_y > gorny_zakres: 
                true_y = (true_y-gorny_zakres)*(wysokosc_ekranu/(dolny_zakres-gorny_zakres))+30
                print("True Y:", true_y) 
                update_db(f"UPDATE mouse_data SET pos_y = {true_y} WHERE id=0")
                # pyautogui.moveTo(int(szerokosc_ekranu*1.5), int(true_y))
    
    #Display image
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
