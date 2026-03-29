import streamlit as st
import requests
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# ---------------- CONFIG ----------------
GEMINI_API_KEY = "AIzaSyCyqhGHRJ__-hR56D44iZXl2qoD4FYG-hg"
GOOGLE_API_KEY = "AIzaSyB6yBjUkLifCQd0erTDT3C8i7NlTlxPvK4"
CX_ID = "51fd225c21c2c4c38"

SENDER_EMAIL = "tejasnj14@gmail.com"
APP_PASSWORD = "fpqe tkvo mjgi tbzc "

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")

# ---------------- GOOGLE SEARCH ----------------
def google_search(query, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": CX_ID,
        "q": query,
        "num": num_results
    }

    res = requests.get(url, params=params)
    data = res.json()

    if "items" not in data:
        return "No search results found."

    snippets = []
    for item in data["items"]:
        title = item.get("title", "No title")
        snippet = item.get("snippet", "No description available")
        snippets.append(f"• {title}: {snippet}")

    return "\n".join(snippets)

# ---------------- PROMPTS ----------------
def build_general_prompt(user_query, context=""):
    return f"""
You are a highly intelligent, reliable AI assistant.

Guidelines:
- Answer clearly and concisely
- Use provided context if available
- Do NOT hallucinate
- If unsure, say so

Context:
{context}

User Question:
{user_query}
"""

def build_news_prompt(context):
    return f"""
Give me top 10 latest news in each of the following genres:
1. Technology
2. Indian Politics
3. Sports
4. Finance
5. Stock Market
6. Lifestyle

Requirements:
- Each category should have exactly 10 crisp bullet points.
- Keep points short (maximum 1 sentence).
- Do NOT add extra text like introductions or summaries.
- Use ONLY the provided context.

Context:
{context}
"""

# ---------------- GEMINI ----------------
def ask_gemini(prompt):
    response = model.generate_content(prompt)
    return response.text

# ---------------- EMAIL ----------------
def send_email(subject, body, receiver_email):
    try:
        msg = MIMEMultipart()
        msg["From"] = SENDER_EMAIL
        msg["To"] = receiver_email
        msg["Subject"] = subject

        msg.attach(MIMEText(body, "plain"))

        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(SENDER_EMAIL, APP_PASSWORD)
        server.sendmail(SENDER_EMAIL, receiver_email, msg.as_string())
        server.quit()

        return "✅ Email sent successfully!"
    except Exception as e:
        return f"❌ Error: {e}"

# ---------------- UI ----------------
st.set_page_config(page_title="Smart AI Chatbot", layout="wide")

st.title("🤖 Smart AI Chatbot")

option = st.selectbox(
    "Choose Functionality",
    [
        "Real-time Search only",
        "Gemini only",
        "Search + Gemini Summary",
        "Live News → Email"
    ]
)

# ---------------- OPTION 1 ----------------
if option == "Real-time Search only":
    query = st.text_input("Enter your question")

    if st.button("Search"):
        if query:
            results = google_search(query)
            st.subheader("🔎 Search Results")
            st.text(results)

# ---------------- OPTION 2 ----------------
elif option == "Gemini only":
    query = st.text_input("Enter your question")

    if st.button("Ask Gemini"):
        if query:
            prompt = build_general_prompt(query)
            answer = ask_gemini(prompt)
            st.subheader("🤖 Gemini Answer")
            st.write(answer)

# ---------------- OPTION 3 ----------------
elif option == "Search + Gemini Summary":
    query = st.text_input("Enter your question")

    if st.button("Get Answer"):
        if query:
            search_data = google_search(query)
            prompt = build_general_prompt(query, search_data)
            answer = ask_gemini(prompt)

            st.subheader("🔎 Search Data")
            st.text(search_data)

            st.subheader("🧠 Gemini Summary")
            st.write(answer)

# ---------------- OPTION 4 ----------------
elif option == "Live News → Email":
    receiver_email = st.text_input("Enter receiver email")

    if st.button("Send Live News"):
        categories = [
            "latest technology news",
            "latest Indian politics news",
            "latest sports news",
            "latest finance news",
            "latest stock market news India",
            "latest lifestyle news"
        ]

        with st.spinner("Fetching live news..."):
            combined_context = ""
            for cat in categories:
                combined_context += google_search(cat, 10) + "\n"

            news_prompt = build_news_prompt(combined_context)
            news_summary = ask_gemini(news_prompt)

        st.subheader("📰 Generated News Summary")
        st.text(news_summary)

        if receiver_email:
            status = send_email("Today's Live News Summary", news_summary, receiver_email)
            st.success(status)
        else:
            st.warning("⚠️ Please enter a receiver email")
