# 🌲 2026 유스AI프로젝트:D

> P.I.N.E. 2기 '나만의 AI 서비스 : PINE A+'

**대상**: 17~19세 청소년 20명 (AI 분야 진로 확정 청소년)  
**기간**: 4회차 ~ 9회차 (5월 ~ 8월)
**실습 환경**: GitHub Codespaces + Jupyter Notebook  
**기술 스택**: Python, Azure OpenAI SDK, Microsoft Agent Framework (MAF)  
**협력**: KB데이타시스템 × 한국 Microsoft  

---

## 📅 회차별 요약

| 회차 | 날짜 | 주제 | 핵심 내용 | 숙제 |
|------|------|------|-----------|------|
| 4회차 | 5/16 | AI 기초 이론 | Transformer, 토큰화, 프롬프트 엔지니어링 | 프롬프트 마스터 챌린지 |
| 5회차 | 5/30 | AI 프로그래밍 실습 | Azure OpenAI SDK, API 호출, Temperature 실험 | 나만의 AI 챗봇 (Gradio) |
| 6회차 | 7/11 | AI 에이전트 개발 1차 | Function Calling, ReAct 패턴, 도구 연동 | 꼬맨틀 클론 만들기 |
| 7회차 | 7/18 | AI 에이전트 개발 2차 | 멀티 에이전트, RAG, 벡터 DB | AI 학교 생활 도우미 |
| 8회차 | 8/8  | 해커톤 | 디자인 싱킹 + 팀별 AI 에이전트 프로토타입 개발 | - |
| 9회차 | 8/22 | P.I.N.E CON AI 축제 | 데모데이, 시상식, 현직자 강연 | - |

> 상세 커리큘럼은 [`AI_커리큘럼_개괄자료.md`](AI_커리큘럼_개괄자료.md)를 참고하세요.

---

## 📁 프로젝트 구조

```
2026-youth-ai-project/
├── session-04-ai-basics/          # 4회차 — AI 기초 이론
│   ├── slides/                    #   PPT 자료 (.pptx)
│   ├── notebooks/                 #   실습 노트북 (.ipynb)
│   └── homework/                  #   숙제 자료
│
├── session-05-ai-programming/     # 5회차 — AI 프로그래밍 실습
│   ├── slides/
│   ├── notebooks/
│   └── homework/
│
├── session-06-agent-v1/           # 6회차 — AI 에이전트 개발 1차
│   ├── slides/
│   ├── notebooks/
│   └── homework/
│
├── session-07-agent-v2/           # 7회차 — AI 에이전트 개발 2차
│   ├── slides/
│   ├── notebooks/
│   └── homework/
│
├── session-08-hackathon/          # 8회차 — 해커톤
│   ├── guides/                    #   디자인 싱킹 가이드, 평가 기준
│   └── templates/                 #   프로젝트 템플릿
│
├── .devcontainer/                 # Codespace 환경 설정
├── assets/                        # 공용 이미지/자료
├── pyproject.toml                 # uv 패키지 의존성
├── uv.lock                        # 패키지 락 파일
└── AI_커리큘럼_개괄자료.md          # 커리큘럼 전체 개괄
```

### 4~7회차 자료 올리기

각 회차 폴더에 아래와 같이 자료를 추가합니다:

- **`slides/`** — 수업용 PPT 파일 (`.pptx`)
- **`notebooks/`** — Jupyter 실습 노트북 (`.ipynb`)
- **`homework/`** — 숙제 안내 및 템플릿

---

## 🛠️ 실습 환경

| 항목 | 값 |
|------|-----|
| Azure OpenAI 인증 | APIM 프록시 (`api-key` 헤더) |
| APIM Endpoint | `https://apim-foundryproxy-dev.azure-api.net/foundry/gpt-5.4/` |
| 사용 모델 | gpt-5.4 |
| 노출 API | Chat Completions, Responses |
| Python 환경 | uv + Python 3.12 |

### 빠른 테스트

```python
from openai import OpenAI

API_KEY = "<API 키>"

client = OpenAI(
    api_key="placeholder",
    base_url="https://apim-foundryproxy-dev.azure-api.net/foundry/gpt-5.4/",
    default_headers={"api-key": API_KEY},
)

response = client.chat.completions.create(
    model="gpt-5.4",
    messages=[{"role": "user", "content": "안녕! 자기소개 해줘."}],
    max_completion_tokens=200,
)
print(response.choices[0].message.content)
```