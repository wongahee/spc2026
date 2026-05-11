my_list = [1, 2, 3, 4, 5]

print(my_list)
print(len(my_list))

print(my_list[0])
print(my_list[4])
# print(my_list[5])   # 오류 - 리스트 범위에 없음

print(my_list[-1])    # 역순 출력  (5)
print(my_list[-2])

# 슬라이싱
print(my_list[1:3])   # 1 ~ 2까지
print(my_list[3:5])
print(my_list[:2])    # 처음부터 1까지
print(my_list[2:])    # 2부터 끝까지

# 요소 추가
my_list.append(6)
print(my_list)

# 특정 위치에 요소 추가
my_list.insert(2, 99)   # 세번째 위치에 99 추가
print(my_list)

# 요소 삭제
my_list.remove(99)
print(my_list)

# 특정 위치에 요소 삭제
my_list.pop(3)      # pop() 시, 맨뒤에 값 삭제
print(my_list)

# 리스트 비우기
my_list.clear()
print(my_list)

my_list = [5, 2, 1, 3, 4, 7, 6, 8, 9]
print(my_list)

# 정렬
# sort() - 원본에 반영되어 정렬이 변경됨
print(my_list.sort())       
print(my_list)

# sorted() - 원본에 반영되지 않고 정렬 (복제본 생성)
my_list = [5, 2, 1, 3, 4, 7, 6, 8, 9]
new_list = sorted(my_list)
print(my_list)
print(new_list)

# copy() - 복제본 생성
copyed_list = my_list.copy()
print(copyed_list)
copyed_list.sort(reverse=True);
print(copyed_list)
print(my_list)

# List Comprehension, 리스트 컴프리헨션
print('-' * 30)

# 0 ~ 9 까지
numbers = [x for x in range(1, 10)]
print(numbers)

# 0 ~ 4 까지
numbers = [x for x in range(5)]
print(numbers)

# 제곱수
numbers = [x**2 for x in range(5)]
print(numbers)

# 짝수 출력
numbers = [x for x in range(1, 10) if x % 2 == 0]
print(numbers)

# 홀수 출력
numbers = [x for x in range(1, 10) if x % 2 == 1]
print(numbers)

# 리스트 합치기
list1 = [1, 2, 3]
list2 = [4, 5, 6]

list12 = list1 + list2
print(list12)           # [1, 2, 3, 4, 5, 6]
print(list1 * 3)        # [1, 2, 3, 1, 2, 3, 1, 2, 3]