import re
from io import StringIO
import pandas as pd

def validate_csv_input(csv_text: str, max_size_kb: int = 1024) -> bool:
    """Validate CSV input for safety and size."""
    if not csv_text or len(csv_text.strip()) == 0:
        return False
    
    # Size check (1MB = 1024 KB)
    if len(csv_text.encode('utf-8')) > max_size_kb * 1024:
        return False
    
    # Basic CSV structure check (at least one comma)
    if ',' not in csv_text[:100]:
        return False
    
    # Prevent code injection (very basic)
    dangerous_patterns = [r'__import__', r'exec\(', r'eval\(', r'system\(']
    for pattern in dangerous_patterns:
        if re.search(pattern, csv_text, re.IGNORECASE):
            return False
    
    return True

def safe_load_csv(csv_text: str):
    """Safely load CSV with error handling."""
    try:
        df = pd.read_csv(StringIO(csv_text), nrows=1000)  # Limit rows
        return df
    except Exception:
        raise ValueError("Invalid CSV format")
