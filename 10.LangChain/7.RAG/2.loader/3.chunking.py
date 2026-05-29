from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter, RecursiveCharacterTextSplitter

# 문서 파일 읽기
loader = TextLoader("./hbm.txt", encoding="utf-8")
documents = loader.load()

contents = documents[0].page_content
print(f"원본 글자수: {len(documents)}")

# 일반적으로, 1000:200 / 1500:300 / 2000:500 정도 내외로, 실제 짤린 내용을 보고 판단함
char_splitter = CharacterTextSplitter(
    separator="\n\n",
    chunk_size=500,        # 최대 갯수 설정
    chunk_overlap=100,     # 문장 짤림 방지
)

chunk_char = char_splitter.split_documents(documents)
print(f"[CharSplitter] {len(chunk_char)}")
print(f"첫 청크 글자수: {len(chunk_char[0].page_content)}")

#####################################

recur_splitter = RecursiveCharacterTextSplitter(
    chunk_size=500,
    chunk_overlap=100
)

chunks_recur = recur_splitter.split_documents(documents)
print(f"[chunks_recur] {len(chunks_recur)}")
print(f"첫 청크 글자수: {len(chunks_recur[0].page_content)}")
