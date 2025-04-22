import random
import time
import logging
from obstacle_detection import detect_obstacle

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def simulate_movement():
    logging.info("Robot movement simulation started...")
    for _ in range(10):
        distance = random.uniform(5, 20)  # ⚠️ Replace with real sensor value
        logging.info(f"Distance: {distance:.2f} cm")
        if detect_obstacle(distance):
            logging.warning("Obstacle too close! Emergency stop.")
            break
        time.sleep(0.5)

simulate_movement()
