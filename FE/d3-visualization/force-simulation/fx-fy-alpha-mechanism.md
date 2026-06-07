---
title: D3 force simulation — 슬라이더가 선택 노드만 영향 주는 메커니즘
aliases: [d3 alpha boost, fx fy lerp skip, force simulation slider]
type: concept
status: budding
created: 2026-05-04
updated: 2026-05-23
tags: [fe/d3, status/budding, career/fe, force-simulation, ux]
related:
  - "[[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]]"
  - "[[FE/d3-visualization/_concepts/d3-zoom-state-machine]]"
  - "[[FE/d3-visualization/_concepts/d3-react-hover-stale]]"
source: ["INP-105/INP-117 파라미터 슬라이더 분석"]
migrated-from: MindGraph-TIL/03-D3-Graph-Logic/2026-05-04-d3-force-fx-fy-alpha-mechanism.md
---

# D3 force simulation — fx/fy + alpha 메커니즘

> TL;DR: 슬라이더가 일부 노드만 움직이는 이유 3개 결합: ①`bubbleTickCorrections`가 `fx == null`일 때만 lerp ②드래그 종료 후 `fx = null` 안 함 ③`alpha(0.3)` 약한 boost. 해결: alpha boost 강화 + 명시 "재배치" 액션 분리.

## What
D3 force simulation에서 `alpha`(전역 활성도) × `force.strength`(개별 영향)의 곱셈 모델. `alpha = 0`이면 모든 force 무시. `fx`/`fy`는 "고정" 의도 — 한 번 설정되면 force 영향 받지 않음.

## Why it matters
사용자가 슬라이더 조정해도 일부 노드만 움직이면 "왜 안 먹지?" 인지 부하 폭증. alpha와 fx/fy 두 메커니즘이 비자명하게 결합됨.

## How

### 흐름 추적
```ts
function bubbleTickCorrections(node) {
  if (node.fx == null) {  // 핵심
    node.x += (target.x - node.x) * 0.85;
    node.y += (target.y - node.y) * 0.85;
  }
}

// 드래그 종료 — 의도적으로 fx 유지
.on('end', (event, d) => {
  if (!event.active) simulation.alphaTarget(0);
  // d.fx = null;  ← 호출 안 함
})

// 파라미터 변경 — 약한 boost
function applyParams(simulation, params) {
  simulation.force('charge', d3.forceManyBody().strength(params.CHARGE));
  simulation.alpha(0.3).restart();
}
```

### 해결 — alpha 강화 + 재배치 분리
```ts
// B. alpha boost 강화
simulation.alpha(0.6).restart();

// C. 명시 "재배치" — 모든 fx 해제 + 풀 재시뮬
function relayout() {
  simulation.nodes().forEach(n => { n.fx = null; n.fy = null; });
  simulation.alpha(1).restart();
}
```

## Pitfalls
- 슬라이더는 보존적 적용(alpha 0.6), 재배치는 강제(alpha 1) — 두 의도 분리
- drag end 후 fx 자동 해제 여부는 UX 의사결정 (PR 마다 일관성)
- alpha=0 + alphaMin=0 조합은 idle 상태 — 슬라이더 효과가 빠르게 소멸

## Related
- [[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]] — fx/fy 의미 분리 (확장)
- [[FE/d3-visualization/_concepts/d3-zoom-state-machine]]
- [[FE/d3-visualization/_concepts/d3-react-hover-stale]]

## Sources
- INP-105 / INP-117 파라미터 슬라이더 분석
