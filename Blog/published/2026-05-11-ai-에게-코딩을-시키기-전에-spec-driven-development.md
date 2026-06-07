---
title: "AI에게 코딩을 시키기 전에 — 같은 프롬프트, 다른 결과의 함정과 SDD"
date: 2026-05-11
category: 04-Product-Insights
tags:
  - sdd
  - spec-driven-development
  - ai-engineering
  - claude-code
  - gemini-cli
  - antigravity
  - workflow
  - 1인-개발
source: "Claude Max + 멀티 AI 도구 한 달 운영 회고"
status: published-ready
related_post: "[[2026-05-11-1인-개발-워크플로우-1편-context-오염과-22일-폐기]]"
---

# AI에게 코딩을 시키기 전에 — 같은 프롬프트, 다른 결과의 함정과 SDD

## 어제는 됐는데 오늘은 다르다

AI 에이전트와 한 달을 함께 일하면서 가장 답답했던 순간은 결과물의 퀄리티가 낮았을 때가 아니었습니다. 어제 "로그인 페이지 만들어줘" 했을 때 멀쩡하게 돌아가는 깔끔한 코드를 받았는데, 오늘 같은 프롬프트를 넣으니 폴더 구조가 다르고, 네이밍 규칙이 다르고, 상태관리 방식이 다른 코드가 나올 때였습니다. 둘 다 동작하긴 합니다. 다만 두 결과를 한 프로젝트 안에서 섞어 쓸 수가 없습니다.

같은 프롬프트가 같은 결과를 보장하지 않는다는 건 사소해 보이지만, 엔지니어링 관점에서는 치명적입니다. 일관성이 없으면 재현 가능한 의사결정이 불가능하고, 재현이 불가능하면 시스템이 아니라 매번 새로 짜는 작업이 됩니다.

처음에는 답이 프롬프트에 있다고 생각했습니다. 더 정교하고 길고 구체적인 프롬프트를 쓰면 AI가 같은 결과를 낼 거라고요. 며칠 시도해 보니 한계가 분명했습니다. 프롬프트가 길어질수록 빠뜨리는 항목이 생기고, 같은 프롬프트라도 세션이 다르면 컨텍스트 윈도우의 상태가 달라서 결과가 흔들렸습니다. Claude에서 잘 돌아가던 게 Gemini에서 다른 모양으로 나오는 건 또 다른 문제였습니다.

그래서 방향을 바꿨습니다. 프롬프트를 매번 잘 쓰는 게 아니라, AI가 참조할 수밖에 없는 시스템을 프로젝트 안에 박아 두는 쪽으로요. 이게 흔히 SDD(Spec-Driven Development)라고 부르는 접근의 출발점이었습니다.

---

## "No Documentation, No Code"

SDD는 한 문장으로 요약됩니다. 문서화된 설계와 사용자의 승인 없이는 AI가 단 한 줄의 코드도 작성하지 못하게 만드는 것. 거창해 보이지만 핵심은 단순합니다. AI는 맥락을 먹고 자라는데, 코드부터 짜기 시작하면 그 맥락이 매번 다른 추측에서 시작합니다. 추측이 쌓이면 할루시네이션과 스파게티 코드로 이어집니다.

전통적 개발에서는 요구사항 → 코딩 → 문서화(나중에 또는 안 함) 순서였다면, SDD에서는 요구사항 → 문서화 → AI 검증 → 승인 → 코딩 → 문서 자동 동기화 순으로 흐릅니다. 명확한 spec이 있다고 해서 AI가 매번 한 글자도 안 틀리는 동일 코드를 뱉는다는 뜻은 아닙니다. LLM은 본질적으로 확률적이라 결과가 완벽히 같을 수는 없습니다. 다만 spec이 한 곳에 박혀 있으면 AI가 매 세션마다 참조하는 컨텍스트가 같아집니다. 컨텍스트가 같아지면 결과의 분산이 눈에 띄게 줄어듭니다. 폴더 구조의 큰 틀, 네이밍 규칙, 상태관리 방식의 결정 같이 "프로젝트의 모양"을 좌우하는 축들이 흔들리지 않고, 어제 짠 코드와 오늘 짠 코드가 한 프로젝트 안에서 자연스럽게 이어집니다. Claude로 시작한 작업을 Gemini로 넘겨도 같은 spec을 참조하는 한 두 결과의 모양이 어색하게 충돌하지 않습니다.

