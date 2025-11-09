# # # backend/tools/summarize_tool.py
# import os
# import requests
# import json
# from dotenv import load_dotenv

# load_dotenv()

# OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# def _extract_text_from_ollama_response(j):
#     """Extract text safely from multiple Ollama JSON formats."""
#     if not j:
#         return ""

#     if isinstance(j, dict):
#         if "text" in j:
#             return j["text"]
#         # Handle newer Ollama "response" or "output" formats
#         if "response" in j:
#             return j["response"]
#         out = j.get("output") or j.get("out")
#         if isinstance(out, str):
#             return out
#         if isinstance(out, list):
#             text_out = ""
#             for item in out:
#                 if isinstance(item, dict):
#                     content = item.get("content", [])
#                     if isinstance(content, list):
#                         for c in content:
#                             if c.get("type") == "output_text" and c.get("text"):
#                                 text_out += c["text"]
#             return text_out
#     return str(j)

# def summarize_tool_fn(text: str) -> str:
#     """
#     Summarize text via Ollama (llama3).
#     Robust against streaming, 500 errors, and non-standard JSON.
#     """
#     if not text.strip():
#         return "⚠️ Please provide text to summarize."

#     prompt = f"Summarize this text in 2–4 sentences:\n\n{text.strip()}"
#     url = f"{OLLAMA_API_URL}/api/generate"
#     payload = {"model": OLLAMA_MODEL, "prompt": prompt}

#     try:
#         with requests.post(url, json=payload, stream=True, timeout=90) as r:
#             if r.status_code != 200:
#                 return f"❌ Error summarizing: HTTP {r.status_code} - {r.text[:200]}"
#             out_text = ""
#             for line in r.iter_lines():
#                 if not line:
#                     continue
#                 try:
#                     j = json.loads(line.decode("utf-8"))
#                     chunk = _extract_text_from_ollama_response(j)
#                     out_text += chunk
#                 except Exception:
#                     continue
#         return out_text.strip() or "⚠️ No summary produced."
#     except requests.exceptions.RequestException as e:
#         return f"❌ Ollama connection error: {e}"
#     except Exception as e:
#         return f"❌ Error summarizing: {e}"
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

