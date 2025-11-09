
# backend/agent_core.py - Alternative implementation using Gemini 2.5 Flash

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
    return [
        Tool(name="weather", func=weather_tool_fn, description="Get weather for a city."),
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
        result = agent.run(prompt)
        return result
    except Exception as e:
        return f"⚠️ Agent error: {str(e)}"

