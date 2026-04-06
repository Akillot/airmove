<h1 align="center">AirMove</h1>

<p align="center">
  <strong>Control your computer with hand gestures. No mouse needed.</strong>
</p>

<p align="center">
  <a href="https://github.com/Akillot/AirMove/blob/master/LICENSE"><img src="https://img.shields.io/github/license/Akillot/AirMove?style=flat-square" alt="License"></a>
  <img src="https://img.shields.io/badge/python-3.8+-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/platform-macOS%20%7C%20Windows%20%7C%20Linux-lightgrey?style=flat-square" alt="Platform">
</p>

---

## What is this?

AirMove uses your webcam to track hand gestures and translate them into mouse input. Point with your index finger to move the cursor. Pinch to click. No hardware beyond a standard webcam.

Built with OpenCV and MediaPipe.

## How it works

```
Webcam → MediaPipe Hand Detection → Landmark Extraction → Gesture Recognition → System Input
```

1. **Tracking** — MediaPipe detects 21 hand landmarks at 30+ FPS
2. **Smoothing** — 5-frame rolling average + linear interpolation eliminates jitter
3. **Gesture detection** — pinch distance between index finger and thumb triggers actions
4. **macOS hotzones** — top-left corner of screen maps to window controls (close / minimize / fullscreen)

## Features

| Gesture | Action |
|---------|--------|
| Point with index finger | Move cursor |
| Pinch (index + thumb) | Click |
| Pinch in top-left hotzone | Window control (close / minimize / fullscreen) |

**Technical details:**
- Pinch-in threshold: 40px, pinch-out: 70px (hysteresis to prevent flicker)
- Action cooldown: 600ms
- Smoothing factor: 0.30
- Hotzone: 180x80px (top-left, divided into 3 sectors)

## Quick Start

### Requirements

- Python 3.8+
- Webcam
- macOS, Windows, or Linux (X11 recommended on Linux)

### Setup

```bash
git clone https://github.com/Akillot/AirMove.git
cd AirMove
python -m venv .venv
source .venv/bin/activate    # Windows: .venv\Scripts\activate
pip install opencv-python mediapipe pyautogui
```

### Run

```bash
python main.py
```

### Stop

```
Ctrl + C
```

## Configuration

Constants at the top of `main.py`:

```python
PINCH_IN = 40          # px — pinch trigger distance
PINCH_OUT = 70         # px — pinch release distance
COOLDOWN = 0.6         # sec — action cooldown
SMOOTHING = 0.30       # cursor interpolation factor (0 = no smoothing, 1 = instant)
SMOOTH_BUFFER = 5      # frames for rolling average
HOTZONE_W = 180        # px — hotzone width
HOTZONE_H = 80         # px — hotzone height
```

## Architecture

```
main.py (single file, ~100 lines)
├── MediaPipe Hands — detection & tracking
├── Gesture Engine — pinch state machine with hysteresis
├── Cursor Smoother — deque-based rolling average + lerp
├── Hotzone System — screen-region → macOS action mapping
└── PyAutoGUI — system-level mouse/keyboard control
```

## Limitations

- Single hand only (max_num_hands=1)
- macOS hotzone actions use `Cmd+W` / `Cmd+M` / `Ctrl+Cmd+F` — won't work on other OS without modification
- Wayland on Linux has limited support — X11 is recommended
- No GUI — headless by design (no webcam preview window to save CPU)

## License

[MIT](./LICENSE)
