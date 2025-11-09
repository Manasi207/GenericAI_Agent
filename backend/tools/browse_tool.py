
###########################################################################################################################

# backend/tools/browse_tool.py - Simple web browsing tool using requests and BeautifulSoup
import requests
import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def browse_tool_fn(url: str) -> str:
    """Fetch and summarize webpage content using Gemini"""
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        return "⚠️ Please provide a valid URL starting with http:// or https://"

    try:
        r = requests.get(url, timeout=10, headers={"User-Agent": "gemini-ai-agent/1.0"})
        r.raise_for_status()
        text = r.text[:3000]  # limit input length
        model = genai.GenerativeModel("gemini-2.0-flash")
        prompt = f"Summarize this webpage in a few sentences and list the key insights:\n\n{text}"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        return f"❌ Error browsing: {e}"
