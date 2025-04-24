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
        self.configure(bg="white")

        # ——— Vision setup ———
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

        # ——— Cart & aisle tracking ———
        self.cart = ["Coke", "Pepsi"]
        self.detected_items_in_frame = set()
        self.current_aisle = 1
        self.item_aisle_map = {}

        # ——— UI setup ———
        self.camera_frame = tk.Label(self, bg="black")
        self.camera_frame.pack(pady=10)

        self.label_text = tk.StringVar(value="Welcome to the Autonomous Soda Selector!")
        tk.Label(self, textvariable=self.label_text,
                 font=("Helvetica", 14), bg="white").pack(pady=5)

        btn_frame = tk.Frame(self, bg="white")
        btn_frame.pack(pady=10)
        for name, color in [("Coke", "#d32f2f"),
                            ("Pepsi", "#1976d2"),
                            ("Fanta", "#f57c00"),
                            ("Sprite", "#00A752")]:
            self.create_circle_button(btn_frame, name, color)

        # Vision control
        self.start_vision_btn = tk.Button(self, text="Start Vision",
                                          font=("Helvetica", 14),
                                          command=self.toggle_detection)
        self.start_vision_btn.pack(pady=5)

        # Aisle-search control
        self.start_search_btn = tk.Button(self, text="Start Aisle Search",
                                          font=("Helvetica", 14),
                                          command=self.start_robot_search)
        self.start_search_btn.pack(pady=5)

        # Cart UI
        self.cart_btn = tk.Button(self, text=f"View Cart ({len(self.cart)})",
                                  font=("Helvetica", 12),
                                  command=self.view_cart_popup)
        self.cart_btn.pack(pady=5)

        # Auto‐size window
        self.update_idletasks()
        w, h = self.winfo_reqwidth(), self.winfo_reqheight()
        self.geometry(f"{w}x{h}")

        # Kick off camera‐feed loop
        self.update_camera_feed()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    # ——— Vision Detection ———
    def toggle_detection(self):
        self.is_detecting = not self.is_detecting
        if self.is_detecting:
            self.start_vision_btn.config(text="Stop Vision")
            threading.Thread(target=self.detect_objects, daemon=True).start()
            self.label_text.set("Vision started.")
        else:
            self.start_vision_btn.config(text="Start Vision")
            self.label_text.set("Vision stopped.")

    def detect_objects(self):
        while self.is_detecting:
            ret, frame = self.cap.read()
            if not ret:
                self.is_detecting = False
                self.label_text.set("Camera error.")
                break

            # show raw camera feed
            frame_resized = cv2.resize(frame, (640, 480))
            rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
            img = ImageTk.PhotoImage(Image.fromarray(rgb))
            self.camera_frame.config(image=img)
            self.camera_frame.image = img

            # run YOLO
            results = self.model(frame_resized, verbose=False)[0]
            out = frame_resized.copy()
            seen = set()

            for box in results.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf, cls = float(box.conf[0]), int(box.cls[0])
                label = self.model.names[cls]

                # **only process if this label is in the cart**
                if label not in self.cart or conf < self.confidence_threshold:
                    continue

                seen.add(label)
                # draw box+label
                col = self.class_colors.get(label, (0,255,0))
                text = f"{label} {conf:.2f}"
                (tw, th), _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, .6, 2)
                cv2.rectangle(out, (x1, y1-th-10), (x1+tw, y1), col, -1)
                cv2.putText(out, text, (x1, y1-5),
                            cv2.FONT_HERSHEY_SIMPLEX, .6, (255,255,255), 2)
                cv2.rectangle(out, (x1, y1), (x2, y2), col, 2)

                # and alert once per frame
                if label not in self.detected_items_in_frame:
                    self.detected_items_in_frame.add(label)
                    self.after(0, lambda l=label: self.show_found_popup(l))
                    self.cart.remove(label)
                    self.after(0, self.update_cart_button)

            self.detected_items_in_frame = seen

            # display annotated frame
            rgb2 = cv2.cvtColor(out, cv2.COLOR_BGR2RGB)
            img2 = ImageTk.PhotoImage(Image.fromarray(rgb2))
            self.camera_frame.config(image=img2)
            self.camera_frame.image = img2

            time.sleep(0.03)

    # ——— Aisle / Popup Logic ———
    def show_found_popup(self, item):
        if item not in self.item_aisle_map:
            self.item_aisle_map[item] = self.current_aisle
        messagebox.showinfo("Found!", f"{item} detected in Aisle {self.current_aisle}!")
        self.label_text.set(f"{item} was in Aisle {self.current_aisle}")

    def make_turn(self):
        if self.current_aisle < 5:
            self.current_aisle += 1
        self.label_text.set(f"Turning… now in Aisle {self.current_aisle}")

    # ——— Sequential Aisle Search ———
    def start_robot_search(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add sodas first.")
            return
        self.label_text.set("Starting aisle-by-aisle search…")
        threading.Thread(target=self.process_cart_items, daemon=True).start()

    def process_cart_items(self):
        while self.cart and self.current_aisle <= 5:
            for item in list(self.cart):
                self.after(0, lambda i=item: self.label_text.set(f"Searching for {i} in Aisle {self.current_aisle}…"))
                found = self.robot_camera_scan(item)
                if found:
                    self.after(0, lambda i=item: self.show_found_popup(i))
                    self.cart.remove(item)
                    self.after(0, self.update_cart_button)
                else:
                    self.after(0, lambda i=item: self.label_text.set(f"{i} not in Aisle {self.current_aisle}"))
                time.sleep(1)
            if self.cart:
                self.make_turn()
                time.sleep(1)

        summary = "\n".join(f"{it} → Aisle {a}" for it, a in self.item_aisle_map.items()) \
                  or "No items located."
        self.after(0, lambda: messagebox.showinfo("Summary", summary))
        self.current_aisle = 1
        self.item_aisle_map.clear()
        self.after(0, lambda: self.label_text.set("Done!"))

    def robot_camera_scan(self, item):
        """
        Stub: hook into your real camera API.
        Return True if 'item' is seen.
        """
        time.sleep(2)
        return False

    # ——— UI Helpers ———
    def create_circle_button(self, parent, soda_name, color):
        c = tk.Canvas(parent, width=100, height=100, bg="white", highlightthickness=0)
        c.pack(side=tk.LEFT, padx=5)
        circle = c.create_oval(5,5,95,95, fill=color, outline="white", width=2)
        txt = c.create_text(50,50, text=soda_name, fill="white", font=("Helvetica",10,"bold"))
        for tag in (circle, txt):
            c.tag_bind(tag, "<Button-1>", lambda e, s=soda_name: self.add_to_cart(s))

    def add_to_cart(self, item):
        if item in self.cart:
            self.label_text.set(f"{item} already in cart.")
        else:
            self.cart.append(item)
            self.label_text.set(f"{item} added.")
            self.update_cart_button()

    def update_cart_button(self):
        self.cart_btn.config(text=f"View Cart ({len(self.cart)})")

    def view_cart_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Your Cart")
        popup.geometry("250x250")
        tk.Label(popup, text="Tap to remove:", font=("Helvetica",12)).pack(pady=10)
        if not self.cart:
            tk.Label(popup, text="(empty)").pack(pady=20)
            return
        for it in list(self.cart):
            btn = tk.Button(popup, text=it, command=lambda i=it, p=popup: self.remove_item(i,p))
            btn.pack(fill=tk.X, padx=10, pady=3)

    def remove_item(self, item, popup):
        self.cart.remove(item)
        popup.destroy()
        self.update_cart_button()
        self.view_cart_popup()

    def update_camera_feed(self):
        ret, frame = self.cap.read()
        if ret:
            f = cv2.resize(frame, (640, 480))
            img = ImageTk.PhotoImage(Image.fromarray(
                cv2.cvtColor(f, cv2.COLOR_BGR2RGB)))
            self.camera_frame.config(image=img)
            self.camera_frame.image = img
        self.after(30, self.update_camera_feed)

    def on_closing(self):
        self.is_detecting = False
        self.cap.release()
        self.destroy()

if __name__ == "__main__":
    app = SodaSelector()
    app.mainloop()
