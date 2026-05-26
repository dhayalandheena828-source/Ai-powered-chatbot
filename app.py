"""
AI-Powered Chatbot — Flask Backend
Uses the Anthropic API to power intelligent conversations.
"""

import os
import json
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import anthropic

app = Flask(__name__, static_folder="static")
CORS(app)

# ─── Anthropic client ────────────────────────────────────────────────────────
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY", ""))

SYSTEM_PROMPT = """You are ARIA (Adaptive Reasoning Intelligence Assistant), a helpful, 
friendly, and knowledgeable AI chatbot. You give clear, concise, and useful responses. 
You are conversational, warm, and occasionally use light humor. 
When asked technical questions, you explain things clearly without being condescending.
Keep responses focused and avoid being overly verbose unless the topic demands depth."""


# ─── Routes ──────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return send_from_directory("static", "index.html")


@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Accepts: { "messages": [ {"role": "user"|"assistant", "content": "..."} ] }
    Returns: { "reply": "...", "usage": {...} }
    """
    try:
        data = request.get_json(force=True)
        messages = data.get("messages", [])

        if not messages:
            return jsonify({"error": "No messages provided"}), 400

        # Validate message format
        for msg in messages:
            if msg.get("role") not in ("user", "assistant"):
                return jsonify({"error": f"Invalid role: {msg.get('role')}"}), 400
            if not isinstance(msg.get("content"), str):
                return jsonify({"error": "Message content must be a string"}), 400

        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )

        reply = response.content[0].text
        usage = {
            "input_tokens": response.usage.input_tokens,
            "output_tokens": response.usage.output_tokens,
        }

        return jsonify({"reply": reply, "usage": usage})

    except anthropic.AuthenticationError:
        return jsonify({"error": "Invalid API key. Set ANTHROPIC_API_KEY env variable."}), 401
    except anthropic.RateLimitError:
        return jsonify({"error": "Rate limit reached. Please wait a moment."}), 429
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/health")
def health():
    key_set = bool(os.environ.get("ANTHROPIC_API_KEY", ""))
    return jsonify({"status": "ok", "api_key_configured": key_set})


@app.route("/api/clear", methods=["POST"])
def clear():
    """Stateless endpoint — history lives on the client. Just confirms clear."""
    return jsonify({"status": "cleared"})


# ─── Entry point ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"\n🤖 ARIA Chatbot running on http://localhost:{port}")
    print(f"   API key configured: {bool(os.environ.get('ANTHROPIC_API_KEY'))}\n")
    app.run(host="0.0.0.0", port=port, debug=debug)
