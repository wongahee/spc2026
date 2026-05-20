import sqlite3

class MyDatabase():
    def __init__(self):
        # 여러 thread 허용 옵션
        self.db = sqlite3.connect('board.sqlite', check_same_thread=False)
        self.db.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def execute(self, query, args={}):
        self.cursor.execute(query, args)

    def execute_fetch(self, query, args={}):
        self.cursor.execute(query, args)
        result = self.cursor.fetchall()
        return result
    
    def commit(self):
        self.db.commit()

def init_db():
    print("초기화 코드 추가하기")
    return

print("여기는 이 파일이 불릴 때")   # 이 부분은 출력 안됨

if __name__ == "__main__":
    print("여기는 DB 테스트")
    db = MyDatabase()

    db.execute("CREATE TABLE IF NOT EXISTS board (id INTEGER PRIMARY KEY AUTOINCREMENT, title VARCHAR(50), message VARCHAR(200))")
    db.execute("INSERT INTO board (title, message) VALUES (?, ?)", ("title1", "message1"))
    db.commit()

    result = db.execute_fetch("SELECT * FROM board")
    print(result)
    
    db.execute("DELETE FROM board")
    db.commit()