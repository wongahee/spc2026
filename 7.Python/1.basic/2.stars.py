print('*')
print('**')
print('***')
print('****')
print('*****')

print("*" * 30)
print("=           성적표           =")
print("*" * 30)

# 왼쪽 삼각형
print('\n - 1 - ')
for i in range(1, 6):      # 1 ~ 5까지 반복
    # print(f"hello {i}")
    print("*" * i)

# 오른쪽 삼각형
print('\n - 2 - ')
for i in range(1, 6):
    print(" " * (5 - i) + "*" * i)    # 공백 + 별

    
print('\n - 3 - ')
for i in range(1, 6):
    print(" " * (5 - i) + "*" * (2 * i - 1))