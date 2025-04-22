import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

def handle_command(command):
    if command == "pause":
        logging.info("Pausing robot...")
    elif command == "stop":
        logging.info("Stopping robot...")
    elif command == "status":
        logging.info("Robot status: All systems operational.")
    else:
        logging.warning("Unknown command received.")
