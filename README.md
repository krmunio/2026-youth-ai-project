# 🚀 고등학생 AI 교육 프로그램 2026

> **"미래세대가 만들어가는 AI 축제"** — Microsoft x 주강사 & 대학생 멘토 팀 프로젝트

## 📋 프로그램 개요

| 항목 | 내용 |
|------|------|
| **대상** | 고등학생 (프로그래밍 초보 ~ 중급) |
| **기간** | 2026년 5월 ~ 8월 (총 6회) |
| **실습 환경** | GitHub Codespaces + Jupyter Notebook |
| **기술 스택** | Python, Azure OpenAI, MAF, LangChain, Gradio, ChromaDB |

## 🗓️ 커리큘럼

| 회차 | 날짜 | 주제 | 숙제 |
|------|------|------|------|
| 4회차 | 5/16(토) | [AI 기초 이론](./session-04/) | 프롬프트 마스터 챌린지 |
| 5회차 | 5/30(토) | [AI 프로그래밍 실습](./session-05/) | 나만의 AI 챗봇 만들기 |
| 6회차 | 7/11(토) | [AI 에이전트 개발 1](./session-06/) | 꼬맨틀(Semantle) 클론 |
| 7회차 | 7/18(토) | [AI 에이전트 개발 2](./session-07/) | AI 학교 생활 도우미 |
| 8회차 | 8/8(토) | [해커톤](./session-08/) | - |
| 9회차 | 8/22(토) | [파인콘 AI 축제](./session-09/) | - |

## ⚡ 빠른 시작

### 1. Codespace 열기

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new)

### 2. 환경 변수 설정

```bash
cp .env.example .env
# .env 파일을 열고 수업 시간에 공유받은 API 키를 입력하세요
```

### 3. 실습 시작

각 `session-XX/` 폴더의 README.md를 읽고, Jupyter Notebook(`.ipynb`)을 열어 실습을 진행하세요.

## 📁 폴더 구조

```
ai-class-2026/
├── .devcontainer/          # Codespace 환경 설정
├── utils/                  # 공통 유틸리티
├── session-04/             # AI 기초 이론
├── session-05/             # AI 프로그래밍
├── session-06/             # 에이전트 개발 1
├── session-07/             # 에이전트 개발 2
├── session-08/             # 해커톤
└── session-09/             # AI 축제
```

## ⚠️ 주의사항

- 🔑 **API 키 보안**: `.env` 파일은 절대 커밋하지 마세요
- 💰 **비용 관리**: API 호출 시 `max_tokens`를 적절히 설정하세요
- 🤖 **AI 윤리**: AI의 편향, 할루시네이션, 저작권 문제를 항상 인식하세요

## 📚 참고 자료

- [Microsoft Agent Framework Samples](https://github.com/microsoft/Agent-Framework-Samples)
- [Azure OpenAI 공식 문서](https://learn.microsoft.com/azure/ai-services/openai/)
- [Prompt Engineering Guide (한국어)](https://www.promptingguide.ai/kr)
- [Gradio 공식 문서](https://www.gradio.app/docs)
