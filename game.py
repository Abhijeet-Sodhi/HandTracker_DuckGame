import cv2
from cvzone.HandTrackingModule import HandDetector
import math
import numpy as np
import cvzone
import random
import time
import pygame
import sys

def init_game():
    """initialise game resources."""
    # Webcam
    cap = cv2.VideoCapture(0)
    cap.set(3, 1280) # width of video frame
    cap.set(4, 720) # height of video frame

    # Hand Detector with 80% confidence
    detector = HandDetector(detectionCon=0.8, maxHands=1)

    # initialise pygame mixer
    pygame.mixer.init()
    score_sound = pygame.mixer.Sound('coin.mp3')
    score_sound.set_volume(0.2)

    # Draw Duck
    original_img = cv2.imread('duck.png', -1)  # duck image
    hit_image = cv2.imread('green_duck.png', -1) # duck hit image

    return cap, detector, score_sound, original_img, hit_image # return initialised resources


def process_hand_input(detector, img, cx, cy, coff, show_green_duck, disappear_time):
    """Processes hand input and determines interaction with the duck."""
    
    # Detect hands to start game
    hands, img = detector.findHands(img, draw=False) # disabled drawing hand landmarks
    hand_present = False
    if hands: 
        hand_present = True 
        lmList = hands[0]["lmList"] # list of landmarks for detected hand
        x, y, w, h = hands[0]['bbox'] # bounding box around hand
        x1, y1, _ = lmList[5] # coordinate of one finger joint
        x2, y2, _ = lmList[17] # coordinate of another finger joint

        # calculate distance between landmarks to estimate hand size
        distance = int(math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2))
        A, B, C = coff # polynomial coefficients for distance-to-centimeter mapping
        distanceCM = A*distance**2 + B*distance + C 

        if distanceCM < 40: # hand close enough to interact with duck
            if x < cx < x + w and y < cy < y + h and not show_green_duck:
                show_green_duck = True # duck is hit
                disappear_time = time.time()

        cv2.rectangle(img, (x,y), (x+w, y+h), (0, 0, 255), 3) # red bounding box 
        cvzone.putTextRect(img, f'{int(distanceCM)} cm', (x+5, y-10), colorR=(140, 0, 0)) 

    return img, hand_present, show_green_duck, disappear_time


def render_game(img, current_img, cx, cy, score, totalTime, timeStart, hand_present):
    """Renders game elements like the duck and HUD."""
    # dynamically reduce size of duck as score increases
    scale_factor = max(0.5, 1.5 - (score * 0.1))
    new_width = int(current_img.shape[1] * scale_factor)
    new_height = int(current_img.shape[0] * scale_factor)
    resized_img = cv2.resize(current_img, (new_width, new_height), interpolation=cv2.INTER_AREA)

    # overlay the dynamically scaled image at target position
    img = cvzone.overlayPNG(img, resized_img, [cx - new_width // 2, cy - new_height // 2])

    # game HUD (time remaining and score)
    cvzone.putTextRect(img, f'Time: {int(totalTime-(time.time()-timeStart))}',
                        (1000, 75), scale=3, offset=20, colorR=(140, 0, 0))
    cvzone.putTextRect(img, f'Score: {str(score).zfill(2)}', (60, 75), scale=3, offset=20, colorR=(140, 0, 0))    

    if not hand_present: # display warning if hand is not detected
        cvzone.putTextRect(img, "Put your hand back in view!", (350, 400), scale=2, offset=20, colorR=(140, 0, 0))

    return img


def exit_game(cap):
    """Cleanup resources and exit."""
    cap.release() # release the webcam
    cv2.destroyAllWindows() # close all OpenCV windows
    sys.exit() # terminate the script

def main():
    """Main game loop."""
    cap, detector, score_sound, original_img, hit_image = init_game()

    # Game Variables
    x = [240, 188, 161, 125, 110, 98, 90, 85, 75, 64, 62, 57, 52, 50, 47, 44, 43]
    y = [20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95, 100]
    coff = np.polyfit(x, y, 2) # polynomial coefficients for distance conversion y = Ax^2 + Bx + c

    cx, cy = 250, 250 # initial duck position
    score = 0 # player's score
    timeStart = time.time() # initial start time
    totalTime = 20 
    game_started = False # flag to track game state
    show_green_duck = False # flag for duck hit state
    disappear_time = 0 # time when duck disappears

    # Loop
    while True:
        _, img = cap.read() # read frame from webcam 
        key = cv2.waitKey(1) # check for keypress

        # can flip camera with cv2.flip(img, 1)

        if not game_started:
            hands, img = detector.findHands(img, draw=False) # display start message until hand is detected
            cvzone.putTextRect(img, "Show your hand to start the game", (300, 400), scale=2, offset=20, thickness=3, colorR=(140, 0, 0))
            if hands:
                game_started = True # start the game 
                timeStart = time.time() # reset the game timer

        else:
            if time.time() - timeStart < totalTime:
                img, hand_present, show_green_duck, disappear_time = process_hand_input(detector, img, cx, cy, coff, show_green_duck, disappear_time)

                if show_green_duck:
                    score_sound.play() # play sound and reposition the duck after a hit
                    if time.time() - disappear_time > 0.2:
                        show_green_duck = False
                        cx = random.randint(100, 1100) # randomise positions
                        cy = random.randint(100, 600) # randomise positions
                        current_img = original_img
                        score += 1 # increment score

                current_img = hit_image if show_green_duck else original_img
                img = render_game(img, current_img, cx, cy, score, totalTime, timeStart, hand_present)
            else: 
                # display game over screen
                cvzone.putTextRect(img, f'Game Over! Your Score: {score}', (300, 400), scale=3, offset=20, colorR=(140, 0, 0))
                cvzone.putTextRect(img, 'Press R to restart or Q to quit', (350, 475), scale=2, offset=10, colorR=(140, 0, 0))

        if key == ord('q'): # quitting game
            cvzone.putTextRect(img, 'Exiting the game...', (460, 575), scale=2, offset=10, colorR=(140, 0, 0))
            cv2.imshow("Image", img)
            cv2.waitKey(1000)
            exit_game(cap)

        if key == ord('r'): # restart the game 
            # resetting game variables
            cx, cy = 250, 250
            score = 0
            timeStart = time.time()
            game_started = False
            show_green_duck = False
            disappear_time = 0
        
        cv2.imshow("Image", img) # display game frame
        
if __name__ == "__main__":
    main()






        
            