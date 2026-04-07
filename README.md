# 🧠 Gemini + Google Search Intelligence Engine

A sophisticated, multi-functional AI platform combining the reasoning power of **Google Gemini 2.5 Flash** with the real-time retrieval capabilities of the **Google Custom Search API**. This application delivers precise, context-aware information directly to your browser or inbox.

---

## 🚀 Key Functionalities

### 🔎 1. Real-time Web Search
*   Harnesses the **Google Custom Search API** to fetch live, high-relevance web results.
*   Provides clean, distilled snippets with direct links to sources.

### 🤖 2. Gemini AI Assistant
*   Powered by `gemini-2.5-flash` for lightning-fast, intelligent dialogue.
*   Optimized for conciseness, technical accuracy, and creative problem-solving.

### 🧠 3. Hybrid Intelligence (Search + Synthesis)
*   **The Powerhouse Mode:** Fetches real-time data first, then feeds it into Gemini for a synthesized, context-rich summary.
*   Eliminates AI hallucinations by grounding responses in verified web data.

### 📰 4. Automated News Digest
*   Aggregates the latest news across 6 genres: *Tech, Politics, Sports, Finance, Markets, and Lifestyle*.
*   Summarizes complex headlines into distinct, actionable bullet points.
*   **Direct-to-Inbox:** Delivers the curated digest via secure SMTP email integration.

---

## 🛠️ Tech Architecture

*   **Backend:** Python 3.10+ (Flask Framework)
*   **Frontend:** Vanilla JavaScript, HTML5, CSS3 (Glassmorphic Design)
*   **AI Engine:** Google Generative AI (Gemini API)
*   **Search Core:** Google Custom Search JSON API
*   **Icons:** Lucide-React Icons
*   **Notification:** SMTP (Gmail Protocol)

---

## ⚙️ Quick Start Guide

### 1. Prerequisites
*   Python 3.8 or higher installed on your system.
*   A Google Cloud Project for Gemini and Search API keys.
*   A Gmail account with an "App Password" for email functionality.


### 2. Configuration
Open `app.py` and update the following credentials:
```python
# API Keys
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
CX_ID = "YOUR_CUSTOM_SEARCH_ENGINE_ID"

# Email Credentials
SENDER_EMAIL = "your-email@gmail.com"
APP_PASSWORD = "your-16-digit-app-password"
```

### 3. Running the Application
```bash
python app.py
```
Visit **`http://localhost:5500`** in your browser to start exploring!

---

