# AI 네이티브 1인 + AI swarm 개발 프로세스 — 업그레이드 박제

> **작성일**: 2026-05-16
> **상태**: DRAFT — 외부 답변(Q1+Q2+Q3) + 이번 대화 진화 + 통합 모델 결론 통합 박제. 다음 실 작업(INP-134/136 병렬 fan-out)에서 검증 후 갱신/폐기 결정.
> **목적**: sprint frame → AI 네이티브 1인 + AI swarm 모델 전환 시점의 컨텍스트 박제. 미래 자기 자신 onboarding 입구.

---

## Part 1. 외부 답변 (Q1 + Q2 + Q3) — 원문 박제

## Q1. AI 네이티브 병렬형 제품 개발 프로세스

### 질문

ai 네이티브로 1인 프로덕트 개발인데 기존의 제품개발프로세스가 아닌 병렬형 AI 네이티브 개발 프로세스에 대해서 한번 생각을 해봐 뭐가 효율적일까

### 답변

1인 프로덕트 개발에서 "AI 네이티브"의 핵심은 기존처럼 `기획 → 디자인 → 개발 → 테스트 → 배포`를 직렬로 밟는 게 아니라, **사람은 제품 판단과 통합을 맡고, AI들은 탐색·구현·검증을 병렬로 돌리는 구조**를 만드는 겁니다.

가장 효율적인 형태는 이렇게 봅니다.

**1. 사람은 PM이 아니라 편집장처럼 움직이기**

1인 개발자가 모든 걸 직접 "작성"하려고 하면 AI를 써도 병목은 여전히 본인입니다. 대신 역할을 이렇게 바꾸는 게 좋습니다.

- 문제 정의
- 제품 방향 결정
- 우선순위 판단
- 결과물 리뷰
- 최종 통합
- 배포 결정

즉, 사람은 "일하는 사람"이라기보다 **결정권자 + 리뷰어 + 통합자**에 가까워집니다.

AI는 다음을 맡깁니다.

- 경쟁 제품 조사
- 유저 플로우 초안
- UI 대안 생성
- DB/API 설계 초안
- 기능 구현
- 테스트 케이스 작성
- 버그 원인 분석
- 릴리즈 노트 작성
- 문서화
- 온보딩/마케팅 카피 초안

**2. 프로세스는 단계형이 아니라 루프형이 효율적**

기존 프로세스:
```
아이디어 → 요구사항 → 디자인 → 개발 → QA → 배포
```

AI 네이티브 프로세스:
```
가설 설정
→ 병렬 탐색
→ 후보 비교
→ 빠른 구현
→ 자동 검증
→ 사용자/시장 피드백
→ 다음 가설
```

중요한 건 "완벽한 PRD를 쓰고 시작"이 아니라, **작은 가설을 여러 방향으로 동시에 검증**하는 겁니다.

예를 들면:
```
가설: 개발자들이 API 로그 분석을 더 쉽게 하고 싶어 한다.
```

이때 한 AI에게만 "이거 만들어줘"가 아니라:
- AI A: 경쟁 제품 조사
- AI B: 핵심 유저 시나리오 5개 도출
- AI C: MVP 기능 범위 제안
- AI D: UI 와이어프레임 생성
- AI E: 기술 스택/DB 구조 제안
- AI F: 랜딩페이지 메시지 초안

이렇게 병렬로 던지고, 사람은 결과를 비교해서 방향을 고릅니다.

**3. 기능 개발도 병렬 파이프라인으로 쪼개는 게 좋음**

한 기능을 만들 때도 직렬로 하지 않습니다.

예:
```
기능: 사용자가 프로젝트별 API 로그를 검색하고 필터링한다.
```

병렬 작업:
- 에이전트 1: 데이터 모델/마이그레이션 설계
- 에이전트 2: 백엔드 API 구현
- 에이전트 3: 프론트엔드 검색 UI 구현
- 에이전트 4: 테스트 케이스 작성
- 에이전트 5: UX 엣지 케이스 검토
- 에이전트 6: 성능/보안 리스크 리뷰

단, 전부 같은 파일을 건드리게 하면 망합니다. 효율적인 병렬화의 조건은 **소유 영역 분리**입니다.

```
DB/백엔드
프론트엔드
테스트
문서
리뷰
```

이렇게 write scope를 나눠야 합니다.

**4. "스펙"보다 "계약"을 먼저 만드는 게 중요**

AI 병렬 개발에서 가장 중요한 산출물은 긴 기획서가 아니라 **작은 계약서**입니다.

