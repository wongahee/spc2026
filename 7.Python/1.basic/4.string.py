s = "Hello, World"

print(s)
print(s.lower())
print(s.upper())
print(s.capitalize())       # 각 문장의 시작 대문자
print(s.title())            # 각 단어의 시작 대문자

s = "   Hello,   World    "
print(s.strip())            # 앞 뒤 공백 제거    (Hello,   World)
print(s.strip() + "!!")     # 공백 제거 후 합침   (Hello,   World!!)
print(s.lstrip())           # 왼쪽 공백 제거
print(s.rstrip())           # 오른쪽 공백 제거

print(s.split())            # 분할  (['Hello,', 'World'])

s = "apple banana cherry"
print(s.split())

s = "apple, banana, cherry"
print(s.split())

s = "apple,banana,cherry"
print(s.split())            # 분할 불가 - ['apple,banana,cherry']
print(s.split(","))

s_list = s.split(",")
print(s_list)
print(",".join(s_list))     # 리스트 합치기
print(".".join(s_list))
print(" ".join(s_list))

s = "Hello, World"
print(s)
print(s.startswith("Hello"))    # 시작 여부 확인   (True)
print(s.startswith("hello"))    # False
print(s.endswith("World"))      # 끝 여부 확인

print(s.find("World"))          # 7  (존재하는 위치 출력)
print(s.find("world"))          # -1 (없음)

s = "김길동"
print(s.startswith("김"))       # True
print(s.startswith("홍"))       # False