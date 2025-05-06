import time
import sys
from Wheel_funcs import forward, turn_right, stop, cleanup  # Motor control functions
import serial
import customtkinter as ctk

# Initialize Arduino serial connection
try:
    arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Serial connection failed: {e}")
    sys.exit(1)


def get_sensor_data():
    try:
        return arduino.readline().decode().strip()
    except:
        return None


def navigate_aisles(app):  # Add app parameter
    turn_count = 0  # Initialize turn counter
    try:
        while True:
            print("Driving forward...")
            forward()

            while True:
                arduino.reset_input_buffer()
                time.sleep(0.1)
                sensor_data = get_sensor_data()

                if sensor_data == "1":
                    print("Wall detected! Performing 180-degree turn...")
                    stop()
                    time.sleep(0.5)

                    turn_right()
                    time.sleep(0.5)

                    forward()
                    time.sleep(1.5)

                    turn_right()
                    time.sleep(0.5)

                    stop()
                    time.sleep(0.5)
                    
                    turn_count += 1  # Increment turn counter
                    print(f"Turn count: {turn_count}")
############
                     # Decide turn direction using modulo
                    if current_aisle % 2 == 0:
                        print("Even aisle — turning LEFT.")
                        # Turn left (180° turn via left)
                        turn_right()  # Assuming right turn actually turns left logically
                        time.sleep(0.5)
                        forward()
                        time.sleep(1.5)
                        turn_right()
                        time.sleep(0.5)
                    else:
                        print("Odd aisle — turning RIGHT.")
                        # Turn right (180° turn via right)
                        turn_right()
                        time.sleep(0.5)
                        forward()
                        time.sleep(1.5)
                        turn_right()
                        time.sleep(0.5)
##############
                    stop()
                    time.sleep(0.5)

                    
                    # Update aisle number in main application
                    app.after(0, app.update_aisle)
                    
                    if turn_count >= 3:
                        print("Three turns completed. Stopping navigation.")
                        stop()
                        # Show end search popup
                        app.after(0, app.show_end_search_popup)
                        cleanup()
                        return  # Exit the function
                        
                    break  # Go to next aisle (start the loop again)

    except KeyboardInterrupt:
        print("User stopped the program.")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        stop()
        cleanup()


if __name__ == "__main__":
    navigate_aisles()
