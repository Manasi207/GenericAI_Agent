
# ###########################################################################################################
# # backend/agent_core.py
# import os
# from typing import List
# from dotenv import load_dotenv
# load_dotenv()

# # LangChain imports
# from langchain.agents import initialize_agent, AgentType
# from langchain.tools import Tool

# # Try to import Ollama LLM wrapper. If your LangChain version doesn't have it, replace with a custom wrapper.
# try:
#     from langchain.llms import Ollama
#     LLM_AVAILABLE = True
# except Exception:
#     LLM_AVAILABLE = False

# from tools.weather_tool import weather_tool_fn
# from tools.email_tool import send_email_tool
# from tools.summarize_tool import summarize_tool_fn
# from tools.sentiment_tool import sentiment_tool_fn
# from tools.browse_tool import browse_tool_fn

# OLLAMA_API_URL = os.getenv("OLLAMA_API_URL", "http://127.0.0.1:11434")
# OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3")  # default to llama3

# def get_llm():
#     if LLM_AVAILABLE:
#         return Ollama(base_url=OLLAMA_API_URL, model=OLLAMA_MODEL, verbose=False)
#     else:
#         from langchain.llms.base import LLM
#         import requests, json

#         class OllamaFallback(LLM):
#             def _call(self, prompt: str, stop=None):
#                 url = f"{OLLAMA_API_URL}/api/generate"
#                 payload = {"model": OLLAMA_MODEL, "prompt": prompt}
#                 resp = requests.post(url, json=payload, timeout=30)
#                 resp.raise_for_status()
#                 data = resp.json()
#                 # try common fields
#                 if isinstance(data, dict) and "text" in data:
#                     return data["text"]
#                 if isinstance(data, dict) and "out" in data:
#                     return str(data["out"])
#                 return json.dumps(data)
#             @property
#             def _identifying_params(self):
#                 return {"model": OLLAMA_MODEL}
#             @property
#             def _llm_type(self):
#                 return "ollama-fallback"

#         return OllamaFallback()

# def get_tools() -> List[Tool]:
#     return [
#         Tool(
#             name="weather",
#             func=weather_tool_fn,
#             description="Get current weather for a city. Input: city name. Example: 'Pune, IN' or 'London'. Returns weather summary."
#         ),
#         Tool(
#             name="send_email",
#             func=send_email_tool,
#             description="Send an email. Input: semi-structured string with fields: to, subject, body."
#         ),
#         Tool(
#             name="summarize",
#             func=summarize_tool_fn,
#             description="Summarize any text. Input: the text to summarize. Returns a short summary."
#         ),
#         Tool(
#             name="sentiment",
#             func=sentiment_tool_fn,
#             description="Return sentiment (positive/neutral/negative) and short score for given text."
#         ),
#         Tool(
#             name="browse",
#             func=browse_tool_fn,
#             description="Fetch content from a URL and return a short summary of the page. Input: a URL (must start with http or https)."
#         )
#     ]

# _agent = None

# def get_agent():
#     global _agent
#     if _agent is None:
#         llm = get_llm()
#         tools = get_tools()
#         _agent = initialize_agent(
#             tools, llm, agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=False
#         )
#     return _agent

# def run_agent(agent, prompt: str) -> str:
#     result = agent.run(prompt)
#     return result
# ###########################################################################################################

# backend/agent_core.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import initialize_agent, AgentType
from langchain.tools import Tool

from tools.weather_tool import weather_tool_fn
from tools.email_tool import send_email_tool
from tools.summarize_tool import summarize_tool_fn
from tools.sentiment_tool import sentiment_tool_fn
from tools.browse_tool import browse_tool_fn

load_dotenv()


def get_llm():
    """Return Gemini 2.5 Flash model."""
    api_key = os.getenv("GEMINI_API_KEY")
    model_id = os.getenv("MODEL_ID", "gemini-2.5-flash")

    if not api_key:
        raise ValueError("Missing GEMINI_API_KEY in environment variables.")

    return ChatGoogleGenerativeAI(
        model=model_id,
        google_api_key=api_key,
        temperature=0.7,
        convert_system_message_to_human=True,
    )


def get_tools():
    """Return available tool list for the LangChain agent."""

    # ✅ Wrap weather tool to force concise output
    def short_weather_tool(city_name: str) -> str:
        result = weather_tool_fn(city_name)
        # Ensure it is single-line and concise
        return result.replace("\n", " ").strip()

    return [
        Tool(name="weather", func=short_weather_tool, description="Get short weather for a city."),
        Tool(name="send_email", func=send_email_tool, description="Send email with recipient, subject, and body."),
        Tool(name="summarize", func=summarize_tool_fn, description="Summarize text using Gemini."),
        Tool(name="sentiment", func=sentiment_tool_fn, description="Analyze text sentiment."),
        Tool(name="browse", func=browse_tool_fn, description="Fetch webpage content and summarize it."),
    ]


_agent = None


def get_agent():
    """Create or reuse global LangChain agent."""
    global _agent
    if _agent is None:
        llm = get_llm()
        tools = get_tools()
        _agent = initialize_agent(
            tools,
            llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=False,
        )
    return _agent


def run_agent(agent, prompt: str):
    """Safely run the agent and catch any errors."""
    try:
        # ✅ If prompt starts with 'weather:', call our short tool directly
        if prompt.lower().startswith("weather:"):
            city = prompt.split(":", 1)[1].strip()
            return weather_tool_fn(city)

        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"⚠️ Agent error: {str(e)}"
