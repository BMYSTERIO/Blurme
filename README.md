# BlurMe

**BlurMe** is an open-source application that blurs specific data based on user-defined options, whether it's an image or a long PDF.

## How to Use

1. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
2. **Download Additional Libraries:**
   - Download [Poppler](https://github.com/oschwartz10612/poppler-windows/releases/) and [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).
   - Place them in the `lib` folder with the same names "poppler" , "tesseract" or you can change the dir in settings.json.

3. **Run the Application:**
   - For **Command Line Interface (CLI):**
     ```bash
     python main.py
     ```
     - Select PDF or image.
     - Input the file.
     - Adjust the config or leave it as default.
   
   - For **Graphical User Interface (GUI):**
     ```bash
     python main_gui.py
     ```

## About

**BlurMe** is made by **MYST** and is completely free to use.