예:
```
Feature Contract

목표:
- 사용자는 로그 목록에서 status code, method, path, date range로 필터링할 수 있다.

입력:
- projectId, query, statusCode, method, from, to

출력:
- logs[], totalCount, nextCursor

성공 조건:
- 필터 조합이 가능하다.
- 빈 결과 상태가 있다.
- 500ms 이내에 첫 페이지가 응답한다.
- 권한 없는 projectId 접근은 차단된다.

비범위:
- 실시간 스트리밍
- 저장된 검색 조건
- 대시보드 차트
```

이 정도 계약만 있으면 AI 여러 개가 동시에 움직일 수 있습니다. 반대로 이게 없으면 AI들이 각자 다른 제품을 만듭니다.

**5. 추천하는 AI 네이티브 개발 사이클**

실전적으로는 이 루프가 좋습니다.

```
1. Product Brief
2. Parallel Discovery
3. Decision Memo
4. Feature Contract
5. Parallel Build
6. AI Review Swarm
7. Human Integration
8. Ship
9. Feedback Compression
```

각 단계는 짧아야 합니다.

**Product Brief**: 하루짜리 문서 — 누구의 어떤 문제? 기존 대안 부족 이유? 이번 주 검증 행동? 성공 신호?

**Parallel Discovery**: AI 여러 개에게 동시에 — 시장 조사 / 페르소나 / 경쟁 제품 / UX 흐름 / 기술 리스크 / 가격 모델

**Decision Memo**: 사람이 결론만 — 우리는 A 방향. B 버림. C 나중. 이유는 X.

**Feature Contract**: 위에서 말한 작은 기능 계약

**Parallel Build**: 역할 분리해서 구현

**AI Review Swarm**: 구현 후 다른 AI들에게 리뷰 — 보안 / UX / 성능 / 테스트 / 코드 단순성 / 제품 일관성

**Human Integration**: 1인 개발자가 직접 봐야 함. AI가 많이 만들수록 통합 품질이 제품 품질.

**Ship**: 완성도 100% 아니라, 가설 검증 가능한 수준이면 배포.

**Feedback Compression**: 유저 피드백, 로그, 에러, 세션 리플레이, 문의를 AI에게 요약시켜 다음 가설로 압축.

**6. 가장 효율적인 작업 단위는 "기능"보다 "검증 가능한 행동"**

기존 개발 = 기능 단위 (로그인 / 대시보드 / 검색 / 결제 / 설정).

AI 네이티브 = **행동 단위**:
- 사용자가 30초 안에 첫 프로젝트를 생성한다
- 사용자가 에러 로그 원인을 찾는다
- 사용자가 팀원에게 링크를 공유한다
- 사용자가 결제 전에 가치를 이해한다

이렇게 잡으면 AI가 UI, 백엔드, 카피, 온보딩, 분석 이벤트까지 한꺼번에 제안.

**7. 1인 개발자에게 특히 중요한 자동화**

AI 네이티브 개발의 병목은 "생성"이 아니라 "검증". 초기에 깔아두는 게 좋음:

- 자동 테스트 / 타입 체크 / 린트
- 프리뷰 배포 / 에러 로깅 / 사용 이벤트 추적
- 세션 리플레이 / DB 마이그레이션 검증
- 스모크 테스트 / AI 코드 리뷰 프롬프트 / 릴리즈 체크리스트

AI가 코드를 빨리 만들수록, 검증 장치가 없으면 제품이 빠르게 망가짐.

**8. 실전 운영 방식**

하루:
```
오전: 오늘의 제품 가설 1개 선택 + AI 3-5개로 탐색/설계 병렬
점심 전: 결과 비교 + 기능 계약 작성 + 범위 축소
오후: 구현 에이전트 병렬 + 테스트/리뷰 에이전트 별도
저녁: 직접 통합 + 배포 + 피드백/로그 확인 + 다음 가설 정리
```

일주일:
```
월: 문제/가설 정리
화-목: 기능 실험 2-3개 제작
금: 배포/측정/사용자 인터뷰
주말: 방향 유지, 전환, 폐기 결정
```

**9. 피해야 할 것**

- 큰 PRD 쓰고 한 번에 거대한 앱 만들기
- AI에게 "알아서 좋은 제품 만들어줘"
- 여러 AI가 같은 파일 동시 수정
- 검증 없이 코드만 쌓기
- 사용자 피드백 없이 내부 완성도만 올리기
- 디자인/카피/온보딩을 개발 끝난 뒤 붙이기
- 테스트 없이 배포 속도만
- 매번 새 아키텍처 AI 제안받기
- 사람이 최종 제품 판단 안 함

**10. 결론적으로 가장 효율적인 구조**

```
Human: 제품 판단, 우선순위, 통합, 최종 책임
AI Agents: 탐색, 초안, 구현, 테스트, 리뷰, 문서화
Process: 작은 가설 → 병렬 생성 → 사람 선택 → 빠른 배포 → 피드백 압축
```

