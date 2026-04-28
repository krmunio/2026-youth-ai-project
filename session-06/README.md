# 6회차 — AI 에이전트 개발 1차 (7/11 토, 10:00~13:00)

## 🎯 학습 목표

1. 도구(Tools)와 Function Calling 개념 이해
2. 코드 인터프리터, 웹 검색 도구 연동
3. ReAct(Reason+Act) 패턴 학습 및 구현

## 📊 강의 흐름

| 섹션 | 내용 | 시간 |
|------|------|------|
| 에이전트란? | LLM + 도구 = 에이전트, 챗봇과의 차이 | 15분 |
| 도구(Tools) 만들기 | Function Calling 개념, 도구 정의 방법 | 30분 |
| ReAct 패턴 | Think → Act → Observe 루프 설명 | 20분 |
| 실습: 수학 에이전트 | 계산기 + 그래프 도구 에이전트 빌드 | 40분 |
| 응용 & 과제 안내 | 웹 검색 에이전트 시연 | 15분 |

## 🛠️ 실습 파일

- `practice.ipynb` — 도구 정의, 에이전트 루프 구현, 수학 에이전트, 웹 검색 에이전트

## 📚 참고 레포

[microsoft/Agent-Framework-Samples](https://github.com/microsoft/Agent-Framework-Samples) 폴더 01~04 기반

## 🔑 핵심 개념

| 개념 | 설명 |
|------|------|
| Function Calling | AI가 외부 함수를 호출하도록 하는 기능 |
| Tool | AI가 사용할 수 있는 도구 (함수) |
| ReAct | Reason + Act, 생각하고 행동하는 패턴 |
| Agent Loop | Think → Act → Observe를 반복하는 루프 |

---

## 📝 숙제: 꼬맨틀(Semantle) 클론 만들기

### 게임 규칙

1. 정답 단어를 하나 정함
2. 사용자가 단어를 입력하면 정답과의 유사도(0~100)를 반환
3. 유사도가 높을수록 정답에 가까움
4. 최소 시도로 정답 맞추기!

### 핵심 기술: 임베딩 유사도

```python
def get_similarity(word1, word2):
    response = client.embeddings.create(
        model="text-embedding-ada-002", input=[word1, word2]
    )
    emb1 = np.array(response.data[0].embedding)
    emb2 = np.array(response.data[1].embedding)
    return round(np.dot(emb1, emb2) / (np.linalg.norm(emb1) * np.linalg.norm(emb2)) * 100, 2)
```

### 템플릿

`semantle_template.py`를 완성하세요.

### 보너스 ⭐

- Gradio UI 추가
- 힌트 기능 (유사도 80+ 단어 알려주기)
- 리더보드 (최소 시도 횟수 랭킹)
