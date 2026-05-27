from flask import Flask, send_from_directory, request, jsonify

import os
import requests
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = Flask(__name__, static_folder="public")

@app.route('/')
def index():
    return send_from_directory("public", "index.html")

@app.route('/api/codecheck', methods=['POST'])
def code_check():
    data = request.get_json()

    url = data.get('url')

    print("입력 URL:", url)
    
    raw_url = url.replace(
        "github.com",
        "raw.githubusercontent.com"
    ).replace(
        "/blob/",
        "/"
    )

    # 실제 코드 가져오기
    res = requests.get(raw_url)
    source_code = res.text
    print(source_code)

    prompt = (
        "다음 소스코드를 보고 취약점을 분석하시오. \n"
        "각 취약점에 대해 해당 코드의 라인번호, 코드 스니펫, 취약점 설명과 개선 방안을 간단하게 설명하시오. 코드 내의 주석은 무시해도 됩니다. \n\n"
        "소스코드:\n"
        "----------\n"
        f"{source_code}\n"
        "----------\n"
    )
    print("출력확인:", prompt)

    # chatGPT API 요청
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages = [
            {"role": "system", "content": "당신은 소스코드 분석 보안 전문가입니다."},
            {"role": "user", "content": prompt}
        ]
    )
    print("출력확인:", response)
    
    chatbot_reply = response.choices[0].message.content

    return jsonify({
        "s_code": source_code,
        "result": chatbot_reply
    })
    
if __name__ == "__main__":
    app.run(debug=True)