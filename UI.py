import tkinter as tk
from tkinter import messagebox
import threading
import time

class SodaSelector(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Autonomous Soda Selector")
        self.geometry("500x420")
        self.configure(bg="white")

        self.cart = []
        self.current_index = 0

        self.show_welcome_page()

    # ----------------- Welcome Page ----------------- #
    def show_welcome_page(self):
        self.clear_window()
        welcome_label = tk.Label(self, text="Lets Go Shopping!", font=("Helvetica", 20), bg="white")
        welcome_label.pack(pady=40)

        start_button = tk.Button(self, text="Choose your items, and our robot will find them!", font=("Helvetica", 16), command=self.show_selection_page)
        start_button.pack(pady=20)

    # ----------------- Selection Page ----------------- #
    def show_selection_page(self):
        self.clear_window()

        # Header frame (for cart icon)
        header_frame = tk.Frame(self, bg="white")
        header_frame.pack(fill=tk.X, pady=5)

        self.label = tk.Label(header_frame, text="Select Your Soda(s)", font=("Helvetica", 20), bg="white")
        self.label.pack(side=tk.LEFT, padx=10)

        cart_button = tk.Button(header_frame, text="🛒", font=("Helvetica", 16), command=self.view_cart_popup, relief=tk.FLAT, bg="white")
        cart_button.pack(side=tk.RIGHT, padx=10)

        # Soda buttons
        button_frame = tk.Frame(self, bg="white")
        button_frame.pack(pady=10)

        self.create_circle_button(button_frame, "Coke", "#d32f2f")
        self.create_circle_button(button_frame, "Pepsi", "#1976d2")
        self.create_circle_button(button_frame, "Fanta", "#f57c00")
        self.create_circle_button(button_frame, "Sprite", "#00A752")

        # Start robot button
        start_button = tk.Button(self, text="Start Robot", font=("Helvetica", 14), command=self.start_robot_search)
        start_button.pack(pady=15)

    def create_circle_button(self, parent, soda_name, color):
        canvas = tk.Canvas(parent, width=130, height=130, bg="white", highlightthickness=0)
        canvas.pack(side=tk.LEFT, padx=10)

        canvas.create_oval(15, 15, 115, 115, fill="gray80", outline="gray80")
        circle = canvas.create_oval(10, 10, 110, 110, fill=color, outline="white", width=3)
        canvas.create_arc(10, 10, 110, 110, start=45, extent=90, style='arc',
                          outline='white', width=2)
        text = canvas.create_text(60, 60, text=soda_name, fill="white", font=("Helvetica", 14, "bold"))

        def on_enter(e):
            canvas.itemconfig(circle, width=5)
        def on_leave(e):
            canvas.itemconfig(circle, width=3)

        for tag in (circle, text):
            canvas.tag_bind(tag, "<Enter>", on_enter)
            canvas.tag_bind(tag, "<Leave>", on_leave)
            canvas.tag_bind(tag, "<Button-1>", lambda e: self.add_to_cart(soda_name))

    # ----------------- Cart Logic ----------------- #
    def add_to_cart(self, item):
        if item in self.cart:
            self.label.config(text=f"{item} is already in the cart!")
        else:
            self.cart.append(item)
            self.label.config(text=f"{item} added to cart.")

    def view_cart_popup(self):
        popup = tk.Toplevel(self)
        popup.title("Your Cart")
        popup.geometry("250x250")
        popup.configure(bg="white")

        if not self.cart:
            tk.Label(popup, text="Cart is empty.", font=("Helvetica", 12), bg="white").pack(pady=20)
            return

        tk.Label(popup, text="Tap an item to remove it:", font=("Helvetica", 12), bg="white").pack(pady=10)

        for item in self.cart:
            item_button = tk.Button(
                popup, text=f"🧃 {item}", font=("Helvetica", 12),
                bg="lightgray", relief=tk.RAISED,
                command=lambda i=item: self.remove_item(i, popup)
            )
            item_button.pack(pady=5, padx=10, fill=tk.X)

    def remove_item(self, item, popup):
        self.cart.remove(item)
        popup.destroy()
        self.view_cart_popup()  # Refresh the popup

    def start_robot_search(self):
        if not self.cart:
            messagebox.showwarning("Empty Cart", "Add at least one soda before starting.")
            return

        self.label.config(text="Robot is starting...")
        self.current_index = 0
        threading.Thread(target=self.process_cart_items, daemon=True).start()

    def process_cart_items(self):
        while self.current_index < len(self.cart):
            item = self.cart[self.current_index]
            self.after(0, lambda i=item: self.label.config(text=f"Fetching: {i}..."))
            self.navigate_to_object(item)
            self.current_index += 1

        self.cart.clear()
        self.after(0, lambda: self.label.config(text="All items collected. Choose more!"))

    def navigate_to_object(self, object_name):
        print(f"Robot navigating to: {object_name}")
        time.sleep(3)  # Simulated search
        print(f"Robot found: {object_name}")
        self.after(0, lambda: messagebox.showinfo("Object Found", f"{object_name} has been located!"))

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()


if __name__ == "__main__":
    app = SodaSelector()
    app.mainloop()
