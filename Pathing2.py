import time
import sys
from Wheel_funcs import forward, turn_right, stop  # motor functions
import serial
import random

# Mock robot state
navigation_active = True
cart = ['Coke', 'Sprite', 'Pepsi']  # Simulate sodas to find
new_item_detected = False

# Setup Arduino connection
try:
    arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Serial connection failed: {e}")
    sys.exit(1)

def get_sensor_data():
    try:
        line = arduino.readline().decode().strip()
        return line
    except:
        return None

def navigate_aisles():
    global navigation_active, cart, new_item_detected

    try:
        while navigation_active:
            if not cart:
                print("All sodas found! Stopping robot.")
                stop()
                break

            print("Starting down a new aisle...")
            forward()

            while True:
                time.sleep(0.1)

                # Simulate soda detection randomly
                if random.random() < 0.05:  # 5% chance each loop
                    new_item_detected = True

                if new_item_detected:
                    found_soda = cart.pop(0)
                    print(f"{found_soda} detected in aisle! Pausing briefly...")
                    stop()
                    time.sleep(2)
                    new_item_detected = False
                    forward()

                sensor_data = get_sensor_data()
                if sensor_data == "1":
                    print("Wall detected! Preparing to turn...")
                    stop()
                    time.sleep(0.5)
                    turn_right()
                    time.sleep(0.5)
                    forward()
                    time.sleep(1.5)
                    turn_right()
                    time.sleep(0.5)
                    forward()
                    stop()
                    time.sleep(0.5)
                    break

                if not cart:
                    print("All sodas found during aisle! Stopping robot.")
                    stop()
                    navigation_active = False
                    return

    except KeyboardInterrupt:
        print("User Stopped Program")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        stop()
        cleanup()

def cleanup():
    try:
        arduino.close()
    except:
        pass
    finally:
        sys.exit(0)

if __name__ == "__main__":
    navigate_aisles()
