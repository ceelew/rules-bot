import os
import anthropic
from flask import Flask, request, jsonify, render_template
import PyPDF2

app = Flask(__name__)

# Initialize Anthropic client
client = anthropic.Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))

# Cache the rules text so we don't re-read the PDF on every request
_rules_text = None

def load_rules():
    """Load and cache the rules from rules.pdf in the project root."""
    global _rules_text
    if _rules_text is not None:
        return _rules_text

    # Look for rules.pdf in the same directory as this file
    rules_path = os.path.join(os.path.dirname(__file__), 'rules.pdf')

    if not os.path.exists(rules_path):
        return None

    try:
        text = ""
        with open(rules_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() + "\n"
        _rules_text = text.strip()
        print(f"✅ Rules loaded: {len(_rules_text)} characters from {len(reader.pages)} pages")
        return _rules_text
    except Exception as e:
        print(f"Error reading PDF: {e}")
        return None


@app.route('/')
def index():
    rules_loaded = load_rules() is not None
    return render_template('index.html', rules_loaded=rules_loaded)


@app.route('/chat', methods=['POST'])
def chat():
    """Handle a chat message from the user."""
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({'error': 'No message provided'}), 400

    user_message = data['message'].strip()
    if not user_message:
        return jsonify({'error': 'Empty message'}), 400

    rules = load_rules()
    if rules is None:
        return jsonify({
            'response': "The rules PDF hasn't been added to the app yet. Please contact the league administrator."
        })

    # Build the system prompt with the rules embedded
    system_prompt = f"""You are a helpful Little League rules assistant. Your job is to answer questions about the league rules clearly and accurately.

You have access to the official league rulebook below. When answering:
- Base your answers strictly on the rules provided
- If a rule section number or page is identifiable, mention it
- If a situation isn't clearly covered by the rules, say so honestly
- Keep answers concise and easy to understand for coaches and parents
- If a question is outside the scope of the rulebook, say so politely

--- LEAGUE RULEBOOK ---
{rules}
--- END OF RULEBOOK ---"""

    try:
        message = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Cost-effective for this use case
            max_tokens=1024,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message}
            ]
        )
        return jsonify({'response': message.content[0].text})

    except anthropic.AuthenticationError:
        return jsonify({'error': 'Invalid API key. Check your ANTHROPIC_API_KEY environment variable.'}), 500
    except Exception as e:
        print(f"API error: {e}")
        return jsonify({'error': 'Something went wrong. Please try again.'}), 500


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
