# AI 네이티브 1인 제품 개발 프로세스 대화 기록

## Q1. AI 네이티브 병렬형 제품 개발 프로세스

### 질문

ai 네이티브로 1인 프로덕트 개발인데 기존의 제품개발프로세스가 아닌 병렬형 AI 네이티브 개발 프로세스에 대해서 한번 생각을 해봐 뭐가 효율적일까

### 답변

1인 프로덕트 개발에서 “AI 네이티브”의 핵심은 기존처럼 `기획 → 디자인 → 개발 → 테스트 → 배포`를 직렬로 밟는 게 아니라, **사람은 제품 판단과 통합을 맡고, AI들은 탐색·구현·검증을 병렬로 돌리는 구조**를 만드는 겁니다.

가장 효율적인 형태는 이렇게 봅니다.

**1. 사람은 PM이 아니라 편집장처럼 움직이기**

1인 개발자가 모든 걸 직접 “작성”하려고 하면 AI를 써도 병목은 여전히 본인입니다. 대신 역할을 이렇게 바꾸는 게 좋습니다.

- 문제 정의
- 제품 방향 결정
- 우선순위 판단
- 결과물 리뷰
- 최종 통합
- 배포 결정

즉, 사람은 “일하는 사람”이라기보다 **결정권자 + 리뷰어 + 통합자**에 가까워집니다.

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

```text
아이디어 → 요구사항 → 디자인 → 개발 → QA → 배포
```

AI 네이티브 프로세스:

```text
가설 설정
→ 병렬 탐색
→ 후보 비교
→ 빠른 구현
→ 자동 검증
→ 사용자/시장 피드백
→ 다음 가설
```

중요한 건 “완벽한 PRD를 쓰고 시작”이 아니라, **작은 가설을 여러 방향으로 동시에 검증**하는 겁니다.

예를 들면:

```text
가설: 개발자들이 API 로그 분석을 더 쉽게 하고 싶어 한다.
```

이때 한 AI에게만 “이거 만들어줘”가 아니라:

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

```text
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

```text
DB/백엔드
프론트엔드
테스트
문서
리뷰
```

이렇게 write scope를 나눠야 합니다.

**4. “스펙”보다 “계약”을 먼저 만드는 게 중요**

AI 병렬 개발에서 가장 중요한 산출물은 긴 기획서가 아니라 **작은 계약서**입니다.

예:

```text
Feature Contract

목표:
- 사용자는 로그 목록에서 status code, method, path, date range로 필터링할 수 있다.

입력:
- projectId
- query
- statusCode
- method
- from
- to

출력:
- logs[]
- totalCount
- nextCursor

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

```text
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

**Product Brief**

하루짜리 문서입니다.

```text
누구의 어떤 문제인가?
기존 대안은 왜 부족한가?
이번 주에 검증할 행동은 무엇인가?
성공 신호는 무엇인가?
```

**Parallel Discovery**

AI 여러 개에게 동시에 시킵니다.

```text
시장 조사
페르소나
경쟁 제품
UX 흐름
기술 리스크
가격 모델
```

**Decision Memo**

사람이 결론만 씁니다.

```text
우리는 A 방향으로 간다.
B는 버린다.
C는 나중에 한다.
이유는 X다.
```

**Feature Contract**

위에서 말한 작은 기능 계약입니다.

**Parallel Build**

역할 분리해서 구현합니다.

**AI Review Swarm**

구현 후 다른 AI들에게 리뷰시킵니다.

- 보안 리뷰
- UX 리뷰
- 성능 리뷰
- 테스트 리뷰
- 코드 단순성 리뷰
- 제품 일관성 리뷰

**Human Integration**

여기서 1인 개발자가 직접 봐야 합니다. AI가 많이 만들수록 통합 품질이 제품 품질입니다.

**Ship**

완성도가 100%일 때가 아니라, 가설 검증 가능한 수준이면 배포합니다.

**Feedback Compression**

유저 피드백, 로그, 에러, 세션 리플레이, 문의를 AI에게 요약시켜 다음 가설로 압축합니다.

**6. 가장 효율적인 작업 단위는 “기능”보다 “검증 가능한 행동”**

기존 개발은 기능 단위로 쪼갭니다.

```text
로그인
대시보드
검색
결제
설정
```

AI 네이티브 개발에서는 행동 단위가 더 좋습니다.

```text
사용자가 30초 안에 첫 프로젝트를 생성한다.
사용자가 에러 로그 원인을 찾는다.
사용자가 팀원에게 링크를 공유한다.
사용자가 결제 전에 가치를 이해한다.
```

이렇게 잡으면 AI가 UI, 백엔드, 카피, 온보딩, 분석 이벤트까지 한꺼번에 제안할 수 있습니다.

**7. 1인 개발자에게 특히 중요한 자동화**

AI 네이티브 개발의 병목은 “생성”이 아니라 “검증”입니다. 그래서 아래는 초기에 깔아두는 게 좋습니다.

- 자동 테스트
- 타입 체크
- 린트
- 프리뷰 배포
- 에러 로깅
- 사용 이벤트 추적
- 세션 리플레이
- DB 마이그레이션 검증
- 스모크 테스트
- AI 코드 리뷰 프롬프트
- 릴리즈 체크리스트

AI가 코드를 빨리 만들수록, 검증 장치가 없으면 제품이 빠르게 망가집니다.

**8. 실전 운영 방식**

하루 단위로 보면 이렇게 할 수 있습니다.

```text
오전:
- 오늘의 제품 가설 1개 선택
- AI 3~5개로 탐색/설계 병렬 실행

