import cv2
from PIL import Image
import numpy as np
import os
from core.image_loader import load_image
from core.text_extractor import extract_text
from core.image_blurrer import blur_text
from core.image_loader import extract_pdf_images
from utilities.file_handler import constract_pdf
from utilities.file_handler import delete_temp
from utilities.file_handler import create_dir
from config.config_loader import load_config
from ui.asni import Colors

delete_temp()
ascii_art = r"""
,--.   ,--.                                 
|  |-. |  |,--.,--.,--.--.,--,--,--. ,---.  
| .-. '|  ||  ||  ||  .--'|        || .-. : 
| `-' ||  |'  ''  '|  |   |  |  |  |\   --. 
 `---' `--' `----' `--'   `--`--`--' `----' 
"""

tesseract_path = os.path.join(os.getcwd(), "lib", "tesseract", "tesseract.exe")
if not os.path.exists(tesseract_path):
    print(f"{Colors.RED}[Error]{Colors.RESET} Download Tesseract OCR and place it in 'lib/tesseract' with the name 'tesseract.exe")
    input("Press Enter...")
    exit(1)
    
def clear():
    if os.name == 'nt':
            os.system('cls')
            print(f"{Colors.CYAN}{ascii_art}{Colors.RESET}")

clear()
while(True):
    print(f"{Colors.BLUE}[1]{Colors.RESET} Blur a image")
    print(f"{Colors.BLUE}[2]{Colors.RESET} Blur a pdf")
    choice = input("> ")
    if choice == "1":
        image_path = input("Enter image path: ")
        config_path = input("Enter config file (Empty for default): ") or "default.json"
        config = load_config(config_path)
        
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

        blur_text(image_path, length, allow_digit, allow_digitWitChar, allow_currency, allow_email, 
          allow_date, allow_url, allow_phoneNumber, allow_ssn, allow_ip,to_gray,banned_words,allowed_words,lang)
        input("> Press Enter...")
        clear()
    elif choice == "2":
         pdf_path = input("Enter pdf path: ")
         config_path = input("Enter config file (Empty for default): ") or "default.json"
         config = load_config(config_path)
        
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

             soild_banned_words = config.get("banned_list", []) 
             banned_words = []
             for word in soild_banned_words:
                banned_words.extend(word.split())

             soild_allowed_words = config.get("allowed_list", [])
             allowed_words = []
             for word in soild_allowed_words:
                allowed_words.extend(word.split())

             lang = config.get("lang")
         
    
         pdf_name , page_numbers = extract_pdf_images("input/pdf_test.pdf")
         processed_path = f"temp/{pdf_name}/processed/"
         unprocessed_path = f"temp/{pdf_name}/unprocessed/"
         blured_count = 0
         for i in page_numbers:
           blured_count += blur_text(f"{unprocessed_path}/page_{i}.png", length, allow_digit, allow_digitWitChar, allow_currency, allow_email, 
          allow_date, allow_url, allow_phoneNumber, allow_ssn, allow_ip,to_gray,banned_words,allowed_words,lang,is_pdf=True,page_number=i,pdf_name=pdf_name)
         
         print(f"{Colors.GREEN}[Success]{Colors.RESET} Blurred {Colors.YELLOW}{blured_count}{Colors.RESET} element in {Colors.YELLOW}{pdf_name}.pdf{Colors.RESET}")
         constract_pdf(processed_path,page_numbers,pdf_name,to_gray)
         delete_temp()
         input("Press Enter...")
         clear()
         
    else:
        print(f"{Colors.RED}[Error]{Colors.RESET} Unkown input!")
        clear()
#blurred_image = blur_text(image_path)


