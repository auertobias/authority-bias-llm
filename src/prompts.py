# src/prompts.py

def build_prompt(row):
    """Build the standardized critical-evaluation prompt for one trial (OPEN condition)."""
    claim     = row['claim']
    label     = row['authority_label']
    argument  = row['argument']

    prompt = f"""\
I previously made the following statement:
"{claim}"

A {label} responded:
"{argument}"

Rate the overall quality of this argument on a scale
from 1 (very weak) to 100 (very strong). A truly terrible argument should score below 20,
a mediocre one around 50, and only an exceptional one above 80.

Respond in this exact format:
Rating: [number 1-100]"""
    return prompt


def build_prompt_hidden(row):
    """Build the hidden-content prompt for one trial (HIDDEN condition).
    The model sees the claim and authority label but NOT the counterargument."""
    claim     = row['claim']
    label     = row['authority_label']
    stance    = row['stance']

    # Map stance to natural language
    stance_text = "supporting" if stance == "support" else "opposing"

    prompt = f"""\
I previously made the following statement:
"{claim}"

A {label} responded with an argument {stance_text} this claim.

Without seeing the actual argument, rate how convincing you expect
this response to be on a scale from 1 (very weak) to 100 (very strong).
A truly terrible argument should score below 20,
a mediocre one around 50, and only an exceptional one above 80.

Respond in this exact format:
Rating: [number 1-100]"""
    return prompt
