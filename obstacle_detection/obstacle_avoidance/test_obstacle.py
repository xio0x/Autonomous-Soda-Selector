import logging
from obstacle_detection import detect_obstacle

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

distance = 8  # ⚠️ Replace with sensor reading

if detect_obstacle(distance):
    logging.info("Take evasive action!")
