# 🚀 2026 유스AI프로젝트:D — 커리큐럼 가이드

> P.I.N.E. 2기 '나만의 AI 서비스 : PINE A+'

## 프로그램 개요

**대상**: 17~19세 청소년 20명 (AI 분야 진로 확정 청소년)
**기간**: 4회차 ~ 9회차 (5월 ~ 8월)  
**실습 환경**: GitHub Codespaces + Jupyter Notebook  
**기술 스택**: Python, Azure OpenAI SDK, Microsoft Agent Framework (MAF)  

---

## 실습 환경 세팅 가이드

### GitHub Codespaces 구성

```
📁 2026-youth-ai-project/
├── 📁 .devcontainer/              # Codespace 환경 설정
├── 📁 session-04-ai-basics/       # 4회차 — AI 기초 이론
│   ├── slides/                    #   PPT 자료 (.pptx)
│   ├── notebooks/                 #   실습 노트북 (.ipynb)
│   └── homework/                  #   숙제 자료
├── 📁 session-05-ai-programming/  # 5회차 — AI 프로그래밍 실습
│   ├── slides/
│   ├── notebooks/
│   └── homework/
├── 📁 session-06-agent-v1/        # 6회차 — AI 에이전트 개발 1차
│   ├── slides/
│   ├── notebooks/
│   └── homework/
├── 📁 session-07-agent-v2/        # 7회차 — AI 에이전트 개발 2차
│   ├── slides/
│   ├── notebooks/
│   └── homework/
├── 📁 session-08-hackathon/       # 8회차 — 해커톤
│   ├── guides/                    #   디자인 싱킹 가이드, 평가 기준
│   └── templates/                 #   프로젝트 템플릿
├── 📁 assets/                     # 공용 이미지/자료
├── AI_커리큘럼_개괄자료.md
├── pyproject.toml
└── README.md
```

### devcontainer.json

> 실제 설정은 [`.devcontainer/devcontainer.json`](.devcontainer/devcontainer.json)을 참고하세요.

```json
{
  "name": "2026-youth-ai-project",
  "image": "mcr.microsoft.com/devcontainers/python:3.12",
  "postCreateCommand": "bash .devcontainer/post-create.sh",
  "customizations": {
    "vscode": {
      "extensions": [
        "ms-python.python",
        "ms-toolsai.jupyter",
        "GitHub.copilot",
        "GitHub.copilot-chat"
      ]
    }
  },
  "forwardPorts": [7860, 8888]
}
```

### 패키지 관리 (uv + pyproject.toml)

> 의존성은 [`pyproject.toml`](pyproject.toml)에서 관리합니다. `uv sync`으로 설치합니다.

```toml
[project]
dependencies = [
    "matplotlib>=3.7",
    "openai>=1.0",
    "python-dotenv>=1.0",
    "ipykernel>=6.0",
    "gradio>=6.0",
    "chromadb>=1.0",
    "tiktoken>=0.12",
    "numpy",
    "pandas>=3.0",
    "requests>=2.33",
    "beautifulsoup4>=4.14",
]
```

---

## 📅 회차별 상세 계획

---

## 4회차 (5/16) — AI 기초 이론

### 🎯 학습 목표
- 생성형 AI(LLM)의 작동 원리 이해
- Transformer, 토큰화, 프롬프트 엔지니어링 개념 학습
- ChatGPT/GPT 활용 사례 체험

### 📊 PPT 구성 (권장 30~40슬라이드)

| 섹션 | 내용 | 시간 |
|------|------|------|
| 1. AI란 무엇인가? | AI 역사 타임라인, 전통 AI vs 생성형 AI 비교 | 15분 |
| 2. LLM 작동 원리 | 토큰화 시연, Transformer 직관적 설명(번역기 비유), Attention 메커니즘 | 30분 |
| 3. 프롬프트 엔지니어링 | Zero-shot, Few-shot, Chain-of-Thought, 시스템 프롬프트 역할 | 30분 |
| 4. 활용 사례 & 토론 | 텍스트 생성, 요약, 번역, 코드 생성 데모 / 그룹 토론 | 30분 |
| 5. 실습 & 과제 안내 | Azure OpenAI Playground 체험 | 15분 |

### 🛠️ 수업 중 실습

