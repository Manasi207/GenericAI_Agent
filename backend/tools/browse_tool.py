
########################################################
# backend/tools/browse_tool.py
# import requests
# import os
# from dotenv import load_dotenv
# load_dotenv()

# OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")

# def _fetch_url_text(url: str, max_chars=3000) -> str:
#     try:
#         r = requests.get(url, timeout=10, headers={"User-Agent": "generic-ai-agent/1.0"})
#         r.raise_for_status()
#         text = r.text
#         return text[:max_chars]
#     except Exception as e:
#         return f"Error fetching URL: {e}"

# def browse_tool_fn(url: str) -> str:
#     url = url.strip()
#     if not (url.startswith("http://") or url.startswith("https://")):
#         return "Please provide a full URL starting with http:// or https://"

#     page_text = _fetch_url_text(url)
#     prompt = f"Here is the raw HTML/text of a page (truncated). Provide a short, 3-sentence summary and list the page's main topics.\n\n{page_text}"
#     try:
#         payload = {"model": OLLAMA_MODEL, "prompt": prompt}
#         r = requests.post(f"{OLLAMA_API_URL}/api/generate", json=payload, timeout=20)
#         r.raise_for_status()
#         j = r.json()
#         if "text" in j:
#             return j["text"].strip()
#         out = j.get("output") or j.get("out")
#         text_out = ""
#         if isinstance(out, list):
#             for item in out:
#                 if isinstance(item, dict):
#                     content = item.get("content") or []
#                     for c in content:
#                         if c.get("type") == "output_text":
#                             text_out += c.get("text", "")
#         return text_out.strip() or page_text[:800]
#     except Exception as e:
#         return f"Error summarizing page: {e}"
###########################################################################################################################

# backend/tools/browse_tool.py - Simple web browsing tool using requests and BeautifulSoup
import webbrowser
import requests
import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def browse_tool_fn(url: str) -> str:
    """
    Fetch and summarize webpage content using Gemini
    and open the webpage in a new browser tab.
    """
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url  # Auto-fix missing prefix

    try:
        # Open the URL in the user's browser
        webbrowser.open_new_tab(url)

        # Fetch limited content for Gemini summary
        r = requests.get(url, timeout=10, headers={"User-Agent": "gemini-ai-agent/1.0"})
        r.raise_for_status()
        text = r.text[:3000]

        # Summarize page using Gemini
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Provide a concise 3-sentence summary of this webpage:\n\n{text}"
        response = model.generate_content(prompt)

        return f"🌐 Opened {url} in a new browser tab.\n\n🔍 Summary:\n{response.text.strip()}"
    except Exception as e:
        return f"❌ Error browsing {url}: {e}"
