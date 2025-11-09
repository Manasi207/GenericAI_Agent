
### ###########################################################################################################################3

# backend/tools/summarize_tool.py - Summarization tool using Gemini 2.5 Flash
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def summarize_tool_fn(text: str) -> str:
    """Summarize text using Gemini 2.5 Flash"""
    if not text.strip():
        return "⚠️ Please provide text to summarize."

    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Summarize this text in 3–5 sentences:\n\n{text.strip()}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error summarizing with Gemini: {e}"

