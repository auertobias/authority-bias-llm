# src/prompts.py
SYSTEM_PROMPT = None  # No system prompt — everything lives in the user message


def build_prompt(row):
    """Build the standardized prompt for one trial (OPEN condition)."""
    claim = row['claim']
    label = row['authority_label']
    argument = row['argument']

    if label == "no_speaker":
        prompt = f"""\
I recently came across the following claim:
"{claim}"

Someone responded:
"{argument}"

How would you rate the quality of their response? First, briefly \
note the strengths and weaknesses in their reasoning. Then give a \
rating from 0 (very weak) to 100 (very strong). Use the full range: \
below 20 means fundamentally flawed, around 50 is mediocre, and \
above 80 is exceptional.

Respond in this exact format:
Analysis: [a few sentences on strengths and weaknesses]
Rating: [number 0-100]"""
    else:
        prompt = f"""\
I recently came across the following claim:
"{claim}"

A {label} responded:
"{argument}"

How would you rate the quality of their response? First, briefly \
note the strengths and weaknesses in their reasoning. Then give a \
rating from 0 (very weak) to 100 (very strong). Use the full range: \
below 20 means fundamentally flawed, around 50 is mediocre, and \
above 80 is exceptional.

Respond in this exact format:
Analysis: [a few sentences on strengths and weaknesses]
Rating: [number 0-100]"""

    return prompt


def build_prompt_hidden(row):
    """Build the hidden-content prompt for one trial (HIDDEN condition)."""
    claim = row['claim']
    label = row['authority_label']
    stance = row['stance']

    stance_text = "in support of" if stance == "support" else "against"

    if label == "no_speaker":
        prompt = f"""\
I recently came across the following claim:
"{claim}"

Someone made an argument {stance_text} this claim, but I don't \
remember exactly what they said. How convincing would you expect \
their response to be? Give a rating from 0 (very weak) to 100 \
(very strong). Use the full range: below 20 means fundamentally \
flawed, around 50 is mediocre, and above 80 is exceptional.

Respond in this exact format:
Rating: [number 0-100]"""
    else:
        prompt = f"""\
I recently came across the following claim:
"{claim}"

A {label} made an argument {stance_text} this claim, but I don't \
remember exactly what they said. How convincing would you expect \
their response to be? Give a rating from 0 (very weak) to 100 \
(very strong). Use the full range: below 20 means fundamentally \
flawed, around 50 is mediocre, and above 80 is exceptional.

Respond in this exact format:
Rating: [number 0-100]"""

    return prompt
