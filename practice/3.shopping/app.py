from flask import Flask, send_from_directory, jsonify, request

from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder="public")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 댓글 저장 (평점, 후기를 값으로 {'rating','comment'} )
reviews = []

# --------------
# API 라우팅
# --------------

# POST
@app.route('/api/reviews', methods=['POST'])
def add_review():
    # reviews에 저장하기
    data = request.get_json()

    rating = data.get('rating')
    comment = data.get('comment')
    # print(rating, comment)

    reviews.append({
        'rating': rating, 
        'comment': comment
    })

    return jsonify({'message': 'Review added successfully'})

# GET
@app.route('/api/reviews')
def get_review():
    # reviews 반환
    return jsonify({'reviews': reviews})

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