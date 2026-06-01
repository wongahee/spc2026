# 표준 LCEL로 RAG 모델 구현하기

import os
from dotenv import load_dotenv

# Chatting
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

# Embedding
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

load_dotenv()

DB_DIR = "./chroma_db"
COLLECTION_NAME = "my_rag"

# 1. 벡터 스토어 정의
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

store = Chroma(collection_name=COLLECTION_NAME, embedding_function=embeddings, persist_directory=DB_DIR)

if store._collection.count() == 0:
    docs = TextLoader("./nvme.txt", encoding="utf-8").load() \
          + TextLoader("./hbm.txt", encoding="utf-8").load()
    
    chunks = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100).split_documents(docs)
    for c in chunks:
        c.metadata["source"] = os.path.basename(c.metadata.get("source", "?"))

    store.add_documents(chunks)

retriever = store.as_retriever(search_kwargs={"k": 3})

# 2. LLM + Prompt 설계
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
prompt = ChatPromptTemplate.from_messages([
    ("system", 
        "당신은 문서 기반 QA 시스템입니다. 아래 문서만 참고해서 답변하시오. \n\n"
        "문서에 필요한 내용이 없으면 '모른다'라고 답변하시오. \n\n 문서: \n{context}\n"),
    ("user", "{question}")
])

# 3. Chaining - 표준 질의 응답을 위한 파이프 라인 설계
def format_docs(docs):
    return "\n\n".join(f"[{i}] {d.page_content}" for i, d in enumerate(docs, start=1))
    # reference 번호 붙여주기

# HW. 아래 코드에서 개별 답변 번호와 참고자료 번호 맞추기 (중복 레퍼런스 허용)
# 프롬프트 명확하게 - 답변 번호와 출처의 번호를 맞춰 답변하기
# source 출처 가져오기
def extract_source(docs):
    seen, sources = set(), []   # source를 unique하게 출력
                                # 같은 source를 여러 번 반복해서 출력하지 않기위함
    for d in docs:
        src = d.metadata.get("source", "N/A")

        if src not in seen:
            seen.add(src)
            sources.append(src)
    return sources

def retriever_and_split(inputs):
    docs = retriever.invoke(inputs["question"])

    return {
        "question": inputs["question"],
         "context": format_docs(docs),
         "sources": extract_source(docs)
    }

def append_sources(d):
    src_lines = "\n".join(f" - {s}" for s in d["sources"])
    return f"{d["answer"]}\n\n 참고문서: \n{src_lines}"

chain = (
    RunnableLambda(retriever_and_split)
    | RunnablePassthrough.assign(answer=(prompt | llm | StrOutputParser()))
    | RunnableLambda(append_sources)
)

# 4. 최종 질문
print(chain.invoke({"question": "NVMe와 HBM의 차이는?"}))