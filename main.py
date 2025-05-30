import sys
import json
from agents.classifier_agent import classify_input
from agents.pdf_agent import process_pdf
from agents.json_agent import process_json
from agents.email_agent import process_email

def process_content(content_data, content_type=None):
    # Phase 1: Determine content type and purpose
    analysis = classify_input(content_data)
    content_format = analysis.get("format")
    content_purpose = analysis.get("intent")
    print(f"Detected Format: {content_format}")
    print(f"Detected Purpose: {content_purpose}")

    # Phase 2: Handle content based on format
    processed_output = None
    
    if content_format == "PDF":
        processed_output = handle_pdf_content(content_data)
    elif content_format == "JSON":
        processed_output = handle_json_content(content_data)
    elif content_format == "Email":
        processed_output = handle_email_content(content_data)
    else:
        print("Unsupported content format")
        return

    # Phase 3: Display results
    display_processing_results(processed_output)

def handle_pdf_content(file_path):
    return process_pdf(file_path, source="external")

def handle_json_content(data):
    if isinstance(data, str):
        data = json.loads(data)
    return process_json(data)

def handle_email_content(email_text):
    return process_email(email_text)

def display_processing_results(output):
    print("Processing Output:", output)
    print("Session ID:", output.get("conversation_id"))

def cli_handler():
    if len(sys.argv) != 2:
        print("Error: Please provide input file or content")
        print("Usage: python script.py <input_file_or_content>")
        return

    user_input = sys.argv[1]

    if user_input.lower().endswith('.pdf'):
        process_content(user_input)
    else:
        try:
            json_data = json.loads(user_input)
            process_content(json_data)
        except json.JSONDecodeError:
            process_content(user_input)

if __name__ == "__main__":
    cli_handler()
