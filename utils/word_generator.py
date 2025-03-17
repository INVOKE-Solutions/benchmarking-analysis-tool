import tempfile
from docx import Document

def generate_word(content):
    """Generate a Word document from text content"""
    doc = Document()
    doc.add_paragraph(content)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".docx")
    doc.save(temp_file.name)
    return temp_file.name