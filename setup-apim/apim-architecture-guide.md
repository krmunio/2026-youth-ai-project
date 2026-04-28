# APIM 기반 실습환경 아키텍처 가이드

> **목적**: API Key(Azure OpenAI 원본 키) 직접 배포 방식을 없애고,
> **APIM Subscription Key** 하나만으로 학생들이 안전하게 LLM을 호출할 수 있는 실습환경을 구성합니다.
>
> **전제**: 실습 학생은 **Azure 계정 / Entra ID(AAD) 테넌트 계정이 없습니다.**
> 따라서 OAuth2 / Bearer Token / `az login` 방식은 사용하지 않습니다.

- 관련 문서: [`apim-setup-guide.md`](./apim-setup-guide.md) — 실제 CLI/정책 적용 스텝
- 본 문서: 아키텍처 원칙, 보안 모델, 운영 패턴, 마이그레이션 절차

---

## 1. 왜 바꾸는가 (Why)

### 기존 방식의 문제점
```
학생 노트북 → (Azure OpenAI API Key) → Azure OpenAI
```
- Azure OpenAI 원본 `api-key`가 학생 20명에게 그대로 배포됨
- 키 유출 시 **구독 전체** 비용 폭탄 / 모델 전체 노출
- 학생별 사용량 분리, 호출 제한, 감사(audit) 불가
- 키 회전(rotation) 시 **모든 학생 환경을 동시에 재설정**해야 함
- 특정 학생만 차단(회수)하는 것이 불가능

### APIM 도입 후
```
학생 노트북 ──(APIM Subscription Key)──▶ APIM ──(Managed Identity)──▶ Azure OpenAI
```
- 학생이 가지는 키는 APIM이 발급한 **학생 전용 가짜 키(Subscription Key)**
- Azure OpenAI 원본 키는 **APIM 내부에만 존재** (혹은 MI 사용 시 아예 불필요)
- 학생별 발급/회수/쿼터/로깅이 독립적
- 특정 학생 키를 **즉시 비활성화** 가능
- 프롬프트/응답 감사, 호출 지표(Application Insights) 일괄 수집

---

## 2. 아키텍처 개요 (High-Level)

```
┌───────────────────────┐
│  학생 (Codespaces /    │
│   Jupyter Notebook)    │
│                        │
│  환경변수:              │
│   ENDPOINT=https://... │
│   SUBSCRIPTION_KEY=xxx │
└──────────┬─────────────┘
           │ HTTPS
           │ Header: Ocp-Apim-Subscription-Key: <학생키>
           ▼
┌──────────────────────────────────────────────────┐
│  Azure API Management (Consumption/Standard)     │
│                                                  │
│  ① Subscription Key 검증   → 학생 식별           │
│  ② Rate Limit / Quota     → 남용 방지            │
│  ③ IP Allowlist (선택)    → 교육장 네트워크 제한  │
│  ④ Policy: MI 토큰 발급   → AAD 대행 인증        │
│  ⑤ 헤더 치환              → api-key 제거 /       │
│                             Authorization 주입   │
│  ⑥ Logging → App Insights                        │
└──────────┬───────────────────────────────────────┘
           │ Authorization: Bearer <MI Token>
           │ (학생은 이 토큰을 절대 보지 못함)
           ▼
┌──────────────────────────────────────────────────┐
│  Azure OpenAI / AI Foundry                       │
│  - gpt-4.1-mini / gpt-5.4-mini / ...             │
│  - text-embedding-3-large                        │
│  RBAC: "Cognitive Services OpenAI User"          │
│        → APIM의 System Assigned MI에 부여         │
└──────────────────────────────────────────────────┘
```

### 핵심 설계 원칙
1. **학생은 Entra ID 계정이 필요 없다.** APIM이 대신 인증한다.
2. **Azure OpenAI 원본 키는 누구에게도 노출하지 않는다.** (MI로 완전히 대체)
3. **학생 자격증명은 1회성/회수 가능한 Subscription Key** 이다.
4. **정책(Policy)은 코드로 관리**한다. (XML 파일, Git에 커밋)
5. **APIM은 신뢰경계(Trust Boundary)** 이다. 이후 구간은 내부망/MI.

---

## 3. 인증 모델 (Entra ID 없는 학생 케이스)

학생 구간과 APIM↔AOAI 구간의 인증을 **완전히 분리**합니다.