말로만 들으면 당연한 얘기인데 막상 짜 보면 어디서부터 손대야 할지 막막합니다. 그래서 한 달 동안 직접 운영해 본 프레임워크의 구조를 풀어 보려 합니다. 두 개의 축, 네 개의 워크플로우, 그리고 멀티 AI 도구 추상화 한 겹입니다.

---

## 두 개의 축 — 역할과 문서

핵심은 두 가지를 프로젝트 루트에 따로 두는 일입니다. 하나는 AI가 어떤 페르소나로 일할지 정의하는 `.agents/` 디렉토리, 다른 하나는 그 AI가 일하기 전에 반드시 채워야 할 문서들이 들어 있는 `DOCS/` 디렉토리입니다. 이 둘이 모든 AI 도구에 공통이고, 도구별 어댑터(`.claude/`, `.gemini/`, `.antigravity/`)는 그저 진입점만 담는 얇은 레이어로 둡니다.

```
project-root/
├── .agents/        ← AI-agnostic. 모든 AI가 공유하는 지식
├── DOCS/           ← AI-agnostic. 프로덕트 문서 36개
├── .claude/        ← Claude 전용 어댑터 (CLAUDE.md + hooks + commands)
├── .gemini/        ← Gemini 전용 어댑터 (GEMINI.md + workflows)
└── .antigravity/   ← Antigravity 전용 (필요 시)
```

이 분리가 왜 중요한지는 멀티 AI를 한 번이라도 같이 써 보면 알게 됩니다. Claude에서 잘 돌아가던 컨벤션을 Gemini에서 다시 정의하고, 그걸 또 Antigravity에서 한 번 더 정의하는 일을 반복하다 보면 정의 자체가 산발적으로 흩어집니다. `.agents/`와 `DOCS/`를 도구 독립적으로 두면 진실의 근원이 한 곳이 되고, 도구별 어댑터는 그 한 곳을 가리키는 포인터만 담으면 됩니다.

### 첫 번째 축 — `.agents/` (역할 분담)

`.agents/` 디렉토리에는 기획자, 디자이너, 프론트엔드 엔지니어, 백엔드 엔지니어 같은 페르소나가 폴더로 분리돼 있습니다. 회사로 치면 직원들이고, 각자의 역할·페르소나·규칙을 따로 정의합니다.

```
.agents/
├── README.md            시스템 개요 + 에이전트 인덱스
├── planner/             기획자
│   ├── AGENT.md         페르소나: 시니어 프로덕트 매니저
│   └── rules/
│       ├── prd-format.md       PRD 작성 규칙
│       └── story-format.md     유저스토리 포맷
├── designer/            디자이너
│   ├── AGENT.md         페르소나: 시니어 UI/UX 디자이너
│   └── rules/
│       ├── design-tokens.md     디자인 토큰 컨벤션
│       └── component-pattern.md  Atom→Molecule→Organism 분류
├── frontend/            프론트엔드 엔지니어
│   ├── AGENT.md         페르소나: 시니어 프론트엔드 엔지니어
│   └── rules/
│       ├── code-style.md         함수형 전용, CSS Modules
│       └── test-standard.md      커버리지 80%, Given-When-Then
├── backend/             백엔드 엔지니어
│   ├── AGENT.md         페르소나: 시니어 백엔드 엔지니어
│   └── rules/
│       ├── api-design.md         RESTful, 응답 포맷, 상태 코드
│       └── security-checklist.md OWASP, 입력 검증, 토큰 관리
└── workflows/           범용 워크플로우 (모든 AI 공용)
    ├── agent-dispatch.md
    ├── spec-gate.md
    ├── integrity-sync.md
    └── cross-doc-validation.md
```

