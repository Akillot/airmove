import cv2
import mediapipe as mp
import pyautogui
import time
import math
from collections import deque

PINCH_IN = 40
PINCH_OUT = 70
COOLDOWN = 0.6
SMOOTHING = 0.30
FPS_SLEEP = 0.01

HOTZONE_W = 180
HOTZONE_H = 80
SMOOTH_BUFFER = 5

pyautogui.FAILSAFE = False
pyautogui.PAUSE = 0

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    model_complexity=1,
    max_num_hands=1,
    min_detection_confidence=0.6,
    min_tracking_confidence=0.5
)

last_action_time = 0
pinch_state = False

screen_w, screen_h = pyautogui.size()
cap = cv2.VideoCapture(0)
prev_x, prev_y = pyautogui.position()
positions_x = deque(maxlen=SMOOTH_BUFFER)
positions_y = deque(maxlen=SMOOTH_BUFFER)

def dist(p1, p2):
    return math.hypot(p1[0]-p2[0], p1[1]-p2[1])

def mac_action(which):
    if which == 'close':
        pyautogui.hotkey('command', 'w')
    elif which == 'min':
        pyautogui.hotkey('command', 'm')
    elif which == 'full':
        pyautogui.hotkey('ctrl', 'command', 'f')

def in_hotzone(x, y):
    return (0 <= x < HOTZONE_W) and (0 <= y < HOTZONE_H)

def sector(x):
    sw = HOTZONE_W / 3
    if x < sw:
        return 'close'
    elif x < 2*sw:
        return 'min'
    else:
        return 'full'

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    if result.multi_hand_landmarks:
        for lm in result.multi_hand_landmarks:
            ix, iy = lm.landmark[8].x * w, lm.landmark[8].y * h
            tx, ty = lm.landmark[4].x * w, lm.landmark[4].y * h
            d = dist((ix, iy), (tx, ty))

            if not pinch_state and d < PINCH_IN:
                pinch_state = True
            elif pinch_state and d > PINCH_OUT:
                pinch_state = False

            screen_x = int(lm.landmark[8].x * screen_w)
            screen_y = int(lm.landmark[8].y * screen_h)
            positions_x.append(screen_x)
            positions_y.append(screen_y)
            avg_x = sum(positions_x) / len(positions_x)
            avg_y = sum(positions_y) / len(positions_y)
            smooth_x = prev_x + (avg_x - prev_x) * SMOOTHING
            smooth_y = prev_y + (avg_y - prev_y) * SMOOTHING
            smooth_x = max(0, min(int(smooth_x), screen_w - 1))
            smooth_y = max(0, min(int(smooth_y), screen_h - 1))
            pyautogui.moveTo(smooth_x, smooth_y)
            prev_x, prev_y = smooth_x, smooth_y

            current_time = time.time()
            if pinch_state and (current_time - last_action_time > COOLDOWN):
                if in_hotzone(smooth_x, smooth_y):
                    mac_action(sector(smooth_x))
                else:
                    pyautogui.click()
                last_action_time = current_time

    time.sleep(FPS_SLEEP)

cap.release()