| 구간 | 주체 | 인증 방식 | 자격증명 |
|------|------|----------|----------|
| 학생 → APIM | 학생(익명 사용자) | **Subscription Key** | `Ocp-Apim-Subscription-Key` 헤더 |
| APIM → Azure OpenAI | APIM 자신 | **Managed Identity (System Assigned)** | AAD에서 자동 발급한 Bearer 토큰 |

### 요청 변환 흐름

학생이 보낸 요청:
```http
POST /openai/deployments/gpt-4.1-mini/chat/completions?api-version=2024-12-01-preview
Host: {apim name}.azure-api.net
Ocp-Apim-Subscription-Key: abc123...(학생키)
Content-Type: application/json

{"messages":[{"role":"user","content":"안녕"}]}
```

APIM 정책 처리 후 백엔드로 나가는 요청:
```http
POST /openai/deployments/gpt-4.1-mini/chat/completions?api-version=2024-12-01-preview
Host: ai-foundry-010.openai.azure.com
Authorization: Bearer eyJhbGciOi... (APIM MI가 AAD에서 받은 토큰)
Content-Type: application/json

{"messages":[{"role":"user","content":"안녕"}]}
```

- 학생이 우회적으로 `api-key` 헤더를 넣어도 APIM 정책이 **제거**합니다.
- MI 토큰은 APIM이 **자동 캐싱/갱신**하므로 학생/관리자 모두 신경 쓸 필요 없습니다.

---

## 4. 보안 모델

### 4.1 신뢰 경계
- **학생 노트북**: 신뢰 불가 (키 유출 가능성 상존)
- **APIM**: 신뢰 경계. 모든 정책/쿼터/로깅의 단일 지점
- **Azure OpenAI**: 내부 자원. 외부 직접 접근 차단 가능

### 4.2 최소 권한
- APIM MI에 부여: **`Cognitive Services OpenAI User`**
  - 추론(invoke)만 가능, 모델 배포/삭제/키 조회 **불가**
- 교육 운영자(관리자)에게만 APIM/AOAI Contributor 부여
- 학생에게는 Azure 포털 접근 권한 **일절 없음**

### 4.3 Azure OpenAI 원본 키 처리 (권장)
- AOAI 리소스의 **Local auth(API Key 인증) 자체를 비활성화** 권장:
  - `properties.disableLocalAuth = true`
  - 이러면 MI/Entra ID 기반 인증만 허용되어 **원본 키가 유출되어도 의미 없음**

### 4.4 남용 방지 레이어
| 방어선 | 정책 | 단위 |
|--------|------|------|
| 학생별 호출 빈도 | `rate-limit-by-key` | 분당 N회 (Standard tier+) |
| 학생별 토큰 사용량 | `azure-openai-token-limit` | 분/시간당 토큰 수 |
| 교육장 네트워크 | `ip-filter` | CIDR allowlist |
| 일일 호출 총량 | `quota-by-key` | 키별 일간 호출 수 |
| 감사 | Diagnostic Logs → Log Analytics | 요청/응답/토큰 |

> Consumption tier는 `rate-limit-by-key` 미지원. 세밀한 학생별 제어가 필요하면 **Standard v2** 권장.

---

## 5. 환경/토폴로지 선택

### 5.1 APIM SKU
| SKU | 적합성 | 비고 |
|-----|-------|------|
| **Consumption** | ✅ 기본 추천 | 서버리스, 최저비용. `rate-limit-by-key` 불가 |
| **Basic v2 / Standard v2** | 교육생 많거나 엄격한 쿼터 필요 시 | 고정 월비용, 완전한 정책 기능 |
| Premium | 과함 | 멀티리전/VNet injection 필요 시만 |

### 5.2 단일 vs 세션별 분리
- 본 프로젝트는 **회차(session-04 ~ 08) 공통으로 하나의 APIM 인스턴스** 사용 권장
- 회차별 제어가 필요하면 **API Product를 회차별로 분리** (e.g. `workshop-s05`, `workshop-s06`)하고 Subscription만 나누기

### 5.3 모델 배포 전략
- 학생에게 노출할 배포(Deployment) 이름은 **APIM 오퍼레이션의 `{deployment-id}`**로 파라미터화
- 기본 허용 목록: `gpt-4.1-mini`, `gpt-5.4-mini`, `gpt-5.4-nano`, `text-embedding-3-large`
- 비허용 배포는 정책에서 차단:
  ```xml
  <choose>
    <when condition="@(!new[]{"gpt-4.1-mini","gpt-5.4-mini","gpt-5.4-nano","text-embedding-3-large"}.Contains((string)context.Request.MatchedParameters["deployment-id"]))">
      <return-response>
        <set-status code="403" reason="Model not allowed" />
      </return-response>
    </when>
  </choose>
  ```