이렇게 나누는 이유는 단순합니다. "로그인 UI 만들어줘" 했을 때 AI가 PRD 작성 규칙이나 DB 보안 체크리스트까지 메모리에 끌어올 필요는 없습니다. 작업에 맞는 페르소나의 지식만 로드하면 토큰이 절약되고 응답 품질이 올라갑니다.

키워드를 감지해 적절한 에이전트로 전환하는 규칙은 이런 식입니다.

| 키워드 | 에이전트 | 로드되는 지식 |
|--------|----------|---------------|
| 기획, PRD, 요구사항, KPI | planner | AGENT.md + rules/ + DOCS/01_Product/ |
| 디자인, UI, 색상, 접근성 | designer | AGENT.md + rules/ + DOCS/02_Design/ |
| 프론트, 컴포넌트, React | frontend | AGENT.md + rules/ + DOCS/03_Engineering/ |
| API, DB, 서버, 인증 | backend | AGENT.md + rules/ + DOCS/04_Technical_Spec/ |

도구별 진입점(`CLAUDE.md`, `GEMINI.md`)에는 이 매핑 테이블만 메타데이터로 박아 두고, 실제 지식 파일은 해당 에이전트가 활성화될 때만 로드합니다. 컨텍스트 윈도우를 아끼면서도 일관된 행동을 보장하는 가장 작은 장치입니다.

### 두 번째 축 — `DOCS/` (5개 카테고리, 36개 문서)

`.agents/`가 "누가 일하는가"를 정의한다면, `DOCS/`는 "무엇을 만들고 있는가"를 정의합니다. 다섯 개 카테고리로 자르고 그 안에 총 서른여섯 개 문서가 들어갑니다.

```
DOCS/
├── 01_Product/           기획자가 작성
│   ├── PRD.md                   ⭐ 제품 요구사항 (필수)
│   ├── PRODUCT_PLAN.md          마일스톤 + 로드맵
│   ├── USER_STORY_MAP.md        유저 시나리오
│   ├── COMPETITIVE_ANALYSIS.md  경쟁 분석
│   ├── KPI_METRICS.md           핵심 지표 + 성공 기준
│   └── RELEASE_PLAN.md          릴리즈 전략
│
├── 02_Design/            디자이너가 작성
│   ├── UI_UX_GUIDELINES.md      ⭐ UI/UX 가이드라인 (필수)
│   ├── DESIGN_SYSTEM.md         ⭐ 색상·타이포·스페이싱 (필수)
│   ├── ACCESSIBILITY_GUIDE.md   WCAG 2.1
│   ├── RESPONSIVE_SPEC.md       반응형 브레이크포인트
│   ├── FIGMA_MCP_BRIDGE.md      Figma MCP 연동
│   └── ANIMATION_GUIDE.md       모션·트랜지션
│
├── 03_Engineering/       개발팀 공통
│   ├── CODE_CONVENTIONS.md      ⭐ 코드 컨벤션 (필수)
│   ├── GIT_CONVENTIONS.md       ⭐ 커밋 규칙 (필수)
│   ├── PROJECT_STRUCTURE.md     ⭐ 프로젝트 구조 (필수)
│   ├── API_SPEC.md              RESTful API 규격
│   ├── TEST_GUIDE.md            테스트 전략
│   ├── SECURITY_POLICY.md       보안 정책 + OWASP
│   ├── PERFORMANCE_BUDGET.md    Core Web Vitals
│   ├── ERROR_HANDLING.md        에러 처리 + 로깅
│   └── ENV_SETUP.md             환경 설정
│
├── 04_Technical_Spec/    기술 상세 명세
│   ├── FRONTEND.md / BACKEND.md      FE/BE 기술 스택
│   ├── DATABASE_SCHEMA.md            ERD + 테이블 정의 (Mermaid)
│   ├── STATE_MANAGEMENT.md           서버/클라이언트 상태 분리
│   ├── AUTH_FLOW.md                  인증 시퀀스 다이어그램
│   ├── ALGORITHM_SPEC.md             핵심 알고리즘
│   └── THIRD_PARTY_INTEGRATION.md    외부 서비스 연동
│
└── 05_System_Architecture/  시스템 아키텍처
    ├── SYSTEM_HANDOVER.md            시스템 개요
    ├── DATA_FLOW_DIAGRAM.md          데이터 흐름 (Mermaid)
    ├── DEPLOYMENT_ARCHITECTURE.md    CI/CD + 인프라
    ├── MODULE_DEPENDENCY_MAP.md      모듈 의존성 그래프
    ├── SEQUENCE_DIAGRAMS.md          유스케이스 시퀀스
    └── SCALING_STRATEGY.md           확장 전략
```

