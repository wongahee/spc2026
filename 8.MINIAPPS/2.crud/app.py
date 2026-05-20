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
                password TEXT NOT NULL,
                email TEXT
            )
        ''')

        # 기본 계정 추가
        cur.execute("SELECT COUNT(*) AS count FROM users")
        count = cur.fetchone()['count']
        if count == 0 :
            # 실무적으로는 비밀번호 값은 암호화하여 들어감 (pw1, pw2 ..)
            cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", ("user1", "password1", "a@example.com"))
            cur.execute("INSERT INTO users (username, password) VALUES (?, ?)", ("user2", "password2"))
            
        # 부팅 시 계정 정보 출력
        cur.execute("SELECT * FROM users")
        rows = cur.fetchall()

        print("*" * 30)
        for row in rows:
            print(row['id'], row['username'], row['password'], row['email'])  # row_factory로 딕셔너리 정의하여, 컬럼명으로 검색 가능
        print("*" * 30)

        conn.commit()
        conn.close()


@app.route('/')
def home():
    return render_template("index.html")

@app.route('/profile', methods=["POST"])
def profile_edit():
    # 사용자가 입력한 정보 가져오기
    username = request.form.get('username')
    password = request.form.get('password')
    email = request.form.get('email')

    conn = get_db_connection()
    cur = conn.cursor()

    if password:
        cur.execute("UPDATE users SET password=? WHERE username=?", (password, username))
    if email:
        cur.execute("UPDATE users SET email=? WHERE username=?", (email, username))

    conn.commit()
    flash("정상적으로 수정되었습니다.")

    # 입력한 정보 중 있는 것을 골라 수정함
    return redirect(url_for("profile"))

@app.route('/profile', methods=["GET", "POST"])
def profile():
    # DB에서 나의 정보 조회
    username = session.get('user', None)

    if username:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
    else:
        flash("다시 로그인하세요.")

        return redirect(url_for("signin"))

    return render_template("profile.html", user=user)

@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        email = request.form.get("email")

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))    # 회원가입 전, ID 중복여부 확인
        existing_user = cur.fetchone()

        if existing_user:
            flash("해당 ID는 사용할 수 없습니다.")
            conn.close()
            return redirect(url_for("signin"))
        
        cur.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", (username, password, email))
        conn.commit()
        conn.close()

        flash("회원가입이 성공적으로 완료되었습니다.")
        return redirect(url_for("login"))
        
    return render_template('signin.html')

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