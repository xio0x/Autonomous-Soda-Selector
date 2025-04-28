import time
import sys
from Wheel_funcs import forward, turn_left, stop  # motor functions
from obstacle_detection import is_wall_close  # need to change obstacle detection
from Selector import app  # talk to object detection to change apps

def navigate_aisles():
    try:
        while True:
            # Before moving, check if all sodas found
            if not app.cart:
                print("All sodas found! Stopping robot.")
                stop()
                break

            print("Starting down a new aisle...")
            forward()

            while True:
                # During aisle movement
                time.sleep(0.1)

                # Check if soda detected
                if app.new_item_detected:
                    print("Soda detected in aisle! Pausing briefly...")
                    stop()
                    time.sleep(2)
                    app.new_item_detected = False  # reset flag
                    forward()

                # Check if wall is detected
                if is_wall_close():
                    print("Wall detected! Preparing to turn...")
                    stop()
                    time.sleep(0.5)

                    turn_left()  # or turn_right(), depends on layout
                    time.sleep(0.5)

                    forward()
                    time.sleep(1.5)  # Move into next aisle entrance
                    stop()
                    time.sleep(0.5)
                    break  # Break inner loop -> Start moving in next aisle

                # Also re-check if all sodas found after any movement
                if not app.cart:
                    print("All sodas found during aisle! Stopping robot.")
                    stop()
                    sys.exit()

    except KeyboardInterrupt: #can change into emergency stop
        print("Navigation interrupted by user.")
        stop()
        sys.exit()

if __name__ == "__main__":
    navigate_aisles()

