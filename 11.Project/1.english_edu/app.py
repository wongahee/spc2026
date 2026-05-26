# 1. openai 관련 라이브러리 불러오기
# 2. 커리큘럼 페이지에서 채팅창 FE를 만든다.
# 3-1. 그 Form의 입력값을 BE에서 POST로 받아서, chatGpt api 호출하기
# 3-2. 응답받아서 다시 FE에 반환해서 결과 출력 (SSE 구현해봐도 됨)
# 4. 학년, 커리큘럼에 대해서 영화로 대화하도록 만들기
# 5. [추가] 메모리를 통해 대화 내용 컨텍스트 저장 기능

from flask import Flask, render_template

app = Flask(__name__)

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

@app.route('/grade/<int:grade>')
def grade(grade):
    if grade in curriculums:
        curriculums_index = list(enumerate(curriculums[grade]))
        return render_template('grade.html', grade=grade, grades=curriculums.keys(), curriculums=curriculums_index)
    return "해당 학년은 존재하지 않습니다.", 404

@app.route('/grade/<int:grade>/curriculum/<int:curriculum_id>')
def curriculum(grade, curriculum_id):
    if grade in curriculums and 0 <= curriculum_id < len(curriculums[grade]):
        curriculum_title = curriculums[grade][curriculum_id]
        return render_template('curriculum.html', grade=grade, grades=curriculums.keys(), curriculum_title=curriculum_title)
    return "해당 커리큐럼은 존재하지 않습니다.", 404

if __name__ == "__main__":
    app.run(debug=True)