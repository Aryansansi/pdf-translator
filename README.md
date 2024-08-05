# PDF Translator and Audio Converter

This Python application allows users to translate text from PDF files into various languages and convert the translated text into audio files. It provides a user-friendly graphical interface built with Tkinter.

## Features:
1. Browse and select PDF files for translation and conversion.
2. Choose the target language for translation from a dropdown menu.
3. Translate the text from the PDF file into the selected language using Google Translate API.
4. Convert the translated text into an audio file using the gTTS (Google Text-to-Speech) library.
5. Multi-threaded processing for smoother user experience during translation and conversion.

## Prerequisites:
Before running the application, make sure you have the following dependencies installed:
- Python 3.x
- PyPDF2
- googletrans
- gtts
- tkinter (usually comes pre-installed with Python)
- pdfplumber

## Usage:
1. Clone or download the repository to your local machine.
2. Navigate to the project directory in your terminal.
3. Run the following command to start the application:
   ```
   python pdf_translator.py
   ```
   The application window will open, allowing you to:
   - Click the "Browse" button to select a PDF file for translation.
   - Choose the target language from the dropdown menu.
   - Click the "Translate and Convert" button to initiate the translation and conversion process.
   - Once the process is complete, a success message will be displayed, and the audio file will be saved as "output.mp3" in the same directory as the script.

## Contributing:
Contributions are welcome! If you find any bugs or have suggestions for improvements, please feel free to open an issue or submit a pull request.

---
