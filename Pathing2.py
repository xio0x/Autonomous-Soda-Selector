import time
import sys
from Wheel_funcs import forward, turn_right, stop  # Motor control functions
import serial

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

def navigate_aisles():
    try:
        while True:
            print("Driving forward...")
            forward()

            while True:
                ser.reset_input_buffer() 
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
                    break  # Go to next aisle (start the loop again)

    except KeyboardInterrupt:
        print("User stopped the program.")
    except Exception as e:
        print(f"Error: {e}")
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