점심 전:
- 결과 비교
- 기능 계약 작성
- 범위 축소

오후:
- 구현 에이전트 병렬 실행
- 테스트/리뷰 에이전트 별도 실행

저녁:
- 직접 통합
- 배포
- 피드백/로그 확인
- 다음 가설 정리
```

일주일 단위:

```text
월: 문제/가설 정리
화-목: 기능 실험 2~3개 제작
금: 배포/측정/사용자 인터뷰
주말: 방향 유지, 전환, 폐기 결정
```

**9. 피해야 할 것**

AI 네이티브라고 해도 비효율적인 패턴이 있습니다.

- 큰 PRD를 쓰고 한 번에 거대한 앱 만들기
- AI에게 “알아서 좋은 제품 만들어줘”라고 하기
- 여러 AI가 같은 파일을 동시에 수정하게 하기
- 검증 없이 코드만 계속 쌓기
- 사용자 피드백 없이 내부 완성도만 올리기
- 디자인, 카피, 온보딩을 개발 끝난 뒤에 붙이기
- 테스트 없이 배포 속도만 높이기
- 매번 새 아키텍처를 AI에게 제안받기
- 사람이 최종 제품 판단을 안 하기

**10. 결론적으로 가장 효율적인 구조**

1인 AI 네이티브 제품 개발은 이렇게 정의하는 게 좋습니다.

```text
Human:
제품 판단, 우선순위, 통합, 최종 책임

AI Agents:
탐색, 초안, 구현, 테스트, 리뷰, 문서화

Process:
작은 가설 → 병렬 생성 → 사람의 선택 → 빠른 배포 → 피드백 압축
```

가장 중요한 원칙은 이겁니다.

```text
AI에게 일을 많이 시키는 것보다,
AI들이 서로 충돌하지 않도록 작은 계약과 경계를 잘 주는 것이 더 중요하다.
```

그래서 1인 개발자에게 최적의 프로세스는 “AI가 대신 개발하는 프로세스”가 아니라, **사람 한 명이 여러 명의 AI 작업자를 지휘하는 병렬 제품 시스템**에 가깝습니다.

## Q2. 제품/코드/디자인 문서 관리와 톤앤매너 일관성

### 질문

제품 개발을 하면서 누적 혹은 갱신 되는 제품관련 코드관련 디자인 관련 문서는 어떻게 관리하게 그게 아니면 사이클마다 제품의 톤앤매너가 일관되지 않은제품들이 생성될거같은데

### 답변

맞습니다. AI 네이티브 병렬 개발에서 제일 먼저 무너지는 게 **제품 일관성**입니다. 그래서 문서는 “기획 산출물”이 아니라 **AI들이 매번 참조하는 제품 운영체제**처럼 관리해야 합니다.

핵심은 문서를 많이 만드는 게 아니라, **갱신되는 기준 문서와 일회성 작업 문서를 분리**하는 겁니다.

```text
지속 문서 = 제품의 기억
사이클 문서 = 이번 실험의 작업 지시서
```

**추천 구조**

```text
/docs
  /product
    product-principles.md
    target-users.md
    positioning.md
    feature-map.md
    roadmap.md

  /design
    brand-system.md
    tone-and-manner.md
    ui-principles.md
    components.md
    interaction-patterns.md
    empty-states.md
    copywriting.md

  /engineering
    architecture.md
    coding-conventions.md
    api-contracts.md
    data-model.md
    testing-strategy.md
    security-principles.md

  /decisions
    0001-use-nextjs.md
    0002-pricing-model.md
    0003-dashboard-first-ux.md

  /cycles
    2026-05-16-api-log-search/
      brief.md
      feature-contract.md
      design-notes.md
      implementation-notes.md
      review.md
      learnings.md
