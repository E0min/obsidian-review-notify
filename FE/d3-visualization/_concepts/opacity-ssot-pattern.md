---
title: D3 opacity 분산 patch 누적 → SSOT 단일 함수 통합 패턴
aliases: [opacity ssot, single source of truth, distributed patch antipattern, combinatorial explosion]
type: concept
status: evergreen
created: 2026-05-07
updated: 2026-05-23
tags: [fe/d3, fe/react, status/evergreen, career/fe, career/product-engineer, refactor, antipattern]
related:
  - "[[FE/d3-visualization/_concepts/d3-zoom-state-machine]]"
  - "[[BE/api-design/empty-set-antipattern]]"
  - "[[AI-Native/agents/inp-hierarchy-skip-pattern]]"
  - "[[Projects/mindgraph/decisions/002-opacity-ssot-pattern]]"
source: ["INP-116/118 후속 — commit 6e15df7"]
migrated-from: MindGraph-TIL/03-D3-Graph-Logic/2026-05-07-opacity-ssot-pattern-vs-distributed-patches.md
---

# D3 opacity 분산 patch 누적 → SSOT 통합 패턴

> TL;DR: 여러 메서드가 같은 attr(`opacity`)을 각자 set + 다른 메서드 상태 보존 분기를 들고 있으면 **combinatorial explosion**. opacity 계산을 단일 함수(`computeCircleOpacity`)로 추출하면 race + patch 누적 차단.

## What
D3 SVG의 `opacity` 같은 단일 시각 속성을 여러 메서드(`updateCircles`, `updateLabels`, `setZoomLevel`, `setHighlightDim`)가 각자 set하면 다른 메서드가 설정한 상태를 무시한다. 결함마다 분기를 추가하는 패턴은 N+1 결함의 거름.

## Why it matters
이 패턴은 **D3 외부에도 적용** — 한 attr/state를 여러 코드 경로가 set하면 동일 문제 발생. SSOT는 race + 회귀 + 인지 부하를 동시에 해결하는 근본 패턴.

## How

### Anti-pattern (분산 patch 누적)
```ts
setZoomLevel(k, opacityFn) {
  if (currentDimMode === 'dim-all') { selection.attr('opacity', 0.06); return; }  // patch 1
  if (currentDimMode === 'highlighted') { ... return; }                            // patch 2
  selection.attr('opacity', d => opacityFn(d.depth, k));
}

setHighlightDim(activeIds, duration, mode) {
  selection.interrupt().transition().duration(duration)                            // patch 3 (.interrupt 추가)
    .attr('opacity', d => /* mode/activeIds 분기 */);
}

updateCircles(data) {
  // dim 모드 무시 → tick마다 dim 덮어씀 (다음 결함)
  selection.attr('opacity', d => opacityFn(d.depth, currentK));
}
```

### SSOT (근본 해결)
```ts
// 단일 opacity 계산 — 모든 dim mode 분기를 한 곳에
function computeCircleOpacity(d: ClusterCircleData): number {
  if (currentDimMode === 'dim-all') return 0.06;
  if (currentDimMode === 'highlighted') {
    return currentActiveIds.has(d.id) ? maxOpacity(d) : 0.06;
  }
  return currentOpacityFn ? currentOpacityFn(d.depth, currentK) : 0;
}

// 각 메서드는 자기 책임만
updateCircles(data) { ...; selection.attr('opacity', computeCircleOpacity); }
setZoomLevel(k, fn) {
  currentK = k; currentOpacityFn = fn;
  selection.interrupt().attr('opacity', computeCircleOpacity);
}
setHighlightDim(ids, dur, mode) {
  currentDimMode = ...; currentActiveIds = ids;
  selection.interrupt().transition().duration(dur).attr('opacity', computeCircleOpacity);
}
```

### 핵심 차이

| 측면 | 분산 patch | SSOT |
|------|----------|------|
| opacity source | 4 메서드 분산 | 1 함수 |
| 새 dim 케이스 추가 | N 메서드 수정 | 1 함수 수정 |
| transition 책임 | 모호 | setHighlightDim만 |
| race condition | 잠재 | 차단 |

## Pitfalls
- transition source 단일화 + 다른 메서드는 즉시 set + `.interrupt()` 패턴
- SSOT 안에 모든 mode 분기 — 새 모드 추가 시 함수만 수정
- 함수 시그니처 SSOT도 동일 — `updateVisualParams(params: BubbleParams)` 통합

## Related
- [[FE/d3-visualization/_concepts/d3-zoom-state-machine]]
- [[BE/api-design/empty-set-antipattern]]
- [[AI-Native/agents/inp-hierarchy-skip-pattern]]
- [[Projects/mindgraph/decisions/002-opacity-ssot-pattern]] — ADR

## Sources
- INP-116/118 후속 — commit 6e15df7
