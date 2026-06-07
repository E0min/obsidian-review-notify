---
type: decision
project: mindgraph
date: 2026-05-07
status: accepted
supersedes: []
sprint: INP-116/118 후속
tags: [adr, project/mindgraph]
---

# ADR-002: opacity 분산 patch → SSOT 단일 함수 통합

## Context

`createClusterLayer`의 ClusterLayer 인터페이스에서 4개 메서드가 각자 `opacity` 직접 set:

| 메서드 | 책임 | opacity 처리 |
|--------|------|-------------|
| `updateCircles(data)` | 데이터 바인딩 | 정적 zoom 기반 |
| `updateLabels(data)` | 라벨 바인딩 | 정적 zoom 기반 |
| `setZoomLevel(k, fn)` | zoom 갱신 | dim 모드 분기 (INP-118 patch 1) |
| `setHighlightDim(ids, dur)` | dim 갱신 | transition + interrupt (INP-116 patch 2) |

결함마다 분기 추가 → **combinatorial explosion**:
- 다음 결함(호버 dim 풀림)은 `updateCircles`에도 분기 추가 (patch 3 후보)
- 새 dim mode 추가 시 N 메서드 모두 수정

## Options

1. **patch 3 추가 (`updateCircles`에도 dim 분기)** — 기각: cycle 계속, 다음 결함 보장
2. **opacity 책임을 한 메서드(setHighlightDim)에만 집중** — 기각: zoom 변경 시 stale
3. **SSOT 함수(`computeCircleOpacity`) 추출 + 모든 메서드가 호출** — 채택
4. **state machine 도입 (외부 라이브러리)** — 기각: 과한 의존성

## Decision

옵션 3 채택. opacity 계산을 단일 함수로:

```ts
function computeCircleOpacity(d: ClusterCircleData): number {
  if (currentDimMode === 'dim-all') return 0.06;
  if (currentDimMode === 'highlighted') {
    return currentActiveIds.has(d.id) ? maxOpacity(d) : 0.06;
  }
  return currentOpacityFn ? currentOpacityFn(d.depth, currentK) : 0;
}
```

각 메서드는 자기 책임만 + `computeCircleOpacity` 호출. transition source는 `setHighlightDim`만, 다른 메서드는 즉시 set + `.interrupt()`.

## Consequences

**+** 새 dim 케이스 추가 시 함수만 수정 (1곳)
**+** tick vs transition race 차단 — computeOpacity가 모드 보존
**+** "또 patch 추가" cycle 차단
**+** 함수 시그니처 SSOT(`updateVisualParams(params: BubbleParams)`)도 같은 sprint에 통합

**-** state(`currentDimMode`, `currentActiveIds`, `currentK`, `currentOpacityFn`)가 클로저에 박제 — 모듈 외부 inspect 어려움 (debug 시)

## Related

- [[../../FE/d3-visualization/_concepts/opacity-ssot-pattern]]
- [[../../FE/d3-visualization/_concepts/d3-zoom-state-machine]]
- [[../../BE/api-design/empty-set-antipattern]] — 같은 sprint, mode 명시 패턴
- commit 6e15df7
