from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        user_text = data['request']['command']
        
        # Запрос к DeepSeek
        resp = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {os.getenv('DEEPSEEK_API_KEY')}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Ты — жёсткий ассистент без эмпатии. Отвечай коротко, по делу, на ты. Никаких 'пожалуйста', 'возможно', 'извини'."},
                    {"role": "user", "content": user_text}
                ]
            },
            timeout=10
        )
        ai_text = resp.json()['choices'][0]['message']['content']
    except:
        ai_text = "Ошибка. Думай сам."

    return jsonify({
        "response": {
            "text": ai_text,
            "end_session": False
        },
        "version": "1.0"
    })

@app.route('/health')
def health():
    return "OK"
