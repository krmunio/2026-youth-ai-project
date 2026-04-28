# 5회차 — AI 프로그래밍 실습 (5/30 토, 10:00~13:00)

## 🎯 학습 목표

1. Azure OpenAI Python SDK 설치 및 설정
2. API 키/엔드포인트 설정 후 첫 Completion 실행
3. 프롬프트로 텍스트 생성, 이미지 분석, Q&A 봇 만들기

## 📊 강의 흐름

| 섹션 | 내용 | 시간 |
|------|------|------|
| 환경 세팅 | Codespace 접속, SDK 설치, `.env` 설정 | 20분 |
| 첫 API 호출 | `chat.completions.create()`, 파라미터 실험 | 30분 |
| 코드 예시 실습 | 텍스트 생성, 이미지 분석, Q&A 봇 | 40분 |
| 나만의 봇 만들기 | 시스템 프롬프트 커스터마이징 + Gradio UI | 30분 |

## 🛠️ 실습 파일

- `practice.ipynb` — 첫 API 호출, temperature 실험, 공부 플랜 생성기, 대화형 챗봇, Gradio UI

## 🔑 핵심 코드 패턴

```python
# 기본 패턴
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "역할 설정"},
        {"role": "user", "content": "사용자 질문"}
    ]
)
answer = response.choices[0].message.content
```

---

## 📝 숙제: 나만의 AI 챗봇 만들기

### 미션

특정 **페르소나**를 가진 챗봇을 만들고, Gradio로 웹 UI를 입혀서 공유합니다.

**아이디어 예시:** 게임 공략 봇 / 독서 추천 봇 / 메뉴 추천 봇 / 진로 멘토 봇 / 자유 주제

### 필수 구현

1. 적절한 시스템 프롬프트 (페르소나 + 행동 규칙)
2. 대화 기록 유지 (이전 대화를 기억)
3. Gradio 웹 UI

### 템플릿

`chatbot_template.py`를 기반으로 코드를 완성하세요.

### 제출

- GitHub 레포에 코드 업로드 + README.md (봇 이름, 설명, 스크린샷 2~3장)
