users = [
    {"name": "김민수", "age": 25, "location": "서울", "car": "현대"},
    {"name": "이지은", "age": 29, "location": "부산", "car": "기아"},
    {"name": "박서준", "age": 31, "location": "대구", "car": "BMW"},
    {"name": "최하은", "age": 22, "location": "인천", "car": "아우디"},
    {"name": "윤도윤", "age": 27, "location": "광주", "car": "테슬라"},
    {"name": "한수빈", "age": 24, "location": "대전", "car": "벤츠"},
    {"name": "이예준", "age": 33, "location": "울산", "car": "쉐보레"},
    {"name": "김채원", "age": 26, "location": "수원", "car": "토요타"},
    {"name": "오지호", "age": 30, "location": "제주", "car": "포르쉐"},
    {"name": "백유진", "age": 28, "location": "천안", "car": "볼보"}
]

def find_user_and_print(name):
    for user in users:
        # if user["name"] == name:          # 정확한 이름 찾기
        if user["name"].startswith(name):   # 성으로 찾기
                print(user)

find_user_and_print("김")
find_user_and_print("오")

def find_user_and_return(name):
     found = []         # 찾은 사용자를 담을 list

     for user in users:
          if user["name"].startswith(name):
               found.append(user)

    return found

found_users = find_user_and_return("윤")
print("찾은 사용자: ", found_users)

def find_users2():
     """이름 또는 나이를 입력받아 매칭되는 사람을 반환"""