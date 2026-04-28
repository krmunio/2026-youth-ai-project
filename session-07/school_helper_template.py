"""
🏫 AI 학교 생활 도우미 템플릿
실행: python school_helper_template.py
"""
import os
from datetime import datetime
import gradio as gr
import chromadb
from dotenv import load_dotenv, find_dotenv
from openai import OpenAI

load_dotenv(find_dotenv(usecwd=True), override=True)

APIM_BASE_URL = os.getenv("APIM_BASE_URL")
APIM_KEY = os.getenv("APIM_KEY")
MODEL = os.getenv("CHAT_MODEL", "gpt-5.4")
EMBED = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")

client = OpenAI(
    base_url=f"{APIM_BASE_URL}/{MODEL}/",
    api_key="placeholder",
    default_headers={"api-key": APIM_KEY},
)
embed_client = OpenAI(
    base_url=f"{APIM_BASE_URL}/{EMBED}/",
    api_key="placeholder",
    default_headers={"api-key": APIM_KEY},
)

# 👇 여기를 수정하세요! 최소 10개 이상
SCHOOL_NAME = "OO고등학교"
SCHOOL_DATA = [
    {"id": "info-01", "content": "여기에 학교 정보를 입력하세요", "category": "카테고리"},
    {"id": "info-02", "content": "두 번째 정보", "category": "카테고리"},
    # ... 더 추가!
]

chroma = chromadb.Client()
collection = chroma.create_collection(name="school")

def init_db():
    for doc in SCHOOL_DATA:
        emb = embed_client.embeddings.create(model=EMBED, input=[doc["content"]]).data[0].embedding
        collection.add(ids=[doc["id"]], embeddings=[emb], documents=[doc["content"]], metadatas=[{"cat": doc["category"]}])
    print(f"✅ {collection.count()}개 문서 로드 완료!")

def answer(question, history):
    q_emb = embed_client.embeddings.create(model=EMBED, input=[question]).data[0].embedding
    results = collection.query(query_embeddings=[q_emb], n_results=3)
    ctx = "\n".join([f"[{results['metadatas'][0][i]['cat']}] {results['documents'][0][i]}" for i in range(len(results['documents'][0]))])
    r = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": f"너는 {SCHOOL_NAME} AI 도우미. 문서 기반으로만 답변해. 오늘: {datetime.now().strftime('%Y년 %m월 %d일 %A')}"},
            {"role": "user", "content": f"참고:\n{ctx}\n\n질문: {question}"}
        ],
        temperature=0.3, max_completion_tokens=500
    )
    return r.choices[0].message.content

init_db()
demo = gr.ChatInterface(answer, title=f"🏫 {SCHOOL_NAME} AI 도우미", examples=["오늘 급식 뭐야?", "동아리 언제 해?"], type="messages", theme=gr.themes.Soft())

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860)
