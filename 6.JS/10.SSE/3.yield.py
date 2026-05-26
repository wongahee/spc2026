def numbers():
    for i in range(10000):
        yield i             # for문 한 번 수행 후 대기


for num in numbers():
    print(num)
    if num >= 5:
        break