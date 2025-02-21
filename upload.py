import os
import tkinter as tk
from tkinter import filedialog
import PyPDF2
import re
from docx import Document

def process_text_into_chunks(text, max_chunk_size=400):
    """Split text into chunks of maximum size while preserving sentences."""
    text = re.sub(r'\s+', ' ', text).strip()
    sentences = re.split(r'(?<=[.!?]) +', text)
    
    chunks = []
    current_chunk = ""
    
    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 1 < max_chunk_size:
            current_chunk += (sentence + " ").strip()
        else:
            chunks.append(current_chunk)
            current_chunk = sentence + " "
            
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

def save_chunks_to_vault(chunks):
    """Save processed chunks to vault.txt file."""
    with open("vault.txt", "a", encoding="utf-8") as vault_file:
        for chunk in chunks:
            vault_file.write(chunk.strip() + "\n")

def extract_pdf_text(file_path):
    """Extract text from PDF file."""
    text = ""
    with open(file_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)
        for page in pdf_reader.pages:
            if page.extract_text():
                text += page.extract_text() + " "
    return text

def extract_docx_text(file_path):
    """Extract text from DOCX file."""
    doc = Document(file_path)
    return "\n".join([para.text for para in doc.paragraphs])

def convert_pdf_to_text():
    """GUI handler for PDF upload."""
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    if file_path:
        text = extract_pdf_text(file_path)
        chunks = process_text_into_chunks(text)
        save_chunks_to_vault(chunks)
        print("PDF content appended to vault.txt with each chunk on a separate line.")

def upload_docxfile():
    """GUI handler for DOCX upload."""
    file_path = filedialog.askopenfilename(filetypes=[("Word Files", "*.docx")])
    if file_path:
        text = extract_docx_text(file_path)
        chunks = process_text_into_chunks(text)
        save_chunks_to_vault(chunks)
        print("Word file content appended to vault.txt with each chunk on a separate line.")

def upload_txtfile():
    """GUI handler for TXT upload."""
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        chunks = process_text_into_chunks(text)
        save_chunks_to_vault(chunks)
        print("Text file content appended to vault.txt with each chunk on a separate line.")

def upload_jsonfile():
    """GUI handler for JSON upload."""
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        chunks = process_text_into_chunks(text)
        save_chunks_to_vault(chunks)
        print("JSON file content appended to vault.txt with each chunk on a separate line.")

# Create the main window
root = tk.Tk()
root.title("Upload .pdf, .txt, or .json")

# Create buttons for each file type
pdf_button = tk.Button(root, text="Upload PDF", command=convert_pdf_to_text)
pdf_button.pack(pady=10)

txt_button = tk.Button(root, text="Upload Text File", command=upload_txtfile)
txt_button.pack(pady=10)

docx_button = tk.Button(root, text="Upload docx File", command=upload_docxfile)
docx_button.pack(pady=10)

json_button = tk.Button(root, text="Upload JSON File", command=upload_jsonfile)
json_button.pack(pady=10)

# Run the main event loop
root.mainloop()