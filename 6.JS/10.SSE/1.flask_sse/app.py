# Flask에 Response를 통해 stream event 주기

from flask import Flask, send_from_directory
from flask import request, Response
from queue import Queue

app = Flask(__name__)

# 연결된 사용자 관리
clients = []

@app.route('/')
def index():
    return send_from_directory("static", "index.html")

# 클라이언트에게 응답을 보낼 API 
# SSE 방식: 상대방이 이곳을 바라보고 있으면, 이곳을 통해 내가 메시지 전송을 할 때마다 클라이언트에게 전달됨 = Event-Stream
@app.route('/stream')
def stream():
    print("클라이언트 연결됨 - 누가 이 API를 듣고 있음")

    def event_stream():
        q = Queue()
        clients.append(q)   # 사용자 목록에 새로운 사용자 추가

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


# 클라이언트가 나에게 보내는 API
@app.route('/send', methods=["POST"])
def send():
    message = request.form.get("msg", "")
    print("클라이언트 메시지:", message)

    # 사용자 요청 시 보낼 메시지
    for q in clients:
        q.put(f"서버가 받은 메시지: {message}")

    return ("", 204)    # post 사용에서 잘 받았을 때 사용

if __name__ == "__main__":
    app.run(debug=True)