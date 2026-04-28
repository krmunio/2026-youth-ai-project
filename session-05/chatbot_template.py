"""
🤖 나만의 AI 챗봇 템플릿 — 이 파일을 수정해서 나만의 챗봇을 만들어보세요!
실행: python chatbot_template.py
"""
import os
import gradio as gr
from datetime import datetime
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

api_key = os.getenv("APIM_SUBSCRIPTION_KEY") or os.getenv("AZURE_OPENAI_KEY")
client = AzureOpenAI(
    api_key=api_key,
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
    default_headers={"Ocp-Apim-Subscription-Key": api_key},
)
MODEL = os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4.1-mini")

# ============================================================
# 👇 여기를 수정하세요!
# ============================================================
BOT_NAME = "나만의 봇"

SYSTEM_PROMPT = """
너는 [여기에 페르소나를 입력하세요].
규칙:
- [규칙 1]
- [규칙 2]
"""

EXAMPLES = ["예시 질문 1", "예시 질문 2", "예시 질문 3"]

# ============================================================
chat_log = []

def respond(message, history):
    if message.strip() == "/reset":
        history.clear()
        return "🔄 대화가 초기화되었습니다!"
    messages = [{"role": "system", "content": SYSTEM_PROMPT}]
    for h in history:
        messages.append(h)
    messages.append({"role": "user", "content": message})
    try:
        response = client.chat.completions.create(
            model=MODEL, messages=messages, temperature=0.8, max_tokens=800
        )
        reply = response.choices[0].message.content
        chat_log.append({"time": datetime.now().isoformat(), "user": message, "bot": reply})
        return reply
    except Exception as e:
        return f"❌ 오류: {e}"

with gr.Blocks(theme=gr.themes.Soft()) as demo:
    gr.ChatInterface(
        respond, title=f"🤖 {BOT_NAME}",
        description=f"안녕! 나는 {BOT_NAME}이야. 무엇이든 물어봐!",
        examples=EXAMPLES,
    )

if __name__ == "__main__":
    demo.launch(share=True)
