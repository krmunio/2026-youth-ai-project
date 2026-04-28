# APIM + AI Foundry 연동 가이드 (Step by Step)

> Azure OpenAI의 API Key 인증이 차단된 환경에서,  
> 교육생에게 간단한 Subscription Key만으로 LLM을 사용하게 하는 방법입니다.

---

## 전체 흐름

```
교육생 (APIM Subscription Key로 호출)
    │
    ▼
┌─────────────────────────────────┐
│  Azure API Management (APIM)    │
│  - Subscription Key로 교육생 인증 │
│  - Managed Identity로 토큰 발급   │
└─────────────┬───────────────────┘
              │  Authorization: Bearer <MI 토큰>
              ▼
┌─────────────────────────────────┐
│  AI Foundry (ai-foundry-010)    │
│  - gpt-4.1-mini                 │
│  - gpt-5-mini / gpt-5.4-mini    │
│  - text-embedding-3-large       │
└─────────────────────────────────┘
```

**핵심 포인트:**
- 교육생은 Azure 계정이 없어도 됩니다
- APIM이 Managed Identity로 Entra ID 인증을 대행합니다
- 교육생은 `Ocp-Apim-Subscription-Key` 헤더 하나만 알면 됩니다

---

## 사전 준비

- Azure CLI 로그인 완료 (`az login`)
- AI Foundry 리소스가 이미 생성되어 있고, 모델이 배포된 상태

```bash
# Azure 로그인 확인
az account show --query "{name:name, subscription:id}" -o table

# AI Foundry 리소스 확인
az cognitiveservices account show \
  --name ai-foundry-010 \
  --resource-group RG-AI \
  --query "{name:name, endpoint:properties.endpoint, location:location}" -o table
```

### 리소스 없으면 생성

```bash
# 변수 설정
PREFIX="aaf"      # 리소스명 접두사 (예: aaf, dev, test)
POSTFIX="010"     # 리소스명 접미사 (예: 010, 001, prod)
RESOURCE_GROUP="rg-agent-framework"
LOCATION="eastus2"
FOUNDRY_NAME="ai-${PREFIX}-foundry-${POSTFIX}"

# 1. 리소스 그룹 생성 (없으면)
az group create --name $RESOURCE_GROUP --location $LOCATION

# 2. AI Foundry 리소스 생성 (없으면)
az cognitiveservices account create \
  --name $FOUNDRY_NAME \
  --resource-group $RESOURCE_GROUP \
  --kind AIServices \
  --location $LOCATION \
  --sku S0 \
  --custom-domain $FOUNDRY_NAME

# 3. 모델 배포
#
# ⚠️ 중요: --model-version 은 "1.0" 같은 값이 아니라
# 해당 리전/구독에서 지원되는 실제 버전 문자열이어야 합니다.
# 예: gpt-4.1-mini → "2025-04-14", gpt-5-mini → "2025-08-07",
#     text-embedding-3-large → "1"
#
# 아래 명령으로 현재 리전에서 지원되는 버전을 먼저 조회하세요.

# (a) 리전에서 지원되는 모델·버전 조회
az cognitiveservices model list \
  --location $LOCATION \
  --query "[?kind=='OpenAI' && (model.name=='gpt-4.1-mini' || model.name=='gpt-5-mini' || model.name=='text-embedding-3-large')].{name:model.name, version:model.version, sku:model.skus[0].name}" \
  -o table

# (b) 모델별 최신 버전을 변수로 자동 추출
GPT41_MINI_VER=$(az cognitiveservices model list --location $LOCATION \
  --query "[?kind=='OpenAI' && model.name=='gpt-4.1-mini'].model.version | sort(@) | [-1]" -o tsv)
GPT5_MINI_VER=$(az cognitiveservices model list --location $LOCATION \
  --query "[?kind=='OpenAI' && model.name=='gpt-5-mini'].model.version | sort(@) | [-1]" -o tsv)
EMBED3L_VER=$(az cognitiveservices model list --location $LOCATION \
  --query "[?kind=='OpenAI' && model.name=='text-embedding-3-large'].model.version | sort(@) | [-1]" -o tsv)

echo "gpt-4.1-mini           : $GPT41_MINI_VER"
echo "gpt-5-mini             : $GPT5_MINI_VER"
echo "text-embedding-3-large : $EMBED3L_VER"

# 값이 비어 있으면 해당 리전에 그 모델이 없다는 뜻입니다.
# (다른 리전으로 LOCATION 변경 또는 모델 목록에서 제외)

# gpt-4.1-mini 배포
az cognitiveservices account deployment create \
  --name $FOUNDRY_NAME \
  --resource-group $RESOURCE_GROUP \
  --deployment-name "gpt-4.1-mini" \
  --model-name "gpt-4.1-mini" \
  --model-version "$GPT41_MINI_VER" \
  --model-format "OpenAI" \
  --sku-name "GlobalStandard" \
  --sku-capacity 50

# gpt-5-mini 배포
az cognitiveservices account deployment create \
  --name $FOUNDRY_NAME \
  --resource-group $RESOURCE_GROUP \
  --deployment-name "gpt-5-mini" \
  --model-name "gpt-5-mini" \
  --model-version "$GPT5_MINI_VER" \
  --model-format "OpenAI" \
  --sku-name "GlobalStandard" \
  --sku-capacity 50

# text-embedding-3-large 배포
az cognitiveservices account deployment create \
  --name $FOUNDRY_NAME \
  --resource-group $RESOURCE_GROUP \
  --deployment-name "text-embedding-3-large" \
  --model-name "text-embedding-3-large" \
  --model-version "$EMBED3L_VER" \
  --model-format "OpenAI" \
  --sku-name "Standard" \
  --sku-capacity 50
```

