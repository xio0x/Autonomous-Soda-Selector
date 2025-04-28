# obstacle_detection_file.py

import RPi.GPIO as GPIO
import time

# === GPIO Pin Setup (CHANGE THESE BASED ON WIRING) ===
TRIG_PIN = 20  # GPIO pin connected to TRIG of ultrasonic sensor (Adjust if wired differently)
ECHO_PIN = 21  # GPIO pin connected to ECHO of ultrasonic sensor (Adjust if wired differently)

# === GPIO Setup ===
GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)


def get_distance():
    """Measure distance using ultrasonic sensor."""

    # Send a short pulse to trigger the ultrasonic sensor
    GPIO.output(TRIG_PIN, True)
    time.sleep(0.00001)  # 10 microseconds pulse (DO NOT change unless sensor manual specifies different)
    GPIO.output(TRIG_PIN, False)

    start_time = time.time()
    stop_time = time.time()

    # Wait for echo start
    while GPIO.input(ECHO_PIN) == 0:
        start_time = time.time()

    # Wait for echo end
    while GPIO.input(ECHO_PIN) == 1:
        stop_time = time.time()

    # Calculate time difference
    time_elapsed = stop_time - start_time
    # Calculate distance (Speed of sound = 34300 cm/s)
    distance = (time_elapsed * 34300) / 2  # Formula: (time x speed of sound) / 2

    return distance  # Return distance in centimeters


def is_wall_close(threshold=20):
    """
    Returns True if a wall is closer than the threshold distance.

    Arguments:
    - threshold: Distance in centimeters to consider "close" (default 20cm)

    === CHANGE threshold value during real testing ===
    Example: you may want to adjust to 15 cm or 25 cm based on arena setup
    """
    try:
        distance = get_distance()
        print(f"Measured Distance = {distance:.2f} cm")  # For debugging / optional remove later
        return distance < threshold
    except Exception as e:
        print(f"Ultrasonic sensor error: {e}")
        return False


def cleanup():
    """Cleanup GPIO pins."""
    GPIO.cleanup()


# === Optional: Manual Testing ===
# Only runs if you directly run this file (useful for sensor calibration)
if __name__ == "__main__":
    try:
        while True:
            if is_wall_close():
                print("Wall close detected!")
            else:
                print("No wall nearby.")
            time.sleep(0.5)  # Delay between checks (CAN CHANGE later if needed)
    except KeyboardInterrupt:
        cleanup()
