# mtg_commander_gui_mobile.py
import requests
import random
import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from io import BytesIO
print("This app is under development and is not perfect!")

# Color options including 1–5 color combos, WUBERG, and Colorless
color_options = {
    # Single colors
    "W": "White", "U": "Blue", "B": "Black", "R": "Red", "G": "Green",
    # Two-color combos
    "WU": "White-Blue", "UB": "Blue-Black", "BR": "Black-Red", "RG": "Red-Green", "GW": "Green-White",
    "WB": "White-Black", "UR": "Blue-Red", "BG": "Black-Green", "RW": "Red-White", "GU": "Green-Blue",
    # Three-color combos
    "WUB": "White-Blue-Black", "UBR": "Blue-Black-Red", "BRG": "Black-Red-Green", "RGW": "Red-Green-White", "GWU": "Green-White-Blue",
    "WBR": "White-Black-Red", "URG": "Blue-Red-Green", "BGW": "Black-Green-White", "RWU": "Red-White-Blue", "UBG": "Blue-Black-Green",
    # Four-color combos
    "WUBR": "Non-Green", "UBRG": "Non-White", "BRGW": "Non-Blue", "RGWU": "Non-Black", "GWUB": "Non-Red",
    # Five-color combos
    "WUBRG": "Five-Color",
    # Colorless
    "C": "Colorless"
}

# Function to fetch and display random commander
def get_commander(color_code):
    if color_code == "C":
        # Only fully colorless commander-legal cards
        query = f"https://api.scryfall.com/cards/search?q=(t:legendary+type:creature+OR+oracle:%22can+be+your+commander%22+OR+oracle:partner)+color=colorless&unique=cards"
    else:
        # Legendary creatures or partner/commander-legal cards for a color combo
        query = f"https://api.scryfall.com/cards/search?q=(t:legendary+type:creature+OR+oracle:%22can+be+your+commander%22+OR+oracle:partner)+color={color_code}&unique=cards"

    try:
        response = requests.get(query)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Failed to fetch data: {e}")
        return

    if "data" not in data or len(data["data"]) == 0:
        messagebox.showinfo("No Commanders", "No commanders found for this color combination.")
        return

    commander = random.choice(data["data"])

    # Clear previous image
    image_label.config(image='')

    # Show commander info
    info_text = f"Name: {commander['name']}\nMana Cost: {commander.get('mana_cost', 'N/A')}\nType: {commander.get('type_line', 'N/A')}\nText: {commander.get('oracle_text', 'No description available')}"
    info_label.config(text=info_text)

    # Display image
    img_url = None
    if "image_uris" in commander:
        img_url = commander["image_uris"]["normal"]
    elif "card_faces" in commander:
        img_url = commander["card_faces"][0]["image_uris"]["normal"]

    if img_url:
        response = requests.get(img_url)
        img_data = Image.open(BytesIO(response.content))
        img_data = img_data.resize((223, 310))  # Resize to fit window
        img = ImageTk.PhotoImage(img_data)
        image_label.config(image=img)
        image_label.image = img

# Setup Tkinter window
root = tk.Tk()
root.title("MTG Random Commander Generator")
root.configure(bg="#1a1a1a")  # Dark background for mobile-friendly look

# Create a frame for buttons (grid layout for multiple rows)
button_frame = tk.Frame(root, bg="#7e31fa")
button_frame.pack(pady=10)

# Add buttons in grid (max 3 per row)
row = 0
col = 0
for code, name in color_options.items():
    btn = tk.Button(button_frame, text=name, width=16, height=2, bg="#444", fg="white",
                    command=lambda c=code: get_commander(c))
    btn.grid(row=row, column=col, padx=5, pady=5)
    col += 1
    if col > 2:  # 3 buttons per row
        col = 0
        row += 1

# Label to display commander info
info_label = tk.Label(root, text="", justify="left", wraplength=400, bg="#1a1a1a", fg="white")
info_label.pack(pady=10)

# Label to display commander image
image_label = tk.Label(root, bg="#1a1a1a")
image_label.pack()

# Run the app
root.mainloop()
