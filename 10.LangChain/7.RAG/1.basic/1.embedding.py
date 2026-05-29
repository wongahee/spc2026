# RAG (Retrieval Augmented Generation, 증강 검색 생성)

import numpy as np      # 배열/matrix를 잘 다루는 라이브러리

from dotenv import load_dotenv
from langchain_openai import OpenAIEmbeddings

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

text = "고양이가 소파 위에서 잔다."
vec = embeddings.embed_query(text)      # 위 문장으로 1536차원의 하나의 점을 찍음
# print(vec)

sentences = [
    "고양이가 소파 위에서 잔다.",
    "강아지가 침대 위에서 잔다.",
    "파이썬은 인기있는 프로그래밍 언어다."
]

vectors = embeddings.embed_documents(sentences)

def cosine_similarity(a, b):
    a, b = np.array(a), np.array(b)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))    # 코사인 유사도 계산
    # -1 ~ 1 (-1: 다른 방향, 0: 연관없음, 1: 같은 방향)

print("=== 우리의 문장 간 유사도 (1.0 = 동일함) ===")

for i, s1 in enumerate(sentences):
    for j, s2 in enumerate(sentences):
        # if i < j:
            sim = cosine_similarity(vectors[i], vectors[j])
            print(f" {sim:.4f} {s1[:20]} <-> {s2[:20]}")