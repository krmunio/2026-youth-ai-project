"""
공통 유틸리티 — 모든 노트북에서 import해서 사용합니다.

APIM (Foundry Proxy) 기반 통합 클라이언트 헬퍼.
엔드포인트 구조: {APIM_BASE_URL}/{MODEL_NAME}/

사용법:
    import sys; sys.path.append("..")
    from utils.config import get_client, chat, get_embedding

    client = get_client()                       # 기본 CHAT_MODEL
    embed_client = get_client("embedding")      # EMBEDDING_MODEL
"""

import os
from dotenv import find_dotenv, load_dotenv
from openai import OpenAI

load_dotenv(find_dotenv(usecwd=True), override=True)


def _base_url(model_name: str) -> str:
    base = os.environ["APIM_BASE_URL"].rstrip("/")
    return f"{base}/{model_name}/"


def _api_key() -> str:
    return os.environ["APIM_KEY"]


def get_client(kind: str = "chat") -> OpenAI:
    """
    kind: 'chat' | 'embedding' | 'vision' 또는 모델 이름 문자열을 직접 전달.
    """
    if kind == "chat":
        model = os.getenv("CHAT_MODEL", "gpt-5.4")
    elif kind == "embedding":
        model = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    elif kind == "vision":
        model = os.getenv("VISION_MODEL", os.getenv("CHAT_MODEL", "gpt-5.4"))
    else:
        model = kind  # 모델명 직접 전달
    return OpenAI(
        api_key="placeholder",  # APIM 헤더 인증
        base_url=_base_url(model),
        default_headers={"api-key": _api_key()},
    )


def chat(messages, temperature=0.7, max_completion_tokens=1024, model=None, tools=None):
    deployment = model or os.getenv("CHAT_MODEL", "gpt-5.4")
    client = get_client(deployment)
    kwargs = dict(model=deployment, messages=messages, temperature=temperature, max_completion_tokens=max_completion_tokens)
    if tools:
        kwargs["tools"] = tools
    return client.chat.completions.create(**kwargs).choices[0].message


def get_embedding(texts):
    deployment = os.getenv("EMBEDDING_MODEL", "text-embedding-3-small")
    client = get_client(deployment)
    response = client.embeddings.create(model=deployment, input=texts)
    return [d.embedding for d in response.data]

