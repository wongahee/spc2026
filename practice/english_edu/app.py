# 1. openai 관련 라이브러리 불러오기
# 2. 커리큘럼 페이지에서 채팅창 FE를 만든다.
# 3-1. 그 Form의 입력값을 BE에서 POST로 받아서, chatGpt api 호출하기
# 3-2. 응답받아서 다시 FE에 반환해서 결과 출력 (SSE 구현해봐도 됨)
# 4. 학년, 커리큘럼에 대해서 영화로 대화하도록 만들기
# 5. [추가] 메모리를 통해 대화 내용 컨텍스트 저장 기능

from flask import Flask, render_template, request, jsonify, session, Response

import openai
import os
from dotenv import load_dotenv

from queue import Queue

load_dotenv()

client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder='templates', static_url_path='')
app.secret_key = os.getenv("OPENAI_API_KEY")

history = []

clients = []

# 각 학년별 커리큐럼 데이터 - dict 구조의 key-value
curriculums = {
    # key: [values]
    1: ['기초 인사', '간단한 문장', '동물 이름'],
    2: ['학교 생활', '가족 소개', '자기 소개'],
    3: ['취미와 운동', '날씨 묘사', '간단한 이야기'],
    4: ['쇼핑과 가격', '음식 주문', '여행 이야기'],
    5: ['역사와 문화', '과학과 자연', '사회 이슈'],
    6: ['미래 계획', '진로 탐색', '세계 여행']
}

@app.route('/')
def home():
    return render_template('home.html', grades=curriculums.keys())

@app.route('/stream')
def stream():
    print("클라이언트 연결됨 - 누가 이 API를 듣고 있음")

    def event_stream():
        q = Queue()
        clients.append(q)

        try:
            yield f"data: 서버에 연결되었습니다.! \n\n"     # 웹 표준: event-stream으로 보낼 때, 두 줄 \n

            while True:
                message = q.get()
                if message is None:
                    break
                yield f"data: {message}\n\n"

        except GeneratorExit:
            print("클라이언트 연결 종료")

        finally:
            clients.remove(q)

    return Response(event_stream(), mimetype="text/event-stream")

@app.route('/send', methods=["POST"])
def send():
    message = request.form.get("msg", "")
    print("클라이언트 메시지:", message)

    # 사용자 요청 시 보낼 메시지
    for q in clients:
        q.put(f"서버가 받은 메시지: {message}")

    return ("", 204)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    chat_message = data.get('chatMessage', '')
    print("사용자 입력값 ", chat_message)
    
    history.append({'role':'user', 'content': chat_message})
    
    # chatGPT에게 물어보기
    gpt_reply = ask_chatgpt(chat_message)

    history.append({'role':'assistant', 'content': gpt_reply})

    return jsonify({ 'reply': f'{gpt_reply}'})

def ask_chatgpt(chat_message):
    response = client.chat.completions.create(
        model='gpt-4o-mini',
        messages=[
            {'role':'system', 'content': 'You are a friendly English teacher for Korean elementary school students.'},
            *history
        ],
        stream=True
    )
    return response.choices[0].message.content

@app.route('/grade/<int:grade>')
def grade(grade):
    if grade in curriculums:
        curriculums_index = list(enumerate(curriculums[grade]))
        return render_template('grade.html', grade=grade, grades=curriculums.keys(), curriculums=curriculums_index)
    return "해당 학년은 존재하지 않습니다.", 404

@app.route('/grade/<int:grade>/curriculum/<int:curriculum_id>')
def curriculum(grade, curriculum_id):
    session.pop('chat_history', None)

    if grade in curriculums and 0 <= curriculum_id < len(curriculums[grade]):
        curriculum_title = curriculums[grade][curriculum_id]
        return render_template('curriculum.html', grade=grade, grades=curriculums.keys(), curriculum_title=curriculum_title)
    return "해당 커리큐럼은 존재하지 않습니다.", 404


if __name__ == "__main__":
    app.run(debug=True)