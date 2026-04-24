# src/models.py
from src.config import TEMPERATURE, MAX_TOKENS


def make_gemini_fn(api_key, model_name='gemini-2.5-flash'):
    """Create a Gemini caller. Returns a function: prompt → response text."""
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=api_key)

    def run(prompt):
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=TEMPERATURE,
                    max_output_tokens=MAX_TOKENS,
                )
            )
            return response.text
        except Exception as e:
            print(f"  Gemini error: {e}")
            return None
    return run


def make_gpt_fn(api_key, model_name='gpt-5.4-nano'):
    import openai
    client = openai.OpenAI(api_key=api_key)

    is_gpt5 = model_name.startswith('gpt-5')

    def run(prompt):
        try:
            kwargs = {
                "model": model_name,
                "messages": [{"role": "user", "content": prompt}],
            }
            if is_gpt5:
                kwargs["max_completion_tokens"] = MAX_TOKENS
                # temperature omitted — gpt-5 models only accept default (1.0)
            else:
                kwargs["max_tokens"] = MAX_TOKENS
                kwargs["temperature"] = TEMPERATURE

            response = client.chat.completions.create(**kwargs)
            return response.choices[0].message.content
        except Exception as e:
            print(f"  GPT error: {e}")
            return None
    return run


def make_claude_fn(api_key, model_name='claude-haiku-4-5-20251001'):
    """Create a Claude caller. Returns a function: prompt → response text."""
    import anthropic
    client = anthropic.Anthropic(api_key=api_key)

    def run(prompt):
        try:
            message = client.messages.create(
                model=model_name,
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
                messages=[{"role": "user", "content": prompt}],
            )
            return message.content[0].text
        except Exception as e:
            print(f"  Claude error: {e}")
            return None
    return run

def make_deepseek_fn(api_key, model_name='deepseek-chat'):
    from openai import OpenAI
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
    def run(prompt):
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=TEMPERATURE,
                max_tokens=MAX_TOKENS,
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"  DeepSeek error: {e}")
            return None
    return run

def make_llama_fn(api_key: str, model_name: str = "meta-llama/Llama-3.3-70B-Instruct-Turbo"):
    from openai import OpenAI
    client = OpenAI(
        api_key=api_key,
        base_url="https://api.together.xyz/v1"
    )
    def run(prompt: str) -> str:
        try:
            response = client.chat.completions.create(
                model=model_name,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=MAX_TOKENS,
                temperature=TEMPERATURE,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"  Llama error: {e}")
            return None
    return run
