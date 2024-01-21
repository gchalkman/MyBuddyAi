from docx import Document
import csv
import os

def extract_text_from_docx(docx_path):
    """
    Extract text from a .docx file.
    """
    doc = Document(docx_path)
    texts = [paragraph.text for paragraph in doc.paragraphs if paragraph.text]
    return ' '.join(texts)

def save_to_csv(texts, csv_path):
    """
    Save a list of texts to a CSV file.
    """
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for text in texts:
            writer.writerow([text])

def process_all_docx(folder_path, csv_path):
    """
    Process all .docx files in a folder and save their contents to a single CSV file.
    """
    all_texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.docx'):
            docx_path = os.path.join(folder_path, filename)
            docx_content = extract_text_from_docx(docx_path)
            all_texts.append(docx_content)
    save_to_csv(all_texts, csv_path)

# Specify your .docx folder path and CSV output path
folder_path = 'C:\\Users\\GeorgeChalkiadakis\\OneDrive - k2d properties LTD\\Desktop\\bot\\folderdata'
csv_path = 'C:\\Users\\GeorgeChalkiadakis\\OneDrive - k2d properties LTD\\Desktop\\bot\\docx2csv.csv'

# Process all .docx files and save to a single CSV
process_all_docx(folder_path, csv_path)