```

여기서 중요한 건 `/product`, `/design`, `/engineering`은 계속 갱신되는 **Canonical Docs**이고, `/cycles`는 각 실험/기능의 기록입니다.

**1. Canonical Docs는 짧고 강해야 함**

AI가 매번 읽어야 하는 문서는 길면 안 됩니다. 길수록 안 지킵니다.

예를 들어 `tone-and-manner.md`는 이렇게 구체적이어야 합니다.

```md
# Tone and Manner

## Product Personality
- Calm, precise, professional.
- Helps users feel in control.
- Avoids hype, jokes, and vague encouragement.

## Voice
Use:
- “Import completed”
- “3 issues need review”
- “Connect a workspace to continue”

Avoid:
- “Awesome! You crushed it!”
- “Oopsie, something went wrong”
- “Unlock your productivity superpowers”

## UI Copy Rules
- Prefer verbs over slogans.
- Use sentence case.
- Keep button labels under 3 words when possible.
- Error messages must include next action.
```

이 정도면 AI가 실제로 따릅니다.

반대로 이런 문서는 별로 도움이 안 됩니다.

```md
우리는 심플하고 모던하며 사용자 친화적인 톤을 지향한다.
```

너무 추상적이라 매번 다른 결과가 나옵니다.

**2. 디자인 문서는 “스타일”보다 “제약”이어야 함**

AI에게 “예쁘게 만들어줘”라고 하면 매번 톤이 바뀝니다. 디자인 문서는 취향 설명이 아니라 **금지/허용 규칙**이어야 합니다.

예:

```md
# UI Principles

## Layout
- SaaS/productivity tool style.
- Dense but readable.
- Avoid marketing-style hero sections inside the app.
- Primary app screens should prioritize tables, panels, filters, and clear actions.

## Components
- Cards: max border-radius 8px.
- Buttons: use icon-only buttons for repeated tools.
- Tables: compact row height, clear empty states.
- Forms: labels always visible, no placeholder-only fields.

## Color
- Primary: #2563EB
- Text: #111827
- Muted text: #6B7280
- Border: #E5E7EB
- Danger: #DC2626
- Success: #16A34A

## Do Not Use
- Purple-blue gradient backgrounds.
- Oversized rounded cards.
- Decorative blobs.
- Emoji in product UI.
- Marketing-style language inside operational flows.
```

AI 병렬 개발에서는 “이렇게 해라”보다 **“이 선 밖으로 나가지 마라”**가 더 효과적입니다.

**3. 사이클마다 시작 전에 Context Pack을 만들기**

매번 모든 문서를 다 읽히는 방식은 비효율적입니다. 대신 기능 개발 시작 전에 AI에게 줄 **Context Pack**을 만듭니다.

예:

```md
# Context Pack: API Log Search

Read first:
- /docs/product/product-principles.md
- /docs/design/tone-and-manner.md
- /docs/design/ui-principles.md
- /docs/engineering/architecture.md
- /docs/engineering/api-contracts.md

Current feature:
- /docs/cycles/2026-05-16-api-log-search/feature-contract.md

