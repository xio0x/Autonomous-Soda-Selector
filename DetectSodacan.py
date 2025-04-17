import cv2 #For camera
from ultralytics import YOLO #For AI Model

"""
scp /path/to/live_detect.py matth@192.168.137.224:~/soda_can/
scp /path/to/runs/detect/train/weights/best.pt matth@192.168.137.224:~/soda_can/
"""

model = YOLO("runs/detect/train/weights/best.pt") #The trained AI Model

cap = cv2.VideoCapture(1) #Load Webcam (might need to change value to 0)

#Has to be in BGR format
class_colors = {
    'Coke':(0, 0, 255),
    'Sprite':(0, 255, 0),
    'Pepsi': (255, 0, 0),
    'Fanta': (0, 140, 255)
}

confidence_threshold = 0.8

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to 640x480 for faster detection
    frame = cv2.resize(frame, (640, 480))

    # Run inference
    results = model(frame, verbose=False)[0]

    # Draw the bounding boxes
    for box in results.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]
        cls = int(box.cls[0])
        label = model.names[cls]

        # Get color for the class or default to green
        color = class_colors.get(label, (0, 255, 0))

        if conf > confidence_threshold:
            label_text = f"{label} {conf:.2f}"
            (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
            cv2.rectangle(frame, (x1, y1 - text_h - 10), (x1 + text_w, y1), color, -1)
            cv2.putText(frame, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)

    # Show the frame
    cv2.imshow("Soda Can Detector", frame)

    # Quit if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
