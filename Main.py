import cv2
import customtkinter as ctk
from ultralytics import YOLO
import threading
import time
import sys
from Pathing import navigate_aisles
from Wheel_funcs import stop, cleanup


class SodaSelector(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Autonomous Soda Selector")
        self.geometry("1200x800")
        self.minsize(1000, 700)
        ctk.set_appearance_mode("light")
        self.cart_lock = threading.Lock()
        self.navigation_thread = None
        self.navigation_active = False
        self.found_items_locations = {}

        self.model = YOLO("runs/detect/train/weights/best.pt")
        self.cap = None
        # Initialize camera with retry logic
        for camera_index in range(2):  # Try both camera 0 and 1
            try:
                self.cap = cv2.VideoCapture(camera_index)
                if self.cap.isOpened():
                    print(f"Successfully connected to camera {camera_index}")
                    break
            except Exception as e:
                print(f"Failed to open camera {camera_index}: {e}")
                if self.cap:
                    self.cap.release()
                self.cap = None

        self.class_colors = {
            'Coke': (0, 0, 255),
            'Sprite': (0, 255, 0),
            'Pepsi': (255, 0, 0),
            'Fanta': (0, 140, 255)
        }
        self.confidence_threshold = 0.70
        self.is_detecting = False
        self.detection_thread = None
        self.detection_stopped = threading.Event()
        self.camera_reconnecting = False  # ADDED

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

        self.start_robot_button = ctk.CTkButton(self, text="Start Robot Vision", font=("Helvetica", 16),
                                                command=self.toggle_detection)
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

    def toggle_detection(self):
        if self.is_detecting:
            # Stopping detection
            self.is_detecting = False
            self.navigation_active = False  # Stop navigation
            self.start_robot_button.configure(text="Start Robot Vision")
            self.detection_stopped.set()
            if self.detection_thread and self.detection_thread.is_alive():
                self.detection_thread.join()
            self.detection_thread = None
            # Stop the motors when detection is stopped
            stop()
        else:
            try:
                # Try to initialize camera if not already initialized
                if not self.cap or not self.cap.isOpened():
                    for camera_index in range(2):
                        try:
                            self.cap = cv2.VideoCapture(camera_index)
                            if self.cap.isOpened():
                                print(f"Connected to camera {camera_index}")
                                break
                        except Exception as e:
                            print(f"Failed to open camera {camera_index}: {e}")
                            if self.cap:
                                self.cap.release()
                            self.cap = None
                            continue

                if not self.cap or not self.cap.isOpened():
                    raise IOError("Could not initialize any camera")

                # Test camera with a single frame read
                ret, _ = self.cap.read()
                if not ret:
                    raise IOError("Camera initialized but cannot read frames")

                # If we get here, camera is working
                self.is_detecting = True
                self.navigation_active = True
                self.start_robot_button.configure(text="Stop Robot Vision")
                self.detection_stopped.clear()

                # Start threads
                self.detection_thread = threading.Thread(target=self.detect_objects, daemon=True)
                self.detection_thread.start()

                self.navigation_thread = threading.Thread(target=navigate_aisles, daemon=True)
                self.navigation_thread.start()


            except Exception as e:
                print(f"Error starting detection: {e}")
                self.label_text.set(f"Error starting detection: {e}")
                self.is_detecting = False
                self.navigation_active = False
                self.start_robot_button.configure(text="Start Robot Vision")
                stop()  # Ensure motors are stopped if there's an error

    def _run_navigation(self):
        navigate_aisles()  # This will now return after 3 turns
        # When navigation is done, stop everything
        self.is_detecting = False
        self.navigation_active = False
        self.after(0, lambda: self.start_robot_button.configure(text="Start Robot Vision"))
        self.after(0, lambda: self.label_text.set("Navigation complete - three turns made"))
        stop()

    def _attempt_camera_reconnect(self):
        print("Attempting to reconnect to camera...")
        self.camera_reconnecting = True

        if self.detection_thread and self.detection_thread.is_alive():
            self.detection_stopped.set()
            self.detection_thread.join()
            self.detection_stopped.clear()

        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
            time.sleep(1)  # Give time for OS to release the camera resource

        try:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                print("Failed to reconnect to camera.")
                return False
            print("Camera reconnected successfully.")
            return True
        except Exception as e:
            print(f"Error during camera reconnection: {e}")
            self.label_text.set(f"Camera Reconnect Error: {e}")
            return False
        finally:
            self.camera_reconnecting = False

    def update_camera_feed(self):
        try:
            if self.cap is None:
                print("Camera is not initialized.  Attempting to reinitialize.")
                if not self._attempt_camera_reconnect():
                    self.label_text.set("Camera initialization failed.")
                    self.after(5000, self.update_camera_feed)
                    return

            ret, frame = self.cap.read()
            if not ret:
                print("Error: Couldn't read frame in update_camera_feed.")
                if not self._attempt_camera_reconnect():
                    self.label_text.set("Camera read failed.")
                    self.after(5000, self.update_camera_feed)
                    return
        except cv2.error as e:
            print(f"OpenCV error in update_camera_feed: {e}")
            self.label_text.set(f"OpenCV Error: {e}")
            if not self._attempt_camera_reconnect():
                self.after(5000, self.update_camera_feed)
                return
        except Exception as e:
            print(f"An unexpected error in update_camera_feed: {e}")
            self.label_text.set(f"Update Camera Feed Error: {e}")
            if not self._attempt_camera_reconnect():
                self.after(5000, self.update_camera_feed)
                return
        finally:
            self.after(30, self.update_camera_feed)

    def detect_objects(self):
        while self.is_detecting and not self.detection_stopped.is_set():  # Add continuous detection loop
            try:
                # Check if cart is empty - if it is, stop everything
                if not self.cart:
                    print("Cart is empty - all items found!")
                    self.is_detecting = False
                    self.navigation_active = False
                    self.start_robot_button.configure(text="Start Robot Vision")
                    stop()  # Stop motors
                    self.label_text.set(f"All items found! Mission complete!\n{self.found_items_locations}")
                    self.after(0, self.show_summary_popup)
                    return

                ret, frame = self.cap.read()
                if not ret:
                    self.is_detecting = False
                    self.label_text.set("Error: Camera feed lost in detection.")
                    return

                resized_frame = self.resize_frame(frame)

                try:
                    results = self.model(resized_frame, verbose=False)[0]
                except Exception as e:
                    print(f"Model error during detection: {e}")
                    self.label_text.set(f"Model error during detection: {e}")
                    self.is_detecting = False
                    return

                detected_in_frame = set()
                for box in results.boxes:
                    conf = box.conf[0]
                    cls = int(box.cls[0])
                    label = self.model.names[cls]

                    if conf > self.confidence_threshold:
                        if label in self.cart and label not in detected_in_frame and not self.camera_reconnecting:
                            print(f"Detected: {label}, Cart before removal: {self.cart}")
                            print(f"Removing {label} from cart.")
                            self.found_items_locations[label] = f"Aisle {self.current_aisle}"
                            self.after(0, lambda l=label: self.show_found_popup(l))
                            try:
                                self.cart.remove(label)
                                detected_in_frame.add(label)
                            except ValueError as e:
                                print(f"Error removing {label} from cart: {e}, Current cart: {self.cart}")
                                self.label_text.set(f"Error removing item: {e}")
                            self.update_cart_button()
                        elif label in detected_in_frame:
                            print(f"Already processed {label} in this frame.")
                        elif label not in self.cart:
                            print(f"{label} not in cart.")

                time.sleep(0.03)  # Small delay to prevent CPU overuse

            except Exception as e:
                print(f"Camera error: {e}")
                self.is_detecting = False
                self.label_text.set("Error during detection process")
                return

        print("Detection loop ended")
        if self.cap and self.cap.isOpened():
            self.cap.release()

    def add_to_cart(self, item):
        with self.cart_lock:
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
        print(f"Removing {item} from cart via GUI. Current cart: {self.cart}")
        if item in self.cart:
            self.cart.remove(item)
            self.update_cart_button()
            popup.destroy()
            self.view_cart_popup()

    def on_closing(self):
        self.is_detecting = False
        self.detection_stopped.set()
        if self.detection_thread and self.detection_thread.is_alive():
            self.detection_thread.join()
        if hasattr(self, 'cap') and self.cap is not None:
            self.cap.release()
        cleanup()
        self.destroy()

    def show_found_popup(self, label):
        popup = ctk.CTkToplevel(self)
        popup.title("Item Found!")
        popup.geometry("300x150")
        popup.attributes('-topmost', True)

        message = f"Found {label}!"
        ctk.CTkLabel(popup, text=message, font=("Helvetica", 16, "bold")).pack(pady=20)

        def close_popup():
            popup.destroy()

        popup.after(2000, close_popup)

    def show_summary_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Shopping Summary")
        popup.geometry("400x300")
        popup.attributes('-topmost', True)

        # Header
        ctk.CTkLabel(popup, text="Items Found Summary",
                     font=("Helvetica", 18, "bold")).pack(pady=10)

        # Create a frame for the summary
        summary_frame = ctk.CTkFrame(popup)
        summary_frame.pack(pady=10, padx=20, fill="both", expand=True)

        # Add header row
        ctk.CTkLabel(summary_frame, text="Item",
                     font=("Helvetica", 14, "bold")).grid(row=0, column=0, padx=10, pady=5)
        ctk.CTkLabel(summary_frame, text="Location",
                     font=("Helvetica", 14, "bold")).grid(row=0, column=1, padx=10, pady=5)

        # Add items
        for row, (item, location) in enumerate(self.found_items_locations.items(), 1):
            ctk.CTkLabel(summary_frame, text=item,
                         font=("Helvetica", 12)).grid(row=row, column=0, padx=10, pady=5)
            ctk.CTkLabel(summary_frame, text=location,
                         font=("Helvetica", 12)).grid(row=row, column=1, padx=10, pady=5)

        # Close button
        ctk.CTkButton(popup, text="Close",
                      command=popup.destroy).pack(pady=10)

    def show_end_search_popup(self):
        popup = ctk.CTkToplevel(self)
        popup.title("Search Complete")
        popup.geometry("400x200")
        popup.attributes('-topmost', True)

        # Header
        ctk.CTkLabel(popup, text="End of Search", 
                     font=("Helvetica", 24, "bold")).pack(pady=20)

        # Message
        remaining_items = len(self.cart)
        if remaining_items > 0:
            items_text = ', '.join(self.cart)
            message = f"Unable to find {remaining_items} item{'s' if remaining_items > 1 else ''}:\n{items_text}"
        else:
            message = "All items have been found!"
        
        ctk.CTkLabel(popup, text=message, 
                     font=("Helvetica", 14)).pack(pady=20)

        # Close button
        ctk.CTkButton(popup, text="Close", 
                  command=popup.destroy).pack(pady=10)

        # Show the summary popup after this one closes
        popup.after(3000, lambda: [popup.destroy(), self.show_summary_popup()])


if __name__ == "__main__":
    app = SodaSelector()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    try:
        app.mainloop()
    except Exception as e:
        print(f"Mainloop error: {e}")
        sys.exit(1)
