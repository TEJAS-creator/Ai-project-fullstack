# 🤖 Smart AI Chatbot (Streamlit App)

An intelligent, multi-functional AI chatbot built using **Streamlit**, **Google Gemini API**, and **Google Custom Search API**.
This application combines real-time web search, AI-generated responses, and automated email delivery into a single powerful interface.

---

## 🚀 Features

### 🔎 1. Real-time Search

* Fetches live results using Google Custom Search API
* Displays concise titles and snippets

### 🤖 2. Gemini AI Chat

* Uses Gemini model (`gemini-2.5-flash`)
* Provides clear, concise, and reliable answers

### 🔍 3. Search + AI Summary

* Combines real-time search with AI summarization
* Ensures accurate, context-based responses

### 📰 4. Live News → Email

* Fetches latest news across categories:

  * Technology
  * Indian Politics
  * Sports
  * Finance
  * Stock Market
  * Lifestyle
* Summarizes using AI
* Sends directly to any email

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **AI Model:** Google Gemini API
* **Search Engine:** Google Custom Search API
* **Email Service:** SMTP (Gmail)

---

## 🔑 Configuration

Replace the following values in your code:

```python
GEMINI_API_KEY = "YOUR_GEMINI_API_KEY"
GOOGLE_API_KEY = "YOUR_GOOGLE_API_KEY"
CX_ID = "YOUR_CX_ID"

SENDER_EMAIL = "your_email@gmail.com"
APP_PASSWORD = "your_app_password"
```

## 📸 Features Overview

| Feature | Description             |
| ------- | ----------------------- |
| Search  | Live Google results     |
| Gemini  | AI-generated answers    |
| Hybrid  | Search + AI summary     |
| News    | AI-curated news + Email |

---

## 📧 Email Functionality

* Sends news summaries using Gmail SMTP
* Dynamic receiver email input
* Supports real-time delivery

---
