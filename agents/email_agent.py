from memory_manager import MemoryManager
from uuid import uuid4
import re

memory_mgr = MemoryManager()

def find_email_address(text):
    # Find and extract email addresses from the text content
    email_pattern = r'[\w\.-]+@[\w\.-]+' 
    found_emails = re.findall(email_pattern, text)
    return found_emails[0] if found_emails else "sender_unknown"

def assess_priority(text):
    # Determine message priority based on content analysis
    priority_indicators = {
        "high": ["urgent", "critical", "immediate", "crucial", "emergency"],
        "low": ["flexible", "when possible", "at your convenience", "not pressing"],
    }
    
    text = text.lower()
    for priority_level, indicators in priority_indicators.items():
        if any(indicator in text for indicator in indicators):
            return priority_level.title()
    return "Standard"

def analyze_message_type(text):
    # Categorize message based on content analysis
    message_categories = {
        "Price Request": ["price", "quote", "cost estimate", "rates"],
        "Support Case": ["help needed", "not working", "malfunction", "broken"],
        "Billing Query": ["payment", "invoice", "billing", "charge"],
        "Compliance": ["legal", "requirement", "standard", "protocol"],
    }
    
    text = text.lower()
    for category, indicators in message_categories.items():
        if any(indicator in text for indicator in indicators):
            return category
    return "Misc"

def analyze_email(message_text, origin="system_default", thread_id=None):
    email_address = find_email_address(message_text)
    priority_level = assess_priority(message_text)
    message_type = analyze_message_type(message_text)

    if not thread_id:
        thread_id = str(uuid4())

    analysis_results = {
        "from": email_address,
        "priority": priority_level,
        "category": message_type,
    }

    memory_mgr.log_entry(
        source=origin,
        fmt="Email",
        conversation_id=thread_id,
        extracted_data=analysis_results,
    )

    analysis_results["thread_id"] = thread_id
    return analysis_results