Non-negotiables:
- Follow existing dashboard layout.
- Do not introduce new colors.
- Reuse existing table and filter components.
- Empty state copy must match tone-and-manner.md.
- Add analytics events listed in feature-contract.md.
```

즉, AI에게 매번 “우리 제품답게 해줘”라고 하지 말고, **참조해야 할 기준 문서와 이번 기능의 경계**를 같이 줘야 합니다.

**4. 결정은 ADR로 남기기**

AI가 흔히 반복해서 흔드는 것들이 있습니다.

- 기술 스택
- 상태 관리 방식
- 폴더 구조
- DB 모델링 방식
- 인증 방식
- 가격 정책
- UX 흐름
- 네이밍

이건 `decisions`에 남깁니다.

예:

```md
# 0003 Dashboard-first UX

## Decision
The product opens directly into the workspace dashboard after login.

## Why
Users come to inspect operational data, not consume marketing content.

## Consequences
- No app home hero after login.
- Navigation is persistent.
- Empty states should guide setup, not explain the entire product.
- Future features must attach to the dashboard IA unless there is a strong reason.
```

ADR이 있으면 AI가 매번 “더 좋은 아이디어”라며 방향을 바꾸는 걸 막을 수 있습니다.

**5. 코드 쪽은 문서보다 “샘플 파일”이 더 중요**

코딩 컨벤션 문서도 필요하지만, AI에게는 실제 예시가 더 강합니다.

그래서 이런 식으로 관리하는 게 좋습니다.

```text
/docs/engineering/coding-conventions.md
/src/features/example-feature/
/src/components/ui/
```

그리고 지시할 때:

```text
새 기능은 /src/features/example-feature 구조를 따라라.
API 핸들러는 /src/server/routes/projects.ts 스타일을 따라라.
폼은 /src/components/forms/ProjectForm.tsx 패턴을 따라라.
```

AI는 추상 규칙보다 기존 코드 패턴을 잘 따라갑니다. 따라서 **대표 구현체를 의도적으로 깨끗하게 유지하는 것**이 중요합니다.

**6. 문서는 “누가 업데이트하나?”**

1인 개발이라도 이렇게 역할을 나누면 됩니다.

개발 사이클 종료 후 AI에게 시킵니다.

```text
이번 변경사항을 보고 다음 문서를 업데이트해라:
- feature-map.md
- api-contracts.md
- components.md
- decisions/*.md 필요 여부
- cycle learnings.md

단, 기존 원칙을 바꾸는 변경은 proposal로만 작성하고 바로 수정하지 마라.
```

여기서 중요한 규칙:

```text
기능 추가는 문서 갱신 가능
제품 원칙 변경은 제안만 가능
```

예를 들어 버튼 스타일이 새로 생겼다면 `components.md` 갱신 가능.  
하지만 제품 톤을 “더 캐주얼하게” 바꾸는 건 AI가 마음대로 하면 안 됩니다.

**7. 변경 규칙을 두 단계로 나누기**

문서는 전부 같은 무게가 아닙니다.

```text
Level 1: Product Constitution
- product-principles.md
- positioning.md
- tone-and-manner.md
- ui-principles.md

변경 권한:
- 사람만 승인

Level 2: Product Memory
- feature-map.md
- components.md
- api-contracts.md
- data-model.md

변경 권한:
- AI가 초안 작성, 사람이 리뷰

Level 3: Cycle Records
- brief.md
- implementation-notes.md
- review.md
- learnings.md

변경 권한:
- AI가 자유롭게 작성
```

이렇게 해야 AI가 제품의 정체성을 매 사이클마다 바꾸지 않습니다.

**8. 매 작업 시작 프롬프트에 고정으로 넣을 것**

AI에게 이런 기본 지시를 반복적으로 줘야 합니다.

```text
Before making changes:
1. Read the relevant canonical docs.
2. Reuse existing patterns.
3. Do not introduce new visual language unless explicitly requested.
4. If the requested change conflicts with canonical docs, flag it before implementing.
5. After implementation, update only the affected product memory docs.
6. Do not modify product principles without explicit human approval.
```

이건 거의 시스템 프롬프트처럼 써야 합니다.

**9. 추천 문서 최소 세트**

처음부터 문서를 너무 많이 만들 필요는 없습니다. 최소로 시작한다면 이 8개면 됩니다.

```text
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

이 정도만 있어도 제품 일관성이 크게 좋아집니다.

**10. 핵심 운영 원칙**

가장 중요한 건 이겁니다.

```text
사이클 문서는 축적하고,
기준 문서는 통제해서 갱신한다.
```

AI 네이티브 개발에서 문서는 기록용이 아니라 **AI 작업자들의 공유 기억**입니다.  
그리고 그 기억은 아무나 바꾸면 안 됩니다.

그래서 최종 구조는 이렇게 가는 게 좋습니다.

```text
Canonical Docs:
제품의 정체성, 디자인 원칙, 기술 원칙

Cycle Docs:
이번 기능의 가설, 계약, 구현 기록, 배운 점

Decision Records:
되돌아가면 안 되는 판단의 이유

Reference Code:
AI가 따라야 할 실제 구현 예시
```

이 네 가지가 있으면 병렬 AI 개발을 하더라도 매번 다른 제품이 튀어나오는 문제를 꽤 강하게 막을 수 있습니다.

## Q3. 문서 간 정합성, 최신화, 컨텍스트 효율화, 제품 문서화

### 질문

문서 간의 정합성은 어떻게 다룰건데 문서시스템은 너말대로 사용자를 위한 기록(이건 깃을 보면 되고)이 아닌 컨텍스트를 효율적으로 관리하기 위한 것이라고 생각해 문서간의 정합성 및 문서간의 최신화 그리고 어떤 문서를 언제 올바르게 참조할것이고 시간이 지나면서 거대해지는 문서는 어떻게 쪼갤 것이며 참조할 문서에 대해 컨텍스트를 항상 효율적으로 관리할것인가 더불어 제품에 대한 문서화도 하면 좋겠지 한번 생각해봐

### 답변

맞습니다. 이 문서 시스템의 목적은 “기록 보관”이 아니라 **AI와 사람이 제품을 계속 같은 방식으로 이해하게 만드는 컨텍스트 관리 계층**입니다. 그래서 핵심 문제는 문서 작성이 아니라 아래 5개입니다.

```text
1. 어떤 문서가 진실의 원천인가
2. 문서 간 충돌을 어떻게 감지하는가
3. 어떤 작업에서 어떤 문서만 읽게 할 것인가
4. 문서가 커질 때 어떻게 분할할 것인가
5. 제품/코드 변경 후 무엇을 최신화할 것인가
```

제가 설계한다면 문서 시스템을 이렇게 가져갑니다.

## 1. 문서에는 계층이 있어야 함

모든 문서를 동등하게 두면 정합성이 무너집니다. 문서마다 권위가 달라야 합니다.

```text
L0. Index / Context Map
L1. Canonical Principles
L2. Domain Source of Truth
L3. Operational Guides
L4. Cycle / Decision Records
L5. Generated Summaries
```

예시:

```text
/docs
  context-map.md

  /principles
    product-principles.md
    design-principles.md
    engineering-principles.md

  /domains
    onboarding.md
    projects.md
    billing.md
    api-logs.md
    teams.md

  /systems
    design-system.md
    architecture.md
    data-model.md
    analytics.md
    permissions.md

  /playbooks
    feature-development.md
    ui-change.md
    api-change.md
    schema-change.md
    release.md

  /decisions
    0001-dashboard-first.md
    0002-use-postgres-rls.md

  /cycles
    2026-05-16-api-log-search/
      brief.md
      contract.md
      review.md
      learnings.md

  /generated
    ai-context-pack.md
    product-summary.md
    design-summary.md
    engineering-summary.md
```

권위는 위에서 아래로 흐릅니다.

```text
principles > domains/systems > playbooks > cycles > generated
```

즉, `/cycles`에 있는 내용이 `/principles`와 충돌하면 `/principles`가 이깁니다.  
`/generated`는 편의를 위한 캐시일 뿐이고 절대 진실의 원천이 아닙니다.

## 2. 문서마다 “소유 범위”를 명확히 둬야 함

정합성 문제는 대부분 같은 사실을 여러 문서에 중복해서 쓰기 때문에 생깁니다.

나쁜 예:

```text
pricing.md에도 Free/Pro 가격이 있음
landing-copy.md에도 Free/Pro 가격이 있음
billing-domain.md에도 Free/Pro 가격이 있음
sales-faq.md에도 Free/Pro 가격이 있음
```

좋은 방식:

```text
/docs/domains/billing.md
```

여기만 가격 정책의 원천입니다.

다른 문서는 이렇게 참조만 합니다.

```md
Pricing details are defined in /docs/domains/billing.md#plans.
```

문서의 frontmatter에 소유 범위를 박아두는 게 좋습니다.

```md
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
supersedes: []
---

# Billing Domain
```

각 문서는 “내가 어떤 사실의 원천인지”를 가져야 합니다.

```md
## Source Of Truth For
- Plan names
- Pricing model
- Trial policy
- Upgrade/downgrade rules

## Not Source Of Truth For
- Marketing copy
- Payment provider implementation
- Invoice UI layout
```

이게 없으면 시간이 지나면서 같은 내용이 여러 군데 퍼지고, 정합성이 깨집니다.

## 3. `context-map.md`가 문서 라우터 역할을 해야 함

AI가 매번 모든 문서를 읽으면 비효율적입니다. 반대로 너무 적게 읽으면 제품이 흔들립니다.

그래서 최상위에 **문서 라우팅 테이블**이 필요합니다.

```md
# Context Map

## Always Read
- /docs/principles/product-principles.md
- /docs/principles/design-principles.md
- /docs/principles/engineering-principles.md

## By Task Type

### New Feature
Read:
- /docs/playbooks/feature-development.md
- affected /docs/domains/{domain}.md
- relevant /docs/systems/{system}.md
- latest related ADRs

Update:
- affected /docs/domains/{domain}.md
- /docs/systems/analytics.md if events changed
- /docs/generated/product-summary.md

### UI Change
Read:
- /docs/principles/design-principles.md
- /docs/systems/design-system.md
- affected domain doc
- existing component examples

Update:
- /docs/systems/design-system.md if reusable pattern changed
- affected domain doc if UX behavior changed

### API Change
Read:
- /docs/systems/architecture.md
- /docs/systems/data-model.md
- affected domain doc
- relevant API contracts

Update:
- /docs/systems/api-contracts.md
- /docs/systems/data-model.md if schema changed
- affected domain doc

### Copy Change
Read:
- /docs/principles/product-principles.md
- /docs/principles/design-principles.md
- /docs/systems/copy-style.md
- affected domain doc

Update:
- affected domain doc only if product behavior changed
```

이 파일은 AI에게 “무엇을 읽을지 결정하는 파일”입니다.  
즉, 컨텍스트의 입구는 항상 `context-map.md` 하나여야 합니다.

## 4. 문서 간 정합성은 “링크 그래프 + 체크”로 관리

문서 정합성은 감으로 관리하면 안 됩니다. 최소한의 자동 검증이 필요합니다.

각 문서에 frontmatter를 넣습니다.

```md
---
id: domain.api_logs
status: canonical
authority: source
last_reviewed: 2026-05-16
depends_on:
  - principles.product
  - principles.design
  - systems.data_model
related_code:
  - src/features/api-logs
  - src/server/api/logs
related_tests:
  - tests/api-logs
---
```

그다음 스크립트로 체크합니다.

검증 항목:

```text
- 모든 depends_on id가 존재하는가
- 깨진 문서 링크가 있는가
- 같은 source_of_truth 범위가 여러 문서에 중복 선언되어 있는가
- last_reviewed가 너무 오래된 canonical 문서가 있는가
- related_code 경로가 존재하는가
- 코드 변경이 있었는데 관련 문서가 갱신되지 않았는가
- generated 문서가 canonical 문서를 수정하려고 하지 않는가
```

예를 들어 PR 전에:

```bash
npm run docs:check
```

또는:

```bash
pnpm docs:check
```

이런 식으로 문서 시스템도 테스트 대상이 되어야 합니다.

## 5. 최신화는 “코드 diff 기반”으로 해야 함

문서를 매번 수동으로 기억해서 업데이트하면 실패합니다. 변경된 파일을 기준으로 문서 업데이트 대상을 찾는 게 좋습니다.

예:

```text
src/features/billing/** 변경
→ /docs/domains/billing.md 업데이트 필요 여부 확인

src/components/ui/** 변경
→ /docs/systems/design-system.md 업데이트 필요 여부 확인

src/server/api/** 변경
→ /docs/systems/api-contracts.md 업데이트 필요 여부 확인

db/migrations/** 변경
→ /docs/systems/data-model.md 업데이트 필요 여부 확인

analytics events 변경
→ /docs/systems/analytics.md 업데이트 필요 여부 확인
```

이를 위해 `doc-ownership.yml` 같은 매핑 파일을 둡니다.

```yaml
rules:
  - code: "src/features/billing/**"
    docs:
      - "docs/domains/billing.md"

  - code: "src/components/ui/**"
    docs:
      - "docs/systems/design-system.md"

  - code: "src/server/api/**"
    docs:
      - "docs/systems/api-contracts.md"

  - code: "db/migrations/**"
    docs:
      - "docs/systems/data-model.md"
```

그러면 AI에게도 명확히 지시할 수 있습니다.

```text
이번 diff를 보고 doc-ownership.yml 기준으로 업데이트가 필요한 문서를 식별해라.
필요하면 수정하고, 필요 없으면 docs/no-update-needed.md에 이유를 남겨라.
```

## 6. 거대해지는 문서는 “크기”가 아니라 “책임”으로 쪼갬

문서가 길어졌다고 무조건 나누면 참조 비용이 커집니다. 쪼개는 기준은 길이가 아니라 **서로 다른 변경 이유**입니다.

예를 들어 `design-system.md`가 커졌다면 이렇게 나눕니다.

```text
나쁜 분할:
design-system-1.md
design-system-2.md
design-system-3.md

좋은 분할:
design-system.md
components/buttons.md
components/forms.md
components/tables.md
patterns/empty-states.md
patterns/navigation.md
copy-style.md
```

분할 기준:

```text
- 서로 다른 사람이/AI가 자주 따로 수정하는가
- 서로 다른 작업 타입에서 참조되는가
- 변경 주기가 다른가
- source_of_truth 범위가 분리되는가
- 한 문서를 읽기 위해 불필요한 내용이 너무 많은가
```

각 큰 문서는 “허브 문서”로 바꿉니다.

```md
# Design System

This document routes design references.

## Core
- Color, typography, spacing: /docs/systems/design/tokens.md
- Component rules: /docs/systems/design/components.md

## Components
- Buttons: /docs/systems/design/components/buttons.md
- Forms: /docs/systems/design/components/forms.md
- Tables: /docs/systems/design/components/tables.md

## Patterns
- Empty states: /docs/systems/design/patterns/empty-states.md
- Navigation: /docs/systems/design/patterns/navigation.md
```

AI는 허브를 먼저 읽고 필요한 세부 문서만 따라가면 됩니다.

## 7. 항상 효율적인 컨텍스트를 위해 “요약 캐시”를 둠

AI에게 canonical 문서 전체를 매번 읽히는 건 비싸고 느립니다. 그래서 `/docs/generated`에 요약 캐시를 둡니다.

```text
/docs/generated
  product-context.md
  design-context.md
  engineering-context.md
  domain-index.md
  ai-context-pack.md
```

단, 규칙이 필요합니다.

```text
generated 문서는 참조 최적화용 캐시다.
generated 문서와 canonical 문서가 충돌하면 canonical 문서가 이긴다.
generated 문서는 자동 재생성 가능해야 한다.
```

예를 들어 `ai-context-pack.md`는 이렇게 구성합니다.

```md
# AI Context Pack

Generated from:
- principles/product-principles.md
- principles/design-principles.md
- principles/engineering-principles.md
- systems/design-system.md
- systems/architecture.md

## Product Invariants
- ...

## Design Invariants
- ...

## Engineering Invariants
- ...

## Current Domains
- Billing: /docs/domains/billing.md
- API Logs: /docs/domains/api-logs.md

## Task Routing
For task-specific docs, read /docs/context-map.md.
```

AI 작업 시작 시 기본은:

```text
1. Read /docs/generated/ai-context-pack.md
2. Read /docs/context-map.md
3. Read only task-specific domain/system docs
```

이렇게 갑니다.

## 8. 최신화 흐름은 사이클 끝에 몰아서 하면 안 됨

문서 업데이트를 마지막에 한 번에 하면 거의 누락됩니다. 사이클 중간에 체크포인트를 둬야 합니다.

추천 흐름:

```text
Before Build:
- context-map.md로 참조 문서 결정
- affected domain/system docs 읽기
- feature contract 작성

During Build:
- 계약과 다른 구현이 생기면 contract 또는 구현 중 하나를 수정
- 새로운 결정은 ADR 후보로 기록

Before Merge:
- docs:check
- doc-ownership.yml 기준 문서 업데이트 확인
- generated summaries 재생성
- AI consistency review

After Release:
- 실제 피드백 반영
- domain doc의 “Observed Behavior / Learnings” 업데이트
```

핵심은 구현이 문서와 달라졌을 때, 둘 중 하나를 반드시 고르는 겁니다.

```text
문서가 맞고 구현이 틀렸는가?
구현이 새로운 의사결정이고 문서를 바꿔야 하는가?
```

이 판단을 미루면 문서 시스템은 바로 신뢰를 잃습니다.

## 9. 제품 문서화는 “사용자용”과 “AI용”을 분리

제품 문서화도 필요하지만, 목적이 다릅니다.

```text
AI용 문서:
- 제품을 일관되게 만들기 위한 내부 컨텍스트
- 원칙, 제약, 도메인 모델, UX 규칙

사용자용 문서:
- 사용자가 제품을 성공적으로 쓰게 하기 위한 설명
- 가이드, FAQ, 튜토리얼, 릴리즈 노트
```

구조는 분리하는 게 좋습니다.

```text
/docs
  /internal
    context-map.md
    principles/
    domains/
    systems/
    decisions/

  /user-facing
    getting-started.md
    guides/
    faq.md
    changelog.md
    release-notes/
```

하지만 연결은 있어야 합니다.

예:

```md
---
id: user.guide.api_logs_search
source_domain: domain.api_logs
depends_on:
  - domain.api_logs
  - systems.permissions
last_synced: 2026-05-16
---
```

즉, 사용자 문서는 내부 도메인 문서를 기반으로 생성/갱신됩니다.

AI에게는 이렇게 시킵니다.

```text
domain.api_logs를 기준으로 사용자용 가이드를 업데이트해라.
제품 내부 정책은 노출하지 말고, 사용자가 수행할 수 있는 행동 중심으로 설명해라.
```

## 10. 문서 작업에도 리뷰 역할을 둠

병렬 AI 개발에서는 “문서 정합성 리뷰어” 역할이 있어야 합니다.

작업 후 별도 AI에게 이렇게 시킵니다.

```text
Act as a documentation consistency reviewer.

Check:
- Does the implementation conflict with canonical docs?
- Are any source-of-truth facts duplicated?
- Are changed code paths mapped in doc-ownership.yml?
- Are generated summaries stale?
- Are user-facing docs affected?
- Are new decisions captured as ADRs?
- Are any docs too large and needing split by responsibility?

Return:
- Required doc updates
- Conflicts
- Stale docs
- Suggested splits
- No-change justifications
```

이 역할은 구현 AI와 분리하는 게 좋습니다. 구현한 AI는 자기 변경을 과신합니다.

## 결론

AI 네이티브 개발에서 문서 시스템은 이렇게 봐야 합니다.

```text
문서 = 기록물이 아니라 컨텍스트 라우팅 시스템
```

좋은 시스템은 다음을 갖습니다.

```text
1. context-map.md
   어떤 작업에서 무엇을 읽고 업데이트할지 결정

2. canonical docs
   제품/디자인/엔지니어링의 진실의 원천

3. domain docs
   기능 영역별 현재 상태와 행동 규칙

4. doc-ownership.yml
   코드 변경과 문서 업데이트 책임 연결

5. frontmatter metadata
   의존성, 권위, 최신성, 관련 코드 추적

6. docs:check
   링크, 중복, stale, ownership 검증

7. generated context packs
   AI 컨텍스트 비용을 줄이는 요약 캐시

8. user-facing docs
   내부 도메인 문서에서 파생되는 제품 사용 문서
```

가장 중요한 운영 원칙은 이겁니다.

```text
같은 사실은 한 문서에만 쓴다.
다른 문서는 링크하거나 파생한다.
AI는 context-map을 통해 필요한 문서만 읽는다.
변경은 doc-ownership 기준으로 문서 최신화 대상이 자동 결정된다.
generated 문서는 캐시이고 canonical 문서가 항상 이긴다.
```

이렇게 하면 문서가 커져도 “전부 읽는” 방식이 아니라 “필요한 컨텍스트만 라우팅하는” 방식으로 유지할 수 있습니다.
