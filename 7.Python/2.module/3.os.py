import os

print(os.getcwd())
# print(os.mkdir("Hello"))
# print(os.rmdir("Hello"))

os.chdir("C:/src/ai_agentic_web")

cwd = os.getcwd()

print(cwd)
print(os.listdir(cwd))