#!/bin/bash
set -e

echo "=== 2026 유스 AI 프로젝트 환경 세팅 ==="

# 1) uv 설치
echo "📦 uv 설치 중..."
curl -LsSf https://astral.sh/uv/install.sh | sh
export PATH="$HOME/.local/bin:$PATH"

# 2) uv sync (의존성 설치 + .venv 생성)
echo "📦 패키지 설치 중..."
uv sync

# 3) 한글 폰트 설치 (matplotlib 한글 깨짐 방지)
echo "🔤 한글 폰트 설치 중..."
sudo apt-get update -qq && sudo apt-get install -y -qq fonts-nanum > /dev/null 2>&1

# 4) .env 파일 생성 (없을 경우)
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  .env 파일이 생성되었습니다. API_KEY를 설정해주세요!"
fi

echo "✅ 환경 세팅 완료!"
