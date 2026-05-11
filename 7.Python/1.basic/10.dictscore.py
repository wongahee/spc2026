students = {
    "김철수": 70,
    "김상수": 87,
    "이영희": 92,
    "박민경": 78,
    "최지은": 95,
    "홍길동": 89,
    "고길동": 81,
    "한지민": 83,
    "조지웅": 84,
    "백하준": 91
}

print(students)

def get_a_student(students):
    a_students = []
    for name, score in students.items():    # dict 요소 하나씩 가져옴
        if score >= 90:
            a_students.append(name)
    return a_students

print("A 등급 학생: ", get_a_student(students))