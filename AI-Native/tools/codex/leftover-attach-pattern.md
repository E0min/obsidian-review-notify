---
title: 멀티라운드 Codex review의 잔존 finding 박제 패턴
aliases: [codex multi-round, leftover findings, A.X labeling, commit message attach]
type: concept
status: budding
created: 2026-05-16
updated: 2026-05-23
tags: [ai/codex, ai/agent-pattern, status/budding, career/ai-native, career/product-engineer, sprint]
related:
  - "[[AI-Native/tools/codex/pair-programming-root-fix]]"
  - "[[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]]"
  - "[[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]]"
  - "[[AI-Native/agents/inp-hierarchy-skip-pattern]]"
source: ["INP-145 commit 5b07918 → INP-146 commit 394078d"]
migrated-from: MindGraph-TIL/01-Workflow-and-Harness/2026-05-16-codex-finding-leftover-attach-pattern.md
---

# 멀티라운드 Codex review의 잔존 finding 박제 패턴

> TL;DR: multi-round review에서 가장 중요한 박제는 **"이번 round에서 안 다룬 finding"**을 commit message에 명시적으로 적기. `A.4 = 다음 round` 라벨로 1주일 후 `A.4 진행` 한 줄 진입 가능.

## What
Codex 협업의 multi-round review에서 round-N 종료 시 잔존 finding이 발생. commit message body 마지막에 `잔존 (A.X = 다음 round)` 섹션으로 박제하면 git log 영구 + future self/AI 진입점 역할.

## Why it matters
LLM 세션 컨텍스트는 휘발성. 박제 위치 3개 중 commit message가 가장 자주 검색됨(`git log -10`로 1초 진입). plan 문서는 STALE 위험 + spec-gate 부담 → commit message 박제가 다이어트 정합.

## How — 패턴 4요소

1. **A 카테고리 박제** — round 단위 finding 그룹 식별자 (`A.1`=타입+스키마, `A.2`=흐름, `A.3`=영속화, `A.4`=잔존)
2. **잔존 finding 우선순위 명시** — 작은 fix vs 큰 작업 구분
3. **Codex finding 번호 보존** — `Codex finding #5`처럼 round-N numbering 유지 (시간 경과 후 review 재추적)
4. **별 INP 박제 vs 같은 INP 후속** — 별 작업이면 INP 발급, 작은 fix면 기존 INP 코멘트

## How — 예시

```
dev-fix(graph): relayout root fix — fx/fy 의미 분리 + layoutPinned 영속화 (refs INP-145)

ROOT CAUSE (Codex 협업 진단): ...
ROOT FIX (의미 분리): ...

변경 범위 (12 파일 + migration 1):
1. 타입 + 스키마 (A.1)
2. 시뮬레이션 흐름 (A.2 + P2.3)
3. UI 통로 (A.2 dragStateRef plumbing)
4. 저장 API + 영속화 (A.3)

잔존 (A.4 = 다음 round):
  - relayout 후 즉시 박제 좌표가 alpha 가열 직후 stale
  - 600 tick 동기 loop 그대로 (chunk runner 미박제)
  - 자동 회귀 테스트 5개

Co-Authored-By: Claude Opus 4.7 (1M context) <noreply@anthropic.com>
Co-Authored-By: Codex CLI (gpt-5-codex high) <noreply@openai.com>
```

1주일 후:
```
사용자: A.4 진행
AI: # git log grep A.4 → INP-146 발급 (chunk runner)
```

## Pitfalls
1. **잔존 항목 위치** — 마지막 `Co-Authored-By` 직전 표준화. 첫 줄/중간이면 못 봄
2. **별 INP 발급 권장 명시** — "별 INP 박제 권장" 1줄이 trigger
3. **A 카테고리 명명 일관** — `A.X / P.X` 둘 중 하나 표준
4. **Codex review 출처** — `Codex review (2026-05-16) finding #5` 박제로 재추적 가능

## Related
- [[AI-Native/tools/codex/pair-programming-root-fix]] — Codex 협업 전체 흐름
- [[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]] — INP-145 round-1 (A.1~A.3)
- [[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]] — INP-146 (A.4 진입)
- [[AI-Native/agents/inp-hierarchy-skip-pattern]]

## Sources
- INP-145 commit 5b07918
- INP-146 commit 394078d
