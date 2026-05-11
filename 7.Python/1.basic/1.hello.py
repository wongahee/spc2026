print('Hello, Python')                  # ; (세미콜론) 사용 안 함
print('Hello, ','Python')               # , : 띄어쓰기 적용됨
                                        # + : 띄어쓰기 적용 안 됨
print("Hello, " + 'Python')             # "", '' 혼용 가능
print('"Hello, "' + "'Python'")         # 안쪽 기호만 출력 "", ''
print('"Hello, "' + "'Python'" + "!!")  # 여러 개의 문자 + 가능


# 다양한 출력 방법
num = 5
name = "홍길동"
print("Hello, {}".format(name))
print("Hello, {}. My lucky number is {}".format(name, num))
print("Hello, {0}. My lucky number is {1}".format(name, num))
print("Hello, {1}. My lucky number is {0}".format(name, num))

# C 언어의 컴퓨터 친화적 특징과는 다르게 간편함 
print("Hello, %s" % name)
print("Hello, %s" % name, end="")   # end="": 줄바꿈 안 함
print("홍길동", end="")
print("홍길동", end="\n")

multiline = """
멀티라인 - 여러 줄의 문자열
긴 주석 Zone입니다.
"""
print(multiline)