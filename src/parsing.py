# src/parsing.py
import re


def extract_rating(response_text):
    """Extract a 1–100 rating from model response."""
    if not response_text:
        return None
    match = re.search(r'Rating:\s*(\d+)', response_text)
    if match:
        val = int(match.group(1))
        if 1 <= val <= 100:
            return val
    return None


def extract_weaknesses(response_text):
    """Extract the weaknesses text from model response."""
    if not response_text:
        return None
    match = re.search(r'Weaknesses:\s*(.+?)(?=Rating:|$)', response_text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return None