> **추가 트러블슈팅**
> - `DeploymentModelNotSupported` → `--model-version` 값이 잘못됨. 위 (a) 명령의 결과에 있는 값만 사용하세요.
> - `SkuNotSupported` → 리전이 해당 SKU(`GlobalStandard`/`Standard`)를 지원하지 않는 경우입니다. 조회 결과의 `sku` 컬럼을 그대로 `--sku-name`에 쓰세요.
> - 특정 모델이 조회되지 않으면 해당 리전에 아직 미제공입니다. `LOCATION`을 `eastus`, `swedencentral` 등으로 바꿔 재시도.

---

## Step 1. 변수 설정

아래 변수를 본인 환경에 맞게 수정하세요.

```bash
# ===== 본인 환경에 맞게 수정 =====
PREFIX="aaf"      # 리소스명 접두사 (예: aaf, dev, test)
POSTFIX="010"     # 리소스명 접미사 (예: 010, 001, prod)
RESOURCE_GROUP="rg-agent-framework"
LOCATION="eastus2"
PUBLISHER_NAME="AI Workshop"
PUBLISHER_EMAIL="admin@csakr.net"
STUDENT_COUNT=20  # 생성할 교육생 키 수

# ===== 접두사/접미사를 이용한 리소스명 자동 생성 =====
APIM_NAME="apim-ai-${PREFIX}-${POSTFIX}"
FOUNDRY_NAME="ai-${PREFIX}-foundry-${POSTFIX}"

# ===== 자동으로 설정되는 값 (수정 불필요) =====
SUBSCRIPTION_ID=$(az account show --query id -o tsv)
FOUNDRY_RESOURCE_ID=$(az cognitiveservices account show \
  --name $FOUNDRY_NAME --resource-group $RESOURCE_GROUP --query id -o tsv)
FOUNDRY_ENDPOINT=$(az cognitiveservices account show \
  --name $FOUNDRY_NAME --resource-group $RESOURCE_GROUP --query properties.endpoint -o tsv)

echo "구독 ID: $SUBSCRIPTION_ID"
echo "AI Foundry: $FOUNDRY_RESOURCE_ID"
echo "엔드포인트: $FOUNDRY_ENDPOINT"
```

---

## Step 2. APIM 생성

Consumption tier는 서버리스 방식으로, 사용한 만큼만 과금됩니다.  
`--enable-managed-identity true`로 System Assigned MI를 함께 생성합니다.

```bash
az apim create \
  --name $APIM_NAME \
  --resource-group $RESOURCE_GROUP \
  --location $LOCATION \
  --publisher-name "$PUBLISHER_NAME" \
  --publisher-email "$PUBLISHER_EMAIL" \
  --sku-name Consumption \
  --enable-managed-identity true
```

> ⏳ 생성에 1~5분 정도 소요됩니다.

### 생성 확인

```bash
az apim show --name $APIM_NAME --resource-group $RESOURCE_GROUP \
  --query "{state:provisioningState, gateway:gatewayUrl, mi:identity.principalId}" -o table
```

| 항목 | 확인 사항 |
|---|---|
| state | `Succeeded` 이어야 함 |
| gateway | `https://<APIM_NAME>.azure-api.net` |
| mi | Managed Identity의 Principal ID (다음 단계에서 사용) |

```bash
# MI Principal ID 저장
MI_PRINCIPAL_ID=$(az apim show --name $APIM_NAME --resource-group $RESOURCE_GROUP \
  --query identity.principalId -o tsv)
echo "MI Principal ID: $MI_PRINCIPAL_ID"
```

---

## Step 3. RBAC 역할 할당

APIM의 MI가 AI Foundry에 접속할 수 있도록 `Cognitive Services OpenAI User` 역할을 부여합니다.

```bash
az role assignment create \
  --assignee-object-id $MI_PRINCIPAL_ID \
  --assignee-principal-type ServicePrincipal \
  --role "Cognitive Services OpenAI User" \
  --scope "$FOUNDRY_RESOURCE_ID"
```

