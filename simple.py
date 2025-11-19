import pdfplumber
from transformers import pipeline

# Load pre-trained QA model
qa_model = pipeline('question-answering')

def process_pdf(file_path):
    with pdfplumber.open(file_path) as pdf:
        text = " ".join(page.extract_text() for page in pdf.pages)
    return text

def get_answer(query, document):
    result = qa_model(question=query, context=document)
    return result['answer']

# Example usage
pdf_file_path = 'C:\\MM\\rag2windows-whats-new (1).pdf'
query = 'Your question related to the PDF'

# Extract text from the PDF
document_text = process_pdf(pdf_file_path)

# Try to get an answer based on the query
if document_text:
    print(f"Document text: {document_text[:500]}...")  # Print only a part of the document text for brevity
    answer = get_answer(query, document_text)
    print(f"Answer: {answer}")
else:
    print("PDF file is empty or could not be processed.")