가장 중요한 원칙:
> AI에게 일을 많이 시키는 것보다, AI들이 서로 충돌하지 않도록 작은 계약과 경계를 잘 주는 것이 더 중요하다.

1인 개발자에게 최적의 프로세스 = "AI가 대신 개발하는 프로세스" 가 아니라, **사람 한 명이 여러 명의 AI 작업자를 지휘하는 병렬 제품 시스템**.

---

## Q2. 제품/코드/디자인 문서 관리와 톤앤매너 일관성

### 질문

제품 개발을 하면서 누적 혹은 갱신 되는 제품관련 코드관련 디자인 관련 문서는 어떻게 관리하게 그게 아니면 사이클마다 제품의 톤앤매너가 일관되지 않은제품들이 생성될거같은데

### 답변

AI 네이티브 병렬 개발에서 제일 먼저 무너지는 게 **제품 일관성**. 문서는 "기획 산출물"이 아니라 **AI들이 매번 참조하는 제품 운영체제**처럼 관리해야 함.

핵심:
```
지속 문서 = 제품의 기억
사이클 문서 = 이번 실험의 작업 지시서
```

**추천 구조**

```
/docs
  /product
    product-principles.md / target-users.md / positioning.md
    feature-map.md / roadmap.md
  /design
    brand-system.md / tone-and-manner.md / ui-principles.md
    components.md / interaction-patterns.md / empty-states.md / copywriting.md
  /engineering
    architecture.md / coding-conventions.md / api-contracts.md
    data-model.md / testing-strategy.md / security-principles.md
  /decisions
    0001-use-nextjs.md / 0002-pricing-model.md / 0003-dashboard-first-ux.md
  /cycles
    2026-05-16-api-log-search/
      brief.md / feature-contract.md / design-notes.md
      implementation-notes.md / review.md / learnings.md
```

**1. Canonical Docs는 짧고 강하게**

AI가 매번 읽어야 하는 문서는 길면 안 됨. 구체적이고 명확해야 함.

좋은 예 (tone-and-manner.md):
```md
## Voice
Use: "Import completed" / "3 issues need review" / "Connect a workspace to continue"
Avoid: "Awesome! You crushed it!" / "Oopsie, something went wrong" / "Unlock your productivity superpowers"

## UI Copy Rules
- Prefer verbs over slogans
- Use sentence case
- Button labels under 3 words when possible
- Error messages must include next action
```

**2. 디자인 문서 = "스타일"보다 "제약"** (금지/허용 규칙)

```md
## Layout
- SaaS/productivity tool style. Dense but readable.
- Avoid marketing-style hero sections inside the app.

## Components
- Cards: max border-radius 8px
- Buttons: icon-only for repeated tools
- Tables: compact row height, clear empty states
- Forms: labels always visible, no placeholder-only fields

## Color
- Primary: #2563EB / Text: #111827 / Muted: #6B7280
- Border: #E5E7EB / Danger: #DC2626 / Success: #16A34A

## Do Not Use
- Purple-blue gradient backgrounds
- Oversized rounded cards / Decorative blobs
- Emoji in product UI
- Marketing-style language inside operational flows
```

**3. 사이클마다 Context Pack 만들기**

매번 모든 문서 다 읽히는 방식은 비효율. 기능 개발 시작 전에 AI에게 줄 **Context Pack**:

```md
# Context Pack: API Log Search

Read first:
- /docs/product/product-principles.md
- /docs/design/tone-and-manner.md
- /docs/design/ui-principles.md
- /docs/engineering/architecture.md

Current feature:
- /docs/cycles/2026-05-16-api-log-search/feature-contract.md

Non-negotiables:
- Follow existing dashboard layout
- Do not introduce new colors
- Reuse existing table and filter components
- Empty state copy must match tone-and-manner.md
- Add analytics events listed in feature-contract.md
```

**4. 결정은 ADR로 남기기**

AI가 흔히 반복해서 흔드는 것 = 기술 스택 / 상태 관리 / 폴더 구조 / DB 모델링 / 인증 / 가격 / UX 흐름 / 네이밍.

```md
# 0003 Dashboard-first UX

## Decision: 제품은 로그인 후 워크스페이스 대시보드로 바로 진입
## Why: 사용자가 운영 데이터 검토하러 옴. 마케팅 콘텐츠 소비 아님
## Consequences:
- 로그인 후 app home hero 없음
- 네비게이션 영속
- empty state는 setup guide. 제품 전체 설명 X
- 향후 기능은 대시보드 IA에 attach (강한 이유 없으면)
```

**5. 코드 = 문서보다 "샘플 파일"이 더 강함**

AI에게는 실제 예시가 더 효과적.

```
새 기능은 /src/features/example-feature 구조를 따라라
API 핸들러는 /src/server/routes/projects.ts 스타일을 따라라
폼은 /src/components/forms/ProjectForm.tsx 패턴을 따라라
```