> **`Cognitive Services OpenAI User`란?**
> - OpenAI API 호출(추론)만 허용하는 역할
> - 모델 배포/삭제/리소스 관리 권한은 없음
> - 교육 환경에 적합한 최소 권한

---

## Step 4. API 등록

APIM에 Azure OpenAI를 프록시하는 API를 등록합니다.

```bash
az apim api create \
  --resource-group $RESOURCE_GROUP \
  --service-name $APIM_NAME \
  --api-id azure-openai \
  --display-name "Azure OpenAI" \
  --path "openai" \
  --protocols https \
  --service-url "${FOUNDRY_ENDPOINT}openai" \
  --subscription-required true
```

> `--path "openai"`이므로 최종 URL은 `https://<APIM>.azure-api.net/openai/...`가 됩니다.

---

## Step 5. 오퍼레이션 등록

어떤 API 경로를 허용할지 정의합니다. Chat Completions, Responses, Embeddings를 등록합니다.

```bash
BASE_URL="https://management.azure.com/subscriptions/$SUBSCRIPTION_ID/resourceGroups/$RESOURCE_GROUP/providers/Microsoft.ApiManagement/service/$APIM_NAME"

# Chat Completions
az rest --method PUT \
  --url "$BASE_URL/apis/azure-openai/operations/chat-completions?api-version=2024-05-01" \
  --body '{
    "properties": {
      "displayName": "Chat Completions",
      "method": "POST",
      "urlTemplate": "/deployments/{deployment-id}/chat/completions",
      "templateParameters": [{"name": "deployment-id", "type": "string", "required": true}]
    }
  }'

# Embeddings
az rest --method PUT \
  --url "$BASE_URL/apis/azure-openai/operations/embeddings?api-version=2024-05-01" \
  --body '{
    "properties": {
      "displayName": "Embeddings",
      "method": "POST",
      "urlTemplate": "/deployments/{deployment-id}/embeddings",
      "templateParameters": [{"name": "deployment-id", "type": "string", "required": true}]
    }
  }'

# Responses
az rest --method PUT \
  --url "$BASE_URL/apis/azure-openai/operations/responses?api-version=2024-05-01" \
  --body '{
    "properties": {
      "displayName": "Responses",
      "method": "POST",
      "urlTemplate": "/deployments/{deployment-id}/responses",
      "templateParameters": [{"name": "deployment-id", "type": "string", "required": true}]
    }
  }'

```

---

## Step 6. 정책 적용

이 정책이 **전체 구조의 핵심**입니다.  
APIM이 MI로 Entra ID 토큰을 자동 발급받아 백엔드에 전달합니다.

### 정책 파일 생성

`apim-policy.xml` 파일을 만듭니다:

```xml
<policies>
    <inbound>
        <base />

        <!-- 1) 백엔드 라우팅: 교육생 요청을 AI Foundry 엔드포인트로 전달 -->
        <set-backend-service base-url="https://ai-aaf-foundry-010.openai.azure.com/openai" />

        <!-- 2) MI 인증: APIM의 Managed Identity로 Entra ID 토큰을 자동 발급
             → Authorization: Bearer <token> 헤더가 백엔드 요청에 추가됨 -->
        <authentication-managed-identity resource="https://cognitiveservices.azure.com" />

        <!-- 3) 보안: 교육생이 api-key 헤더를 보내더라도 삭제 (MI 인증만 사용) -->
        <set-header name="api-key" exists-action="delete" />
    </inbound>
    <backend>
        <base />
    </backend>
    <outbound>
        <base />
    </outbound>
    <on-error>
        <base />
    </on-error>
</policies>
```

### 선택 사항: 접근 제한 정책

필요에 따라 `<inbound>` 블록 안에 아래 정책을 추가할 수 있습니다.

#### IP 제한 (특정 네트워크에서만 허용)

```xml
<!-- 특정 IP 대역만 허용 (예: 교육장 네트워크) -->
<ip-filter action="allow">
    <address-range from="203.0.113.0" to="203.0.113.255" />
</ip-filter>
```

#### 호출 횟수 제한 (남용 방지)

> ⚠️ Consumption tier에서는 `rate-limit-by-key`를 사용할 수 없습니다.  
> Standard tier 이상에서만 사용 가능합니다.

```xml
<!-- Standard tier 이상: Subscription Key별 분당 60회 제한 -->
<rate-limit-by-key calls="60" renewal-period="60"
    counter-key="@(context.Subscription.Id)" />
```

#### CORS (브라우저에서 직접 호출할 경우)

```xml
<cors allow-credentials="false">
    <allowed-origins>
        <origin>*</origin>
    </allowed-origins>
    <allowed-methods>
        <method>POST</method>
    </allowed-methods>
    <allowed-headers>
        <header>*</header>
    </allowed-headers>
</cors>
```

