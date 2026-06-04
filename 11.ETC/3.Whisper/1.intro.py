# Whisper (STT, Speech To Text)
# 말 -> text

import os
import base64

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()

# 오디오를 설명하시오
def transcribe_audio(file):
    with open(file, 'rb') as af:   # audio file
        transcript = client.audio.transcriptions.create(
            model="whisper-1",
            file=af,
            response_format="text",
            language="ko"
        )
    return transcript

result = transcribe_audio("kuniv_sample.mp3")
print("결과: ", result)