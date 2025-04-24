import cv2  # For camera
from ultralytics import YOLO  # For AI Model
import tkinter as tk
from tkinter import messagebox
import threading
import time
from PIL import Image, ImageTk  # For displaying OpenCV frames in Tkinter

class SodaSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Autonomous Soda Selector")
        self.attributes("-fullscreen", True)

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.main_frame = tk.Frame(self, bg="white")
        self.main_frame.grid(row=0, column=0, sticky="nsew")

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(0, weight=2)  # Camera feed takes more vertical space
        self.main_frame.grid_rowconfigure(1, weight=1)  # Label area
        self.main_frame.grid_rowconfigure(2, weight=1)  # Buttons
        self.main_frame.grid_rowconfigure(3, weight=1)  # Cart button

        self.model = YOLO("runs/detect/train/weights/best.pt")  # Load the trained AI Model
        self.cap = cv2.VideoCapture(0)  # Load Webcam (change to 1 if needed)

        self.class_colors = {
            'Coke': (0, 0, 255),
            'Sprite': (0, 255, 0),
            'Pepsi': (255, 0, 0),
            'Fanta': (0, 140, 255)
        }
        self.confidence_threshold = 0.8
        self.is_detecting = False

        self.cart = []
        self.current_index = 0

        self.camera_frame = tk.Label(self.main_frame, bg="black")
        self.camera_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self.current_image = None

        self.label_text = tk.StringVar()
        self.label = tk.Label(self.main_frame, textvariable=self.label_text, font=("Helvetica", 14), bg="white")
        self.label.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
        self.label_text.set("Welcome to the Autonomous Soda Selector!")

        self.button_frame = tk.Frame(self.main_frame, bg="white")
        self.button_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")
        self.button_frame.grid_columnconfigure(0, weight=1)
        self.button_frame.grid_columnconfigure(1, weight=1)
        self.button_frame.grid_columnconfigure(2, weight=1)
        self.button_frame.grid_columnconfigure(3, weight=1)

        self.create_scaled_button(self.button_frame, "Coke", "#d32f2f", 0)
        self.create_scaled_button(self.button_frame, "Pepsi", "#1976d2", 1)
        self.create_scaled_button(self.button_frame, "Fanta", "#f57c00", 2)
        self.create_scaled_button(self.button_frame, "Sprite", "#00A752", 3)

        self.start_robot_button = tk.Button(self.main_frame, text="Start Robot Vision", font=("Helvetica", 14), command=self.toggle_detection)
        self.start_robot_button.grid(row=3, column=0, padx=10, pady=15, sticky="ew")

        self.cart_button = tk.Button(self.main_frame, text="View Cart", font=("Helvetica", 12), command=self.view_cart_popup)
        self.cart_button.grid(row=4, column=0, padx=10, pady=5, sticky="ew")
        self.update_cart_button()

        self.detected_items_in_frame = set()

        self.bind("<Configure>", self.on_resize)
        self.update_camera_feed()

    def on_resize(self, event):
        # This event is triggered when the window is resized.
        # You can add logic here to recalculate sizes or layouts if needed,
        # although with grid and weight configurations, Tkinter often handles
        # scaling quite well automatically for many widgets.
        pass

    def toggle_detection(self):
        self.is_detecting = not self.is_detecting
        if self.is_detecting:
            self.start_robot_button.config(text="Stop Robot Vision")
            threading.Thread(target=self.detect_objects, daemon=True).start()
            self.label_text.set("Robot vision started.")
        else:
            self.start_robot_button.config(text="Start Robot Vision")
            self.label_text.set("Robot vision stopped.")

    def detect_objects(self):
        while self.is_detecting:
            ret, frame = self.cap.read()
            if not ret:
                self.is_detecting = False
                self.label_text.set("Error: Could not read camera feed.")
                self.start_robot_button.config(text="Start Robot Vision")
                break

            # Keep the camera feed aspect ratio consistent
            h, w, _ = frame.shape
            screen_width = self.winfo_width()
            screen_height = self.winfo_height()

            if w / h > screen_width / (screen_height * 0.6):  # Adjust 0.6 based on row weight
                new_width = int(screen_width * 0.9)
                new_height = int(new_width * h / w)
            else:
                new_height = int(screen_height * 0.5)
                new_width = int(new_height * w / h)

            resized_frame = cv2.resize(frame, (new_width, new_height))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            self.current_image = tk_image
            self.camera_frame.config(image=self.current_image)

            try:
                results = self.model(resized_frame, verbose=False)[0]
            except Exception as e:
                print("YOLO inference failed:", e)
                self.label_text.set("Model failed. Check your architecture or camera.")
                self.is_detecting = False
                return

            detection_frame = resized_frame.copy()
            detected_in_current_frame = set()
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                # Scale the bounding box coordinates back to the original frame size for drawing
                scale_x = w / new_width
                scale_y = h / new_height
                orig_x1, orig_y1, orig_x2, orig_y2 = int(x1 * scale_x), int(y1 * scale_y), int(x2 * scale_x), int(y2 * scale_y)

                conf = box.conf[0]
                cls = int(box.cls[0])
                label = self.model.names[cls]

                color = self.class_colors.get(label, (0, 255, 0))

                if conf > self.confidence_threshold:
                    detected_in_current_frame.add(label)
                    label_text = f"{label} {conf:.2f}"
                    (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6 * min(scale_x, scale_y), 2) # Scale text size
                    cv2.rectangle(detection_frame, (x1, y1 - int(text_h * 1.2)), (x1 + text_w, y1), color, -1)
                    cv2.putText(detection_frame, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6 * min(scale_x, scale_y), (255, 255, 255), 2)
                    cv2.rectangle(detection_frame, (x1, y1), (x2, y2), color, 2)

                    if label in self.cart and label not in self.detected_items_in_frame:
                        self.after(0, lambda l=label: self.show_found_popup(l))
                        self.cart.remove(label)
                        self.after(0, self.update_cart_button)
                        self.detected_items_in_frame.add(label)

            self.detected_items_in_frame = detected_in_current_frame

            rgb_detection_frame = cv2.cvtColor(detection_frame, cv2.COLOR_BGR2RGB)
            pil_detection_image = Image.fromarray(rgb_detection_frame)
            tk_detection_image = ImageTk.PhotoImage(image=pil_detection_image)
            self.current_image = tk_detection_image
            self.camera_frame.config(image=self.current_image)

            time.sleep(0.03)

    def show_found_popup(self, item):
        messagebox.showinfo("Soda Found!", f"{item} has been detected!")
        self.label_text.set(f"{item} found and removed from the list.")

    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            h, w, _ = frame.shape
            screen_width = self.winfo_width()
            screen_height = self.winfo_height()

            if w / h > screen_width / (screen_height * 0.6):
                new_width = int(screen_width * 0.9)
                new_height = int(new_width * h / w)
            else:
                new_height = int(screen_height * 0.5)
                new_width = int(new_height * w / h)

            resized_frame = cv2.resize(frame, (new_width, new_height))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            self.current_image = tk_image
            self.camera_frame.config(image=self.current_image)
        self.after(30, self.update_camera_feed)

    def create_scaled_button(self, parent, soda_name, color, grid_column):
        button = tk.Button(parent, text=soda_name, bg=color, fg="white", font=("Helvetica", 12, "bold"),
                           command=lambda: self.add_to_cart(soda_name), relief=tk.RAISED, bd=2)
        button.grid(row=0, column=grid_column, padx=5, pady=5, sticky="nsew")

    def add_to_cart(self, item):
        if item in self.cart:
            self.label_text.set(f"{item} is already in the cart!")
        else:
            self.cart.append(item)
            self.label_text.set(f"{item} added to cart.")
            self.update_cart_button()

    def update_cart_button(self):
        self.cart_button.config(text=f"View Cart ({len(self.cart)})")

    def view_cart_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Your Cart")
        popup.geometry("250x250")
        popup.configure(bg="white")

        if not self.cart:
            tk.Label(popup, text="Cart is empty.", font=("Helvetica", 12), bg="white").pack(pady=20)
            return

        tk.Label(popup, text="Tap an item to remove it:", font=("Helvetica", 12), bg="white").pack(pady=10)

        for item in list(self.cart):
            item_button = tk.Button(
                popup, text=f"\U0001F9C3 {item}", font=("Helvetica", 12),
                bg="lightgray", relief=tk.RAISED,
                command=lambda i=item, p=popup: self.remove_item_from_cart_and_popup(i, p)
            )
            item_button.pack(pady=5, padx=10, fill=tk.X)

    def remove_item_from_cart_and_popup(self, item, popup):
        if item in self.cart:
            self.cart.remove(item)
            self.update_cart_button()
            popup.destroy()
            self.view_cart_popup()

    def start_robot_search(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add at least one soda before starting the robot.")
            return

        self.label_text.set("Robot search started...")
        self.current_index = 0
        threading.Thread(target=self.process_cart_items, daemon=True).start()

    def process_cart_items(self):
        while self.current_index < len(self.cart):
            item = self.cart[self.current_index]
            self.after(0, lambda i=item: self.label_text.set(f"Fetching: {i}..."))
            self.navigate_to_object(item)
            self.current_index += 1

        self.cart.clear()
        self.after(0, lambda: self.label_text.set("All items collected. Choose more!"))
        self.update_cart_button()

    def navigate_to_object(self, object_name):
        print(f"Robot navigating to: {object_name}")
        time.sleep(3)
        print(f"Robot found: {object_name}")
        self.after(0, lambda: messagebox.showinfo("Object Found", f"{object_name} has been located!"))

    def on_closing(self):
        self.is_detecting = False
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = SodaSelector()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
