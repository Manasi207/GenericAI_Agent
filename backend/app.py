# backend/app.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Import tools
from tools.weather_tool import weather_tool_fn
from tools.summarize_tool import summarize_tool_fn
from tools.sentiment_tool import sentiment_tool_fn
from tools.email_tool import send_email_tool
from tools.browse_tool import browse_tool_fn

# Initialize FastAPI app
app = FastAPI(title="Gemini 2.5 Flash AI Agent")

# Allow CORS (frontend connection)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic request model
class AgentRequest(BaseModel):
    prompt: str


@app.get("/")
def root():
    """Root route"""
    return {"status": "✅ Gemini 2.5 Flash AI Agent is running!"}


@app.post("/agent")
async def run_agent(req: AgentRequest):
    """Main AI Agent endpoint — routes to tools or Gemini reasoning."""
    user_prompt = req.prompt.strip()
    if not user_prompt:
        raise HTTPException(status_code=400, detail="Prompt cannot be empty")

    lower = user_prompt.lower()

    # --- Weather Tool (Always short output) ---
    if lower.startswith("weather:"):
        city = user_prompt.split(":", 1)[1].strip()
        short_weather = weather_tool_fn(city)
        return {"response": short_weather}

    # --- Summarize Tool ---
    elif lower.startswith("summarize:"):
        text = user_prompt.split(":", 1)[1].strip()
        return {"response": summarize_tool_fn(text)}

    # --- Sentiment Tool ---
    elif lower.startswith("sentiment:"):
        text = user_prompt.split(":", 1)[1].strip()
        return {"response": sentiment_tool_fn(text)}

    # --- Email Tool (supports multi-line input) ---
    elif "send email" in lower:
        try:
            lines = [l.strip() for l in user_prompt.splitlines() if l.strip()]
            to = subject = body = None

            for line in lines:
                if line.lower().startswith("to:"):
                    to = line.split(":", 1)[1].strip()
                elif line.lower().startswith("subject:"):
                    subject = line.split(":", 1)[1].strip()
                elif line.lower().startswith("body:"):
                    body = line.split(":", 1)[1].strip()

            if not to:
                raise HTTPException(status_code=400, detail="Missing recipient email address.")

            response = send_email_tool(to, subject or "No Subject", body or "")
            return {"response": response}

        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Email tool error: {str(e)}")

    # --- Browse Tool ---
    elif lower.startswith("browse:"):
        url = user_prompt.split(":", 1)[1].strip()
        return {"response": browse_tool_fn(url)}

    # --- Default: Use Gemini reasoning for everything else ---
    try:
        model = genai.GenerativeModel("gemini-2.5-flash")
        response = model.generate_content(user_prompt)
        return {"response": response.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")


# Startup Event
@app.on_event("startup")
def startup_event():
    print("🚀 Gemini AI Agent backend is running on http://127.0.0.1:8000")
