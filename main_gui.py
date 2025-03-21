import cv2
import numpy as np
import os
from core.image_loader import load_image
from core.text_extractor import extract_text
from core.image_blurrer import blur_text
from core.image_loader import extract_pdf_images
from utilities.file_handler import constract_pdf
import json
from utilities.file_handler import delete_temp
from utilities.file_handler import create_dir
from config.config_loader import load_config
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk



#colors core
BG_COLOR = "#1E1E1E"  # Dark Background
FG_COLOR = "#FFFFFF"  # White Text
BTN_COLOR = "#333333"  # Dark Gray Button
HIGHLIGHT = "#0078D7"  # Blue Accent
FG_COLOR = "white"
BG_GREEN = "\033[42m"


#bluring
def blur():
    config = load_config("default.json")
    if config:
             length = config["length"]
             allow_digit = config["allow_digit"]
             allow_digitWitChar = config["allow_digitWitChar"]
             allow_currency = config["allow_currency"]
             allow_email = config["allow_email"]
             allow_date = config["allow_date"]
             allow_url = config["allow_url"]
             allow_phoneNumber = config["allow_phoneNumber"]
             allow_ssn = config["allow_ssn"]
             allow_ip = config["allow_ip"]
             to_gray = config["to_gray"]
             
             soild_banned_words = config.get("banned_words", []) 
             banned_words = []
             for word in soild_banned_words:
                banned_words.extend(word.split())

             soild_allowed_words = config.get("allowed_words", [])
             allowed_words = []
             for word in soild_allowed_words:
                allowed_words.extend(word.split())
             
             lang = config.get("lang")

    if selected_file:
        global label_done
        if selected_file.endswith(".pdf"):           
           pdf_name , page_numbers = extract_pdf_images(selected_file)
           processed_path = f"temp/{pdf_name}/processed/"
           unprocessed_path = f"temp/{pdf_name}/unprocessed/"
           blured_count = 0
           for i in page_numbers:
                blured_count += blur_text(f"{unprocessed_path}/page_{i}.png", length, allow_digit, allow_digitWitChar, allow_currency, allow_email, 
                allow_date, allow_url, allow_phoneNumber, allow_ssn, allow_ip,to_gray,banned_words,allowed_words,lang,is_pdf=True,page_number=i,pdf_name=pdf_name)
           constract_pdf(processed_path,page_numbers,pdf_name,to_gray)
           delete_temp()
           label_done = tk.Label(root, text="Done", bg="green", fg=FG_COLOR, font=("Arial", 8, "bold"))
           label_done.place(x=282,y=450)
        else:
            blur_text(selected_file, length, allow_digit, allow_digitWitChar, allow_currency, allow_email, 
          allow_date, allow_url, allow_phoneNumber, allow_ssn, allow_ip,to_gray,banned_words,allowed_words,lang)
            label_done = tk.Label(root, text="Done", bg="green", fg=FG_COLOR, font=("Arial", 8, "bold"))
            label_done.place(x=282,y=450) 

    pass


#selecting a file
def select_file():
    global selected_file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files or PDF", "*.png;*.jpg;*.jpeg;*.pdf"), ("PDF Files", "*.pdf")])
    if file_path:
        selected_file = file_path
        label_file = tk.Label(root, text=f"Selected: {os.path.splitext(os.path.basename(selected_file))[0]}", bg=BTN_COLOR, fg=FG_COLOR, font=("Arial", 8, "bold"))
        label_file.place(x=300, y=210, anchor="center") 
        btn_select = tk.Button(root, text="Blur me", command=blur, width=12,height=4, bg=BTN_COLOR, fg=FG_COLOR, relief="flat")
        btn_select.place(x=300,y=400, anchor="center")
        if label_done:
            label_done.destroy()
            

#settings

config_path = "default.json"
config = load_config(config_path) or {}


