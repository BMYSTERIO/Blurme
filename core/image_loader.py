import cv2
from PIL import Image
from pdf2image import convert_from_path
from config.config_loader import load_config
from utilities.file_handler import create_dir
import numpy as np
import os
from ui.asni import Colors 

#loading settings
settings = load_config("settings.json")
if settings:
    poppler_path = f"{settings["poppler_path"]}\\Library\\bin"
    tesseract_path = f"{settings["tesseract_path"]}\\tesseract.exe"
    pass


def load_image(image_path, to_gray, resize_factor=1.0):
    try:
        
        image = cv2.imread(image_path)
        
        if image is None:
            raise FileNotFoundError(f"{Colors.RED}[Error]{Colors.RESET} Cannot locate : {image_path}")
        
        if to_gray:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if resize_factor != 1.0:
            width = int(image.shape[1] * resize_factor)
            height = int(image.shape[0] * resize_factor)
            image = cv2.resize(image, (width,height))
        
        return image


    except Exception as e:
        print(f"{Colors.RED}[Error]{Colors.RESET} {e}")
        return None


def save_image(image, path,to_gray = True):
    if image is None:
        print(f"{Colors.RED}[Error]{Colors.RESET} Cannot save: image is None!")
        return False

    if isinstance(image, Image.Image):  
        if to_gray:
            image = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)
        else:
            image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

    if not isinstance(image, np.ndarray):  
        print(f"{Colors.RED}[Error]{Colors.RESET} Cannot save: image is not a NumPy array!")
        return False

    success = cv2.imwrite(path, image)

def extract_pdf_images(pdf_path, to_gray=True, resize_factor=1.0):
    page_numbers = []
    try:
        
        try:
            images = convert_from_path(pdf_path, poppler_path=poppler_path)
        except Exception as e:
            print(f"{Colors.RED}[Error]{Colors.RESET} Download Poppler and put its path in config/settings.json")
            pass
        for i, img in enumerate(images):
            
            image = np.array(img)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if to_gray:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            if resize_factor != 1.0:
                width = int(image.shape[1] * resize_factor)
                height = int(image.shape[0] * resize_factor)
                image = cv2.resize(image, (width, height))
            pdf_name = os.path.splitext(os.path.basename(pdf_path))[0]
            page_number = i+1
            page_numbers.append(page_number)
            temp_path = f"temp/{pdf_name}/unprocessed/page_{page_number}.png"
            try:
                create_dir(f"temp/{pdf_name}/unprocessed/")
            except:
                pass
            save_image(image,temp_path,to_gray)
        return pdf_name,page_numbers

    except Exception as e:
        print(f"{Colors.RED}[Error]{Colors.RESET} {e}")
        return None
    
#path = "input/pdf_test.pdf"
#print(os.path.basename(path.replace(".pdf"," ")))

