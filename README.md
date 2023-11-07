
# Latająca Piłeczka
![Logo](https://raw.githubusercontent.com/SzymonMarciniak/Latajaca_pileczka/main/images/logo.png)

### Prezentation: 
https://docs.google.com/presentation/d/1QchrGWV-QBSqh4k-jzdKdF7a84PtAdxQcrXbs8DeNok/edit?usp=sharing 

## Program setup 

### GIT 
- Install git for your system (https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) 

### Copy program to your computer:
 
    git clone https://github.com/SzymonMarciniak/Latajaca_pileczka.git

### Python 
Required python 3.9

### Create and activate virtual environment: (optional)
    pip install virtualenv
   
    cd */project/path/*

    python -m venv latajaca_pileczka
    
(Linux lub MacOS):

    ./latajaca_pileczka/Scripts/activate

(Windows):

    source latajaca_pileczka/bin/activate 
 

### Install all required packages:

    pip install - r requirements.txt

### Run program:
    - python main.py 

## Projector positioning
The projector should be suspended from the ceiling and throw the image onto a wall or board. The image should be of good quality and as large as possible.

## Camera setup 

Connect your camera via LAN to computer and set rtsp address in camera setup/config.yaml file.

Hint: If you do not connect a camera, you can select the webcam (if available), which is usually hidden under id 0.

### Mounting the camera on the wall

The camera should be approximately 2 meters away from the closer edge of the displayed image. The most important thing is that the camera covers the entire image projected on the wall in the Y axis (from bottom to top), the rest can be adjusted with the program.

![CamSetup](https://raw.githubusercontent.com/SzymonMarciniak/Latajaca_pileczka/main/images/cam_setup.png) 

### Camera configuration in the program

After turning on the game and selecting the "Camera Settings" option, select the camera from the drop-down list, set whether the wall is on the left or right of the camera and select the color of the balls you will throw. Then, using the sliders, we set the upper and lower limits of the projected image, the left slider is responsible for determining the line from behind which we will throw the ball, and the right one should be set so that the entire game image is in the gray field.

### Run ball detector 
    python frame_detector.py

Hint:
you must have two python files enabled for the application to work properly:
 - main.py 
 - frame_detector.py