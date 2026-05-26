def test():
    print("A")  # 함수 수행할 일 1
    yield 1     # 일단 멈춤 return 1

    print("B")  # 함수 수행할 일 2
    yield 2     # 일단 멈춤 return 2

    print("C")  # 함수 수행할 일 3
    yield 3     # 일단 멈춤 return 3

x = test()

print(next(x))
# print(next(x))
# print(next(x))

try:
    while True:
        print(next(x))
        
except StopIteration:
    print("모든 데이터 사용 완료")