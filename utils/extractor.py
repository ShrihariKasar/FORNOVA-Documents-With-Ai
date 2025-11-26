import pdfplumber, docx2txt, pytesseract, re
from PIL import Image
from transformers import pipeline
import spacy

nlp = spacy.load("en_core_web_sm")
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def extract_text(file_path):
    if file_path.endswith('.pdf'):
        with pdfplumber.open(file_path) as pdf:
            return " ".join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file_path.endswith('.docx'):
        return docx2txt.process(file_path)
    elif file_path.endswith(('.jpg', '.jpeg', '.png')):
        return pytesseract.image_to_string(Image.open(file_path))
    return ""
def extract_resume_fields(text):
    data = {}
    data['name'] = re.search(r'([A-Z][a-z]+ [A-Z][a-z]+)', text)
    data['email'] = re.search(r'[\w\.-]+@[\w\.-]+', text)
    data['phone'] = re.search(r'\+?\d[\d\s-]{8,}\d', text)
    data['skills'] = [token.text for token in nlp(text).ents if token.label_ in ['ORG', 'SKILL']]
    data['summary'] = summarizer(text[:1000], max_length=100, min_length=30, do_sample=False)[0]['summary_text']
    return {k: (v.group(0) if hasattr(v, "group") else v) for k, v in data.items()}


def process_document(file_path):
    text = extract_text(file_path)
    return extract_resume_fields(text)