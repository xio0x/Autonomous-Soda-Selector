# Autonomous Soda Selector

## Overview

The Autonomous Soda Selector is a Python-based application that simulates an autonomous robot navigating a grocery store to find and identify specific soda cans selected by the user. Utilizing computer vision through a webcam and a trained YOLOv8 object detection model, the application allows users to create a virtual shopping cart of desired sodas. Upon initiating the "robot vision," the application processes the webcam feed, identifies the selected soda cans in view, and notifies the user when an item is found. While this version doesn't control a physical robot, it demonstrates the core functionality of automated item detection in a retail environment.

## Features

* **Intuitive User Interface:** Built with `customtkinter`, providing a clean and user-friendly interface to select desired soda cans.
* **Real-time Object Detection:** Employs a trained YOLOv8 model (`ultralytics`) to detect soda cans in the webcam feed.
* **Virtual Shopping Cart:** Allows users to add and remove soda types from a virtual cart before initiating the detection process.
* **Visual Feedback:** Displays the processed webcam feed with bounding boxes and labels around detected soda cans.
* **Item Found Notification:** Provides a pop-up notification when a selected soda can is detected.
* **Cart Management:** Enables users to view and manage the items currently in their virtual cart.
* **Simulated Autonomous Navigation (Conceptual):** While not physically moving a robot, the "Start Robot Vision" button conceptually initiates the automated search process. The aisle information is currently simulated and would be integrated with actual robot navigation in a real-world implementation.

## Prerequisites

Before running the Autonomous Soda Selector, ensure you have the following installed on your system:

* **Python 3.6 or higher:** You can download it from [python.org](https://www.python.org/downloads/).
* **pip:** Python's package installer, usually included with Python installations.

You will also need to install the required Python libraries. Open your terminal or command prompt and run the following command:

```bash
pip install opencv-python customtkinter Pillow ultralytics
