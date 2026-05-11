# 외부 모듈은 설치가 필요
# 가상환경 접속 후 (conda activate 가상환경명) pip install 모듈명
# pypi.org로부터 다운받아서 나의 가상환경에 설치됨

import requests

# resp = requests.get("http://www.naver.com")
# print(resp)
# print(resp.headers)
# print(resp.text)

resp = requests.get("https://api.githubs.com")
print(resp)

if(resp.status_code == 200):
    print(resp.text)
else:
    print("해당 페이지를 가져오는데 실패했습니다. code: ", resp.status_code)