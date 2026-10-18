from flask import Flask, request, jsonify
from flask_cors import CORS
from duckduckgo_search import DDGS
import wikipedia
import re

app = Flask(__name__)
CORS(app)

wikipedia.set_lang("bn")

def web_search(query):
    """ক্যাপচা ছাড়া লাইভ ওয়েব ব্রাউজিং ও সার্চ ফাংশন"""
    try:
        # প্রথমে উইকিপিডিয়া চেক করবে
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except Exception:
        pass

    # উইকিপিডিয়ায় না পেলে DuckDuckGo ব্রাউজার দিয়ে ওয়েব সার্চ করবে
    try:
        results = DDGS().text(query, max_results=2)
        if results:
            snippets = [r['body'] for r in results if 'body' in r]
            return " ".join(snippets)
    except Exception as e:
        print("Search error:", e)
    
    return None

@app.route('/')
def home():
    return "🇧🇩 Shahajjo AI Browser & Search Backend Active!"

@app.route('/api/chat', methods=['POST'])
def chat_api():
    data = request.get_json() or {}
    user_msg = data.get('message', '').strip()
    selected_lang = data.get('language', 'bn')

    if not user_msg:
        return jsonify({"success": False, "reply": "অনুগ্রহ করে কিছু লিখুন।"}), 400

    # ১. ওয়েব সার্চ ও তথ্য সংগ্রহ
    search_result = web_search(user_msg)

    if search_result:
        reply = search_result
    else:
        # ২. ব্যাকআপ স্মার্ট রেসপন্স
        if selected_lang == 'bn':
            reply = f"আমি সাহায্য! '{user_msg}' নিয়ে সুনির্দিষ্ট কোনো তথ্য ইন্টারনেটে পাইনি, তবে আপনার সহায়তায় আমি আছি।"
        elif selected_lang == 'banglish':
            reply = f"Ami Shahajjo! '{user_msg}' niye exact kono তথ্য khuje paini."
        else:
            reply = f"I am Shahajjo! Couldn't find specific web details regarding '{user_msg}'."

    return jsonify({
        "success": True,
        "reply": reply,
        "language": selected_lang
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