**실습 1: 토큰화 체험하기**
- OpenAI Tokenizer(https://platform.openai.com/tokenizer) 사용
- 한국어 vs 영어 토큰 수 비교
- "왜 한국어가 더 많은 토큰을 사용하는가?" 토론

**실습 2: 프롬프트 배틀**
- 같은 질문에 대해 다양한 프롬프트 전략 비교
- 예: "삼국지를 요약해줘" vs "당신은 역사 전문가입니다. 고등학생이 이해할 수 있도록 삼국지의 핵심 사건 5가지를 시간순으로 정리해주세요."
- 모둠별로 최고의 프롬프트를 만들어 발표

**실습 3: AI 활용 사례 그룹 토론**
- 모둠별로 일상/학교 생활에서 AI를 활용할 수 있는 사례 브레인스토밍
- 과제 도우미 만들기 아이디어 구상

### 📝 숙제 — "프롬프트 마스터 챌린지"

> **미션**: 5가지 다른 주제(과학, 수학, 역사, 영어, 일상)에 대해 각각 "나쁜 프롬프트"와 "좋은 프롬프트"를 작성하고, 결과를 비교 분석하는 보고서 작성

**제출물**: 노션 또는 구글 독스에 스크린샷과 함께 정리  
**보너스**: 프롬프트 체이닝(여러 번 이어지는 대화)으로 복잡한 문제를 해결한 사례 추가

---

## 5회차 (5/30) — AI 프로그래밍 실습

### 🎯 학습 목표
- Azure OpenAI Python SDK 설치 및 설정
- API 키/엔드포인트 설정 후 첫 Completion 실행
- 프롬프트로 텍스트 생성, 이미지 분석, Q&A 봇 만들기

### 📊 PPT 구성

| 섹션 | 내용 | 시간 |
|------|------|------|
| 1. 환경 세팅 | Codespace 접속, SDK 설치, .env 설정 | 20분 |
| 2. 첫 API 호출 | chat.completions.create() 실행, 파라미터(temperature, max_tokens 등) 실험 | 30분 |
| 3. 코드 예시 실습 | 텍스트 생성, 이미지 분석, Q&A 봇 | 40분 |
| 4. 나만의 봇 만들기 | 학생별 시스템 프롬프트 커스터마이징 | 30분 |

### 🛠️ 수업 중 실습

**실습 1: Hello, AI! — 첫 API 호출**
```python
from openai import OpenAI

API_KEY = "<학생별 API 키>"

client = OpenAI(
    api_key="placeholder",
    base_url="https://apim-foundryproxy-dev.azure-api.net/foundry/gpt-5.4/",
    default_headers={"api-key": API_KEY},
)

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[
        {"role": "system", "content": "너는 친절한 고등학교 선생님이야."},
        {"role": "user", "content": "광합성이 뭐야? 쉽게 설명해줘."}
    ],
    temperature=0.7
)
print(response.choices[0].message.content)
```

**실습 2: Temperature 실험실**
- temperature 0.0 vs 0.5 vs 1.0 으로 같은 질문 반복
- 결과 차이를 표로 정리하고 토론

**실습 3: "고등학생 공부 플랜 생성" 봇 만들기**
- 학생별 노트북에서 시스템 프롬프트 설정
- 시험 과목, 남은 일수를 입력하면 공부 계획을 짜주는 봇 제작

### 📝 숙제 — "나만의 AI 챗봇 만들기" 🤖

> **미션**: 특정 페르소나를 가진 챗봇을 만들고, Gradio로 간단한 웹 UI를 입혀서 공유

**아이디어 예시**:
- 🎮 게임 공략 도우미 봇 (특정 게임의 공략법을 알려주는 봇)
- 📚 독서 추천 봇 (취향을 물어보고 책을 추천)
- 🍽️ 오늘 뭐 먹지? 봇 (위치, 예산, 기분에 따라 메뉴 추천)
- 🎵 노래 추천 봇 (기분에 따라 플레이리스트 제안)
- 🐱 고양이 성격 분석 봇 (고양이 행동을 설명하면 성격 분석)

**Gradio 기본 템플릿**:
```python
import gradio as gr

def chat(message, history):
    response = client.chat.completions.create(
        model="gpt-5.4",
        messages=[
            {"role": "system", "content": "여기에 페르소나 입력"},
            *[{"role": m["role"], "content": m["content"]} for m in history],
            {"role": "user", "content": message}
        ]
    )
    return response.choices[0].message.content

demo = gr.ChatInterface(chat, title="나만의 AI 봇")
demo.launch()
```

**제출물**: GitHub 레포 링크 + 스크린샷  
**보너스**: 대화 기록 저장 기능 추가

---

## 6회차 (7/11) — AI 에이전트 개발 1차

### 🎯 학습 목표
- 도구(Tools) 개념 이해
- 코드 인터프리터, 웹 검색 도구 연동
- ReAct(Reason+Act) 패턴 학습 및 구현

### 📊 PPT 구성

| 섹션 | 내용 | 시간 |
|------|------|------|
| 1. 에이전트란? | LLM + 도구 = 에이전트, 기존 챗봇과의 차이 | 15분 |
| 2. 도구(Tools) 만들기 | Function Calling 개념, 도구 정의 방법 | 30분 |
| 3. ReAct 패턴 | Think → Act → Observe 루프 설명 | 20분 |
| 4. 실습: 수학 에이전트 | 계산기 + 그래프 도구를 가진 에이전트 빌드 | 40분 |
| 5. 응용 & 과제 안내 | 웹 검색 에이전트 시연 | 15분 |

### 🛠️ 수업 중 실습

**실습 1: 나만의 도구(Tool) 만들기**
```python
tools = [
    {
        "type": "function",
        "function": {
            "name": "calculate",
            "description": "수학 계산을 수행합니다",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "계산할 수식 (예: 2+3*4)"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]
```

**실습 2: 수학 문제 해결 에이전트 빌드**
- 사칙연산 + 그래프 그리기 도구를 가진 에이전트
- "y = 2x + 3 그래프를 그려줘" → matplotlib으로 그래프 생성
- "123 * 456 + 789는?" → 계산기 도구 호출

**실습 3: 웹 검색 에이전트**
- requests + BeautifulSoup으로 간단한 웹 검색 도구 구현
- "오늘 서울 날씨 알려줘" → 웹 검색 → 결과 요약

### 📝 숙제 — "꼬맨틀(Semantle) 클론 만들기" 🧩

> **미션**: 단어 유사도 기반 게임을 AI 도구로 구현!

**게임 규칙**:
1. 정답 단어를 하나 정함
2. 사용자가 단어를 입력하면 정답과의 유사도(0~100)를 반환
3. 유사도가 높을수록 정답에 가까움
4. 최소 시도로 정답 맞추기!

**구현 가이드**:
```python
from openai import OpenAI

def get_similarity(word1, word2):
    """두 단어의 임베딩 유사도를 계산 (임베딩 API 필요)"""
    response = client.embeddings.create(
        model="text-embedding-3-large",
        input=[word1, word2]
    )
    import numpy as np
    emb1 = np.array(response.data[0].embedding)
    emb2 = np.array(response.data[1].embedding)
    similarity = np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2))
    return round(similarity * 100, 2)

# 게임 루프
target = "고양이"
print("🧩 꼬맨틀 게임 시작! 정답 단어를 맞춰보세요.")
for attempt in range(1, 21):
    guess = input(f"[{attempt}번째 시도] 단어 입력: ")
    score = get_similarity(guess, target)
    print(f"   유사도: {score}/100")
    if score > 95:
        print(f"🎉 정답! {attempt}번 만에 맞췄습니다!")
        break
```

**보너스 과제**:
- Gradio UI 추가해서 웹에서 플레이 가능하게 만들기
- 힌트 기능 추가 (유사도 80 이상인 단어 하나 알려주기)
- 리더보드(최소 시도 횟수 랭킹) 기능

---

## 7회차 (7/18) — AI 에이전트 개발 2차

### 🎯 학습 목표
- 멀티 에이전트 워크플로(GroupChatBuilder) 이해
- 메모리/컨텍스트 관리 방법
- RAG(Retrieval-Augmented Generation) 구현

### 📊 PPT 구성

| 섹션 | 내용 | 시간 |
|------|------|------|
| 1. 멀티 에이전트 | 에이전트 간 협업, 역할 분담 개념 | 20분 |
| 2. 메모리 관리 | 대화 히스토리, 요약 메모리, 벡터 메모리 | 20분 |
| 3. RAG 개념 | 검색 + 생성, 임베딩, 벡터 DB 개념 | 25분 |
| 4. 실습: RAG 에이전트 | ChromaDB + OpenAI로 나만의 지식 베이스 구축 | 40분 |
| 5. 해커톤 준비 안내 | 팀 빌딩, 아이디어 브레인스토밍 | 15분 |

### 🛠️ 수업 중 실습

**실습 1: 메모리가 있는 챗봇**
```python
from collections import deque

class MemoryChat:
    def __init__(self, max_memory=10):
        self.memory = deque(maxlen=max_memory)
    
    def chat(self, user_input):
        self.memory.append({"role": "user", "content": user_input})
        response = client.chat.completions.create(
            model="gpt-5.4",
            messages=[
                {"role": "system", "content": "이전 대화를 기억하며 답변해."},
                *list(self.memory)
            ]
        )
        reply = response.choices[0].message.content
        self.memory.append({"role": "assistant", "content": reply})
        return reply
```

**실습 2: 나만의 RAG 시스템 구축**
- 교과서 PDF 또는 위키피디아 문서를 청크로 분할
- ChromaDB에 임베딩 저장
- 질문 → 관련 문서 검색 → LLM에게 답변 생성

**실습 3: 멀티 에이전트 토론 시뮬레이션**
- "찬성" 에이전트와 "반대" 에이전트가 주제에 대해 토론
- "사회자" 에이전트가 토론을 정리

### 📝 숙제 — "AI 학교 생활 도우미" 🏫

> **미션**: RAG를 활용해서 학교 정보를 기반으로 답변하는 에이전트 만들기

**구현 방향**:
- 학교 학칙, 시간표, 급식 메뉴, 동아리 정보 등을 벡터 DB에 저장
- "내일 급식 뭐야?", "수학 동아리 활동일이 언제야?" 같은 질문에 답변
- 도구를 추가하여 시간표 조회, 급식 메뉴 검색 등 기능 구현

**보너스**: 여러 에이전트를 조합해 "학습 코치 + 일정 관리 + 급식 안내"를 한번에 처리

---

## 8회차 (8/8) — 해커톤 (디자인 싱킹 + 개발)

### 🎯 목표
- 디자인 싱킹으로 실제 문제 정의
- 팀별 AI 에이전트 프로토타입 개발
- Microsoft 전문가 멘토링 및 피드백

### ⏰ 타임테이블 (10:00~17:00)

| 시간 | 활동 | 상세 |
|------|------|------|
| 10:00~11:00 | 디자인 싱킹 워크숍 | Empathize → Define → Ideate |
| 11:00~11:30 | 팀 빌딩 & 아이디어 선정 | 모둠 구성, Copilot 활용 프로토타이핑 |
| 11:30~12:30 | 프로토타입 스케치 | 와이어프레임, 유저 플로우 설계 |
| 12:30~13:30 | 점심 | - |
| 13:30~15:30 | 개발 스프린트 | 팀별 코딩, 멘토 서포트 |
| 15:30~16:00 | 멘토링 세션 | Microsoft 직원 피드백 |
| 16:00~16:30 | 데모 발표 | 팀별 3분 발표 + 2분 Q&A |
| 16:30~17:00 | 시상 & 피드백 | 우수팀 선정, 전문가 피드백 |

### 💡 해커톤 주제 아이디어

1. **개인화 학습 코치**: 학생의 약점을 분석하고 맞춤 문제를 출제하는 에이전트
2. **진로 상담 AI**: 적성검사 + 진로 정보 RAG로 진로 추천
3. **학교 분실물 매칭**: 분실물 사진/설명을 등록하면 AI가 매칭
4. **급식 리뷰 & 영양 분석**: 급식 사진 → 메뉴 인식 → 영양 정보 + 리뷰
5. **시험 대비 퀴즈 생성기**: 교과서 업로드 → 자동 퀴즈 생성 → 오답 해설

---

## 9회차 (8/22) — 파인콘 (P.I.N.E CON) AI 축제

### 프로그램 구성
- 1부: 개막 및 현직자 강연
- 2부: AI 체험 부스
- 3부: 데모데이 및 시상식

---

## 🎮 추가 재미있는 실습 아이디어 모음

### 초급 (4~5회차 숙제용)

| 이름 | 설명 | 난이도 |
|------|------|--------|
| 🎭 AI 성격 테스트 | MBTI 질문을 AI가 분석해서 성격 유형 판별 | ⭐ |
| 📝 AI 독후감 작성기 | 책 제목만 입력하면 다양한 스타일의 독후감 생성 | ⭐ |
| 🌏 AI 여행 플래너 | 예산, 기간, 취향 입력 → 여행 코스 추천 | ⭐⭐ |
| 🎤 AI 래퍼 | 주제를 입력하면 한국어 랩 가사 생성 | ⭐ |
| 📊 수행평가 도우미 | 주제 입력 → 개요 → 본문 → 참고문헌 자동 생성 | ⭐⭐ |

### 중급 (6~7회차 숙제용)

| 이름 | 설명 | 난이도 |
|------|------|--------|
| 🧩 AI 스무고개 | AI가 사물을 정하고 학생이 질문, 또는 반대로 | ⭐⭐ |
| 🎨 AI 밈 생성기 | 상황 설명 → 적절한 밈 텍스트 + 이미지 프롬프트 생성 | ⭐⭐ |
| 🕵️ AI 탐정 게임 | AI가 미스터리 시나리오를 생성, 학생이 단서 수집하며 범인 추리 | ⭐⭐⭐ |
| 📰 AI 뉴스 팩트체커 | 뉴스 URL 입력 → 웹 검색으로 교차 검증 → 신뢰도 판별 | ⭐⭐⭐ |
| 🎵 AI DJ | 기분/상황 설명 → Spotify API 연동하여 플레이리스트 추천 | ⭐⭐⭐ |

### 고급 (해커톤 준비용)

| 이름 | 설명 | 난이도 |
|------|------|--------|
| 🏫 AI 학교 위키 | 학교 정보를 RAG로 구축, 신입생 안내 봇 | ⭐⭐⭐ |
| 🤖 AI 토론 심판 | 두 사람의 토론을 분석하고 논리적 오류 지적 | ⭐⭐⭐⭐ |
| 📱 AI 인스타 캡션 | 사진 분석 → 상황에 맞는 캡션 + 해시태그 생성 | ⭐⭐⭐ |
| 🎮 AI 텍스트 RPG | 멀티 에이전트로 NPC 구현, 스토리 분기 자동 생성 | ⭐⭐⭐⭐ |
| 🧬 AI 과학 실험 도우미 | 실험 주제 → 가설 → 실험 설계 → 결과 분석 도움 | ⭐⭐⭐⭐ |

---

## 💡 수업 운영 팁

### 모둠 활동 구성
- 4인 1모둠 권장 (코더 2명 + 기획 1명 + 발표 1명)
- 회차별로 역할 로테이션
- 모둠별 GitHub Organization 또는 Team 활용

### 평가 기준 (숙제)
- **완성도** (40%): 코드가 정상 작동하는가
- **창의성** (30%): 독창적인 아이디어인가
- **문서화** (20%): README, 주석이 잘 작성되었는가
- **발표** (10%): 결과를 잘 설명할 수 있는가

### 학생 동기 부여
- 매 회차 "Best Homework" 시상 (소정의 상품)
- 숙제 갤러리 운영 (우수작을 모아 전시)
- 해커톤 우수팀에 Microsoft 본사 견학 또는 인턴십 연결 기회

### ⚠️ 주의사항
- API 키 보안: 절대 코드에 하드코딩하지 않도록 교육 (.env 파일 사용)
- 비용 관리: Azure 리소스 사용량 제한 설정
- 윤리 교육: AI 편향, 할루시네이션, 저작권 문제 매 회차 언급
- 안전한 사용: 개인정보를 AI에 입력하지 않도록 주의

---

## 📦 회차별 숙제 요약

| 회차 | 숙제 | 핵심 스킬 | 제출 형태 |
|------|------|-----------|-----------|
| 4→5 | 프롬프트 마스터 챌린지 | 프롬프트 엔지니어링 | 문서 |
| 5→6 | 나만의 AI 챗봇 (Gradio) | API 호출, UI 구현 | GitHub 링크 |
| 6→7 | 꼬맨틀 클론 만들기 | 임베딩, Function Calling | GitHub 링크 |
| 7→8 | AI 학교 생활 도우미 | RAG, 멀티 에이전트 | GitHub 링크 |

---

## 📚 참고 자료

- [Azure OpenAI 공식 문서](https://learn.microsoft.com/azure/ai-services/openai/)
- [Microsoft Agent Framework 문서](https://github.com/microsoft/agent-framework)
- [Prompt Engineering Guide](https://www.promptingguide.ai/kr)
- [GitHub Codespaces 가이드](https://docs.github.com/codespaces)
- [Gradio 공식 문서](https://www.gradio.app/docs)
- [ChromaDB 가이드](https://docs.trychroma.com/)