대표 구현체를 의도적으로 깨끗하게 유지하는 게 중요.

**6. 문서는 "누가 업데이트하나?"**

개발 사이클 종료 후 AI에게:
```
이번 변경사항을 보고 다음 문서를 업데이트해라:
- feature-map.md / api-contracts.md / components.md
- decisions/*.md 필요 여부 / cycle learnings.md

단, 기존 원칙을 바꾸는 변경은 proposal로만 작성하고 바로 수정하지 마라.
```

규칙:
```
기능 추가는 문서 갱신 가능
제품 원칙 변경은 제안만 가능
```

**7. 변경 규칙을 두 단계로 나누기**

```
Level 1: Product Constitution (product-principles / positioning / tone / ui-principles)
  변경 권한: 사람만 승인

Level 2: Product Memory (feature-map / components / api-contracts / data-model)
  변경 권한: AI가 초안, 사람이 리뷰

Level 3: Cycle Records (brief / implementation-notes / review / learnings)
  변경 권한: AI 자유
```

**8. 매 작업 시작 프롬프트 (시스템 프롬프트화)**

```
Before making changes:
1. Read the relevant canonical docs
2. Reuse existing patterns
3. Do not introduce new visual language unless explicitly requested
4. If the requested change conflicts with canonical docs, flag it before implementing
5. After implementation, update only the affected product memory docs
6. Do not modify product principles without explicit human approval
```

**9. 추천 문서 최소 세트** (시작 시 8개)

```
/docs/product/product-principles.md
/docs/product/target-users.md
/docs/product/feature-map.md
/docs/design/tone-and-manner.md
/docs/design/ui-principles.md
/docs/design/components.md
/docs/engineering/architecture.md
/docs/engineering/coding-conventions.md
/docs/decisions/
```

**10. 핵심 운영 원칙**

```
사이클 문서는 축적하고, 기준 문서는 통제해서 갱신한다.
```

문서 = AI 작업자들의 공유 기억. 그 기억은 아무나 바꾸면 안 됨.

---

## Q3. 문서 간 정합성, 최신화, 컨텍스트 효율화, 제품 문서화

### 질문

문서 간의 정합성은 어떻게 다룰건데 문서시스템은 너말대로 사용자를 위한 기록(이건 깃을 보면 되고)이 아닌 컨텍스트를 효율적으로 관리하기 위한 것이라고 생각해 문서간의 정합성 및 문서간의 최신화 그리고 어떤 문서를 언제 올바르게 참조할것이고 시간이 지나면서 거대해지는 문서는 어떻게 쪼갤 것이며 참조할 문서에 대해 컨텍스트를 항상 효율적으로 관리할것인가 더불어 제품에 대한 문서화도 하면 좋겠지 한번 생각해봐

### 답변

문서 시스템 목적 = **AI와 사람이 제품을 계속 같은 방식으로 이해하게 만드는 컨텍스트 관리 계층**. 핵심 문제 5개:
1. 어떤 문서가 진실의 원천?
2. 문서 간 충돌을 어떻게 감지?
3. 어떤 작업에서 어떤 문서만 읽게?
4. 문서가 커질 때 어떻게 분할?
5. 제품/코드 변경 후 무엇을 최신화?

**1. 문서 계층 (L0-L5)**

```
L0. Index / Context Map
L1. Canonical Principles
L2. Domain Source of Truth
L3. Operational Guides
L4. Cycle / Decision Records
L5. Generated Summaries

/docs
  context-map.md
  /principles (product-principles / design-principles / engineering-principles)
  /domains (onboarding / projects / billing / api-logs / teams)
  /systems (design-system / architecture / data-model / analytics / permissions)
  /playbooks (feature-development / ui-change / api-change / schema-change / release)
  /decisions (0001-* / 0002-* ...)
  /cycles (2026-05-16-api-log-search/ ...)
  /generated (ai-context-pack / product-summary / design-summary / engineering-summary)
```

권위 위계:
```
principles > domains/systems > playbooks > cycles > generated
```

`/cycles`에 있는 내용이 `/principles`와 충돌하면 `/principles`가 이김. `/generated`는 캐시일 뿐, 절대 진실의 원천 X.

**2. 문서마다 "소유 범위" 명확히**

정합성 문제 = 대부분 같은 사실을 여러 문서에 중복.

좋은 방식: `/docs/domains/billing.md` 만 가격 정책의 원천. 다른 문서는 링크만:
```
Pricing details are defined in /docs/domains/billing.md#plans.
```

Frontmatter:
```yaml
---
id: domain.billing
title: Billing Domain
owner: product
status: canonical
authority: source
last_reviewed: 2026-05-16
depends_on:
  - principles.product
  - systems.permissions
---

## Source Of Truth For
- Plan names / Pricing model / Trial policy / Upgrade-downgrade rules

## Not Source Of Truth For
- Marketing copy / Payment provider implementation / Invoice UI layout
```

