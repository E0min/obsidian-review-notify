---
type: decision
project: mindgraph
date: 2026-05-16
status: accepted
supersedes: []
sprint: INP-145
tags: [adr, project/mindgraph]
---

# ADR-001: fx/fy 의미 분리 — position + layoutPinned

## Context

D3 force simulation의 `fx/fy`는 의미상 "force 무영향 고정 좌표"(단일 의미). 그런데 도메인에서는 두 의미를 다 박제하고 싶었다:
1. **DB 저장 좌표 복원** — 페이지 진입 시 layout seed
2. **사용자 드래그 고정** — 드래그 결과 보존 (force 무영향)

두 의미를 `fx/fy` 한 필드에 박제했더니 3개 symptom 발생:
- 첫 진입 위치 ≠ relayout 결과
- idle CPU ~100% (hasFixedNode 무한 tick)
- 600 tick 동기 settle = main thread block 60-200ms

각각 다른 fix 시도(alpha(0.3), alphaMin=0, tick 수 줄임) → 모두 revert. 3번 revert가 root cause 신호.

## Options

1. **알파/idle 튜닝으로 표면 해결** — 기각: 다른 노드 흩어짐, jitter 회귀
2. **fx/fy 한 필드 유지 + 별도 컬렉션으로 의미 분기** — 기각: IndexedDB schema 부풀림
3. **명시 flag로 의미 분리: `position` + `layoutPinned`** — 채택
4. **null/undefined로 의미 분기** — 기각: 가독성 + 회귀 위험

## Decision

옵션 3 채택. 노드 인터페이스에 두 필드:
- `position?: { x: number; y: number }` — 모든 노드에 적용 (layout seed)
- `layoutPinned?: boolean` — true일 때만 fx/fy 박제 (force 무영향)

복원 시: `position`은 항상 `x`/`y`로 적용, `layoutPinned === true`인 경우만 `fx`/`fy`도 박제.

idle 판정은 `dragStateRef`로만 — fx 박제 노드 있어도 stop 가능.

## Consequences

**+** 한 root cause 해결 → 3개 symptom 동시 사라짐
**+** Type-safe + migration 가능 (NULL → unpinned default, 안전한 backfill)
**+** drag end 즉시 박제 + 1초 debounce 분리로 race 차단

**-** drag end 좌표 stale race 발견 (의미 분리 후) → `d.x = d.fx` 강제 동기화로 추가 fix
**-** debounce + 페이지 이탈 race → 즉시 단일 노드 박제 패턴

## Related

- [[../../FE/d3-visualization/force-simulation/fx-fy-dual-semantics]]
- [[../../FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]] — symptom 3 후속 해결
- [[../../AI-Native/tools/codex/pair-programming-root-fix]] — Codex 페어로 root 진단
- commit 5b07918
