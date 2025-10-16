# Autonomous Soda Selector  
*CMPSC 497 - Special Topics: Raspberry Pi*  

### Team Members  
- **Xiomara Mohamed** – UI & Integration Developer  
- Andrew Herman   
- Matthew Henry  
- Fern Martins

---

## Overview  

The **Autonomous Soda Selector** is a Python-based system designed to simulate an autonomous robot that detects and identifies soda cans based on a user’s selection.  
It integrates a **CustomTkinter graphical interface** with **YOLOv8 object detection** to allow users to choose specific soda brands, visualize real-time camera detection, and receive alerts when selected items are found.

This project was developed as part of *CMPSC 497 – Raspberry Pi Special Topics* at Penn State Abington.  
My primary role was designing and programming the **Cart User Interface (CartUI)** and **connecting it to the backend detection system**, ensuring seamless communication between the user selection and YOLOv8’s recognition outputs.

---

## My Contributions  

###  **Graphical User Interface (GUI)**
- Designed and built the **CustomTkinter UI** for soda selection and robot simulation.
- Created the **“virtual cart”** system where users can add or remove sodas (Coke, Pepsi, Fanta, Sprite).
- Developed clear **status labels**, color schemes, and buttons for usability and visual appeal.
- Added **real-time visual feedback** to show when a soda is being searched for or detected.

### 🔗 **System Integration**
- Connected the UI controls to the YOLOv8 detection logic so that the application reacts based on user input.
- Implemented **communication hooks** between the selection panel and the detection module to trigger scanning only for chosen items.
- Coordinated final result display logic — once all sodas are found, the interface shows a completion summary (detected items and simulated aisles).

### ⚙️ **Code Organization & Collaboration**
- Structured the interface into modular Python functions for maintainability and clarity.
- Worked closely with the detection and hardware teams to ensure UI synchronization with robot logic and serial data.

---

## Features  

- **Interactive User Interface:** Built with `customtkinter` for a modern, responsive layout.  
- **Dynamic Item Selection:** Add or remove soda brands before scanning.  
- **Start/Stop Control:** One-click “Start Robot Vision” button initiates YOLOv8-based scanning.  
- **Real-Time Detection:** Visual feedback on detected sodas with bounding boxes and labels.  
- **Summary Display:** Shows which sodas were successfully located and their (simulated) aisle positions.  

---

## How It Works  

1. **UI Initialization:**  
   The program launches a custom Tkinter window displaying selectable soda options.

2. **User Selection:**  
   The user builds a “cart” by choosing one or more sodas.

3. **Detection Activation:**  
   Clicking **“Start Robot Vision”** activates the webcam and loads the YOLOv8 model.  
   The program filters detections to match only selected sodas.

4. **Live Feedback:**  
   The interface updates dynamically to show when a soda is detected in view, and which aisle it corresponds to.

5. **Final Summary:**  
   Once all selected sodas are found, a final screen displays completion results.

---

## Technology Stack  

| Component | Description |
|------------|-------------|
| **Python 3** | Core programming language |
| **CustomTkinter** | Graphical user interface library |
| **YOLOv8** | Object detection model for soda recognition |
| **OpenCV** | Camera and image processing |
| **Arduino / Raspberry Pi (Prototype)** | Physical robot control for navigation logic |

---

## Hardware Integration (Team Component)  

In the full robotic implementation, the UI would communicate with:  
- **Raspberry Pi 5:** Running the CartUI and detection scripts.  
- **Arduino Uno:** Managing wheel movement and distance sensing.  
- **Ultrasonic Sensor:** Detecting nearby obstacles and triggering turns.  

My portion focused on ensuring the **software interface correctly initialized and displayed detection results**, and could theoretically control hardware functions through serial connections.

---

## Installation  

