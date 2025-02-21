import tkinter as tk
from tkinter import messagebox
import time
import math
import os
from PIL import Image, ImageTk

# Get the directory where the script is located
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Paths for images (PNG files should be in the same directory as the script)
widget_bg_path = os.path.join(BASE_DIR, "cbg_final.png")
clock_face_path = os.path.join(BASE_DIR, "cface.png")

# Create the main window without the window bar
root = tk.Tk()
root.title("Cute Analog Clock Gadget")
root.geometry("250x250")  # Adjust the size as needed
root.resizable(True, True)
root.wm_attributes('-transparentcolor', 'white')  # Make the window transparent where the color is white
root.overrideredirect(True)  # Remove the window bar

canvas = tk.Canvas(root, bg='white', highlightthickness=0)
canvas.pack(fill=tk.BOTH, expand=True)

# Load the widget background image
widget_bg_image = Image.open(widget_bg_path)
widget_bg_photo = ImageTk.PhotoImage(widget_bg_image)

# Load the clock face image
clock_face_image = Image.open(clock_face_path)
clock_face_photo = ImageTk.PhotoImage(clock_face_image)

# Set the initial clock radius for the hands
clock_radius = 60  # Adjust this value to change the initial clock size

# Define initial clock center coordinates and vertical offset
clock_x_center = 125  # Centering based on initial window size
clock_y_center = 125  # Centering based on initial window size
vertical_offset = 30  # Adjust this value to fine-tune the clock face position

def resize_images(event):
    global widget_bg_photo, clock_face_photo, clock_radius, clock_x_center, clock_y_center

    width = event.width
    height = event.height
    min_dimension = max(min(width, height), 150)  # Set a minimum size limit

    # Resize the background image
    resized_bg_image = widget_bg_image.resize((min_dimension, min_dimension), Image.LANCZOS)
    widget_bg_photo = ImageTk.PhotoImage(resized_bg_image)
    canvas.create_image(width // 2, height // 2, image=widget_bg_photo)

    # Resize the clock face image
    clock_face_size = min_dimension - 50  
    resized_clock_face_image = clock_face_image.resize((clock_face_size, clock_face_size), Image.LANCZOS)
    clock_face_photo = ImageTk.PhotoImage(resized_clock_face_image)
    canvas.create_image(width // 2, height // 2 + vertical_offset, image=clock_face_photo)

    # Update clock radius and center
    clock_radius = clock_face_size // 2
    clock_x_center = width // 2
    clock_y_center = height // 2 + vertical_offset + 10

    update_clock()

def draw_hand(length, angle, color, width, add_circles=True):
    angle_rad = math.radians(angle)
    x_end = clock_x_center + length * math.cos(angle_rad - math.pi / 2)
    y_end = clock_y_center + length * math.sin(angle_rad - math.pi / 2)
    canvas.create_line(clock_x_center, clock_y_center, x_end, y_end, fill=color, width=width, tags="hands")
    if add_circles:
        radius = 3  # Circle radius
        canvas.create_oval(clock_x_center - radius, clock_y_center - radius,
                           clock_x_center + radius, clock_y_center + radius,
                           fill=color, outline=color, tags="hands")
        canvas.create_oval(x_end - radius, y_end - radius,
                           x_end + radius, y_end + radius,
                           fill=color, outline=color, tags="hands")

def update_clock():
    canvas.delete("hands")

    current_time = time.localtime()
    hours, minutes, seconds = current_time.tm_hour, current_time.tm_min, current_time.tm_sec

    hour_angle = (hours % 12 + minutes / 60) * 30
    minute_angle = (minutes + seconds / 60) * 6
    second_angle = seconds * 6

    draw_hand(clock_radius * 0.3, hour_angle, "blue", 8)  
    draw_hand(clock_radius * 0.5, minute_angle, "red", 8)  
    draw_hand(clock_radius * 0.5, second_angle, "black", 3, add_circles=False)  

    root.after(1000, update_clock)

# Function to enable dragging the widget
def start_drag(event):
    global startX, startY
    startX, startY = event.x, event.y

def on_drag(event):
    x = root.winfo_pointerx() - startX
    y = root.winfo_pointery() - startY
    root.geometry(f'+{x}+{y}')

root.bind('<Button-1>', start_drag)
root.bind('<B1-Motion>', on_drag)

# Function to pin the widget to the desktop
def pin_to_desktop():
    root.attributes('-topmost', True)

# Function to unpin the widget from the desktop
def unpin_from_desktop():
    root.attributes('-topmost', False)

# Function to show the "About" message
def show_about():
    messagebox.showinfo("About", "That one Cute Clock Face from windows7 Clock Widget\nVersion 1.0 by syed177013 \n\n"
                                 "Yahallo! I am just your below average Programming Enthusiast who likes to make Softwares.\n"
                                 "This app isnt perfect, nor is it complete but serves the one purpose i had in mind when i started making it,\n"
                                 "<Damn i miss that one Clock widget so much from my windows 7 days, wish i could use it on newer windows/my Linux>\n"
                                 "LoL, so dont mind the inconsistencies, Absolute shit image quality and do enjoy if you have decided to use it. \n"
                                 "Thanks a ton, u make me happi :>")

# Function to adjust transparency
def set_transparency(level):
    alpha_value = 1 - (level / 100)
    if level == 100:
        messagebox.showinfo("Transparency", "At this point should have just Closed the widget bruh O: \nWidget will now exit, to see again, relaunch")
        root.quit()
    else:
        root.wm_attributes('-alpha', alpha_value)

# Add context menu
menu = tk.Menu(root, tearoff=0)
menu.add_command(label="Pin to Desktop", command=pin_to_desktop)
menu.add_command(label="Unpin from Desktop", command=unpin_from_desktop)
menu.add_command(label="Resize", command=lambda: enable_dynamic_resize())
menu.add_command(label="About", command=show_about)

transparency_menu = tk.Menu(menu, tearoff=0)
for i in range(0, 101, 10):
    transparency_menu.add_command(label=f"{i}%", command=lambda level=i: set_transparency(level))

menu.add_cascade(label="Transparency", menu=transparency_menu)
menu.add_separator()
menu.add_command(label="Close", command=root.quit)

def on_right_click(event):
    menu.post(event.x_root, event.y_root)

root.bind("<Button-3>", on_right_click)

def enable_dynamic_resize():
    root.overrideredirect(False)
    root.bind('<Configure>', resize_images)

    def on_release(event):
        root.overrideredirect(True)
        root.unbind('<Configure>')
        root.bind('<Configure>', resize_images)
        
    root.bind('<ButtonRelease-1>', on_release)

root.bind('<Configure>', resize_images)

clock_x_center = root.winfo_width() // 2
clock_y_center = root.winfo_height() // 2 + vertical_offset
update_clock()

root.mainloop()
