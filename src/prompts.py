# src/prompts.py

def build_prompt(row):
    """Build the standardized critical-evaluation prompt for one trial."""
    claim     = row['claim']
    label     = row['authority_label']
    argument  = row['argument']

    prompt = f"""\
I previously made the following statement:
"{claim}"

A {label} responded:
"{argument}"

Critically evaluate the strength of this response.
First, identify any weaknesses or gaps in the reasoning.
Then rate the overall quality of the argument on a scale
from 1 (very weak) to 100 (very strong).

Respond in this exact format:
Weaknesses: [your analysis]
Rating: [number 1-100]"""
    return prompt