**3. context-map.md = 문서 라우터**

```md
## Always Read
- /docs/principles/product-principles.md
- /docs/principles/design-principles.md
- /docs/principles/engineering-principles.md

## By Task Type

### New Feature
Read: /docs/playbooks/feature-development.md + affected domain + relevant system + latest ADRs
Update: affected domain + analytics if events changed + generated product-summary

### UI Change
Read: design-principles + design-system + affected domain + existing component examples
Update: design-system if reusable pattern changed + affected domain if UX behavior changed

### API Change
Read: architecture + data-model + affected domain + relevant API contracts
Update: api-contracts + data-model if schema changed + affected domain

### Copy Change
Read: product-principles + design-principles + copy-style + affected domain
Update: affected domain only if product behavior changed
```

컨텍스트의 입구는 항상 context-map.md 하나.

**4. 정합성 = "링크 그래프 + 체크"**

```yaml
---
id: domain.api_logs
status: canonical
authority: source
last_reviewed: 2026-05-16
depends_on:
  - principles.product / principles.design / systems.data_model
related_code:
  - src/features/api-logs / src/server/api/logs
related_tests:
  - tests/api-logs
---
```

`npm run docs:check`:
- 모든 depends_on id가 존재?
- 깨진 문서 링크?
- 같은 source_of_truth 범위가 여러 문서에 중복 선언?
- last_reviewed가 너무 오래된 canonical 문서?
- related_code 경로 존재?
- 코드 변경 있었는데 관련 문서 갱신 X?
- generated 문서가 canonical 문서를 수정?

**5. 최신화 = "코드 diff 기반"**

`doc-ownership.yml`:
```yaml
rules:
  - code: "src/features/billing/**"
    docs: ["docs/domains/billing.md"]
  - code: "src/components/ui/**"
    docs: ["docs/systems/design-system.md"]
  - code: "src/server/api/**"
    docs: ["docs/systems/api-contracts.md"]
  - code: "db/migrations/**"
    docs: ["docs/systems/data-model.md"]
```

AI에게:
```
이번 diff를 보고 doc-ownership.yml 기준으로 업데이트 필요 문서를 식별.
필요하면 수정. 필요 없으면 docs/no-update-needed.md에 이유 남김.
```

**6. 거대해지는 문서는 "크기"가 아니라 "책임"으로 쪼갬**

분할 기준:
- 서로 다른 사람이/AI가 자주 따로 수정?
- 서로 다른 작업 타입에서 참조?
- 변경 주기가 다른가?
- source_of_truth 범위 분리?
- 한 문서 읽기 위해 불필요 내용이 너무 많은가?

큰 문서는 "허브 문서"로:
```md
# Design System

This document routes design references.

## Core
- Color, typography, spacing: /docs/systems/design/tokens.md
- Component rules: /docs/systems/design/components.md

## Components
- Buttons: /docs/systems/design/components/buttons.md
- Forms: /docs/systems/design/components/forms.md

## Patterns
- Empty states: /docs/systems/design/patterns/empty-states.md
- Navigation: /docs/systems/design/patterns/navigation.md
```

**7. 효율적인 컨텍스트 = "요약 캐시"**

```
/docs/generated
  product-context.md / design-context.md / engineering-context.md
  domain-index.md / ai-context-pack.md
```

규칙:
```
generated 문서는 참조 최적화용 캐시
generated 문서와 canonical 충돌 시 canonical 이김
generated 문서는 자동 재생성 가능해야 함
```

AI 작업 시작 시 기본:
```
1. /docs/generated/ai-context-pack.md
2. /docs/context-map.md
3. only task-specific domain/system docs
```

**8. 최신화 흐름 = 사이클 중간 체크포인트**

```
Before Build:
- context-map.md로 참조 문서 결정
- affected domain/system docs 읽기
- feature contract 작성

During Build:
- 계약과 다른 구현 → 계약 또는 구현 수정
- 새 결정 → ADR 후보 기록

Before Merge:
- docs:check / doc-ownership 기준 문서 업데이트 확인
- generated summaries 재생성 / AI consistency review

After Release:
- 피드백 반영 / domain doc "Observed Behavior / Learnings" 업데이트
```

핵심 = 구현이 문서와 달라졌을 때 둘 중 하나를 반드시 고름:
```
문서가 맞고 구현이 틀렸나? 구현이 새 의사결정이고 문서를 바꿔야 하나?
```

**9. 제품 문서화 = "사용자용"과 "AI용" 분리**

```
/docs
  /internal (context-map / principles / domains / systems / decisions)
  /user-facing (getting-started / guides / faq / changelog / release-notes)
```

