# 2.app_story.py 폴더 set/get 합치기

from flask import Flask, session

# pip install flask-session
from flask_session import Session # 서버측에서 세션을 저장하기 위한 확장 클래스

app = Flask(__name__)
app.secret_key = 'abcd1234'
app.config['SESSION_TYPE'] = 'filesystem'       # 나의 세션을 파일, redis, memcached, mongodb 등 다양한 것을 지원
app.config['SESSION_FILE_DIR'] = './.sessions'   # 내가 정한 폴더명
app.config['SESSION_PERMANENT'] = False         # 브라우저 닫히면 삭제
app.config['SESSION_USE_SIGNER'] = True         # 세션 쿠키에 서며 사용

Session(app)    # 세션에 app 설정들 연결해줌

@app.route('/')
def main():
    if 'username' in session:
        return f"세션에서 당신의 정보를 찾았습니다. {session['username'], session['fullname'], session['hobby']}"
    
    session['username'] = 'spc2026'
    session['fullname'] = '홍길동'
    session['dob'] = '2020/05/05'
    session['hobby'] = '유투브, 쇼핑, 게임'

    return "첫 방문을 환영"

if __name__ == "__main__":
    app.run(debug=True)