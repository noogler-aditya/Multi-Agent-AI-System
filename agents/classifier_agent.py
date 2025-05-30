import json
from utils.llm_utils import call_gemini  # Changed to use Gemini
from agents.pdf_agent import extract_text_from_pdf
import os
import uuid

def detect_format(input_data):
    """
    Detect the format of the input data.
    Returns one of: PDF, JSON, Email, Text, Unknown
    """
    # Format detection logic remains the same
    if isinstance(input_data, dict):
        return "JSON"
    elif isinstance(input_data, str):
        if "From:" in input_data and "Subject:" in input_data:
            return "Email"
        elif input_data.lower().endswith(".pdf"):
            return "PDF"
        else:
            return "Text"
    elif isinstance(input_data, bytes):
        return "PDF"
    else:
        return "Unknown"

def detect_intent(text):
    """
    Use Gemini 1.5 Flash to determine the intent of the content.
    Returns one of: Invoice, RFQ, Complaint, Regulation, Other
    """
    prompt = f"""Classify the following text into exactly one of these categories: Invoice, RFQ, Complaint, Regulation, Other.
    Respond only with the category name.
    
    Text: {text[:1000]}"""
    
    try:
        intent = call_gemini(prompt).strip()
        # Validate the response is one of the expected categories
        valid_intents = {"Invoice", "RFQ", "Complaint", "Regulation", "Other"}
        return intent if intent in valid_intents else "Other"
    except Exception as e:
        print("Intent detection failed:", e)
        return "Other"

def classify(input_data):
    """
    Main classification function.
    Returns a dictionary with detected format and intent.
    """
    fmt = detect_format(input_data)
    intent_text = json.dumps(input_data) if fmt == "JSON" else str(input_data)
    intent = detect_intent(intent_text)
    
    return {
        "format": fmt,
        "intent": intent
    }

def classify_input(input_data):
    """
    Unified classification function using Gemini 1.5 Flash
    """
    # Format detection
    if isinstance(input_data, str):
        if os.path.exists(input_data) and input_data.lower().endswith(".pdf"):
            detected_format = "PDF"
            text = extract_text_from_pdf(input_data)
        elif input_data.strip().startswith("{"):
            detected_format = "JSON"
            text = input_data
        else:
            detected_format = "Email"
            text = input_data
    elif isinstance(input_data, dict):
        detected_format = "JSON"
        text = str(input_data)
    else:
        detected_format = "Unknown"
        text = ""

    # Intent detection using Gemini
    prompt = f"""Classify the intent of this message into one specific category:
    Text: {text}
    Return only the category name."""
    
    intent = call_gemini(prompt).strip()
    
    return {"format": detected_format, "intent": intent}
