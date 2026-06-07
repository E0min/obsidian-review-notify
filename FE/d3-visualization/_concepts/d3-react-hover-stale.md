---
title: D3 + React 호버 stale — panTo() 후 mouseleave 미발생
aliases: [hover stuck, mouseleave race, svg transform hover, d3 react hover]
type: concept
status: budding
created: 2026-05-04
updated: 2026-05-23
tags: [fe/d3, fe/react, fe/browser, status/budding, career/fe, ux]
related:
  - "[[FE/d3-visualization/_concepts/d3-zoom-state-machine]]"
  - "[[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]"
source: ["INP-119 작업 중 사용자 시각 검증 발견"]
migrated-from: MindGraph-TIL/03-D3-Graph-Logic/2026-05-04-d3-hover-stale-on-svg-transform.md
---

# D3 + React 호버 stale — panTo() 후 mouseleave 미발생

> TL;DR: SVG transform 변경(`panTo`, `zoom.transform`)은 노드를 시각적으로 마우스 아래에서 벗어나게 하지만 DOM 노드는 그대로라 `mouseleave` 이벤트가 fire 안 됨 → 호버 dim stuck. `mousedown.hover-cancel` 등 명시적 cleanup 필요.

## What
D3 사용자가 자주 만나는 함정: SVG transform = 좌표계 이동, DOM event = 픽셀 좌표 기반. 두 모델의 분리가 mismatch 원인.

## Why it matters
- panTo / zoom.transform / drag 종료 같은 액션 후 호버 상태가 stuck됨
- 일반화: 시각 상태 변경 액션이 DOM 이벤트와 분리될 때 → 명시적 cleanup 필요

## How
```ts
// Bad — handleNodeClick + panTo 후 호버 dim 영구 stuck
nodeSel
  .on('mouseenter.hover', (_, d) => { isHovering = true; applyDim(...); })
  .on('mouseleave.hover', () => { isHovering = false; applyDim(highlightedIds); });

handleNodeClick(node) {
  graphCanvasRef.current?.panTo(node.x, node.y, PANEL_WIDTH);
  // ↑ SVG transform 변경 → mouseleave 안 fire → dim stuck
}

// Good — mousedown.hover-cancel 보완
.on('mouseleave.hover', () => clearHoverState(duration))
.on('mousedown.hover-cancel', () => {
  if (isHovering) clearHoverState(duration);
});

function clearHoverState(duration: number) {
  isHovering = false;
  applyDim(highlightedIds);
}
```

## Pitfalls
- `mouseenter`/`mouseleave`만으로는 SVG transform 액션 대응 불가
- React + D3 통합 시 모든 커스텀 액션마다 호버 상태 정리 검토

## Related
- [[FE/d3-visualization/_concepts/d3-zoom-state-machine]]
- [[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]

## Sources
- INP-119 작업 중 사용자 시각 검증 발견
