# Pathing Control Script

## Overview
`pathing.py` controls the autonomous movement of the robot through a simulated grocery store environment with aisles.  
The robot moves forward down an aisle, briefly stops if it detects a soda (can), and turns into the next aisle upon reaching a wall.  
The robot stops completely once all sodas in the cart have been detected and removed.

---

## How It Works
- **Forward Movement:** Robot moves forward by default inside an aisle.
- **Soda Detection:** If a soda can is detected (using `placeholder`), the robot stops briefly for 2 seconds, then continues moving.
- **Wall Detection:** If a wall is detected (using ultrasonic sensors), the robot stops, turns left, and continues into the next aisle.
- **Completion:** When all sodas in the cart are found, the robot stops entirely.

---

## Requirements
- Python 3.x
- OpenCV (`cv2`)
- YOLO model (`ultralytics` package)
- Wheel control functions (from `Wheel_funcs.py`)
- Obstacle detection module (`obstacle_detection_file.py`)
- Soda detection app (`Selector.py`)

---

## Important Notes
- The file assumes an instance of `placeholder` (`app`) is already created in `placeholder`.
- `app.new_item_detected` should be set to `True` when a soda is found.
- Wall detection is handled separately using ultrasonic sensors.

---

## Usage
Simply run:

```bash
python3 pathing.py
