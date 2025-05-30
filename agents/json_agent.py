from memory_manager import MemoryManager
from uuid import uuid4

memory_handler = MemoryManager()

# Schema definition for order validation
ORDER_FIELDS = {
    "vendor": str,
    "product_id": str,
    "quantity": int,
    "price_per_unit": float,
    "delivery_date": str,
}

def check_data_validity(order_data):
    """Validates and formats order data against defined schema"""
    issues = []
    processed_data = {}

    for key, expected_type in ORDER_FIELDS.items():
        current_value = order_data.get(key)
        
        if current_value is None:
            issues.append(f"Required field missing: {key}")
            processed_data[key] = None
            continue
            
        if not isinstance(current_value, expected_type):
            issues.append(f"Type mismatch for {key}: Need {expected_type.__name__}, received {type(current_value).__name__}")
            processed_data[key] = current_value
        else:
            processed_data[key] = current_value

    return processed_data, issues

def handle_order_data(order_data, data_source="unspecified", session_id=None):
    """Process and log order data with validation"""
    processed_data, issues = check_data_validity(order_data)

    if not session_id:
        session_id = str(uuid4())

    memory_handler.log_entry(
        source=data_source,
        fmt="JSON",
        conversation_id=session_id,
        extracted_data={
            "processed_order": processed_data,
            "validation_issues": issues,
        }
    )

    return {
        "processed_order": processed_data,
        "validation_issues": issues,
        "session_id": session_id,
    }
