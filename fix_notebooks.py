"""
Fix notebooks: remove all API keys properly by working at the JSON string level.
The previous regex approach broke JSON by introducing unescaped double quotes.
This script reads raw text, fixes all key patterns, and validates JSON.
"""
import re, os

notebooks = [
    'notebooks/Protocol_A0_Original.ipynb',
    'notebooks/Protocol_A1_Corrected.ipynb',
    'notebooks/Protocol_A2_and_B.ipynb',
]

# Patterns that appear inside Python source lines within JSON strings
# These are inside JSON string values, so they use \\n for newlines
# We need to replace the key value but keep the surrounding JSON valid

replacements = [
    # Fix: OPENAI_API_KEY = "YOUR_OPENAI_API_KEY" -> use single quotes
    (r'OPENAI_API_KEY\s*=\s*"YOUR_OPENAI_API_KEY"', "OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'"),
    (r'OPENAI_API_KEY\s{2,}=\s*"YOUR_OPENAI_API_KEY"', "OPENAI_API_KEY  = 'YOUR_OPENAI_API_KEY'"),
    # Fix: GROQ_API_KEY = "YOUR_GROQ_API_KEY" -> use single quotes
    (r'GROQ_API_KEY\s*=\s*"YOUR_GROQ_API_KEY"', "GROQ_API_KEY   = 'YOUR_GROQ_API_KEY'"),
    (r'GROQ_API_KEY\s{3,}=\s*"YOUR_GROQ_API_KEY"', "GROQ_API_KEY   = 'YOUR_GROQ_API_KEY'"),
    # Fix: TOGETHER_API_KEY = "YOUR_TOGETHER_API_KEY" -> use single quotes
    (r'TOGETHER_API_KEY\s*=\s*"YOUR_TOGETHER_API_KEY"(\s*#[^\\n]*)?', r"TOGETHER_API_KEY = 'YOUR_TOGETHER_API_KEY'"),
    # Fix: GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" -> use single quotes
    (r'GEMINI_API_KEY\s*=\s*"YOUR_GEMINI_API_KEY"(\s*#[^\\n]*)?', r"GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'"),
    # Remove actual GCP key (AIzaSy...)
    (r"GEMINI_API_KEY\s*=\s*'AIza[A-Za-z0-9\-_]+'", "GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'"),
    (r'GEMINI_API_KEY\s*=\s*"AIza[A-Za-z0-9\-_]+"', "GEMINI_API_KEY = 'YOUR_GEMINI_API_KEY'"),
    # Remove actual OpenAI keys
    (r"OPENAI_API_KEY\s*=\s*'sk-[A-Za-z0-9\-_]+'", "OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'"),
    (r'OPENAI_API_KEY\s*=\s*"sk-[A-Za-z0-9\-_]+"', "OPENAI_API_KEY = 'YOUR_OPENAI_API_KEY'"),
    # Remove actual Groq keys
    (r"GROQ_API_KEY\s*=\s*'gsk_[A-Za-z0-9\-_]+'", "GROQ_API_KEY = 'YOUR_GROQ_API_KEY'"),
    (r'GROQ_API_KEY\s*=\s*"gsk_[A-Za-z0-9\-_]+"', "GROQ_API_KEY = 'YOUR_GROQ_API_KEY'"),
]

for nb_path in notebooks:
    with open(nb_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    for pattern, replacement in replacements:
        content = re.sub(pattern, replacement, content)
    
    with open(nb_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    # Validate JSON
    import json
    try:
        with open(nb_path, 'r') as f:
            json.load(f)
        changed = "CHANGED" if content != original else "unchanged"
        print(f"OK ({changed}): {nb_path}")
    except json.JSONDecodeError as e:
        print(f"JSON ERROR: {nb_path}: {e}")
        # Show the problematic line
        lines = content.split('\n')
        print(f"  Line {e.lineno}: {lines[e.lineno-1][:100]}")
