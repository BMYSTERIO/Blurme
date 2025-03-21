import cv2
import pytesseract
import argparse
import os
from PIL import Image
from config.config_loader import load_config
from core.image_loader import load_image
from ui.asni import Colors




#loading settings
settings = load_config("settings.json")
if settings:
    poppler_path = f"{settings["poppler_path"]}\\Library\\bin"
    tesseract_path = f"{settings["tesseract_path"]}\\tesseract.exe"
    pass

pytesseract.pytesseract.tesseract_cmd = tesseract_path

def extract_text(image_path,to_gray,lang="eng",psm=6,oem=3):
    try:
        image = load_image(image_path,to_gray)

        if image is None:
            raise ValueError(f"{Colors.RED}[Error]{Colors.RESET} Unable to process image.")

        custom_config = f"--psm {psm} --oem {oem}"
        extracted_text = pytesseract.image_to_string(image, lang=lang, config=custom_config)
        return extracted_text.strip()
    except Exception as e:
        print(f"{Colors.RED}[Error]{Colors.RESET} {e}")
        return None
