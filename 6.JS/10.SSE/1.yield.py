# 하고 싶은 것 - 서버에서 바뀌는 데이터를 알아서 반환
# def test():
#     return 1
#     return 2
#     return 3

# x = test()

# print(x)

# --------------

def test():
    yield 1
    yield 2
    yield 3

x = test()      # generator - 동적으로 바뀌는 데이터를 전달하는 객체

print(next(x))
print(next(x))
print(next(x))