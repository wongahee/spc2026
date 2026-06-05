import os
from dotenv import load_dotenv

# pip install anthropic
import anthropic

load_dotenv()

# client = openai.OpenAI()
client = anthropic.Anthropic()

message = client.messages.create(
    model="claude-haiku-4-5",   # haiku (빠름), sonnet, opus (최신, 고성능 - thinking)
    max_tokens=300,
    messages=[{
        "role": "user",
        "content": "안녕! 한 문장으로 너를 소개해줘."
    }]
)

print(message.content[0].text)