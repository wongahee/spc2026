# Tuple, 튜플
# 읽기 전용 리스트

my_list = [1, 2, 3, 4, 5]       # 리스트
my_tuple = (1, 2, 3, 4, 5)      # 튜플

print(my_list)          # [1, 2, 3, 4, 5]
print(my_tuple)         # (1, 2, 3, 4, 5)

print(my_list[2])       # 3
print(my_tuple[2])      # 3

my_list[2] = 99
# my_tuple[2] = 99    # 오류 발생 - 읽기 전용이기 때문에 값 추가가 안 됨

print(my_list[-1])
print(my_tuple[-1])

print(my_list[3:5])     # [4, 5]
print(my_tuple[3:5])    # (4, 5)

print(my_list[0:1])     # [1]
print(my_tuple[0:1])    # (1,) -> 1개를 출력할 때 ,까지 출력

# 튜플의 값을 사용하고 싶다면 ?
my_newlist = list(my_tuple)     # list로 타입변환 후 복제본 생성
print(my_newlist)

my_newlist[2] = 88
print(my_newlist)
print(my_tuple)

my_newtuple = tuple(my_newlist)
print(my_newtuple)
my_newlist[2] = 77
print(my_newtuple)

# 튜플 언팩킹
# 튜플을 분해하는 작업
print('-' * 30)
a, b, c  = (1, 2, 3)
print(a, b, c)

a_person = ("John", 23, "Student")
print(a_person)

name, age, occ = a_person    # 따로 출력 가능
print(name)
print(age)
print(occ)