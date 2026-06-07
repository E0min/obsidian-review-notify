---
title: D3 zoom state는 명시 상태 머신으로 — dim 충돌 + 모드 전환 fit
aliases: [d3 zoom state machine, zoom dim conflict, fit-to-screen, multi-layout zoom]
type: concept
status: budding
created: 2026-05-04
updated: 2026-05-23
tags: [fe/d3, fe/react, status/budding, career/fe, state-management, ux]
related:
  - "[[FE/d3-visualization/_concepts/opacity-ssot-pattern]]"
  - "[[FE/d3-visualization/_concepts/d3-react-hover-stale]]"
  - "[[BE/api-design/empty-set-antipattern]]"
  - "[[FE/d3-visualization/canvas-svg/canvas-meta-restore-viewmode]]"
source: ["INP-118 클러스터 dim 풀림 + INP-107 모드 전환 viewport fit"]
migrated-from: MindGraph-TIL/03-D3-Graph-Logic/2026-05-04-d3-cluster-zoom-dim-state-loss.md
---

# D3 zoom state는 명시 상태 머신으로

> TL;DR: D3 zoom callback이 zoom level 기반 opacity를 일괄 재설정하면 다른 시각 상태(dim, highlight)를 덮어씀. 명시 상태 머신(`currentDimMode`)으로 의도 보존. 모드 전환만 fit, 슬라이더/리사이즈는 zoom 보존.

## What
D3는 stateless(selection 기반)라 시각 상태 보존이 호출자 책임. 여러 입력(zoom + filter + hover + 모드 전환)이 같은 attr을 다투면 충돌. 입력별 의도를 클로저/ref로 보존하고 callback이 mode 분기로 처리해야 한다.

## Why it matters
- D3 zoom 핸들러가 opacity를 무조건 재설정하면 INP-118처럼 dim이 풀린다
- 모드 전환 시 이전 zoom transform 잔존 + 새 layout viewport 초과 → 노드 화면 밖
- 통합 패턴: zoom state machine

## How

### 사례 A — dim 충돌
```ts
// Bad — zoom마다 opacity 일괄 재설정
zoom.on('zoom', (event) => {
  g.attr('transform', event.transform);
  cluster.setZoomLevel(event.transform.k, opacityFn);
});

cluster.setZoomLevel(k, opacityFn) {
  circles.attr('opacity', d => opacityFn(d.depth, k));  // dim 무시
}

// Good — dim 모드 보존
let currentDimMode: 'restored' | 'highlighted' | 'dim-all' = 'restored';
let currentActiveIds: Set<string> = new Set();

cluster.setZoomLevel(k, opacityFn) {
  if (currentDimMode === 'dim-all') {
    circles.attr('opacity', 0.06); return;
  }
  if (currentDimMode === 'highlighted') {
    circles.attr('opacity', d => currentActiveIds.has(d.id) ? maxOpacity(d) : 0.06);
    return;
  }
  circles.attr('opacity', d => opacityFn(d.depth, k));
}
```

### 사례 B — 모드 전환 fit
```ts
const lastSyncedViewModeRef = useRef<ViewMode | null>(null);

useEffect(() => {
  const isModeChange = lastSyncedViewModeRef.current !== viewMode;
  lastSyncedViewModeRef.current = viewMode;
  setupSimulationMode({
    ...,
    shouldFitView: isModeChange,  // 모드 전환만 fit
  });
}, [viewMode]);

function fitClusterView(svg, nodes, padding, maxScale) {
  const bbox = computeBoundingBox(nodes);
  const scale = Math.min(viewport.w / bbox.w, viewport.h / bbox.h, maxScale);
  svg.call(zoom.transform, d3.zoomIdentity.translate(...).scale(scale));
}
```

## Pitfalls
- 모든 입력이 fit을 트리거하면 사용자 zoom level 사라짐 — fit은 **모드 전환만**
- mode enum이 늘면 readonly union으로 타입 강제
- SVG attr 외에도 적용: CSS class toggle, animation queue, canvas redraw

## Related
- [[FE/d3-visualization/_concepts/opacity-ssot-pattern]] — opacity 단일 책임화
- [[FE/d3-visualization/_concepts/d3-react-hover-stale]] — 호버 상태 정리
- [[BE/api-design/empty-set-antipattern]] — 의도 명시 패턴

## Sources
- INP-118 클러스터 dim 풀림
- INP-107 모드 전환 viewport fit