여기서 중요한 건 각 문서에 상세 목차가 미리 잡혀 있다는 점입니다. 예를 들어 `PRD.md`는 빈 파일이 아니라 이런 골격으로 시작합니다.

```markdown
# PRD (Product Requirements Document)

## 1. 제품 개요
   1.1. 제품 비전 + 미션
   1.2. 문제 정의 (Pain Point)
   1.3. 타겟 사용자 (Persona)
## 2. 요구사항
   2.1. 핵심 기능 (Must-Have)
   2.2. 부가 기능 (Nice-to-Have)
   2.3. 비기능 요구사항
## 3. 사용자 시나리오
## 4. 성공 기준
## 5. 제약 조건 + 가정
## 6. 변경 이력
```

AI에게 "PRD 작성해줘" 하면 AI는 이 목차의 빈칸을 하나씩 채웁니다. 목차가 미리 잡혀 있으니 어떤 AI를 쓰든 같은 구조의 문서가 나옵니다. 36개 문서 모두 이런 식으로 골격이 잡혀 있고, `DATABASE_SCHEMA.md`에는 Mermaid ERD 템플릿이, `AUTH_FLOW.md`에는 시퀀스 다이어그램 입력란이, `SECURITY_POLICY.md`에는 OWASP Top 10 체크리스트가 들어갑니다.

---

## 문서가 있어도 AI가 무시하면 끝이다

여기까지 짜 두고 한 주를 운영해 보니 새로운 문제가 보였습니다. 문서 체계가 있어도 AI가 "이번엔 그냥 코드부터 짜죠" 하고 넘어가면 그만입니다. 사람이 매번 "PRD 먼저 보고 와" 하고 잡아 줘야 한다면 시스템이라기보다 그냥 가이드라인입니다.

그래서 강제 메커니즘을 한 겹 더 얹었습니다. 워크플로우와 hooks 네 개입니다.

| 워크플로우 | 역할 | 트리거 |
|-----------|------|--------|
| spec-gate | 필수 문서 6개 완성 전 코드 작성 거부 | 구현 명령 시 |
| integrity-sync | 코드 변경 시 영향받는 DOCS 자동 안내 | 코드 작성 후 |
| agent-dispatch | 작업 유형에 따라 에이전트 전환 | 새 작업 시 |
| cross-doc-validation | PRD↔API↔DB 교차 정합성 검증 | 문서 수정 시 |

가장 중요한 게 `spec-gate`입니다. SDD의 한 줄 슬로건("No Documentation, No Code")이 코드로 박혀 있는 자리입니다. 사용자가 "구현 시작해" 하면 AI는 먼저 이 게이트를 통과해야 합니다.

