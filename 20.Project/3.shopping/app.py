from flask import Flask, send_from_directory, jsonify

app = Flask(__name__, static_folder="public")

# 댓글 저장 (평점, 후기를 값으로 {'rating','comment'} )
reviews = []


# --------------
# API 라우팅
# --------------

# POST
@app.route('/api/reviews')
def add_review():
    # reviews에 저장하기
    return jsonify({'message': ''})

# GET
@app.route('/api/reviews')
def get_review():
    # reviews 반환
    return jsonify({'message': ''})

@app.route('/api/ai-summary')
def get_ai_summary():
    # reviews 요약
    # prompt, api 호출
    return jsonify({'message': ''})


# --------------
# 웹 서비스 라우팅
# --------------
@app.route('/')
def index():
    return send_from_directory('public', 'index.html')

if __name__ == "__main__":
    app.run(debug=True)