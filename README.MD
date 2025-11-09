# 🧑‍💻 Generic AI Agent

An intelligent, browser-integrated AI assistant built to simplify everyday tasks right from your Chrome tab. This project merges Google Gemini Flash 2.5 LLM, LangChain, and FastAPI with a sleek HTML/CSS/JS frontend — creating a multi-capable agent that can analyze, summarize, browse, and communicate effortlessly.

# 🧩 Features

## Core Modules

#### 🌦 Check Weather – Instantly fetch real-time weather updates for any city.

####

#### 🧩 Sentiment Analysis – Understand the tone and mood of any text input using a custom VADER + Gemini-based analyzer.

#### 📝 Text Summarizer – Condense long articles or paragraphs into crisp, meaningful summaries.

#### 🧩 Browse Through (Web Application) – AI-powered browsing with natural-language commands and content extraction.

#### 📧 Send Emails – Compose and send emails using AI assistance via FastAPI backend integration.

# 🧩 Tech Stack

## Frontend:

#### HTML5, CSS3, JavaScript

#### Chrome Extension Manifest V3

#### Fetch API for backend calls

## Backend:

#### Python (FastAPI)

#### LangChain for LLM orchestration

#### Google Gemini Flash 2.5 API

#### VADER Sentiment Analysis (TextBlob optional)

#### Email & Weather APIs (custom integrations)

## AI & Tools:

#### Google Gemini Flash 2.5 (via Vertex AI API or Gemini REST)

#### LangChain for tool routing and context management

#### OpenAI-style JSON schema for modular responses

# 🧩 Architecture Overview

```plaintext
Frontend (Chrome Extension)
│
├── popup.html / popup.js
│   ├─ UI for weather, summarization, sentiment, email
│   └─ Communicates with backend API endpoints
│
└── Backend (FastAPI Server)
    ├─ /weather        → Weather API Integration
    ├─ /sentiment      → VADER + Gemini sentiment analyzer
    ├─ /summarize      → Gemini summarization
    ├─ /browse         → LangChain + Gemini for browsing tasks
    └─ /email          → Email composition and send

# ⚙️ Setup & Installation

1️⃣ Clone the Repository
git clone https://github.com/<your-username>/generic-ai-agent.git
cd generic-ai-agent

2️⃣ Install Dependencies
pip install -r requirements.txt

3️⃣ Set Up Environment Variables

Create a .env file in the root directory with:

GEMINI_API_KEY=your_google_gemini_key
EMAIL_USER=your_email@example.com
EMAIL_PASS=your_password

4️⃣ Run the Backend
uvicorn backend.main:app --reload

5️⃣ Load the Chrome Extension

Go to chrome://extensions/

Enable Developer Mode

Click Load unpacked and select the frontend/ folder
```
