from flask import Flask, render_template, request
from flask import redirect, url_for
from flask import session, flash

from datetime import timedelta
    
import sqlite3

app = Flask(__name__)
app.secret_key = 'hello1234'
app.permanent_session_lifetime = timedelta(minutes=5)

DATABASE = 'users.sqlite3'   # '나의 파일명'

# DB 연결
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row     # 결과를 dict 포맷으로 관리
                                       # row[0] => row['id'] 형식으로 접근 가능
    return conn

# DB 초기화
def init_db():
    with app.app_context():            # flask app 초기화가 완료된 후
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL
            )
        ''')

        # 기본 계정 추가
        cur.execute("SELECT COUNT(*) AS count FROM users")
        count = cur.fetchone()['count']
        if count == 0 :
            # 실무적으로는 비밀번호 값은 암호화하여 들어감 (pw1, pw2 ..)
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user1", "password1"))
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user2", "password2"))
            
        # 부팅 시 계정 정보 출력
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        print("*" * 30)
        for row in rows:
            print(row['id'], row['username'], row['password'])  # row_factory로 딕셔너리 정의하여, 컬럼명으로 검색 가능
        print("*" * 30)

        conn.commit()
        conn.close()


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))      # 사용자 조회 쿼리
        user_data = cur.fetchone()

        conn.close()

        if user_data:
            session['user'] = username
            flash("로그인에 성공하였습니다.")
            return redirect(url_for("home"))
        else:
            flash("로그인에 실패하였습니다.")
            return redirect(url_for("login"))

    return render_template('login.html')

@app.route('/logout')
def logout():
    flash("성공적으로 로그아웃이 되었습니다.")
    session.pop("user", None)
    return redirect(url_for("home"))

if __name__ == "__main__":
    init_db()
    app.run(debug=True)      # 실무적으로는 debug=False