---

## 6. 구성 요소 카탈로그

| 요소 | 이름(예) | 역할 |
|------|----------|------|
| Resource Group | `RG-AI` | 리소스 모음 |
| Azure OpenAI / AI Foundry | `ai-foundry-010` | 실제 LLM 추론 엔드포인트 |
| APIM | `{apim name}` | 게이트웨이 |
| APIM Managed Identity | System Assigned | AOAI 호출용 AAD 주체 |
| API | `azure-openai` (path: `/openai`) | AOAI 프록시 API |
| Operations | `chat-completions`, `responses`, `embeddings` | 허용 경로 |
| Product | `workshop-students` | 학생용 Subscription 그룹 |
| Subscriptions | `student-01` ~ `student-20` | 학생별 키 |
| Policy | `apim-policy.xml` | MI 주입 / 헤더 제거 / 쿼터 |
| 관측 | Application Insights + Log Analytics | 로깅/지표 |

---

## 7. 학생 배포 패키지

학생에게 전달하는 **최소한의 정보**만 정의합니다. Azure 계정/로그인 필요 없습니다.

### 7.1 전달 정보
| 항목 | 값 |
|------|-----|
| Endpoint | `https://{apim name}.azure-api.net` |
| Subscription Key | (학생별 1개, 운영자가 배포) |
| API Version | `2024-12-01-preview` |
| 모델 | `gpt-4.1-mini` 외 |

### 7.2 `.env` 템플릿 (신규)
```dotenv
# 기존 (❌ 제거 대상)
# ENDPOINT=https://apim-foundryproxy-dev.azure-api.net/foundry/gpt-5.4/
# API_KEY=<Azure OpenAI Key>

# 신규 (✅ APIM Subscription Key 방식)
AZURE_OPENAI_ENDPOINT=https://{apim name}.azure-api.net
AZURE_OPENAI_API_VERSION=2024-12-01-preview
APIM_SUBSCRIPTION_KEY=<학생별 Subscription Key>
AZURE_OPENAI_DEPLOYMENT=gpt-4.1-mini
```

### 7.3 Python 클라이언트 (표준 스니펫)
```python
import os
from openai import AzureOpenAI

client = AzureOpenAI(
    azure_endpoint=os.environ["AZURE_OPENAI_ENDPOINT"],
    api_version=os.environ["AZURE_OPENAI_API_VERSION"],
    api_key="unused",  # APIM은 Ocp-Apim-Subscription-Key를 요구
    default_headers={
        "Ocp-Apim-Subscription-Key": os.environ["APIM_SUBSCRIPTION_KEY"],
    },
)

resp = client.chat.completions.create(
    model=os.environ["AZURE_OPENAI_DEPLOYMENT"],
    messages=[{"role": "user", "content": "안녕!"}],
)
print(resp.choices[0].message.content)
```

> SDK의 `api_key` 파라미터는 내부적으로 `api-key` 헤더로 나가지만, APIM 정책이 이를 **제거**하므로 값은 무엇이든 무방합니다(`"unused"` 권장).

---

## 8. 마이그레이션 절차 (현행 → APIM 전용)

### Phase 0. 사전 점검
- [ ] AOAI 리소스/배포 이름 확정
- [ ] 학생 수 확정 (Subscription 발급 수량)
- [ ] 교육장 IP 대역 확인 (선택적 IP allowlist)

### Phase 1. APIM 구축 (운영자)
[`apim-setup-guide.md`](./apim-setup-guide.md)의 Step 1~6 수행
- APIM 생성 + System Assigned MI 활성화
- MI에 `Cognitive Services OpenAI User` 역할 부여
- API / Operations 등록
- `apim-policy.xml` 적용 (MI 인증 + `api-key` 제거)

### Phase 2. 학생 키 발급
[`apim-setup-guide.md`](./apim-setup-guide.md) Step 7 수행
- Product `workshop-students` 생성
- `student-01` ~ `student-N` 발급 → 안전한 채널로 각 학생에게 전달
  (추천: 1:1 DM, 교육 포털, 1Password 등 — 공용 채팅방 금지)

