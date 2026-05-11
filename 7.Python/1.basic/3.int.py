# 변수에 숫자 할당 시, int 타입 변수가 됨
x = 5
y = 3

print(x + y)
print(x - y)
print(x * y)
print(x / y)    # 나누기   (1.66667)
print(x % y)    # 나머지   (2)

print(x ** y)   # 제곱     (125)

# 다양한 진수
x = 11
print(bin(x))   # 2진수, binary = 0b   (0b1011)
print(oct(x))   # 8진수 = 0o           (0o13)
print(hex(x))   # 16진수 = 0x          (0xb) 

# 절대값
x = -10
print(x)
print(abs(x))   # 10

# 소수점
y = 4.5
print(y)
print(int(y))   # 4  (정수 구하기)

# 문자열 -> 숫자
z = "100"
print(z)
print(int(z))

# 비트 연산자 (AND, OR, NOT, XOR)
x = 5
y = 3

# 5 = 101, 3 = 011
print(x & y)    # AND   (001 = 1)
print(x | y)    # OR    (111 = 7)
print(x != y)   # NOT   (110 = 6)
print(~x)       # XOR   (11111010, 첫째 자리가 부호)

print(x << 1)   # 왼쪽으로 n만큼 이동   (101 -> 1010)
print(x >> 1)   # 오른쪽으로 n만큼 이동  (101 -> 10)