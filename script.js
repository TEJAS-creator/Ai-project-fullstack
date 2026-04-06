// API Config (Extracted from chat.py)
const GEMINI_API_KEY = "AIzaSyCyqhGHRJ__-hR56D44iZXl2qoD4FYG-hg";
const GOOGLE_API_KEY = "AIzaSyB6yBjUkLifCQd0erTDT3C8i7NlTlxPvK4";
const CX_ID = "51fd225c21c2c4c38";

// UI Selectors
const functionSelect = document.getElementById('function-select');
const mainInputContainer = document.getElementById('main-input-container');
const newsSectionContainer = document.getElementById('news-section-container');
const queryInput = document.getElementById('query-input');
const emailInput = document.getElementById('email-input');
const submitBtn = document.getElementById('submit-btn');
const newsBtn = document.getElementById('news-btn');
const loader = document.getElementById('loader');
const searchSection = document.getElementById('search-results-section');
const aiSection = document.getElementById('ai-response-section');
const searchContent = document.getElementById('search-content');
const aiContent = document.getElementById('ai-content');
const emailStatusText = document.getElementById('email-status-text');

// Switch UI based on selection
functionSelect.addEventListener('change', () => {
    if (functionSelect.value === 'news') {
        mainInputContainer.style.display = 'none';
        newsSectionContainer.style.display = 'block';
    } else {
        mainInputContainer.style.display = 'block';
        newsSectionContainer.style.display = 'none';
    }
    clearResults();
});

function clearResults() {
    searchSection.style.display = 'none';
    aiSection.style.display = 'none';
    searchContent.innerText = '';
    aiContent.innerText = '';
    emailStatusText.innerText = '';
}

// ---------------- LOCAL API INTEGRATION ----------------

async function googleSearch(query) {
    try {
        const response = await fetch('/api/search', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ query })
        });
        const data = await response.json();
        return data.results;
    } catch (error) {
        console.error("Search Error:", error);
        return "Search failed.";
    }
}

async function askGemini(prompt) {
    try {
        const response = await fetch('/api/ask', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt })
        });
        const data = await response.json();
        return data.answer;
    } catch (error) {
        console.error("Gemini Error:", error);
        return "AI analysis failed.";
    }
}

// ---------------- MAIN HANDLERS ----------------
submitBtn.addEventListener('click', async () => {
    const query = queryInput.value;
    if (!query) return;

    clearResults();
    loader.style.display = 'block';

    const selectedOption = functionSelect.value;

    if (selectedOption === 'search-only') {
        const results = await googleSearch(query);
        searchContent.innerText = results;
        searchSection.style.display = 'block';
    } 
    else if (selectedOption === 'gemini-only') {
        const answer = await askGemini(`User Question: ${query}\n(Provide a concise, reliable answer)`);
        aiContent.innerText = answer;
        aiSection.style.display = 'block';
    } 
    else if (selectedOption === 'hybrid') {
        const results = await googleSearch(query);
        const prompt = `Context:\n${results}\n\nUser Question: ${query}\nSummarize clearly using the context.`;
        const answer = await askGemini(prompt);
        
        searchContent.innerText = results;
        searchSection.style.display = 'block';
        aiContent.innerText = answer;
        aiSection.style.display = 'block';
    }

    loader.style.display = 'none';
});

// ---------------- NEWS HANDLER ----------------
newsBtn.addEventListener('click', async () => {
    const email = emailInput.value;
    if (!email) {
        alert("Please enter an email!");
        return;
    }

    clearResults();
    loader.style.display = 'block';

    try {
        const response = await fetch('/api/send-news', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email })
        });
        const data = await response.json();

        aiContent.innerText = data.summary;
        aiSection.style.display = 'block';
        emailStatusText.innerText = data.status;
        document.getElementById('email-status-section').style.display = 'block';
    } catch (error) {
        console.error("News Generation Error:", error);
        alert("News generation failed.");
    }

    loader.style.display = 'none';
});
