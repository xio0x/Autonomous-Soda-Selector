# pathing.py

import time
from Wheel_funcs import forward, stop, turn_left
from obstacle_detection import is_wall_close
from tkinter import messagebox  # GUI popup summary

def navigate_aisles(app):
    """
    Called from cartUI when 'Start Aisle Search' is pressed.
    Moves aisle-by-aisle until all sodas in the cart are found.
    """
    try:
        while app.cart and app.current_aisle <= 5:
            print(f"[Aisle {app.current_aisle}] Searching...")
            app.after(0, lambda: app.label_text.set(f"Moving through Aisle {app.current_aisle}..."))
            forward()

            while True:
                time.sleep(0.1)

                if not app.cart:
                    print("Cart is empty. Stopping robot.")
                    stop()
                    break

                if is_wall_close():
                    print("Wall detected! Turning to next aisle.")
                    stop()
                    time.sleep(0.5)

                    turn_left()  # or turn_right() if needed
                    time.sleep(0.5)

                    forward()
                    time.sleep(1.5)
                    stop()
                    time.sleep(0.5)

                    app.make_turn()  # Increments aisle and updates GUI
                    break

        # Show summary after run
        summary = "\n".join(f"{item} → Aisle {aisle}" for item, aisle in app.item_aisle_map.items()) \
                  or "No items were located."
        app.after(0, lambda: messagebox.showinfo("Search Summary", summary))
        app.after(0, lambda: app.label_text.set("Search complete."))
        stop()

    except Exception as e:
        print(f"[ERROR] Pathing failed: {e}")
        stop()