```
Gate 1 (기획):    DOCS/01_Product/PRD.md                      비어 있지 않은가?
Gate 2 (디자인):  DOCS/02_Design/UI_UX_GUIDELINES.md          비어 있지 않은가?
                  DOCS/02_Design/DESIGN_SYSTEM.md             비어 있지 않은가?
Gate 3 (엔지니어링): DOCS/03_Engineering/CODE_CONVENTIONS.md  비어 있지 않은가?
                     DOCS/03_Engineering/PROJECT_STRUCTURE.md 비어 있지 않은가?
                     DOCS/03_Engineering/GIT_CONVENTIONS.md    비어 있지 않은가?

전부 통과 → "[SPEC-GATE 통과] 구현을 시작합니다."
하나라도 실패 →
  "[SPEC-GATE 실패] 구현 불가. 미완성 문서:
    - PRD.md — '요구사항' 섹션 미작성
    - DESIGN_SYSTEM.md — 파일 미존재
   /agent-dispatch planner → PRD 작성부터 시작하세요."
```

핫픽스나 프로토타입은 사용자가 명시적으로 선언하면 우회할 수 있습니다. 다만 우회 시에는 `[SPEC-GATE 우회: 핫픽스]` 같은 로그가 반드시 남도록 해 두면, 나중에 회고할 때 어느 시점에 어떤 이유로 게이트를 풀었는지 추적이 됩니다.

`integrity-sync`는 그 반대편 짝입니다. 코드를 변경할 때마다 영향받는 DOCS를 자동으로 짚어 줍니다.

