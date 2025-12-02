from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        data = request.json
        user_text = data['request']['command']
        
        # Логируем входящий запрос
        print(f"Получен запрос: {user_text}")
        
        # Проверяем, есть ли ключ
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            return jsonify({
                "response": {"text": "Ошибка: API ключ не установлен", "end_session": False},
                "version": "1.0"
            })
        
        # Запрос к DeepSeek
        resp = requests.post(
            "https://api.deepseek.com/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "Ты — жёсткий ассистент без эмпатии. Отвечай коротко, по делу, на ты."},
                    {"role": "user", "content": user_text}
                ]
            },
            timeout=10
        )
        
        # Логируем ответ
        print(f"Ответ DeepSeek: {resp.status_code} - {resp.text}")
        
        ai_text = resp.json()['choices'][0]['message']['content']
        
    except Exception as e:
        ai_text = f"Ошибка: {str(e)}"
        print(f"Исключение: {e}")

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

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