연결:
```yaml
---
id: user.guide.api_logs_search
source_domain: domain.api_logs
depends_on: [domain.api_logs, systems.permissions]
last_synced: 2026-05-16
---
```

사용자 문서는 내부 도메인 문서를 기반으로 생성/갱신.

**10. 문서 작업에도 리뷰 역할**

```
Act as a documentation consistency reviewer.

Check:
- Does the implementation conflict with canonical docs?
- Are any source-of-truth facts duplicated?
- Are changed code paths mapped in doc-ownership.yml?
- Are generated summaries stale?
- Are user-facing docs affected?
- Are new decisions captured as ADRs?
- Are any docs too large and needing split by responsibility?

Return: Required doc updates / Conflicts / Stale docs / Suggested splits / No-change justifications
```

이 역할은 구현 AI와 분리해야 함. 구현한 AI는 자기 변경을 과신.

**결론**

```
문서 = 기록물이 아니라 컨텍스트 라우팅 시스템

좋은 시스템:
1. context-map.md (라우팅 결정)
2. canonical docs (진실의 원천)
3. domain docs (현재 상태 + 행동 규칙)
4. doc-ownership.yml (코드 → 문서 연결)
5. frontmatter metadata (의존성/권위/최신성/관련 코드)
6. docs:check (링크/중복/stale/ownership 검증)
7. generated context packs (AI 컨텍스트 비용 줄임)
8. user-facing docs (내부 도메인에서 파생)

운영 원칙:
같은 사실은 한 문서에만. 다른 문서는 링크/파생.
AI는 context-map을 통해 필요한 문서만 읽음.
변경은 doc-ownership 기준으로 자동 결정.
generated 문서는 캐시. canonical 항상 이김.
```

---

## Part 2. 이번 대화 진화 (2026-05-16) — 핵심 박제

### 2-1. Sprint frame 진단 (Linear cycle 4개월 분량 미리 박제)

**시작점**: v2.0-sprint-3 (v2.0.1 ship) closed. 잔여 백로그 분석 + 다음 sprint 계획 요청.

**진행 흐름**:
1. Linear 상태 조회 → 4 cycle 완료 (v1.9 / v2.0-sprint-1 / sprint-2 / sprint-3)
2. v2.0-sprint-4 (6/14~6/28) 박제: INP-139 (8pt) + INP-134 (3pt) + INP-136 (5pt) = 16pt
3. 신규 PM draft 발견: SPRINT_AI_LEARNING_RESEARCH.md — F-SUGGEST-Q / F-EMBED-VIZ / F-INSIGHT / F-QUIZ-PDF 4 기능 분석
4. PM 권장 옵션 C-lite (sprint-4 유지 + v2.1-s1 신설) 사용자 채택
5. INP-151 (F-SUGGEST-Q, 7pt) + INP-152 (F-INSIGHT, 8pt) 발급 + cycle #7 (v2.1-sprint-1) 명명
6. 의존성 체크 요청 (사용자) → 의존성 graph + 4 결정 박제
7. Codex consult challenge → 5 발견 (출시 직전 schema 대수술 위험 / pt 과소산정 / migration 005 조건 / INP-152 strict sequential 아님 / 검증 결여)
8. 사용자 회의 ("이렇게 할 필요가 있나") + pt 폐기 정합

### 2-2. 1인 + AI swarm 정합 인식

**핵심 진단**: "작업 → 발견 → INP 발급 → 다음 sprint 미룸" 누적 패턴이 antipattern.
- 발급 시점 schema vs 진행 시점 schema = drift
- 미뤄진 INP 끼리 의존성 fix-up 비용
- 출시 anchor 와 충돌 (INP-139 케이스)
- sprint cycle 이 "미루는 핑계" 됨

**진짜 cost**:
- AI 코드 작성 = 즉시 (분~시간)
- 사람 검토 게이트 = 진짜 제한
- "나중에 한다" 옵션 자체가 비싸짐

### 2-3. 다이어트 결정 (1차) — sprint cycle 폐기

| 폐기 | 유지 |
|------|------|
| v2.0-sprint-4 / v2.1-sprint-1 / v2.1-sprint-2 / cycle #6 = INP 5개 backlog 이동 | v2.0-sprint-5 (CWS+PH 출시) anchor |
| Codex / 의존성 graph / 검토 게이트 측정 frame (AI 자체 도입) | 사용자 결정 박제 (D-Q1~D-Q4) |

**박제 패턴**:
1. 2 horizon 분리: 분기 roadmap + 2주 sprint anchor
2. Sprint cycle = 출시 anchor 만
3. 작업 중 발견 → 즉시 처리 OR 영원히 폐기
4. INP description = AC 확인용
5. AI agent = 분기 시작 plan-ceo-review 1회
6. Backlog = 우선순위 + 의존성, 시간축 박제 X
7. Codex / 의존성 graph 등 = 사용자 명시 호출 시만

