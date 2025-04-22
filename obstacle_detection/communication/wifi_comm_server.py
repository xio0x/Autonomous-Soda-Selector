import socket
import logging

logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

HOST = ''  # Listen on all available interfaces
PORT = 65432  # ⚠️ Confirm port

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(1)

logging.info("Waiting for connection...")

conn, addr = server.accept()
logging.info(f"Connected by {addr}")

while True:
    data = conn.recv(1024).decode()
    if not data:
        break
    logging.info(f"Received command: {data}")
    # Example: handle_command(data)

conn.close()
