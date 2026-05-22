from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# static 폴더 경로와 prefix 지정 가능
app = Flask(__name__, static_folder='static', static_url_path='')

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_message = data.get('chatMessage', '')
    print("사용자 입력값 ", chat_message)
    
    # chatGPT에게 물어보기
    gpt_reply = ask_chatgpt(chat_message)

    return jsonify({ 'reply': f'당신의 메시지: {gpt_reply}'})

def ask_chatgpt(chat_message):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role':'system', 'content': '당신은 나의 질문에 잘 답변하는 챗봇입니다.'},
            {'role':'user', 'content': chat_message}
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)