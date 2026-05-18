from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import session       # 새로 배워 따로 기재한 것임

app = Flask(__name__)
app.secret_key = 'my-random-key'

users = [
    {'name': 'Alice', 'id':'alice', 'pw':'alice'},
    {'name': 'Bob', 'id':'bob', 'pw':'bob1234'},
    {'name': 'Charlie', 'id':'charlie', 'pw':'hello'}
]

@app.route('/dashboard')
def welcome():
    user = session.get('user')      # 세션 정보에서 사용자 가져옴
    return render_template('dashboard.html', name=user['name'])

@app.route('/', methods=['GET'])
def home():
    # 로그인한 적 있음
    if session.get('user'):
        return redirect(url_for('welcome'))
    
    # 로그인한 적 없음. 첫 방문 (쿠키 삭제 시, 실행됨)
    return render_template('index.html')

@app.route('/', methods=['POST'])
def login():
    if request.method == 'POST':
        # 1. 요청하여 id, pw 가져오기
        # ( )안에 input의 name 속성
        id = request.form.get('id')
        pw = request.form.get('pw')

        # 2. user DB와 사용자 매칭
        # next(결과값, 안 나왔을 시 default값)
        user = next((u for u in users if u['id'] == id and u['pw'] == pw), None)

        # 방법 2.
        # user = None
        # for u in users:
        #     if u['id'] == id and u['pw'] == pw:
        #         user = u

        # 3. 사용자 있/없 로직
        if user:
            session['user'] = user
            error = None
            return redirect(url_for('welcome'))
        else:
            error = "Invalid ID or password"

        return render_template('index.html', error=error)

# Mission 1.
# 비밀번호 변경 기능 추가
# - method -> POST로 확장
# - users 안에서 나의 비번 바꾸기
# - pw 변경 시, 나의 profile에서 확인
# - pw 변경 버튼 클릭 시, 변경확인 알려줌 (사용자 피드백)

@app.route('/profile')
def profile():
    user = session.get('user')
    # 보안 - 로그인 안됐으면, home으로 이동
    if not user:
        return redirect(url_for('home'))
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    # 키가 없을 때(로그아웃 두 번 했을 때 오류 방지)
    session.pop('user', None)
    return redirect(url_for('home'))
    
if __name__ == "__main__":
    app.run(debug=True)