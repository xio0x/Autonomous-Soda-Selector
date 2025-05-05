import time
import sys
from Wheel_funcs import forward, turn_right, stop  # motor functions
import serial

try:
    arduino = serial.Serial(port="/dev/ttyACM0", baudrate=9600, timeout=1)
except serial.SerialException as e:
    print(f"Failed to open serial connection: {e}")
    sys.exit(1)
data = arduino.readline().decode().strip()


def navigate_aisles(app_instance):
    try:
        while app_instance.navigation_active:
            if not app_instance.cart:
                print("All sodas found! Stopping robot.")
                stop()
                break

            print("Starting down a new aisle...")
            forward()

            while True:
                time.sleep(0.1)

                # Check if soda detected
                if app_instance.new_item_detected:
                    print("Soda detected in aisle! Pausing briefly...")
                    stop()
                    time.sleep(2)
                    app_instance.new_item_detected = False  # reset flag
                    forward()

                # Check if wall is detected - ensure data is defined
                sensor_data = app_instance.get_sensor_data()  # Assuming this method exists
                if sensor_data and sensor_data == "1":
                    print("Wall detected! Preparing to turn...")
                    stop()
                    time.sleep(0.5)
                    turn_right()
                    time.sleep(0.5)  # First 90° turn
                    forward()
                    time.sleep(1.5)  # Move forward into the next aisle
                    turn_right()
                    time.sleep(0.5)  # Second 90° turn
                    forward()
                    stop()
                    time.sleep(0.5)
                    break

                # Check if all sodas found
                if not app_instance.cart:
                    print("All sodas found during aisle! Stopping robot.")
                    stop()
                    return

    except KeyboardInterrupt:
        print("User Stopped Program")
    except Exception as e:
        print(f"Error occurred: {e}")
    finally:
        stop()
        # Add any necessary cleanup here


if __name__ == "__main__":
    navigate_aisles()


def cleanup():
    try:
        arduino.close()
    except:
        pass
    finally:
        sys.exit(0)
