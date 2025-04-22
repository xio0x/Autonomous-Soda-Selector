import logging

# Logging config (in case this runs standalone)
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def detect_obstacle(distance, threshold=10):
    if distance < threshold:
        logging.warning("Obstacle detected!")
        return True
    return False
