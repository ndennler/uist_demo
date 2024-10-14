from pylips.speech import RobotFace
from pylips.face import FacePresets
import random
import time
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision
import cv2
import time
from mediapipe import solutions as mp_solutions
from util import draw_landmarks_on_image, landmark_to_array
import numpy as np
from collections import deque

# Initialize video capture
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise Exception("Error: Cannot open camera.")

# Create a RobotFace object
face = RobotFace(voice_id='com.apple.voice.enhanced.en-US.Nathan')
face.set_appearance({})
time.sleep(.2)

base_options = python.BaseOptions(model_asset_path='./hand_landmarker.task')
options = vision.HandLandmarkerOptions(base_options=base_options,
                                       num_hands=1)
detector = vision.HandLandmarker.create_from_options(options)

def get_user_input(cap, detector, timeout=10):
    start_time = time.time()
    values = deque(maxlen=20)

    while time.time() - start_time < timeout:
        ret, frame = cap.read()
        if not ret: continue
            
        try:
            image = mp.Image(image_format=mp.ImageFormat.SRGB, data=cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            detection_result = detector.detect(image)

            # Print the handedness of the detected hand and the thumb angle
            handedness = detection_result.handedness[0][0].category_name
            landmarks = detection_result.hand_landmarks[0]
            thumb_base, thumb_tip = landmarks[1], landmarks[4]
            if handedness == 'Right':
                angle = - np.arctan2(thumb_tip.y - thumb_base.y, thumb_tip.x - thumb_base.x) * 180 / np.pi
                # print(angle)
            else:
                angle = np.arctan2(thumb_base.y - thumb_tip.y, thumb_base.x - thumb_tip.x) * 180 / np.pi
                print(angle)
            
            values.append(angle)
            if len(values) == values.maxlen and (all([v > 70 for v in values]) or all([v < -70 for v in values])):
                return values[-1]

            annotated_image = draw_landmarks_on_image(image.numpy_view(), detection_result)
            cv2.imshow('Thumb', cv2.cvtColor(annotated_image, cv2.COLOR_RGB2BGR))
            cv2.waitKey(1)

        except Exception as e:
            # print(e)
            cv2.imshow('Thumb', frame)
            cv2.waitKey(1)
            continue

    return 0  # Return 0 if there was no response


# State definitions
class GameState:
    INTRO = "intro"
    INPUT_NUMBER = "input_number"
    PERFORM_GUESS = "perform_guess"
    PROCESS_INPUT = "process_input"
    ASK_HIGHER_LOWER = "ask_higher_lower"
    OUTRO = "outro"
    END = 'end'

class NumberGuessingGame:
    def __init__(self):
        self.state = GameState.INTRO
        self.target_number = None
        self.guess = None
        self.bounds = [1, 10]

    def run(self):
        while self.state != GameState.END:
            time.sleep(.1)
            if self.state == GameState.INTRO:
                self.intro()
            elif self.state == GameState.INPUT_NUMBER:
                self.input_number()
            elif self.state == GameState.PERFORM_GUESS:
                self.perform_guess()
            elif self.state == GameState.PROCESS_INPUT:
                self.process_input()
            elif self.state == GameState.ASK_HIGHER_LOWER:
                self.ask_higher_lower()
            elif self.state == GameState.OUTRO:
                self.outro()

    def intro(self):
        face.say(f"Welcome to the number guessing game! Please think of a number between {self.bounds[0]} and {self.bounds[1]}", wait=True)
        self.state = GameState.INPUT_NUMBER
        

    def input_number(self):
        try:
            self.answer = int(input(f"Enter the number you are thinking of (between {self.bounds[0]} and {self.bounds[1]}): "))
            if self.answer < self.bounds[0] or self.answer > self.bounds[1]:
                raise ValueError("Number out of bounds.")
            
            self.state = GameState.PERFORM_GUESS
        except ValueError:
            print("Invalid input, please enter a valid number.")


    def perform_guess(self):
        self.guess = random.randint(self.bounds[0], self.bounds[1])

        guess_statements = [
            f"Is your number {self.guess}?",
            f"I’m going to guess—your number is {self.guess}, right?",
            f"I think your number might be {self.guess}. Am I correct?",
        ]
        
        face.say(random.choice(guess_statements), wait=True)

        # face.express({'au4': .3, }, time=1000)
        value = get_user_input(cap, detector, timeout=5)
        # face.express({'au4': 0, }, time=100)

        if self.guess == self.answer and value > 0:
            face.say("Yay, I guessed the number!", wait=True)
            self.state = GameState.OUTRO
        elif self.guess != self.answer and value < 0:
            self.state = GameState.ASK_HIGHER_LOWER
        else:
            ask_again_statements = [
                "I think you are trying to fool me! Let me ask again.",
                "Something's fishy here! Let’s try that question again.",
                # "You can’t trick me that easily! Let me ask again.",
            ]
            face.say(random.choice(ask_again_statements), wait=True)


    def ask_higher_lower(self):
        ask_bigger_statements = [   
            f"Is your number bigger than {self.guess}?",
            f"Is your number higher than {self.guess}?",
            f"Is your number greater than {self.guess}?",
            f"Whoops! Is your number bigger than {self.guess}?",
            f"Should I try a higher number than {self.guess} next?",
        ]

        face.say(random.choice(ask_bigger_statements), wait=True)
        
        # face.express({'au4': .3, }, time=1000)
        value = get_user_input(cap, detector, timeout=5)
        # face.express({'au4': 0, }, time=100)
        
        if self.guess < self.answer and value > 0:
            print("Higher!")
            self.bounds[0] = self.guess + 1
            self.state = GameState.PERFORM_GUESS
        elif self.guess > self.answer and value < 0:
            print("Lower!")
            self.bounds[1] = self.guess - 1
            self.state = GameState.PERFORM_GUESS
        else:
            ask_again_statements = [
                "I'm sorry, I didn't get that. Can you try again?",
                "I didn't understand that, please try again.",
                "I didn't see you correctly, can you repeat that?"
            ]
            face.say(random.choice(ask_again_statements), wait=True)
            self.state = GameState.ASK_HIGHER_LOWER
        

    def outro(self):
        time.sleep(.1)
        outro_statements =[
            "Thanks for playing! Goodbye.",
            "I hope you enjoyted the demo!",
        ]
        face.say(random.choice(outro_statements), wait=True)
        self.state = GameState.END

# Run the game
game = NumberGuessingGame()
game.run()
