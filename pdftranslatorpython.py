import threading
import pdfplumber
from deep_translator import GoogleTranslator
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import time

class PDFTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Translator and Audio Converter")

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20)

        self.file_label = tk.Label(self.frame, text="Select PDF File:")
        self.file_label.grid(row=0, column=0, sticky="w")

        self.file_entry = tk.Entry(self.frame, width=40)
        self.file_entry.grid(row=0, column=1, padx=5, pady=5)

        self.browse_button = tk.Button(self.frame, text="Browse", command=self.browse_file)
        self.browse_button.grid(row=0, column=2, padx=5, pady=5)

        self.language_label = tk.Label(self.frame, text="Select Target Language:")
        self.language_label.grid(row=1, column=0, sticky="w")

        self.languages = ["en", "fr", "de", "es", "it", "zh-CN", "ja"]
        self.language_var = tk.StringVar()
        self.language_dropdown = ttk.Combobox(self.frame, textvariable=self.language_var, values=self.languages)
        self.language_dropdown.current(0)
        self.language_dropdown.grid(row=1, column=1, padx=5, pady=5)

        self.translate_button = tk.Button(self.frame, text="Translate and Convert", command=self.translate_and_convert)
        self.translate_button.grid(row=2, columnspan=3, padx=5, pady=5)

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
        self.file_entry.delete(0, tk.END)
        self.file_entry.insert(0, file_path)

    def translate_and_convert(self):
        file_path = self.file_entry.get()
        if not file_path:
            messagebox.showerror("Error", "Please select a PDF file.")
            return

        target_language = self.language_var.get()
        if not target_language:
            messagebox.showerror("Error", "Please select a target language.")
            return

        threading.Thread(target=self.process_pdf_translation, args=(file_path, target_language)).start()

    def process_pdf_translation(self, file_path, target_language):
        try:
            self.translate_button.config(state="disabled")
            self.root.config(cursor="wait")

            pdf_text = self.extract_text_from_pdf(file_path)
            if not pdf_text:
                messagebox.showerror("Error", "No text found in PDF.")
                return

            print("Extracted text from PDF:", pdf_text)  # Debug print statement

            translated_text = self.translate_text(pdf_text, target_language)
            if not translated_text:
                messagebox.showerror("Error", "Translation failed.")
                return

            print("Translated text:", translated_text)  # Debug print statement

            audio_file = self.text_to_audio(translated_text, target_language)
            if not audio_file:
                messagebox.showerror("Error", "Audio conversion failed.")
                return

            messagebox.showinfo("Success", "Translation and audio conversion complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.translate_button.config(state="normal")
            self.root.config(cursor="")

    def extract_text_from_pdf(self, file_path):
        text = ""
        try:
            with pdfplumber.open(file_path) as pdf:
                for page in pdf.pages:
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text + "\n"
        except Exception as e:
            messagebox.showerror("Error", f"Failed to extract text from PDF: {str(e)}")
        return text

    def translate_text(self, text, target_language):
        try:
            translator = GoogleTranslator(source='auto', target=target_language)
            translation = translator.translate(text)
            return translation
        except Exception as e:
            messagebox.showerror("Error", f"Failed to translate text: {str(e)}")
            return None

    def text_to_audio(self, text, target_language):
        try:
            tts = gTTS(text, lang=target_language.lower())
            output_file = "output.mp3"
            tts.save(output_file)
            return output_file
        except Exception as e:
            messagebox.showerror("Error", f"Failed to convert text to audio: {str(e)}")
            return None

def main():
    root = tk.Tk()
    app = PDFTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