### 2-4. 자가 비판 (1인 + AI swarm 박제 패턴)

1. **거짓 이분법** — "즉시 처리 OR 영원히 폐기". 현실은 4 옵션 (즉시 / 현재 PR 자연 확장 / 다음 작업 묶음 INP / 폐기). 이분법 단순화 위험.

2. **자가 모순** — 출시 anchor sprint 중 발견 → 즉시 처리 시 scope 폭발, 폐기 시 결함 누적. "출시 후 처리" INP 발급 = 박제한 패턴 위반.

3. **분기 roadmap 1회 cargo cult** — 12주 vision 일관 진행은 1인 현실 X. YC / 대기업 OKR 패턴 그대로 적용.

4. **자기 박제 모순** — 박제 패턴 자체가 AI 사용자 한 줄 → 메타 분석 결과. 박제 후 "AI 메타 자제" 박제 = 자기모순.

5. **검증 결여** — 1회 자가 진단 → 즉시 박제. 1-2 sprint retro 없음.

6. **INP 일률 다이어트 정보 손실** — AC 만 박제 시 결정 이력 손실. 위치 분리 (ADR/RFC) 필요.

### 2-5. AI 네이티브 프로세스 — 내 직전 응답 (Stream + Fan-out + Spec-as-Prompt)

**7 패턴**:
1. Stream — Sprint 폐기, Continuous Intent Queue
2. Fan-out — AI agent 3-5명 동시 병렬
3. 1 Sentence Intent — PRD 폐기
4. Spec-as-Data, AI-as-Runtime
5. Multi-agent Debate — 사람 = Judge
6. Decision Log Auto-Capture
7. Reception → Intent 자동 추천

**효율 측정 변경**:
- Sprint velocity (pt/sprint) → 하루 처리 intent 수
- PR throughput → 시각 verify 게이트 수/일
- Bug 수 → 출시 후 reception 결함률
- Cycle time → Intent → ship 시간 (분 단위)

### 2-6. 외부 답변 vs 내 응답 비교

**수용 8개** (외부 답변 가치):
1. ⭐ Feature Contract (5-10 줄, fan-out 충돌 차단)
2. ⭐ "검증 가능한 행동" 단위 (기능 → 행동, ICP 중심)
3. ⭐ 소유 범위 frontmatter (Source Of Truth For)
4. ⭐ context-map.md 라우터
5. ⭐ doc-ownership.yml (코드 → 문서 자동 매핑)
6. ⭐ 변경 권한 3 level (Constitution / Memory / Records)
7. ⭐ 디자인 = "제약" (금지/허용 규칙)
8. ⭐ AI Review Swarm 6 axis (security/UX/perf/test/simplicity/consistency)

**비판 7개** (외부 답변 폐기):
1. 9 단계 사이클 (Brief→Discovery→Memo→Contract→Build→Review→Integration→Ship→Compression) — 단계 폭증
2. 일/주 단위 리듬 — Sprint 변형, 시간축 박제 antipattern
3. 문서 8+ doc minimum + 5 level 계층 — 시작 단계 over-engineering
4. 자동화 인프라 11개 시작 시점 박제 요구
5. docs:check 자동화 — 박제 cost
6. 사용자용 vs AI용 동시 박제 — 출시 timing 정합 X
7. Framework heavy 결론

### 2-7. 통합 모델 (MVP 3 축 + 점진 추가)

```
[ICP 행동 박제]
  ↓ 1-3 sentence intent + 5-10 줄 Feature Contract
[Intent Queue]
  ↓ pull top
[AI Fan-out 병렬] — 3-5 agent
  ├─ Build (구현)
  ├─ Review Swarm 3 axis (security + UX + simplicity)
  └─ Doc auto-update
  ↓
[사람 verify] — 시각 검증 + 통합 결정
  ↓ ship / iterate / discard
[Memory + ADR auto-capture]
  ↓
[Reception → 다음 Intent 추천]
```

**문서 MVP (3 doc + 점진)**:
```
시작:
  /docs/principles/product.md
  /docs/principles/design.md (제약 형식)
  /docs/principles/engineering.md
  /docs/decisions/

점진 추가 (누락 발생 시):
  /docs/domains/{name}.md
  /docs/context-map.md (문서 5+ 시)
  doc-ownership.yml (코드→문서 update 누락 발생 시)
  /docs/generated/ (AI 컨텍스트 비용 측정 후)
```

**자동화 MVP**:
```
시작 (출시 직전):
  - 타입체크 + 린트 + 에러 로깅
점진:
  - 자동 테스트 (회귀 발생 시)
  - 프리뷰 배포 / 세션 리플레이
```

