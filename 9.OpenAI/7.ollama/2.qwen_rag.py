from dotenv import load_dotenv
import os
from openai import OpenAI
import faiss
import numpy as np
import requests

MODEL_NAME = "qwen2.5:1.5b"

load_dotenv()

client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

    
documents = [
    "한국소프트웨어저작권협회는 SPC라는 약자를 가지고 있고, 다양한 국내 기업의 SW 라이선스와 저작권을 다루는 곳입니다.",
    "홍길동은 2020년 1월 1일 생으로, 강원도 설빙산에서 태어났고, 그곳에서 호랑이를 잡아먹으며 성장하였습니다.",
    "Python은 개발 언어 중에 가장 쉽다고 하는데, 그렇게 쉬운 언어는 아닙니다."
]

def get_embedding(text):
    response = client.embeddings.create(
        input=text,
        model=MODEL_NAME
    )

    return np.array(response.data[0].embedding)

index = faiss.IndexFlatL2(1536)
doc_embeddings = np.array([get_embedding(doc) for doc in documents])
index.add(doc_embeddings)

def ask_qwen(question):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": MODEL_NAME,
            "prompt": question,
            "stream": False
        }
    )

    data = response.json()
    return data['response']

def rag_query(user_query):
    query_embedding = get_embedding(user_query)
    distance, indices = index.search(np.array([query_embedding]), k=1)
    retrieved_doc = documents[indices[0][0]]

    true_distance = np.sqrt(distance[0][0])
    similarity_score = 1 / (1 + true_distance)

    print(f"사용자 질문: {user_query}")
    print(f"검색된 문서: {retrieved_doc}")
    print(f"유사도 점수: {similarity_score:.3f}")

    if similarity_score < 0.65:
        return "해당 내용은 적합한 답변을 찾을 수 없습니다."

    prompt = f"""아래 질문을 보고 답변하시오. 아래 질문에 관련 자료가 연관이 없거나 답변할 수 없는 내용이면, 모른다고 답변하시오. 그리고 적절한 이모티콘을 사용하시오

    [사용자의 질문]
    {user_query}

    [관련 자료]
    {retrieved_doc}
    """
    
    print(f"질문과 가까운 벡터 인덱스: {indices}, 거리: {distance}")

    return ask_qwen(prompt)

query = "요즘 인기있는 영화는 무엇인가요?"

print(rag_query(query))