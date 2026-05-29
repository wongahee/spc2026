import json
import sys

with open("history.json", "r", encoding="utf-8") as f:
    messages = json.load(f)


ROLE = {"human": "사용자", "ai": "챗봇", "system": "시스템"}

print(f"=== {len(messages)} 메시지 ===")
for i, m in enumerate(messages, 1):
    role = ROLE.get(m.get("type"))
    content = m.get("data").get("content")
    print(f"{i:02d}. [{role:<4}] {content}")