| 코드 변경 | 영향받는 DOCS |
|----------|---------------|
| UI/컴포넌트 수정 | 02_Design/UI_UX_GUIDELINES.md, 04_Technical_Spec/FRONTEND.md |
| API 엔드포인트 변경 | 03_Engineering/API_SPEC.md, 04_Technical_Spec/BACKEND.md |
| DB 스키마 변경 | 04_Technical_Spec/DATABASE_SCHEMA.md, 05_System_Architecture/DATA_FLOW_DIAGRAM.md |
| 인증/인가 수정 | 04_Technical_Spec/AUTH_FLOW.md, 03_Engineering/SECURITY_POLICY.md |
| 아키텍처 변경 | 05_System_Architecture/* 전체 |

자동 갱신은 일부러 하지 않습니다. "이 문서를 손댔으니 저기도 영향이 갈 것"이라는 신호만 명확히 주고, 실제 갱신 결정은 사람의 몫으로 남깁니다.

각 AI 도구에서 어떻게 강제하느냐는 도구마다 다릅니다. Claude Code에서는 `.claude/hooks/spec-gate.sh`가 PreToolUse 단계에서 자동 실행돼 코드 파일 작성을 막습니다. Gemini CLI에서는 `.gemini/workflows/`의 사전 점검 스크립트가 비슷한 역할을 합니다. 그리고 Agent Skills 오픈 표준을 따르는 `.agents/skills/spec-gate/SKILL.md`는 Claude·Gemini·Antigravity 모두에서 동일하게 호출됩니다. 도구별 차이는 어댑터에 흡수되고, 강제할 정책 자체는 한 곳에 있습니다.

---

## 새 프로젝트를 시작할 때 어떻게 흐르는가

말로만 보면 추상적이니 한 흐름을 따라가 보겠습니다. TODO 앱을 새로 시작한다고 가정합니다.

사용자가 "TODO 앱 만들고 싶어"라고 합니다. AI는 먼저 `agent-dispatch`로 기획자 에이전트를 활성화하고 "PRD부터 작성하겠습니다. `DOCS/01_Product/PRD.md`의 목차를 채워 드릴게요"라고 응답합니다. 사용자는 AI와 PRD를 함께 채웁니다(비전, 기능, 유저스토리, KPI). 사용자가 "이제 디자인 잡아줘" 하면 AI는 디자이너 에이전트로 전환하고 `DESIGN_SYSTEM.md`부터 색상, 타이포, 스페이싱 토큰을 정의합니다. "코드 컨벤션이랑 프로젝트 구조도 잡자" 하면 프론트엔드 에이전트로 전환해 `CODE_CONVENTIONS.md`, `PROJECT_STRUCTURE.md`, `GIT_CONVENTIONS.md`를 작성합니다.

여기까지 와서 사용자가 "구현 시작해" 했을 때야 비로소 `spec-gate`가 발동합니다. 필수 문서 여섯 개가 모두 채워져 있으면 "[SPEC-GATE 통과] 구현을 시작합니다"가 뜨고 코드 작성이 시작됩니다. 코드를 짠 직후 `integrity-sync`가 자동으로 따라붙어 "API 엔드포인트가 추가되었습니다. `API_SPEC.md`를 업데이트합니다"라고 안내합니다.

이 흐름 안에서 사용자는 자연어로 대화만 합니다. 시스템이 알아서 네 번의 역할 전환과 한 번의 게이트 검증을 수행합니다. 매번 "이번엔 PRD 먼저 봐 줘" 같은 말을 할 필요가 없습니다.

---

## 운영하면서 자라는 마지막 한 조각

여기서 끝이 아닙니다. 36개 문서가 독립적으로 자라다 보면 어디선가 모순이 생깁니다. PRD에는 "소셜 로그인" 기능이 있는데 API 스펙에는 없다든지, API에서 반환하는 필드가 DB 스키마에 없다든지. 사람이 매번 짚기에는 너무 많고, AI가 글로벌 일관성을 자발적으로 점검할 동기는 없습니다.

`cross-doc-validation`이 그 자리에 들어갑니다. 정기적으로 또는 문서 수정 직후에 한 번 돌리면 이런 보고가 나옵니다.

```
[교차 정합성 검증 결과]

통과:
  PRD ↔ Design — 5/5 기능에 UI 패턴 매칭
  API ↔ DB     — 12/12 필드 매칭

불일치:
  PRD ↔ API   — "소셜 로그인" 기능의 API 엔드포인트 미정의
  Tech Spec ↔ Architecture — "NotificationService"가 의존성 맵에 누락

권장 조치:
  1. API_SPEC.md에 /api/v1/auth/social/* 엔드포인트 추가
  2. MODULE_DEPENDENCY_MAP.md에 NotificationService 반영
```

자동 수정은 하지 않습니다. 어디가 어긋났는지 명확하게 짚어 주고, 어떻게 맞출지는 사람이 결정합니다. 이게 SDD를 한 달 운영하면서 가장 자주 발동한 워크플로우였습니다. 코드보다 문서가 먼저라는 원칙을 박아 두니, 정작 일관성이 깨지는 곳은 코드가 아니라 문서들 사이였습니다.

---

## 가드레일을 깐 다음에 무엇이 오는가

한 달을 정리하면 결국 이런 그림입니다. 에이전트 분리로 AI에게 역할을 부여하고 필요한 지식만 로드하게 했고, 36개 문서로 기획·디자인·엔지니어링·기술 상세·아키텍처를 다섯 축으로 나눴고, `spec-gate`로 문서 완료 전 코드 금지를 강제했고, `integrity-sync`로 코드 변경 시 문서 동기화 신호를 띄웠고, `.agents/`와 `DOCS/`를 도구 독립적으로 둬서 어떤 AI를 써도 같은 진실의 근원을 가리키게 했습니다.

가드레일을 깐다는 게 어떤 의미인지가 한 달 사이에 분명해졌습니다. 자유를 줄이는 일이 아니라, AI가 올바른 방향으로 달릴 수 있는 차선을 그어 주는 일이었습니다. 차선이 없으면 빠르게 달려도 어디로 가는지 모르고, 차선이 있으면 같은 속도로 같은 결과에 도달합니다.

다음 한 달의 질문은 이미 떠오르고 있습니다. 가드레일을 깔고 나면 그 위에서 어떤 자동화를 한 겹 더 얹을 수 있을까. spec과 코드 사이의 동기화를 넘어, spec 자체가 시간이 지나면서 어떻게 진화하는지를 시스템이 추적하고 회고할 수 있을까. 이 시스템을 1인 + AI swarm 환경에서 어디까지 다이어트할 수 있을까. 그 답들은 또 다음 글에서 정리해 보려 합니다.

처음 시작은 같았습니다. 프로젝트 루트에 `.agents/`와 `DOCS/`를 만들고, AI에게 한 줄을 던지는 일.

