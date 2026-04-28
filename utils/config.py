"""
공통 유틸리티 — 모든 노트북에서 import해서 사용합니다.

사용법:
    import sys; sys.path.append("..")
    from utils.config import get_client, chat, get_embedding
"""

import os
from dotenv import load_dotenv
from openai import AzureOpenAI

load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))


def get_client() -> AzureOpenAI:
    api_key = os.getenv("APIM_SUBSCRIPTION_KEY") or os.getenv("AZURE_OPENAI_KEY")
    return AzureOpenAI(
        api_key=api_key,
        api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-06-01"),
        azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
        default_headers={"Ocp-Apim-Subscription-Key": api_key} if os.getenv("APIM_SUBSCRIPTION_KEY") else {},
    )


def chat(messages, temperature=0.7, max_tokens=1024, model=None, tools=None):
    client = get_client()
    deployment = model or os.getenv("AZURE_OPENAI_DEPLOYMENT", "gpt-4o")
    kwargs = dict(model=deployment, messages=messages, temperature=temperature, max_tokens=max_tokens)
    if tools:
        kwargs["tools"] = tools
    return client.chat.completions.create(**kwargs).choices[0].message


def get_embedding(texts):
    client = get_client()
    deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-ada-002")
    response = client.embeddings.create(model=deployment, input=texts)
    return [d.embedding for d in response.data]
