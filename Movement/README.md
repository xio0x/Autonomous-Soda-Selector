"""
README – pathing.py

Overview:
---------
This file defines the robot's autonomous pathing logic that simulates moving down grocery store aisles.
It is NOT meant to be run directly. Instead, it is called by the GUI in cartUI.py when the user clicks "Start Aisle Search".

How It Works:
-------------
- The function `navigate_aisles(app)` is triggered from cartUI.py using a thread.
- The robot moves forward through an aisle using motors until:
    • A wall is detected via ultrasonic sensor (using is_wall_close())
    • All soda items have been removed from the cart (detected via vision in cartUI)
- When a wall is detected:
    • The robot stops, turns left, and enters the next aisle.
    • GUI is updated via app.make_turn()
- When all items are found or max aisles are passed, the robot stops and a summary is shown.

Integration:
------------
This script depends on:
- cartUI.py: for GUI, detection, and cart state
- Wheel_funcs.py: for motor control (forward, stop, turn_left)
- obstacle_detection_file.py: for wall detection using an ultrasonic sensor

Functions Used:
---------------
- navigate_aisles(app): Main entry point called by the GUI. Handles all aisle navigation.
- is_wall_close(): Returns True if a wall is detected nearby.
- app.cart: List of sodas to find; updated by GUI during detection.
- app.make_turn(): Increments the aisle counter and updates GUI.
- app.label_text: Updates current GUI label to show robot state.
- messagebox.showinfo(): Displays a popup with a summary at the end of the run.

How to Trigger:
---------------
# Inside cartUI.py:
from pathing import navigate_aisles

# In start_robot_search():
threading.Thread(target=navigate_aisles, args=(self,), daemon=True).start()

Notes:
------
- Do not run pathing.py directly.
- All soda detection logic remains inside cartUI; this file only handles movement.
"""
