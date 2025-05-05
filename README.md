# Autonomous Soda Selector  
*CMPSC 497 - Special Topics: Raspberry Pi*  

### Team Members  
- Xiomara Mohamed  
- Andrew Herman  
- Matthew Henry  
- Fern Martins  

---

## Overview

The Autonomous Soda Selector is a Python-based application that simulates an autonomous robot navigating a grocery store to identify and locate soda cans selected by the user. It uses computer vision via a webcam and a YOLOv8 object detection model to detect items and notify the user when selected sodas are found. Although this version does not move a physical robot, it demonstrates the foundational logic for automated product detection in a retail setting.

---

## Features

- **User Interface**: Created with `customtkinter` for a clean and user-friendly experience.
- **Object Detection**: Integrates a trained YOLOv8 model to detect soda cans in real-time using a webcam.
- **Virtual Shopping Cart**: Lets users add or remove soda types before scanning.
- **Live Visual Feedback**: Annotates webcam feed with bounding boxes and soda labels.
- **Notification System**: Alerts the user when a selected soda is detected.
- **Simulated Robot Vision**: The "Start Robot Vision" button mimics an autonomous search process and tracks detected items with aisle data.

---

## How It Works

### Software Functionality

- **CartUI Interface**:  
  The interface allows users to select from four soda types: Coke, Pepsi, Fanta, and Sprite. Users can add or remove these from a virtual cart. Once ready, they click "Start Robot Vision."

- **Vision Detection Process**:  
  When initiated, the application activates the webcam and scans the environment for the selected sodas using the trained YOLOv8 model. As sodas are found, the application logs which soda was found and its aisle number (simulated).

- **Final Display**:  
  After all items are found, the application displays a final summary of each soda and its corresponding aisle.

---

## Hardware Requirements

If implementing the full robot system, the following components are needed:

- HelloMaker robot chassis kit  
- Keystudio 37-in-1 sensor kit (including ultrasonic sensor and breadboard)  
- Raspberry Pi 5  
- Arduino Uno  
- Webcam  
- 5V battery pack  
- Portable power bank  

### Hardware Workflow

- **Raspberry Pi 5**: Runs CartUI and motion logic scripts.
- **Arduino Uno**: Reads distance values from the ultrasonic sensor and triggers movement changes.
- **Integration**: The Pi controls forward movement, while the Arduino ensures obstacle avoidance and turning behavior.

---

## Prerequisites

Before running the application:

1. **Install Python 3.x**  
   Download and install from [https://www.python.org](https://www.python.org)

2. **Install Required Libraries**  
   Use pip to install dependencies:
   ```bash
   pip install -r requirements.txt
