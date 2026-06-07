---
title: INP hierarchy cross-dependency — 부분 SKIP + 후속 INP 분리
aliases: [inp cross-dependency, partial skip, hierarchy dependency, refs followup]
type: concept
status: budding
created: 2026-05-06
updated: 2026-05-23
tags: [ai/agent-pattern, status/budding, career/ai-native, career/product-engineer, sprint, scope-management]
related:
  - "[[AI-Native/agents/inp-tracker-followup-pattern]]"
  - "[[AI-Native/agents/swarm-workflow-real-issues]]"
  - "[[FE/d3-visualization/_concepts/opacity-ssot-pattern]]"
source: ["INP-121 (래디얼 클러스터 폐기) 진행 중 발견"]
migrated-from: MindGraph-TIL/01-Workflow-and-Harness/2026-05-06-inp-hierarchy-cross-dependency-skip-pattern.md
---

# INP hierarchy cross-dependency — 부분 SKIP + 후속 INP 분리

> TL;DR: 단일 INP의 hierarchy 일부가 다른 미완 INP 결과물에 의존하면 추측 변경 금지, hierarchy 만 SKIP, Linear 코멘트로 SKIP 사유 박제, AC strikethrough. 충족된 AC만으로 Done 전환 가능.

## What
한 INP 안의 단계적 작업(hierarchy)이 별 INP의 결과물(컬럼/타입/함수)에 의존하면 base 시점에 그 결과물이 없다. 강행하면 SQL 에러/빌드 깨짐. 부분 SKIP + 후속 분리가 안전.

## Why it matters
- 1인 + AI swarm에서 여러 INP가 동시 staged 안 된 채 working tree 누적 패턴 잦음
- 각 INP의 brand base 시점이 의미를 좌우 — cross-INP 의존성 진단 필요
- Linear 코멘트가 cross-INP 의존성 SSOT (description은 작성 시점 계획, 코멘트는 진행 중 발견)

## How

```ts
// Before — INP-121 hierarchy 4가 INP-107 결과 의존
//   base 시점 부재: migrations/004, db-types.ts CanvasMetaRow.node_positions,
//                  schema.ts CanvasMeta.nodePositions, saveNodePositionsForMode
//   강행 시 마이그레이션 005가 존재 안 하는 컬럼 UPDATE → SQL 에러

// After — agent §17 정합 SKIP
// 1. SKIP 사유 Linear 코멘트로 박제 (어떤 미완 INP의 어떤 결과물 의존)
// 2. AC 항목 strikethrough: ❌→📋 마이그레이션 005 → "INP-107 후속"
// 3. 충족된 AC만으로 Done 전환
// 4. 후속 처리: INP-107 main 머지 시점에 nodePositions 단계에서 분리 처리
```

## 운영 절차
1. agent가 hierarchy 단계에서 선결 조건 부재 발견 시 추측 변경 금지
2. 해당 hierarchy만 SKIP, 나머지 진행
3. SKIP 사유를 Linear 이슈 코멘트로 박제 (의존하는 미완 INP 명시)
4. INP description의 AC 항목 strikethrough → 후속 처리 명시
5. Done 전환 가능 (충족된 AC만으로 핵심 가치 달성)

## Pitfalls
- 추측 변경 = SQL 에러 → revert → 사용자가 cross-INP 디버깅 부담 → 비용 폭증
- 새 INP description 의 `Refs` 섹션에 "선결 INP" 항목 추가 = plan 단계 dependency 그래프 명시
- 코멘트 박제가 description 박제보다 강함 — description은 작성 시점, 코멘트는 진행 중 변경 추적

## Related
- [[AI-Native/agents/inp-tracker-followup-pattern]] — 후속 자동 흡수
- [[AI-Native/agents/swarm-workflow-real-issues]] — 1인 + AI swarm 결함 패턴
- [[FE/d3-visualization/_concepts/opacity-ssot-pattern]] — 같은 sprint, race-free SSOT

## Sources
- INP-121 진행 중 발견