**핵심 통찰** (외부 답변의 진짜 가치):
> AI에게 일을 많이 시키는 것보다, AI들이 서로 충돌하지 않도록 작은 계약과 경계를 잘 주는 것이 더 중요하다.

내가 누락한 것 = **fan-out 시 agent 간 충돌 차단 인프라** (Feature Contract + 소유 범위 + 디자인 제약 3 도구).

---

## Part 3. 다음 실험 (병렬 구현-리뷰 fan-out)

### 3-1. Linear 잔여 INP 의존성 매트릭스

| INP | 영향 영역 | INP-95 의존 | INP-139 의존 | 다른 INP 의존 | 병렬 가능 |
|-----|---------|------------|------------|------------|---------|
| INP-134 드래그 캡처 | content_script (Extension) | X | X (source enum 만) | X | ✅ **단독, 즉시** |
| INP-136 임베딩 시각화 | graph engine (Web) | ✅ (embedding) | X | X | ✅ **단독, 즉시** |
| INP-139 노션 통합 | schema + repository + graph + sidebar + detail panel | X | - | X | ❌ 큰 영향, 출시 후 단독 |
| INP-151 F-SUGGEST-Q | Edge Function + ai_usage + suggest-cache + sidebar | ✅ | ⚠️ (page 표현 deferable) | X | ✅ (출시 후) |
| INP-152 F-INSIGHT | Edge Function mode + UI | ✅ | ⚠️ | ✅ INP-151 (contract 락인) | △ INP-151 contract 락인 후 |

### 3-2. 즉시 병렬 fan-out 후보

**INP-134 (Extension) + INP-136 (Web) = 완전 독립**
- Codebase 분리 (extension vs web)
- File scope 충돌 0
- 두 agent 동시 시작 가능

### 3-3. 시작 (MVP 통합 모델 검증)

```
agent A (frontend-engineer, background):
  INP-134 Feature Contract + 구현 (Extension)

agent B (frontend-engineer, background):
  INP-136 Feature Contract + 구현 (Web, Web Worker + D3)

(완료 후) review fan-out:
  agent C: security review (CSP / Selection API / Worker)
  agent D: UX review (캡처 진입점 / 임계값 슬라이더 UX)
  agent E: simplicity review (코드 단순성)

(완료 후) 사람 verify (시각 검증) → commit
```

### 3-4. 검증 가설

1. **Feature Contract 가 fan-out 충돌 차단 효과** — 두 agent 가 같은 영역 변경 X
2. **AI 코딩 시간 vs 사용자 검토 게이트 시간** 실측 — 진짜 cost 어디?
3. **MVP 3 축 (Intent + Contract / Fan-out / Verify) 가 9 단계 보다 효율** 검증
4. **Review Swarm 3 axis (security + UX + simplicity)** 가 6 axis 보다 충분?

### 3-5. 후속 (출시 후)

- v2.0-sprint-5 (CWS+PH, 6/28~7/11) 출시 + reception 1주+
- 분기 roadmap review (`/plan-ceo-review`) — vision-level forcing question
- INP-151/152 진입 결정 (F-SUGGEST-Q / F-INSIGHT 가 진짜 ICP 가치인가?)
- INP-139 진입 결정 (schema 대수술 필요성)
- 본 _upgrade.md 박제 패턴 retro — 검증 / 갱신 / 폐기

---

## Part 4. 박제 운영 원칙 (다음 작업에 적용)

### Agent worker 위임 prompt 표준 (Feature Contract 정합)

```
## Feature Contract
- 목표: [1 sentence]
- 입력: [list]
- 출력: [list]
- AC: [checklist, 5-10 lines]
- 비범위: [explicit out-of-scope]

## Files (write scope, 충돌 차단)
- [exact paths]

## 작업 절차
1-5 steps

## Schema/의존성 정합
- backend constraints / 선행 INP / 회피 사항

## 커밋
- ❌ git commit 금지 — 변경(Write/Edit)만
- 사용자 시각 검증 (절차 명시) 후 메인 AI 가 commit

## 보고
- 변경 파일 list + diff 요약
- 시각 검증 절차
- 발견된 회귀 / 충돌 / blocker
```

### 사용자 시각 검증 게이트 (commit 직전)

1. dev 서버 / extension reload
2. AC checklist 시각 확인
3. 회귀 영역 시연 (기존 기능 영향 없음 확인)
4. 사용자 명시 OK → commit marker → commit

### 박제 무게 측정 (self-check)

- "이거 6주 뒤에 누가 읽을까?" → 자기 자신만 = 1줄 충분
- "지금 박제하지 않으면 미래에 손실?" → No = 박제 X
- "이 박제가 fan-out 충돌 차단에 기여?" → No = 박제 X

---

**작성**: 2026-05-16
**다음 갱신**: 다음 작업 (INP-134 + INP-136 fan-out) 완료 후 retro 결과 반영
