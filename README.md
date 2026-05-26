# 🤖 ARIA — AI-Powered Chatbot

A full-stack AI chatbot built with **Python Flask** + **Anthropic Claude API**, featuring a sleek dark terminal-inspired UI.

---

## 📁 Project Structure

```
ai-chatbot/
├── app.py              # Flask backend (API routes)
├── requirements.txt    # Python dependencies
├── README.md
└── static/
    └── index.html      # Frontend (HTML + CSS + JS, single file)
```

---

## ⚙️ Setup & Run

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set your Anthropic API key
```bash
# Linux / Mac
export ANTHROPIC_API_KEY="your-api-key-here"

# Windows (CMD)
set ANTHROPIC_API_KEY=your-api-key-here
```

Get a free API key at: https://console.anthropic.com

### 3. Run the server
```bash
python app.py
```

### 4. Open in browser
```
http://localhost:5000
```

---

## 🔌 API Endpoints

| Method | Endpoint      | Description                   |
|--------|---------------|-------------------------------|
| GET    | `/`           | Serves the chat UI            |
| POST   | `/api/chat`   | Send messages, get AI reply   |
| GET    | `/api/health` | Check server & API key status |
| POST   | `/api/clear`  | Confirm chat clear (stateless)|

### POST `/api/chat` — Request body
```json
{
  "messages": [
    { "role": "user", "content": "Hello, who are you?" }
  ]
}
```

### POST `/api/chat` — Response
```json
{
  "reply": "I'm ARIA, your AI assistant...",
  "usage": {
    "input_tokens": 42,
    "output_tokens": 85
  }
}
```

---

## 🛠 Tech Stack

| Layer     | Technology             |
|-----------|------------------------|
| Backend   | Python, Flask          |
| AI Model  | Anthropic Claude (Sonnet) |
| Frontend  | Vanilla HTML/CSS/JS    |
| Styling   | Custom dark theme      |

---

## 🧠 How It Works

1. User types a message in the browser
2. Frontend sends the full conversation history to `/api/chat`
3. Flask passes messages to the Anthropic API with a system prompt defining ARIA's persona
4. Claude generates a reply — returned to the browser
5. Frontend appends the reply and tracks token usage

Conversation history is stored **client-side** (in-memory JS array), keeping the backend stateless.

---

## 🚀 Environment Variables

| Variable          | Default | Description              |
|-------------------|---------|--------------------------|
| `ANTHROPIC_API_KEY` | —     | **Required** — your API key |
| `PORT`            | `5000`  | Server port              |
| `FLASK_DEBUG`     | `false` | Enable debug mode        |
