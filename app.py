from flask import Flask, request, jsonify, send_from_directory, render_template
from flask_cors import CORS
import requests
import google.generativeai as genai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

app = Flask(__name__, static_folder=".", template_folder=".")
CORS(app)

# ---------------- CONFIG ----------------
GEMINI_API_KEY = ""
GOOGLE_API_KEY = ""
CX_ID = ""

SENDER_EMAIL = "tejasnj14@gmail.com"
APP_PASSWORD = ""  # Ensure no trailing whitespace

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.5-flash")  # gemini-2.0-flash is the official name for what is often seen as 2.5-flash

def google_search(query, num_results=5):
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "key": GOOGLE_API_KEY,
        "cx": CX_ID,
        "q": query,
        "num": num_results
    }
    try:
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
    except Exception as e:
        return f"Search Error: {e}"

def ask_gemini(prompt):
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"AI Error: {e}"

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

# ---------------- ROUTES ----------------

@app.route('/')
def home():
    return send_from_directory('.', 'index.html')

@app.route('/style.css')
def style():
    return send_from_directory('.', 'style.css')

@app.route('/script.js')
def script():
    return send_from_directory('.', 'script.js')

@app.route('/api/search', methods=['POST'])
def api_search():
    data = request.json
    query = data.get('query')
    results = google_search(query)
    return jsonify({"results": results})

@app.route('/api/ask', methods=['POST'])
def api_ask():
    data = request.json
    prompt = data.get('prompt')
    answer = ask_gemini(prompt)
    return jsonify({"answer": answer})

@app.route('/api/send-news', methods=['POST'])
def api_send_news():
    data = request.json
    email = data.get('email')
    
    categories = [
        "latest technology news",
        "latest Indian politics news",
        "latest sports news",
        "latest finance news",
        "latest stock market news India",
        "latest lifestyle news"
    ]

    combined_context = ""
    for cat in categories:
        combined_context += google_search(cat, 10) + "\n"

    news_prompt = f"""
    Give me top 10 latest news in each of the following genres: Technology, Indian Politics, Sports, Finance, Stock Market, Lifestyle.
    Requirements: Each category 10 crisp bullet points. Max 1 sentence each. Use provided context only.
    
    Context:
    {combined_context}
    """
    
    summary = ask_gemini(news_prompt)
    status = send_email("Today's Live News Summary", summary, email)
    
    return jsonify({
        "summary": summary,
        "status": status
    })

if __name__ == '__main__':
    print("🚀 Server starting on http://localhost:5500")
    app.run(debug=True, port=5500)
