from PyMuPDF import fitz
import re
from memory_manager import MemoryManager
from uuid import uuid4

memory_store = MemoryManager()

def read_pdf_content(pdf_path):
    """Reads and extracts text content from a PDF file"""
    pdf_document = fitz.open(pdf_path)
    content = ""
    for current_page in pdf_document:
        content += current_page.get_text()
    return content

def analyze_document_type(content):
    """Analyzes document content to determine its category"""
    document_categories = {
        "Invoice": ["invoice", "amount due", "billing", "payment due", "total"],
        "Support Case": ["complaint", "issue", "problem", "not working", "damaged"],
        "Price Request": ["request for quotation", "quote", "pricing"],
        "Compliance Doc": ["compliance", "regulation", "policy", "rule"],
    }
    
    content = content.lower()
    for category, indicators in document_categories.items():
        if any(indicator in content for indicator in indicators):
            return category
    return "Miscellaneous"

def parse_invoice_data(content):
    """Extracts key information from invoice text"""
    patterns = {
        "invoice_id": r"Invoice Number[:\s]*([A-Za-z0-9\-]+)",
        "invoice_date": r"Date[:\s]*([\d/.-]+)",
        "amount": r"Total Amount[:\s]*\$?([\d,.]+)"
    }
    
    extracted_data = {}
    for field, pattern in patterns.items():
        match = re.search(pattern, content, re.IGNORECASE)
        extracted_data[field] = match.group(1) if match else None
    
    return extracted_data

def analyze_document(file_path, origin="system", session_id=None):
    """Main function to process and analyze PDF documents"""
    # Extract text content
    document_text = read_pdf_content(file_path)
    
    # Analyze document
    doc_type = analyze_document_type(document_text)
    parsed_data = parse_invoice_data(document_text)
    
    # Generate session ID if not provided
    session_id = session_id or str(uuid4())
    
    # Identify missing fields
    missing_fields = [field for field, value in parsed_data.items() if value is None]
    
    # Log the processing results
    memory_store.log_entry(
        source=origin,
        fmt="PDF",
        conversation_id=session_id,
        extracted_data={
            "type": doc_type,
            "data": parsed_data,
            "missing": missing_fields,
        },
    )
    
    return {
        "type": doc_type,
        "data": parsed_data,
        "missing": missing_fields,
        "session_id": session_id,
    }