### Phase 3. 노트북/코드 업데이트
- 각 세션 폴더의 노트북에서:
  - `API_KEY` 환경변수 참조 → `APIM_SUBSCRIPTION_KEY`
  - `default_headers={"api-key": ...}` → `default_headers={"Ocp-Apim-Subscription-Key": ...}`
- `.env.example` 교체 (위 7.2 템플릿)
- README의 "빠른 테스트" 스니펫을 위 7.3으로 교체

### Phase 4. 검증
- [ ] `curl`로 Chat Completions 호출 성공
- [ ] Python SDK로 호출 성공
- [ ] 잘못된 키 → 401
- [ ] `api-key` 헤더만 넣고 Subscription Key 없음 → 401
- [ ] 허용 외 배포 호출 → 403 (정책 추가 시)

### Phase 5. 원본 키 차단 (권장, 교육 시작 전)
```bash
# Azure OpenAI의 로컬 키 인증 비활성화
az cognitiveservices account update \
  --name ai-foundry-010 \
  --resource-group RG-AI \
  --custom-domain ai-foundry-010 \
  --set properties.disableLocalAuth=true
```
이 순간부터 **APIM을 거치지 않은 모든 호출은 실패**합니다.

### Phase 6. 교육 종료 후
- Subscriptions 전체 비활성화 또는 삭제
- 필요 시 APIM 리소스 자체 삭제 (Consumption tier는 비용 거의 0)

---

## 9. 운영 플레이북

### 9.1 학생 키가 유출되었을 때
```bash
# 해당 키 즉시 비활성화
az rest --method PATCH \
  --url "$BASE_URL/subscriptions/student-07?api-version=2024-05-01" \
  --body '{"properties":{"state":"suspended"}}'

# 새 키 발급(primaryKey 재생성)
az rest --method POST \
  --url "$BASE_URL/subscriptions/student-07/regeneratePrimaryKey?api-version=2024-05-01"
```

### 9.2 특정 학생이 과도 호출할 때
- Application Insights에서 `context.Subscription.Id`별 요청 수 확인
- 해당 Subscription만 `state=suspended` 전환 또는 Product 이동

### 9.3 모델 추가/제거
- AOAI 배포 이름 변경만으로는 부족. **Policy의 허용 목록(5.3)도 업데이트**.

### 9.4 장애 시 체크리스트
1. APIM 게이트웨이 응답 여부 (`/status-0123456789abcdef`)
2. MI 토큰 발급 실패 → RBAC 할당 상태 재확인
3. 백엔드 URL/배포명 오타
4. `api-version` 불일치 (SDK 업데이트 후 빈번)

---

## 10. 관측(Observability)

### 10.1 수집 대상
- APIM 접근 로그 (Subscription 단위)
- 요청/응답 본문 (프롬프트 감사 시)
- 토큰 사용량 (`azure-openai-emit-token-metric` 정책)
- 에러율 / 지연시간

### 10.2 대시보드 지표 예시
| 지표 | 용도 |
|------|------|
| 학생별 분당 요청 수 | 남용 탐지 |
| 학생별 누적 토큰 | 비용 배분 |
| 4xx 비율 | 코드 오류/키 오용 추적 |
| 5xx 비율 | 백엔드 장애 |
| 평균 지연시간 | 교육 품질 |

---

## 11. 비교 요약

| 항목 | API Key 직배포 | APIM 프록시(본 가이드) |
|------|-----------------|------------------------|
| 학생 계정 필요 | ❌ | ❌ |
| 원본 키 노출 위험 | 🔴 매우 높음 | 🟢 없음 |
| 학생별 통제 | 불가 | 가능 (발급/회수/쿼터) |
| 감사/로깅 | 리소스 단위만 | 학생 단위 |
| 남용 방지 | 불가 | Rate/Quota/IP |
| 모델 제한 | 불가 | 정책으로 제한 |
| 키 회전 | 전원 재배포 | 개별 재발급 |
| 비용(추가) | 0 | Consumption tier ≈ 0 |

---

## 12. 참고
- 설정 스텝(실행 명령): [`apim-setup-guide.md`](./apim-setup-guide.md)
- Azure Docs: *Protect Azure OpenAI with Azure API Management*
- Policy Reference: `authentication-managed-identity`, `rate-limit-by-key`, `azure-openai-token-limit`, `azure-openai-emit-token-metric`
