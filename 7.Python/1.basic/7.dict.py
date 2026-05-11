# Dictionary, 딕셔너리
# "키":"값" 으로 쌍을 이루고 있는 자료구조
# JSON과 비슷하게 생겨, 웹 서비스를 만들 때 많이 사용함

my_dict = {"name": "Alice", "age": 25, "location": "서울"}
print(my_dict)

# 개별 출력
print(my_dict["name"])
print(my_dict["age"])
print(my_dict["location"])

# 값 추가하기
my_dict["car"] = "BMW"
print(my_dict)

# 값 삭제하기
del my_dict["location"]
print(my_dict)

my_age = my_dict.pop("age")
print(my_dict)
print(my_age)

# 모든 값 지우기
my_dict.clear()
print(my_dict)

# 키: 결과값
my_squares = {x: x**2 for x in range(10)}
print(my_squares)

print(my_squares.keys())
print(my_squares.values())