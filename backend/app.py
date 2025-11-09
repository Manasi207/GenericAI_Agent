
######################################

# # backend/app.py
# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# from dotenv import load_dotenv
# import os

# # Load environment variables from .env
# load_dotenv()
# import re
# import os

# # import tool functions directly so we can call them for deterministic commands
# from tools.weather_tool import weather_tool_fn
# from tools.email_tool import send_email_tool
# from tools.summarize_tool import summarize_tool_fn
# from tools.sentiment_tool import sentiment_tool_fn
# from tools.browse_tool import browse_tool_fn

# # fallback agent usage
# from agent_core import get_agent, run_agent

# app = FastAPI()

# # Allow your extension to hit the backend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class Prompt(BaseModel):
#     prompt: str

# @app.get("/")
# def root():
#     return {"status": "✅LangChain + OLLAMA Supported ✅✅Generic AI Agent Backend Running Successfully !!! "}

# @app.get("/status")
# def status():
#     return {"Agent": "✅Ollama(llama3) Initialized ✅✅"}

# # helper to extract email, subject, body from more natural sentences
# def _extract_email_parts(s: str):
#     s = s.strip()
#     parts = {"to": None, "subject": None, "body": None}

#     # try easy structured parsing first: "to:someone@example.com; subject:Hi; body:Hello"
#     for match in re.finditer(r"(?P<key>to|subject|body)\s*:\s*(?P<val>[^;]+)", s, flags=re.IGNORECASE):
#         k = match.group("key").lower()
#         parts[k] = match.group("val").strip()

#     # if 'to' still missing, try to find an email in text
#     if not parts["to"]:
#         m = re.search(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", s)
#         if m:
#             parts["to"] = m.group(1)

#     # subject: try "subject" keyword or "subject is" phrasing
#     if not parts["subject"]:
#         m = re.search(r"subject\s+(is\s+)?['\"]?([^'\"]+)", s, flags=re.IGNORECASE)
#         if m:
#             parts["subject"] = m.group(2).strip()

#     # body: look for "body" or "message" or "saying"
#     if not parts["body"]:
#         m = re.search(r"(body|message|saying)\s*[:\-]\s*(.+)$", s, flags=re.IGNORECASE)
#         if m:
#             parts["body"] = m.group(2).strip()

#     return parts

# @app.post("/agent")
# async def agent_endpoint(req: Prompt):
#     user_input = req.prompt.strip()
#     low = user_input.lower()

#     try:
#         # explicit command routing to ensure tools are called deterministically

#         # summarize
#         if low.startswith("summarize") or low.startswith("summarise"):
#             # accept "summarize: <text>" or "summarize <text>"
#             text = re.sub(r'^(summarize|summarise)[:\s]*', '', user_input, flags=re.IGNORECASE).strip()
#             if not text:
#                 return {"response": "Please provide text to summarize after the word 'summarize'."}
#             return {"response": summarize_tool_fn(text)}

#         # sentiment
#         if low.startswith("sentiment") or low.startswith("analyze sentiment"):
#             text = re.sub(r'^(sentiment|analyze sentiment)[:\s]*', '', user_input, flags=re.IGNORECASE).strip()
#             if not text:
#                 return {"response": "Please provide text to analyze sentiment for."}
#             return {"response": (sentiment_text := sentiment_tool_fn(text))}

#         # weather
#         if low.startswith("weather") or low.startswith("checking weather") or low.startswith("what's the weather"):
#             # accept "weather Paris" or "weather: Paris, FR" or "what's the weather in Pune"
#             # try extract city after keywords
#             city = re.sub(r'^(weather|checking weather|what(\'s| is) the weather( in)?)[:\s]*', '', user_input, flags=re.IGNORECASE).strip()
#             if not city:
#                 return {"response": "Please specify a city after the word 'weather', e.g. 'weather Pune,IN'."}
#             return {"response": weather_tool_fn(city)}

#         # # browse / open website -> will fetch page summary and also return the URL in result
#         # if low.startswith("browse") or low.startswith("open") or low.startswith("go to") or low.startswith("visit"):
#         #     # extract URL or site
#         #     # accept "browse https://example.com" or "go to google.com" or "open example.com"
#         #     # if no protocol, try to add https://
#         #     maybe = re.sub(r'^(browse|open|go to|visit)[:\s]*', '', user_input, flags=re.IGNORECASE).strip()
#         #     if not maybe:
#         #         return {"response": "Please provide a full URL or website after 'browse/open' (include domain)."}
#         #     # add protocol if missing and looks like domain
#         #     if not (maybe.startswith("http://") or maybe.startswith("https://")):
#         #         maybe = maybe.strip()
#         #         # if just a domain like google.com, add https
#         #         if re.match(r'^[\w.-]+\.[a-zA-Z]{2,}', maybe):
#         #             maybe = "https://" + maybe
#         #         else:
#         #             return {"response": "Please provide a valid URL (example: https://example.com or example.com)."}
#         #     summary = browse_tool_fn(maybe)
#         #     # include clickable link in returned text (frontend will detect)
#         #     return {"response": f"{summary}\n\nURL: {maybe}"}
#         # Browse / Navigate
#         if low.startswith(("browse", "open", "go to", "visit", "navigate")):
#             maybe = re.sub(r'^(browse|open|go to|navigate|visit)[:\s]*', '', user_input, flags=re.IGNORECASE).strip()
#             if not maybe:
#                 return {"response": "🌍 Please provide a website after 'browse/open/navigate/go to'."}

