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
        self.geometry("1000x800")
        self.configure(bg="white")

        self.model = YOLO("runs/detect/train/weights/best.pt")
        self.cap = cv2.VideoCapture(1)

        self.class_colors = {
            'Coke': (0, 0, 255),
            'Sprite': (0, 255, 0),
            'Pepsi': (255, 0, 0),
            'Fanta': (0, 140, 255)
        }
        self.confidence_threshold = 0.7
        self.is_detecting = False

        self.cart = ["Coke", "Pepsi"]
        self.current_index = 0

        self.current_aisle = 1  # Starts in Aisle 1
        self.item_aisle_map = {}  # Map item to aisle found

        self.camera_frame = tk.Label(self, bg="black")
        self.camera_frame.pack(pady=10)

        self.label_text = tk.StringVar()
        self.label = tk.Label(self, textvariable=self.label_text, font=("Helvetica", 14), bg="white")
        self.label_text.set("Welcome to the Autonomous Soda Selector!")
        self.label.pack(pady=5)

        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=10)

        self.create_circle_button(button_frame, "Coke", "#d32f2f")
        self.create_circle_button(button_frame, "Pepsi", "#1976d2")
        self.create_circle_button(button_frame, "Fanta", "#f57c00")
        self.create_circle_button(button_frame, "Sprite", "#00A752")

        self.start_robot_button = tk.Button(self, text="Start Robot Vision", font=("Helvetica", 14), command=self.toggle_detection)
        self.start_robot_button.pack(pady=15)

        self.cart_button = tk.Button(self, text="View Cart (2)", font=("Helvetica", 12), command=self.view_cart_popup)
        self.cart_button.pack(pady=5)
        self.update_cart_button()

        self.detected_items_in_frame = set()
        self.update_camera_feed()

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

            resized_frame = cv2.resize(frame, (640, 480))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            self.camera_frame.config(image=tk_image)
            self.camera_frame.image = tk_image

            results = self.model(resized_frame, verbose=False)[0]

            detection_frame = resized_frame.copy()
            detected_in_current_frame = set()
            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = box.conf[0]
                cls = int(box.cls[0])
                label = self.model.names[cls]

                color = self.class_colors.get(label, (0, 255, 0))

                if conf > self.confidence_threshold:
                    detected_in_current_frame.add(label)
                    label_text = f"{label} {conf:.2f}"
                    (text_w, text_h), _ = cv2.getTextSize(label_text, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 2)
                    cv2.rectangle(detection_frame, (x1, y1 - text_h - 10), (x1 + text_w, y1), color, -1)
                    cv2.putText(detection_frame, label_text, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
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
            self.camera_frame.config(image=tk_detection_image)
            self.camera_frame.image = tk_detection_image

            time.sleep(0.03)

    def show_found_popup(self, item):
        if item not in self.item_aisle_map:
            self.item_aisle_map[item] = self.current_aisle
        messagebox.showinfo("Soda Found!", f"{item} has been detected in Aisle {self.current_aisle}!")
        self.label_text.set(f"{item} found in Aisle {self.current_aisle} and removed from the list.")

    def make_turn(self):
        if self.current_aisle < 5:
            self.current_aisle += 1
            self.label_text.set(f"Turn made. Now in Aisle {self.current_aisle}")
        else:
            self.label_text.set("Maximum aisle (5) reached.")

    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            resized_frame = cv2.resize(frame, (640, 480))
            rgb_frame = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(rgb_frame)
            tk_image = ImageTk.PhotoImage(image=pil_image)
            self.camera_frame.config(image=tk_image)
            self.camera_frame.image = tk_image
        self.after(30, self.update_camera_feed)

    def create_circle_button(self, parent, soda_name, color):
        canvas = tk.Canvas(parent, width=100, height=100, bg="white", highlightthickness=0)
        canvas.pack(side=tk.LEFT, padx=5, pady=5)

        canvas.create_oval(5, 5, 95, 95, fill="gray80", outline="gray80")
        circle = canvas.create_oval(0, 0, 90, 90, fill=color, outline="white", width=2)
        canvas.create_arc(0, 0, 90, 90, start=45, extent=90, style='arc',
                          outline='white', width=1)
        text = canvas.create_text(45, 45, text=soda_name, fill="white", font=("Helvetica", 10, "bold"))

        def on_enter(e):
            canvas.itemconfig(circle, width=3)
        def on_leave(e):
            canvas.itemconfig(circle, width=2)

        for tag in (circle, text):
            canvas.tag_bind(tag, "<Enter>", on_enter)
            canvas.tag_bind(tag, "<Leave>", on_leave)
            canvas.tag_bind(tag, "<Button-1>", lambda e: self.add_to_cart(soda_name))

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
                popup, text=f"🧃 {item}", font=("Helvetica", 12),
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
            self.make_turn()

        summary = "\n".join([f"{item} → Aisle {aisle}" for item, aisle in self.item_aisle_map.items()])
        self.after(0, lambda: messagebox.showinfo("Item Aisles Summary", summary or "No items were located."))
        self.cart.clear()
        self.item_aisle_map.clear()
        self.current_aisle = 1
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
