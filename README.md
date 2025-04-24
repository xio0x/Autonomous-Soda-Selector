# Autonomous Soda Selector

An AI-powered Python application that uses a webcam to detect and identify soda cans (Coke, Pepsi, Sprite, Fanta) in real time, allowing users to build a virtual cart using a touchscreen-like GUI.

## 🚀 Features

- Fullscreen Tkinter GUI with circular soda selection buttons
- Real-time object detection using YOLOv8 (Ultralytics)
- Webcam feed integration with bounding box overlays
- Scrollable interface for compatibility with all screen sizes
- Interactive cart functionality (add/remove sodas)
- Pop-up notifications when a soda in the cart is detected

## 🖼️ Preview
**(Insert screenshot of application in fullscreen with detection active and cart items)**

## 🧠 Tech Stack

- **Python 3.9+**
- **Tkinter** – GUI framework
- **OpenCV** – Camera input and image processing
- **Pillow (PIL)** – Convert OpenCV images for GUI
- **Ultralytics YOLOv8** – Object detection model

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/yourusername/autonomous-soda-selector.git
cd autonomous-soda-selector
```

### 2. Set up virtual environment (recommended)
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Place your trained model
Put your YOLOv8 `.pt` model in:
```
runs/detect/train/weights/best.pt
```

### 5. Run the app
```bash
python soda_selector.py
```

## 📸 Supported Cans
Make sure your YOLOv8 model is trained to recognize the following classes:
- Coke
- Pepsi
- Sprite
- Fanta

You can use [Roboflow](https://roboflow.com) to help build and export your training dataset.

## 🧪 Model Training Tips
- Ensure you annotate cans from multiple angles and lighting conditions
- Train with images resized to `640x640`
- Aim for high mAP50 and recall values for best real-world detection

## 📱 Fullscreen & Compatibility
- Designed for Raspberry Pi and touchscreen tablets
- Tested on macOS with M1/M2 chips
- Scrollable layout ensures all buttons are accessible on smaller screens

## 🔧 Troubleshooting
- **Camera not showing?** Try switching `cv2.VideoCapture(1)` to `cv2.VideoCapture(0)`
- **Model not loading?** Ensure `.pt` path is correct and YOLOv8 is installed
- **Layout broken on small screen?** Use Escape to exit fullscreen or scroll using mouse/touchpad

## 📄 License
MIT License. Feel free to adapt and expand this project for your own AI-vision experiments!

---
Made with 💡 and 🧃 by Andrew Herman