#             # Add https:// if missing
#             if not (maybe.startswith("http://") or maybe.startswith("https://")):
#                 if re.match(r'^[\w.-]+\.[a-zA-Z]{2,}', maybe):
#                     maybe = "https://" + maybe
#                 else:
#                     return {"response": "❌ Please provide a valid domain or URL."}

#             # Instead of summarizing, just return redirect instruction
#             return {"redirect_url": maybe}

#         # Default fallback (chat)
#         return {"response": f"🤖 Agent says: {user_input}"}

#         # send mail - try to auto-send if fields present
#         if low.startswith("send mail") or low.startswith("send email") or low.startswith("email"):
#             # attempt to parse common patterns
#             parts = _extract_email_parts(user_input)
#             # rebuild a payload string acceptable to send_email_tool
#             payload = ""
#             if parts["to"]:
#                 payload += f"to:{parts['to']}; "
#             if parts["subject"]:
#                 payload += f"subject:{parts['subject']}; "
#             if parts["body"]:
#                 payload += f"body:{parts['body']}; "

#             # if payload has at least recipient and something else, send automatically
#             if parts["to"] and (parts["body"] or parts["subject"]):
#                 result = send_email_tool(payload)
#                 return {"response": result}
#             else:
#                 # fallback: pass entire user_input to tool parser which is permissive
#                 result = send_email_tool(user_input)
#                 # if send_email_tool returns "No recipient specified", return that, else success/failure
#                 return {"response": result}

#         # Fallback: pass through to the agent (llm + tools via agent_core) for general queries
#         agent = get_agent()
#         answer = run_agent(agent, user_input)
#         return {"response": answer}

#     except Exception as e:
#         return {"detail": str(e)}
###########################################################################################################################3

# # backend/app.py - FastAPI backend for Chrome AI Agent using Gemini 2.5 Flash
# from fastapi import FastAPI, HTTPException
# from fastapi.middleware.cors import CORSMiddleware
# from pydantic import BaseModel
# import os
# from dotenv import load_dotenv
# import google.generativeai as genai

# # Load environment variables
# load_dotenv()

# # Configure Gemini
# genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# # Import tools
# from tools.weather_tool import weather_tool_fn
# from tools.summarize_tool import summarize_tool_fn
# from tools.sentiment_tool import sentiment_tool_fn
# from tools.email_tool import send_email_tool
# from tools.browse_tool import browse_tool_fn

# app = FastAPI(title="Gemini 2.5 Flash AI Agent")

# # Enable CORS for extension or frontend
# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

# class AgentRequest(BaseModel):
#     prompt: str

# @app.get("/")
# def root():
#     return {"status": "✅ Gemini 2.5 Flash AI Agent is running!"}

# @app.post("/agent")
# async def run_agent(req: AgentRequest):
#     user_prompt = req.prompt.strip()
#     if not user_prompt:
#         raise HTTPException(status_code=400, detail="Prompt cannot be empty")

#     lower = user_prompt.lower()

#     # Route to correct tool
#     if lower.startswith("weather:"):
#         city = user_prompt.split(":", 1)[1]
#         return {"response": weather_tool_fn(city)}

#     elif lower.startswith("summarize:"):
#         text = user_prompt.split(":", 1)[1]
#         return {"response": summarize_tool_fn(text)}

#     elif lower.startswith("sentiment:"):
#         text = user_prompt.split(":", 1)[1]
#         return {"response": sentiment_tool_fn(text)}

#     elif lower.startswith("email:"):
#         text = user_prompt.split(":", 1)[1]
#         return {"response": send_email_tool(text)}

#     elif lower.startswith("browse:"):
#         url = user_prompt.split(":", 1)[1]
#         return {"response": browse_tool_fn(url)}

#     # Default: use Gemini directly
#     try:
#         model = genai.GenerativeModel("gemini-2.0-flash")
#         response = model.generate_content(user_prompt)
#         return {"response": response.text}
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Gemini API error: {e}")

##############################################################################

# backend/app.py - FastAPI backend for Chrome AI Agent using Gemini 2.5 Flash
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
