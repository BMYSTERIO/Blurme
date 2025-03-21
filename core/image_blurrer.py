import re
import cv2
import numpy as np
import pytesseract
from core.image_loader import load_image
from utilities.file_handler import create_dir
from core.text_extractor import extract_text
from config.config_loader import load_config
from ui.asni import Colors



#loading settings
settings = load_config("settings.json")
if settings:
    poppler_path = f"{settings["poppler_path"]}\\Library\\bin"
    tesseract_path = f"{settings["tesseract_path"]}\\tesseract.exe"
    pass



def contains_digits_and_letters(word):
    return bool(re.search(r"\d", word)) and bool(re.search(r"[a-zA-Z]", word))

def is_currency(text):
    pattern = r"""
        \b(
            (?:[\$€£¥₹₽₩₨])?\d{1,3}(?:,\d{3})*(?:\.\d{2})?\s?(?:USD|EUR|GBP|JPY|INR|RUB|KRW|PKR)?
            | (?:USD|EUR|GBP|JPY|INR|RUB|KRW|PKR)?\s?(?:[\$€£¥₹₽₩₨])?\d{1,3}(?:,\d{3})*(?:\.\d{2})?
        )\b
    """
    return bool(re.search(pattern, text, re.IGNORECASE | re.VERBOSE))

def is_email(word):
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    return bool(re.search(pattern, word))


def is_date(text):
    pattern = r"""
        \b(
            (?:\d{2}[-/]\d{2}[-/]\d{4})
            | (?:\d{4}[-/]\d{2}[-/]\d{2})
            | (?:\d{1,2}[-/]\d{1,2}[-/]\d{2})
            | (?:\d{1,2}[st|nd|rd|th]? \s+ (?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \s+ \d{4})
            | (?:(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]* \s+ \d{1,2},?\s+ \d{4})
            | (?:\d{1,2} \s+ (?:January|February|March|April|May|June|July|August|September|October|November|December) \s+ \d{4})
        )\b
    """
    return bool(re.search(pattern, text, re.IGNORECASE | re.VERBOSE))


import re

def is_url(text):
    pattern = r"""
        \b(
            (?:https?|ftp):\/\/
            (?:[\w-]+\.)*
            [a-zA-Z0-9-]+
            \.[a-zA-Z]{2,}
            (?:\:\d{2,5})?
            (?:\/[^\s]*)?
            (?:\?[^\s]*)?
            (?:[^\s]*)?
        )\b
    """
    return bool(re.search(pattern, text, re.IGNORECASE | re.VERBOSE))

def is_phone_number(word):
    pattern = r"""
    (?:(?:\+?\d{1,3}[\s.-]?)?       
    (?:\(?\d{1,4}\)?[\s.-]?)?       
    \d{3,4}[\s.-]?\d{3,4})          
    """
    return bool(re.search(pattern, word, re.VERBOSE))


def is_ssn(word):
    pattern = r"\b\d{3}[-,.]?\d{2}[-,.]?\d{4}\b"
    return bool(re.search(pattern, word))

def is_ip(word):
    pattern = r"^(?:\d{1,3}\.){3}\d{1,3}[,.]?$"
    return bool(re.match(pattern, word))


#args (digit , digitwitchar , currency , email , date , url , phonenubmer , ssn , ip)
def blur_text(image_path, length=8,allow_digit=True,allow_digitWitChar=True,allow_currency= False,allow_email=False,allow_date=False,allow_url=False,allow_phoneNumber=False,allow_ssn = True,allow_ip = True,to_gray=True,banned_words = [],allowed_words=[], lang="eng",is_pdf = False,pdf_name = None,page_number = None, psm=6, oem=3, blur_intensity=99):
    try:
        image = load_image(image_path, to_gray)
        if image is None:
            raise ValueError(f"{Colors.RED}[Error]{Colors.RESET} Unable to load image.")

        extracted_text = extract_text(image_path, to_gray, lang, psm, oem)
        
        d = pytesseract.image_to_data(image, lang=lang, config=f"--psm {psm} --oem {oem}", output_type=pytesseract.Output.DICT)
        num_boxes = len(d["text"])
        blured_count = 0
        for i, word in enumerate(d["text"]):
            word = word.strip()
            x, y, w, h = d["left"][i], d["top"][i], d["width"][i], d["height"][i]

            if allow_digit and word.isdigit() and len(word) >= length and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            if allow_digitWitChar and contains_digits_and_letters(word) and len(word) >= length and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            if allow_currency and is_currency(word) and len(word) >= length and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            if allow_email and is_email(word) and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            if allow_date and is_date(word) and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            if allow_url and is_url(word) and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            if allow_phoneNumber and is_phone_number(word) and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            if allow_ssn and is_ssn(word) and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            if allow_ip and is_ip(word) and word not in allowed_words:
                roi = image[y:y+h, x:x+w]
                blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                image[y:y+h, x:x+w] = blurred_roi
                blured_count += 1

            for banned in banned_words:
                if re.search(r"\b" + re.escape(banned) + r"\b", word, re.IGNORECASE):
                    
                    x, y, w, h = d["left"][i], d["top"][i], d["width"][i], d["height"][i]
                    roi = image[y:y+h, x:x+w]
                    blurred_roi = cv2.GaussianBlur(roi, (blur_intensity, blur_intensity), 0)
                    image[y:y+h, x:x+w] = blurred_roi 
                    blured_count += 1




        # saving
        import os
        if is_pdf:
            image_name = os.path.splitext(os.path.basename(image_path))[0]
            output_path = f"temp/{pdf_name}/processed/page_{page_number}.png"
            try:
                create_dir(f"temp/{pdf_name}/processed/")
            except:
                pass
            cv2.imwrite(output_path, image)
            return blured_count    
            
        image_name = os.path.splitext(os.path.basename(image_path))[0]
        output_path = f"output/{image_name}.png"
        cv2.imwrite(output_path, image)
        print(f"{Colors.GREEN}[Success]{Colors.RESET} Blurred {Colors.YELLOW}{blured_count}{Colors.RESET} element in {output_path}")

        return output_path
    except Exception as e:
        print(f"{Colors.RED}[Error]{Colors.RESET} {e}")
        return None