### 각 줄의 의미

| 정책 | 역할 |
|---|---|
| `set-backend-service` | 교육생 요청을 AI Foundry 엔드포인트로 라우팅 |
| `authentication-managed-identity` | MI로 Entra ID 토큰을 자동 발급하여 `Authorization: Bearer` 헤더 추가 |
| `set-header api-key delete` | 보안상 api-key 헤더 제거 (MI 인증만 사용) |

### 정책 적용

```bash
POLICY_ESCAPED=$(cat apim-policy.xml | python3 -c "import sys,json; print(json.dumps(sys.stdin.read()))")

az rest --method PUT \
  --url "$BASE_URL/apis/azure-openai/policies/policy?api-version=2024-05-01" \
  --body "{\"properties\": {\"format\": \"xml\", \"value\": $POLICY_ESCAPED}}"
```

### 적용 확인

```bash
az rest --method GET \
  --url "$BASE_URL/apis/azure-openai/policies/policy?api-version=2024-05-01" \
  --query "properties.value" -o tsv
```

---

## Step 7. Product 및 교육생 키 발급

### Product 생성

Product는 API를 묶어서 Subscription Key를 관리하는 단위입니다.

```bash
az rest --method PUT \
  --url "$BASE_URL/products/workshop-students?api-version=2024-05-01" \
  --body '{
    "properties": {
      "displayName": "Workshop Students",
      "description": "AI Workshop 교육생용",
      "subscriptionRequired": true,
      "approvalRequired": false,
      "state": "published"
    }
  }'
```

### Product에 API 연결

```bash
az rest --method PUT \
  --url "$BASE_URL/products/workshop-students/apis/azure-openai?api-version=2024-05-01"
```

### 교육생별 Subscription Key 발급

```bash
for i in $(seq -w 1 $STUDENT_COUNT); do
  az rest --method PUT \
    --url "$BASE_URL/subscriptions/student-$i?api-version=2024-05-01" \
    --body "{
      \"properties\": {
        \"displayName\": \"Student $i\",
        \"scope\": \"/products/workshop-students\",
        \"state\": \"active\"
      }
    }" --query "properties.primaryKey" -o tsv 2>/dev/null
done
```

### 발급된 키 목록 확인

```bash
for i in $(seq -w 1 $STUDENT_COUNT); do
  KEY=$(az rest --method POST \
    --url "$BASE_URL/subscriptions/student-$i/listSecrets?api-version=2024-05-01" \
    --query "primaryKey" -o tsv 2>/dev/null)
  echo "Student $i: $KEY"
done
```

---

## Step 8. 테스트

### curl 테스트

```bash
# 발급받은 키로 테스트
curl -s -X POST \
  "https://$APIM_NAME.azure-api.net/openai/deployments/gpt-4.1-mini/chat/completions?api-version=2024-12-01-preview" \
  -H "Content-Type: application/json" \
  -H "Ocp-Apim-Subscription-Key: <교육생_키>" \
  -d '{"messages": [{"role": "user", "content": "안녕하세요!"}], "max_tokens": 50}' | jq .
```

### Python (OpenAI SDK) 테스트

```python
from openai import AzureOpenAI

SUBSCRIPTION_KEY = "<교육생_키>"

client = AzureOpenAI(
    azure_endpoint="https://{apim name}.azure-api.net",
    api_key=SUBSCRIPTION_KEY,
    api_version="2024-12-01-preview",
    default_headers={"Ocp-Apim-Subscription-Key": SUBSCRIPTION_KEY},
)

response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "대한민국의 수도는?"}],
    max_tokens=50,
)
print(response.choices[0].message.content)
```

> **주의**: `default_headers`에 `Ocp-Apim-Subscription-Key`를 추가해야 합니다.  
> OpenAI SDK는 `api-key` 헤더를 사용하지만, APIM은 `Ocp-Apim-Subscription-Key`를 요구합니다.

---

## 교육생에게 전달할 정보

| 항목 | 값 |
|---|---|
| Endpoint | `https://{apim name}.azure-api.net` |
| Subscription Key | (교육생별 발급된 키) |
| API Version | `2024-12-01-preview` |
| 사용 가능 모델 | `gpt-4.1-mini`, `gpt-5-mini`, `gpt-5.4-mini`, `gpt-5.4-nano`, `text-embedding-3-large` |

---

## 리소스 정리 (교육 종료 후)

```bash
# APIM 삭제
az apim delete --name $APIM_NAME --resource-group $RESOURCE_GROUP -y

# RBAC 역할 할당 삭제
az role assignment delete \
  --assignee $MI_PRINCIPAL_ID \
  --role "Cognitive Services OpenAI User" \
  --scope "$FOUNDRY_RESOURCE_ID"
```