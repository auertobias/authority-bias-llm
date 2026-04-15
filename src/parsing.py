# src/parsing.py
import re


def extract_rating(response_text):
    """Extract a 0–100 rating from model response."""
    if not response_text:
        return None
    match = re.search(r'Rating:\s*(\d+)', response_text)
    if match:
        val = int(match.group(1))
        if 0 <= val <= 100:
            return val
    return None


def extract_analysis(response_text):
    """Extract the Analysis text from model response (open condition only)."""
    if not response_text:
        return None
    match = re.search(r'Analysis:\s*(.+?)(?=Rating:|$)', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # Fallback: everything before Rating: line
    match = re.search(r'^(.*?)(?=Rating:\s*\d+)', response_text, re.DOTALL)
    if match:
        return match.group(1).strip() or None
    return None
