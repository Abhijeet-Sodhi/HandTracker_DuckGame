# HandTracker_DuckGame
This project is a real-time interactive game where players use hand gestures detected via a webcam to "catch" a duck on the screen. The duck moves dynamically, and the game challenges players to score points within a time limit by interacting with it.

## Credits
[![Hand Distance Measurement with Normal Webcam + Game | OpenCV Python](https://img.youtube.com/vi/NGQgRH2_kq8&list=LL/0.jpg)](https://www.youtube.com/watch?v=NGQgRH2_kq8&list=LL) 
Murtaza's Workshop - Robotics and AI
The base code for this project was adapted from Murtaza's Workshop - Robotics and AI. While the original concept and code were used as a foundation, several modifications were made to suit the specific functionality and features of this Duck game.

## Demo

https://github.com/user-attachments/assets/4abb04f8-44da-42a3-bbde-b52aceed92cc

## The Code files:
**hand.py:** is the base understanding of hand detection and how it works

**game.py:** is the implementation of hand detection to create a game

## Functionality

**Hand Tracking Setup:**
The game initializes a webcam feed and uses a pre-trained hand tracking module (HandDetector) to detect and track a player's hand in real-time.
Only one hand is detected at a time, ensuring focused interaction.

**Audio and Visual Elements:**
Background assets like a duck image and its "hit" variant are loaded.
Sound effects are preloaded using the pygame library, adding audio feedback for successful interactions.

**Calibration:**
A calibration curve is computed to convert hand distances into approximate real-world measurements (e.g., cm).

**Gameplay Dynamics**
Starting the Game:
The game waits for a hand to appear in the camera's field of view.
A prompt guides the player to place their hand to start.

**Hand Tracking and Interaction:**
The system identifies the position and bounding box of the hand.
If the hand approaches the duck (based on proximity and overlap), the duck turns green momentarily to indicate a "hit."
After a short delay, the duck respawns in a random location to keep the game dynamic.

**Feedback Mechanisms:**
**Distance Display:** The real-time distance of the hand from a target point is calculated and displayed on the screen.
**Hand Detection Alerts:** If the hand moves out of view, a prompt asks the player to bring their hand back into the frame.

**Score and Timer Management:**
The player's score increments each time the duck is hit.
The game is time-limited (e.g., 20 seconds), with the remaining time shown on-screen.

**Duck Scaling:**
The duck's size decreases as the score increases, making the game progressively more challenging.

**Game Over and Restart Options**
**End of Round:** When the timer runs out, a "Game Over" message displays the player's final score.
**Restart or Exit:** Players can restart the game by pressing R or quit by pressing Q.

## Installation
To run this "Hand Tracker Duck Challenge" game, you'll need to install the following dependencies:

*pip install cvzone==1.6.1*

*pip install numpy==2.1.3*

*pip install opencv-python==4.10.0.84*

*pip install pygame==2.6.1*

## Theory
Hand detection process:
A webcam feed is captured frame by frame.
The HandDetector scans the video frame and identifies hand landmarks based on a pre-trained machine learning model.
The landmarks include the positions of specific hand joints, such as fingertips, knuckles, and the base of the palm.

![image](https://github.com/user-attachments/assets/dd2f8e3a-ec12-4cc6-8ff1-355f51a45657)

A bounding box is drawn around the detected hand to visually indicate its position.The code calculates the distance between the landmark 5 and landmark 17 of the hand using the Euclidean distance formula:

![image](https://github.com/user-attachments/assets/ec749ae0-faf8-470a-8446-47cbc3a59f8f)

This distance is mapped to real-world centimeters using a quadratic calibration formula:

![image](https://github.com/user-attachments/assets/86eb5afa-75a8-4e90-afa2-54e16036d380)

**Purpose:** The calculated distance determines whether the hand is "pinching" (used to interact with the duck).The system tracks the position of the duck and checks whether it overlaps with the hand's bounding box when the hand is in a "pinched" state (distance < 40 cm).

also The remaining time is calculated as:

![image](https://github.com/user-attachments/assets/1296ef8e-0ef8-4568-9a6f-a29eb386ae16)

## the Whys:
**OpenCV** provides an efficient and robust framework for real-time video capture, image processing, and computer vision tasks over alternatives like Pillow or scikit-image.

**cvzone** is a high-level wrapper for OpenCV that simplifies common tasks likeDrawing styled rectangles or Overlaying transparent PNG images It reduces boilerplate code while enhancing the visual output with a professional finish and making it more readable. 

**NumPy** is crucial for mathematical operations, especially in the calibration and distance calculation process Used here to fit a quadratic polynomial.

**cvzone’s HandTrackingModule** eliminates the need for training a custom deep-learning model for hand detection, drastically simplifying the development process.

**pygame.mixer** It provides simple integration with Python, making it easier to handle audio without external complex libraries like PyAudio.
