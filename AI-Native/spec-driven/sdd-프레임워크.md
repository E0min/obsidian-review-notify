---
title: SDD 프레임워크 v2 — 멀티 AI 추상화
aliases: [SDD, spec-driven development, multi-agent, AI abstraction layer]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [ai/agent-pattern, ai/prompt, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[../claude-code/workflows/_MOC]]"
  - "[[../agents/_MOC]]"
source: ["Notion: SDD Framework v2"]
migrated-from: "Notion: SDD 프레임워크"
---

# SDD 프레임워크 v2 — 멀티 AI 추상화

> TL;DR: Spec-Driven Development v2는 `.agents/` AI 에이전트 추상화 + `DOCS/` 5축 문서 구조로 Claude·Gemini 등 다중 AI를 동일한 스펙으로 운영하는 워크플로 패턴.

---

## What

SDD(Spec-Driven Development)는 코드를 먼저 짜는 대신 **스펙(사양)을 먼저 정의**하고, AI 에이전트가 그 스펙을 읽어 구현·검증하는 개발 방법론.

v2의 핵심 혁신: **멀티 AI 추상화** — 동일한 스펙으로 Claude Code·Gemini CLI 등 서로 다른 AI 도구를 호환 가능하게 운영.

---

## How — 디렉토리 구조

### `.agents/` — AI 에이전트 추상화 레이어

```
.agents/
├── shared/               ← AI-agnostic 공통 스펙 (핵심)
│   ├── roles.md          ← 에이전트 역할 정의
│   ├── conventions.md    ← 코딩 컨벤션, 커밋 메시지 형식
│   └── workflows.md      ← 공통 작업 흐름
├── claude/               ← Claude Code 전용 어댑터
│   ├── CLAUDE.md         ← /hooks, /skills, 스킬 트리거
│   └── hooks/            ← pre-commit, post-push 등
└── gemini/               ← Gemini CLI 전용 어댑터 (선택)
    └── GEMINI.md
```

**핵심 원칙**: `shared/`에 모든 스펙을 쓰고, 각 AI 어댑터는 해당 AI의 고유 기능(hooks, slash commands 등)만 담는다. AI가 바뀌어도 스펙은 그대로.

### `DOCS/` — 5축 문서 구조

```
DOCS/
├── 1-goals/              ← Why: 목표, KPI, North Star
│   ├── vision.md
│   └── kpis.md
├── 2-requirements/       ← What: 기능 요구사항, PRD
│   ├── features.md
│   └── constraints.md
├── 3-architecture/       ← How: 기술 설계, ADR
│   ├── overview.md
│   └── decisions/        ← ADR 목록
├── 4-implementation/     ← Detail: API 스펙, 스키마, 컴포넌트 계약
│   ├── api.md
│   ├── schema.md
│   └── components.md
└── 5-operations/         ← Run: 배포, 모니터링, 온콜
    ├── deployment.md
    └── runbooks/
```

---

## 4가지 핵심 워크플로

### 1. Spec-Gate — 구현 전 스펙 검증

```
새 기능 요청 →
  AI가 DOCS/2-requirements/ 참조 →
  요구사항 충족 여부 검사 →
  스펙 미완성 시 구현 블록 (코드 작성 거부) →
  스펙 완성 확인 후 구현 진행
```

AI가 스펙 없이 코드를 짜는 것을 방지. "스펙이 없으면 구현 없다" 규칙 강제.

### 2. Integrity-Sync — 문서 정합성 유지

```
코드 변경 감지 →
  DOCS/4-implementation/api.md 자동 비교 →
  불일치 발견 시 경고 + DOCS 업데이트 제안 →
  사용자 확인 후 DOCS 갱신
```

코드는 바뀌었는데 문서는 안 바뀌는 문제 해결. DOCS가 항상 코드와 동기화.

### 3. Agent-Dispatch — 작업 유형별 에이전트 자동 선택

```
사용자 요청 →
  .agents/shared/roles.md에서 적합한 에이전트 역할 매핑 →
  해당 역할의 AI 어댑터 활성화 →
  역할별 컨텍스트(스펙 파일) 로드 →
  구현 실행
```

예: API 변경 → API 스페셜리스트 역할 로드 → `DOCS/4-implementation/api.md` 컨텍스트 주입.

### 4. Cross-Doc Validation — 문서 간 교차 검증

```
DOCS/ 내 파일 수정 →
  관련 파일 자동 스캔 →
  불일치(예: api.md의 엔드포인트가 schema.md의 타입과 충돌) 탐지 →
  충돌 목록 리포트 →
  사용자 해결
```

---

## 에이전트 역할 정의 예시

```markdown
<!-- .agents/shared/roles.md -->
## 역할 목록

### API Designer
- 담당: REST API 스펙 설계, OpenAPI 작성
- 참조 문서: DOCS/4-implementation/api.md
- 산출물: API 스펙 변경안, 엔드포인트 목록

### Code Reviewer
- 담당: PR 리뷰, 컨벤션 체크, 보안 취약점 스캔
- 참조 문서: .agents/shared/conventions.md
- 산출물: 리뷰 코멘트, LGTM 또는 수정 요청

### Architecture Analyst
- 담당: ADR 작성, 기술 선택 검토
- 참조 문서: DOCS/3-architecture/overview.md
- 산출물: ADR 문서, trade-off 분석
```

---

## Pitfalls

- **`shared/` 비대화 방지**: 공통 스펙이 너무 길면 AI 컨텍스트 초과 → 핵심 규칙만 유지, 세부 사항은 `DOCS/`로 위임
- **어댑터 동기화 부담**: `claude/`와 `gemini/`가 각자 다른 형식으로 벌어지면 관리 포인트 증가 → 공통 부분은 반드시 `shared/`에만
- **Spec-Gate 너무 엄격하면 속도 저하**: 탐색 단계(prototype)에서는 일시적으로 Spec-Gate를 완화 후 안정화 단계에서 복원
- **DOCS/ 5축이 프로젝트 규모에 비해 과할 수 있음**: 소규모 프로젝트는 `goals + requirements + architecture` 3축만으로 시작

---

## Related

- [[_MOC]] — AI-Native 전체 지도
- [[../claude-code/workflows/_MOC]] — Claude Code 구체적 워크플로
- [[../agents/_MOC]] — 멀티 에이전트 패턴 모음

## Sources

- 내부 실험 문서 (SDD v2 설계 노트)
