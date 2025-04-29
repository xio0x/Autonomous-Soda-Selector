import cv2
import customtkinter as ctk
from PIL import Image, ImageTk
from ultralytics import YOLO
import threading
import time

class SodaSelector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Autonomous Soda Selector")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        ctk.set_appearance_mode("light")

        self.model = YOLO("runs/detect/train/weights/best.pt")
        self.cap = cv2.VideoCapture(1)

        self.class_colors = {
            'Coke': (0, 0, 255),
            'Sprite': (0, 255, 0),
            'Pepsi': (255, 0, 0),
            'Fanta': (0, 140, 255)
        }
        self.confidence_threshold = 0.85
        self.is_detecting = False

        self.cart = []
        self.current_index = 0
        self.current_aisle = 1
        self.item_aisle_map = {}

        self.configure_layout()
        self.update_camera_feed()

    def configure_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=5)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)

        self.camera_frame = ctk.CTkLabel(self, text="")
        self.camera_frame.grid(row=0, column=0, padx=20, pady=10, sticky="nsew")

        self.label_text = ctk.StringVar(value="Welcome to the Autonomous Soda Selector!")
        self.label = ctk.CTkLabel(self, textvariable=self.label_text, font=("Helvetica", 20, "bold"))
        self.label.grid(row=1, column=0, padx=20, pady=5, sticky="ew")

        self.button_frame = ctk.CTkFrame(self)
        self.button_frame.grid(row=2, column=0, padx=20, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure((0, 1, 2, 3), weight=1)

        sodas = [
            ("Coke", "#d32f2f"),
            ("Pepsi", "#1976d2"),
            ("Fanta", "#f57c00"),
            ("Sprite", "#00A752")
        ]
        for idx, (name, color) in enumerate(sodas):
            self.create_soda_button(self.button_frame, name, color, idx)

        self.start_robot_button = ctk.CTkButton(self, text="Start Robot Vision", font=("Helvetica", 16), command=self.toggle_detection)
        self.start_robot_button.grid(row=3, column=0, padx=20, pady=10, sticky="ew")

        self.cart_button = ctk.CTkButton(self, text="View Cart", font=("Helvetica", 14), command=self.view_cart_popup)
        self.cart_button.grid(row=4, column=0, padx=20, pady=5, sticky="ew")

    def create_soda_button(self, parent, name, color, column):
        button = ctk.CTkButton(parent, text=name, fg_color=color, corner_radius=50, width=100, height=100,
                               font=("Helvetica", 12, "bold"), command=lambda: self.add_to_cart(name))
        button.grid(row=0, column=column, padx=10, pady=10, sticky="nsew")

    def resize_frame(self, frame):
        screen_width, screen_height = self.winfo_width(), self.winfo_height()
        target_width, target_height = int(screen_width * 0.9), int(screen_height * 0.5)
        h, w, _ = frame.shape
        if w / h > target_width / target_height:
            new_width = target_width
            new_height = int(new_width * h / w)
        else:
            new_height = target_height
            new_width = int(new_height * w / h)
        return cv2.resize(frame, (new_width, new_height))

    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            resized_frame = self.resize_frame(frame)
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(rgb_frame))
            self.camera_frame.configure(image=img)
            self.camera_frame.image = img
        self.after(30, self.update_camera_feed)

    def toggle_detection(self):
        self.is_detecting = not self.is_detecting
        self.start_robot_button.configure(text="Stop Robot Vision" if self.is_detecting else "Start Robot Vision")
        if self.is_detecting:
            threading.Thread(target=self.detect_objects, daemon=True).start()

    def detect_objects(self):
        while self.is_detecting:
            ret, frame = self.cap.read()
            if not ret:
                self.is_detecting = False
                self.label_text.set("Error: Camera feed lost.")
                return
            resized_frame = self.resize_frame(frame)
            try:
                results = self.model(resized_frame, verbose=False)[0]
            except Exception as e:
                self.is_detecting = False
                self.label_text.set("Model error.")
                return

            detection_frame = resized_frame.copy()
            detected = set()
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = self.model.names[cls]
                color = self.class_colors.get(label, (0, 255, 0))

                if conf > self.confidence_threshold:
                    detected.add(label)

                    if label in self.cart:
                        self.after(0, lambda l=label: self.show_found_popup(l))
                        self.cart.remove(label)
                        self.update_cart_button()

            rgb_detection_frame = cv2.cvtColor(detection_frame, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(rgb_detection_frame))
            self.camera_frame.configure(image=img)
            self.camera_frame.image = img

            time.sleep(0.03)

    def add_to_cart(self, item):
        if item not in self.cart:
            self.cart.append(item)
            self.label_text.set(f"{item} added to cart.")
        else:
            self.label_text.set(f"{item} already in cart.")
        self.update_cart_button()

    def update_cart_button(self):
        self.cart_button.configure(text=f"View Cart ({len(self.cart)})")

    def view_cart_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Your Cart")
        popup.geometry("300x300")

        if not self.cart:
            ctk.CTkLabel(popup, text="Cart is empty.", font=("Helvetica", 14)).pack(pady=20)
            return

        ctk.CTkLabel(popup, text="Tap to remove:", font=("Helvetica", 14)).pack(pady=10)
        for item in self.cart:
            ctk.CTkButton(popup, text=f"{item}", command=lambda i=item, p=popup: self.remove_item(i, p)).pack(pady=5)

    def remove_item(self, item, popup):
        if item in self.cart:
            self.cart.remove(item)
            self.update_cart_button()
            popup.destroy()
            self.view_cart_popup()

    def on_closing(self):
        self.is_detecting = False
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = SodaSelector()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
