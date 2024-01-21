import PyPDF2
import csv
import os

def extract_text_from_pdf(pdf_path):
    with open(pdf_path, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        text_list = []
        for page_num in range(len(reader.pages)):
            page = reader.pages[page_num]
            text_list.append(page.extract_text())
        return text_list

def save_to_csv(texts, csv_path):
    with open(csv_path, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        for text in texts:
            writer.writerow([text])

def process_all_pdfs(folder_path, csv_path):
    all_texts = []
    for filename in os.listdir(folder_path):
        if filename.endswith('.pdf'):
            pdf_path = os.path.join(folder_path, filename)
            pdf_content = extract_text_from_pdf(pdf_path)
            all_texts.extend(pdf_content)
    save_to_csv(all_texts, csv_path)

# Specify your PDF folder path and CSV output path
folder_path = 'C:\\Users\\GeorgeChalkiadakis\\OneDrive - k2d properties LTD\\Desktop\\bot\\ΠΕΡΙΟΔΙΚΑ ΕΝ ΟΙΚΩ\\'
csv_path = 'C:\\Users\\GeorgeChalkiadakis\\OneDrive - k2d properties LTD\\Desktop\\bot\\exportPDf.csv'

# Process all PDFs and save to a single CSV
process_all_pdfs(folder_path, csv_path)
