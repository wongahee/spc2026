from flask import Flask, request, jsonify, send_from_directory
import openai
import os
from dotenv import load_dotenv
import sqlite3

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# static 폴더 경로와 prefix 지정 가능
app = Flask(__name__, static_folder='static', static_url_path='')

# 대화 내용 저장 변수
# history = []
# history를 대체할 DB 코드
conn = sqlite3.connect("chatgpt.db", check_same_thread=False)
conn.row_factory = sqlite3.Row      # dict type으로 변경
cursor = conn.cursor()

def init_db():
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
init_db()   # 실행

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_message = data.get('chatMessage', '')
    print("사용자 입력값 ", chat_message)
    
    # history.append({'role':'user', 'content': chat_message})
    cursor.execute("INSERT INTO history (role, content) VALUES (?, ?)", ('user', chat_message))
    conn.commit()

    # chatGPT에게 물어보기
    gpt_reply = ask_chatgpt(chat_message)

    # history.append({'role':'assistant', 'content': gpt_reply})
    cursor.execute("INSERT INTO history (role, content) VALUES (?, ?)", ('assistant', gpt_reply))
    conn.commit()

    return jsonify({ 'reply': f'당신의 메시지: {gpt_reply}'})

def ask_chatgpt(chat_message):
    # cursor.execute("SELECT role, content FROM history")
    cursor.execute("SELECT role, content FROM history ORDER BY id DESC LIMIT 10")   # 최근 대화 10가지만 가져오기
    rows = cursor.fetchall()
    rows = rows[::-1]   # 역순
    print(rows)

    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role':'system', 'content': '당신은 나의 질문에 잘 답변하는 챗봇입니다.'},
            {'role':'user', 'content': chat_message}
            # *history    # expend
        ]
    )
    return response.choices[0].message.content


if __name__ == "__main__":
    app.run(debug=True)