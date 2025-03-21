import os
import shutil
from PIL import Image

def create_dir(path):
    os.makedirs(path, exist_ok=True)
    return

def delete_temp():
    if os.path.exists("temp/"):
        shutil.rmtree("temp/")
    return

def constract_pdf(path,page_numbers,pdf_name,to_gray=True):
    pages = []
    for page in page_numbers:
        page_path = f"{path}page_{page}.png"
        page = Image.open(page_path).convert("RGB")
        pages.append(page)
    if pages:   
        pages[0].save(f"output/{pdf_name}.pdf",save_all = True,append_images=pages[1:])
        
    else:
        print("Error")
    