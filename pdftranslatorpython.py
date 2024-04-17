import threading
import PyPDF2
from googletrans import Translator
from gtts import gTTS
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from pdfreader import SimplePDFViewer

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

        self.languages = ["English", "French", "German", "Spanish", "Italian", "Chinese", "Japanese"]
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
            translated_text = self.translate_text(pdf_text, target_language)
            audio_file = self.text_to_audio(translated_text, target_language)

            messagebox.showinfo("Success", "Translation and audio conversion complete!")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.translate_button.config(state="normal")
            self.root.config(cursor="")

    def extract_text_from_pdf(self, file_path):
        text = ""
        with open(file_path, "rb") as file:
            pdf_viewer = SimplePDFViewer(file)
            pdf_document = pdf_viewer.get_document()
            num_pages = pdf_document.get_num_pages()
            for page in range(num_pages):
                pdf_viewer.current_page = page
                text += pdf_viewer.render()
        return text

    def translate_text(self, text, target_language):
        translator = Translator()
        translation = translator.translate(text, dest=target_language.lower())
        return translation.text

    def text_to_audio(self, text, target_language):
        tts = gTTS(text, lang=target_language.lower())
        output_file = "output.mp3"
        tts.save(output_file)
        return output_file

def main():
    root = tk.Tk()
    app = PDFTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()