1. **Install Python 3.x**  
   Download from [https://www.python.org](https://www.python.org)

2. **Clone the Repository**  
   ```bash# Autonomous Soda Selector  
*CMPSC 497 - Special Topics: Raspberry Pi*  

### Team Members  
- **Xiomara Mohamed** – UI Design, System Integration, and Hardware Navigation  
- Andrew Herman – YOLOv8 Object Detection Model  
- Matthew Henry – Wheel Control and Path Logic  
- Fern Martins – Testing and Documentation  

---

## Overview  

The **Autonomous Soda Selector** is a custom-built robotics system combining a **CustomTkinter user interface**, **YOLOv8 object detection**, and a **Raspberry Pi–Arduino robot chassis** to autonomously locate and identify soda cans selected by the user.  

The robot physically navigated a makeshift grocery store aisle built from cardboard boxes to simulate a retail environment. After the user selected soda options in the interface, the robot autonomously traveled through each aisle, scanning for and detecting the chosen soda cans in real time using a live camera feed.  

This project demonstrates the successful integration of software and hardware systems, including computer vision, motion control, and user interaction through a custom GUI.

---

## My Contributions  

### Graphical User Interface (CustomTkinter)  
- Designed and implemented the full **CartUI interface**, allowing users to select, add, or remove soda types (Coke, Pepsi, Fanta, Sprite).  
- Developed a modern, organized layout with interactive buttons and status labels.  
- Connected user selections directly to the YOLOv8 detection logic.  
- Created live feedback panels to display detection progress and current robot actions.  

### System Integration and Hardware Control  
- Integrated the **CustomTkinter interface**, **YOLOv8 model**, and **Arduino motor system** into a single, cohesive application.  
- Established serial communication between the Raspberry Pi and Arduino to coordinate movement commands (forward, turn, stop).  
- Linked YOLOv8 detection results to robot motion logic so the robot could react in real time to visual input.  
- Validated synchronization between user selection, visual recognition, and physical robot movement.  

### Autonomous Robot Navigation  
- Helped configure and test the **custom-built robot chassis** to autonomously traverse simulated store aisles.  
- Designed and assembled a makeshift grocery environment using cardboard boxes as aisle walls.  
- Verified that once the user finalized selections in the GUI, the robot navigated the aisles, identified target sodas, and reported detections through the interface.  

---

## Features  

- CustomTkinter graphical interface for soda selection and monitoring  
- Real-time YOLOv8 detection of soda cans through a live webcam feed  
- Integration between Raspberry Pi (processing) and Arduino (movement control)  
- Custom-built robot capable of navigating physical aisles  
- Automatic scanning and detection of user-selected soda brands  
- On-screen progress updates and detection feedback  

---

## How It Works  

1. **User Selection:**  
   The user selects one or more soda types from the graphical interface.  

2. **System Start:**  
   When “Start Robot Vision” is pressed, the YOLOv8 model activates and the robot begins moving through the cardboard aisles.  

3. **Autonomous Detection:**  
   The robot continuously scans its environment. When a selected soda is detected, the system logs the detection, updates the interface, and adjusts motion accordingly.  

4. **Completion:**  
   After all selected sodas are found, the robot stops and a summary of detections is displayed on the interface.  

---

## Demo Video  

Watch the live demonstration of the robot navigating the aisle and detecting soda cans:  
[▶ Watch the Project Demo] (https://pennstateoffice365-my.sharepoint.com/:v:/r/personal/xmm5071_psu_edu/Documents/Attachments/IMG_0720.mov?csf=1&web=1&e=jvx1nI&nav=eyJyZWZlcnJhbEluZm8iOnsicmVmZXJyYWxBcHAiOiJTdHJlYW1XZWJBcHAiLCJyZWZlcnJhbFZpZXciOiJTaGFyZURpYWxvZy1MaW5rIiwicmVmZXJyYWxBcHBQbGF0Zm9ybSI6IldlYiIsInJlZmVycmFsTW9kZSI6InZpZXcifX0%3D)


---

## Technology Stack  

| Component | Description |
|------------|-------------|
| **Python 3** | Core programming language |
| **CustomTkinter** | User interface framework |
| **YOLOv8** | Object detection model for soda recognition |
| **OpenCV** | Handles camera input and image processing |
| **Raspberry Pi 4** | Runs the main application and detection pipeline |
| **Arduino Uno** | Controls motors and receives serial commands |
| **Ultrasonic Sensors** | Provides obstacle detection and avoidance |
| **Webcam** | Captures live video feed for YOLOv8 analysis |

---

## Hardware Integration  

| Hardware | Purpose |
|-----------|----------|
| **Custom-Built Robot Chassis** | Designed and assembled for navigating aisles and carrying hardware |
| **Raspberry Pi 4** | Runs detection scripts and sends motion commands |
| **Arduino Uno** | Executes wheel control and sensor readings |
| **Motor Driver Board** | Interfaces between Arduino and motors |
| **Ultrasonic Sensor** | Detects obstacles for real-time avoidance |
| **Webcam** | Captures live video input for detection |
| **Battery Pack** | Provides mobile power to both Pi and motors |

---

## Installation  

1. **Install Python 3.x**  
   [Download Python](https://www.python.org/downloads/)  

2. **Clone this Repository**  
   ```bash
   git clone https://github.com/xio0x/Autonomous_Soda_Selector.git
   cd Autonomous_Soda_Selector

   git clone https://github.com/xio0x/Autonomous_Soda_Selector.git
   cd Autonomous_Soda_Selector
---

## Future Improvements  

- Connect the GUI to a live robot chassis for real-world navigation.  
- Add sound notifications or voice feedback for detections.  
- Expand soda options and improve the model’s accuracy for label recognition.  
- Polish the interface with more animations and a progress indicator.

---

## Acknowledgements  

This project was a collaborative effort between team members in **CMPSC 497 – Raspberry Pi Special Topics**.  
I specifically contributed to **the design, implementation, and integration of the user interface** with the detection logic.  

Original repository: [AndrewHerman28/CMP497_FinalProject](https://github.com/AndrewHerman28/CMP497_FinalProject)  
Forked and modified by **Xiomara Mohamed** to showcase personal contributions in the UI and integration layer.
