"""
🧩 꼬맨틀(Semantle) 클론 — 단어 유사도 게임
실행: python semantle_template.py
"""
import os, random
import numpy as np
import gradio as gr
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)
EMBED_MODEL = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")

# 👇 정답 단어 목록 — 자유롭게 수정하세요!
WORD_LISTS = {
    "쉬움": ["사과", "바나나", "딸기", "수박", "포도", "오렌지"],
    "보통": ["고양이", "우주", "음악", "바다", "학교", "컴퓨터"],
    "어려움": ["행복", "자유", "철학", "정의", "시간", "평화"],
}

embedding_cache = {}

def get_embedding(text):
    if text not in embedding_cache:
        r = client.embeddings.create(model=EMBED_MODEL, input=[text])
        embedding_cache[text] = r.data[0].embedding
    return embedding_cache[text]

def calculate_score(word, target):
    a, b = np.array(get_embedding(word)), np.array(get_embedding(target))
    sim = float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))
    return round(max(0, min((sim - 0.5) * 200, 100)), 2)

def color_emoji(score):
    if score >= 80: return "🟢"
    elif score >= 50: return "🟡"
    elif score >= 30: return "🟠"
    return "🔴"

class SemanticGame:
    def __init__(self):
        self.reset("보통")

    def reset(self, difficulty="보통"):
        self.target = random.choice(WORD_LISTS.get(difficulty, WORD_LISTS["보통"]))
        self.attempts = []
        self.solved = False

    def guess(self, word):
        word = word.strip()
        if not word: return "단어를 입력해주세요!", self._history()
        if self.solved: return "이미 정답! '새 게임'을 눌러주세요.", self._history()
        score = calculate_score(word, self.target)
        self.attempts.append((word, score))
        if word == self.target or score >= 95:
            self.solved = True
            return f"🎉 정답! [{len(self.attempts)}번 만에 맞춤!] 정답: {self.target}", self._history()
        return f"{color_emoji(score)} 유사도: {score}/100 (시도 #{len(self.attempts)})", self._history()

    def _history(self):
        if not self.attempts: return "아직 시도 없음"
        sorted_a = sorted(self.attempts, key=lambda x: x[1], reverse=True)
        lines = ["📊 시도 기록 (유사도순):", "─" * 30]
        for i, (w, s) in enumerate(sorted_a, 1):
            bar = "█" * int(s / 5) + "░" * (20 - int(s / 5))
            lines.append(f"{i:2d}. {color_emoji(s)} {w:<10s} {bar} {s:6.2f}")
        lines.append(f"\n총 {len(self.attempts)}회 시도")
        return "\n".join(lines)

game = SemanticGame()

def on_guess(word):
    msg, hist = game.guess(word)
    return msg, hist, ""

def on_new(diff):
    game.reset(diff)
    return f"🎮 새 게임! (난이도: {diff})", "아직 시도 없음", ""

with gr.Blocks(title="🧩 꼬맨틀", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 🧩 꼬맨틀 (Semantle Clone)\n정답 단어를 맞춰보세요!")
    with gr.Row():
        with gr.Column(scale=2):
            word_input = gr.Textbox(label="단어 입력", placeholder="단어를 입력하세요...", lines=1)
            result = gr.Textbox(label="결과", lines=2, interactive=False)
            guess_btn = gr.Button("추측하기 🎯", variant="primary")
            with gr.Row():
                diff = gr.Radio(["쉬움", "보통", "어려움"], value="보통", label="난이도")
                new_btn = gr.Button("새 게임 🔄")
        with gr.Column(scale=3):
            history = gr.Textbox(label="시도 기록", lines=18, interactive=False)

    guess_btn.click(on_guess, [word_input], [result, history, word_input])
    word_input.submit(on_guess, [word_input], [result, history, word_input])
    new_btn.click(on_new, [diff], [result, history, word_input])

if __name__ == "__main__":
    demo.launch(share=True)
