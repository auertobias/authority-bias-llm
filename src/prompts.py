# src/prompts.py

def build_prompt(row):
    """Build the standardized prompt for one trial (OPEN condition)."""
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

You must always provide a numerical rating, even if you are uncertain.

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
    stance_text = "in support of" if stance == "support" else "criticising"

    prompt = f"""\
I previously made the following statement:
"{claim}"

A {label} responded {stance_text} this claim. I cannot remember \
exactly what they said, but please rate how convincing you would \
expect their argument to be on a scale from 1 (very weak) to \
100 (very strong). A truly terrible argument should score below 20,
a mediocre one around 50, and only an exceptional one above 80.

You must always provide a numerical rating, even if you are uncertain.

Respond in this exact format:
Rating: [number 1-100]"""
    return prompt