def open_settings():
    root.withdraw()  
    settings = tk.Toplevel(root) 
    settings.title("Blurme")
    settings.geometry("600x700")
    icon_path = "ui/blurme.png"
    icon_image = Image.open(icon_path)
    icon_photo = ImageTk.PhotoImage(icon_image)
    settings.iconphoto(False, icon_photo)
    settings.configure(bg=BG_COLOR)  

    # Title Label
    title_label = tk.Label(settings, text="Settings", font=("Arial", 16, "bold"))
    title_label.pack(pady=10)

    # Frame for settings
    top_frame = tk.Frame(settings)
    top_frame.pack(pady=10)

    checkbox_vars = {}
    settings_list = [
        "allow_digit", "allow_digitWitChar", "allow_currency", "allow_email",
        "allow_date", "allow_url", "allow_phoneNumber", "allow_ssn", "allow_ip", "to_gray"
    ]

    # Create checkboxes in a two-column layout
    for i, setting in enumerate(settings_list):
        var = tk.BooleanVar(value=config.get(setting, False))
        checkbox_vars[setting] = var
        chk = tk.Checkbutton(top_frame, text=setting.replace("_", " ").title(), variable=var)
        chk.grid(row=i // 2, column=i % 2, padx=10, pady=5, sticky="w")

    # Banned list Input
    banned_list_label = tk.Label(settings, text="Banned list (comma-separated)")
    banned_list_label.pack(pady=5)
    banned_list_entry = tk.Entry(settings, width=50)
    banned_list_entry.insert(0, ", ".join(config.get("banned_list", [])))
    banned_list_entry.pack(pady=5)

    def clear_banned_list():
        banned_list_entry.delete(0, tk.END)  

    clear_banned_button = tk.Button(settings, text="Clear Banned list", command=clear_banned_list, bg="#f44336", fg="white")
    clear_banned_button.pack(pady=5)

    # Allowed list Input
    allowed_list_label = tk.Label(settings, text="Allowed list (comma-separated)")
    allowed_list_label.pack(pady=5)
    allowed_list_entry = tk.Entry(settings, width=50)
    allowed_list_entry.insert(0, ", ".join(config.get("allowed_list", [])))
    allowed_list_entry.pack(pady=5)

    def clear_allowed_list():
        allowed_list_entry.delete(0, tk.END)  # Clears input field

    clear_allowed_button = tk.Button(settings, text="Clear Allowed list", command=clear_allowed_list, bg="#f44336", fg="white")
    clear_allowed_button.pack(pady=5)

    lang_label = tk.Label(settings, text="Language")
    lang_label.pack(pady=5)
    lang_var = tk.StringVar(value=config.get("lang", "en"))
    lang_entry = tk.Entry(settings, textvariable=lang_var, width=20)
    lang_entry.pack(pady=5)

    def save_settings():
        for setting in settings_list:
            config[setting] = checkbox_vars[setting].get()
        
        config["banned_list"] = [word.strip() for word in banned_list_entry.get().split(",") if word.strip()]
        config["allowed_list"] = [word.strip() for word in allowed_list_entry.get().split(",") if word.strip()]
        config["lang"] = lang_var.get()

        try:
            with open(f"config/{config_path}", "w", encoding="utf-8") as f:
                json.dump(config, f, indent=4)
            print("[INFO] Settings saved successfully.")
        except Exception as e:
            print(f"[ERROR] Failed to save settings: {e}")

    save_button = tk.Button(settings, text="Save", command=save_settings, bg="#4CAF50", fg="white", font=("Arial", 12))
    save_button.pack(pady=10)

    def go_back():
        settings.destroy()  
        root.deiconify()  

    back_button = tk.Button(settings, text="Back", command=go_back, bg="#f44336", fg="white", font=("Arial", 12))
    back_button.pack(pady=10)






root = tk.Tk()
root.title("Blurme")
root.geometry("600x700")
root.configure(bg=BG_COLOR)
icon_path = "ui/blurme.png"
icon_image = Image.open(icon_path)
icon_photo = ImageTk.PhotoImage(icon_image)
root.iconphoto(False, icon_photo)   


#label"slecet"
label_title = tk.Label(root, text="Select an image or a PDF", bg=BTN_COLOR, fg=FG_COLOR, font=("Arial", 19, "bold"))
label_title.place(x=300, y=160, anchor="center") 

#select file
selected_file = None
btn_select = tk.Button(root, text="Select File", command=select_file, width=25,height=4, bg=BTN_COLOR, fg=FG_COLOR, relief="flat")
btn_select.place(x=300,y=300, anchor="center")

#settings
settings_icon = tk.PhotoImage(file="ui/settings.png")  
btn_settings = tk.Button(root, image=settings_icon, bg=BTN_COLOR,command=open_settings, relief="flat", borderwidth=0)
btn_settings.place(x=550, y=10)

root.mainloop()