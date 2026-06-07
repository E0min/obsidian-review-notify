---
title: 진입 경로별 렌더링 차이 — viewMode 분기 누락한 메타 복원
aliases: [viewmode meta restore, layout params persistence, multi-mode state save]
type: concept
status: budding
created: 2026-05-04
updated: 2026-05-23
tags: [fe/d3, fe/react, status/budding, career/fe, state-management]
related:
  - "[[FE/d3-visualization/_concepts/d3-zoom-state-machine]]"
  - "[[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]"
  - "[[Projects/mindgraph/_INDEX]]"
source: ["INP-107 후속 — 진입 경로별 렌더링 일관성"]
migrated-from: MindGraph-TIL/03-D3-Graph-Logic/2026-05-04-canvas-meta-restore-viewmode-branch.md
---

# 진입 경로별 렌더링 차이 — viewMode 분기 누락한 메타 복원

> TL;DR: state persistence 시 활성 view 파라미터만 저장하면 모드 토글 시 다른 view 파라미터가 디폴트로 폴백. 모든 모드 상태를 항상 함께 저장하는 패턴.

## What
같은 모드라도 진입 경로(직접 진입 vs 토글)에 따라 시각 결과가 달라지는 버그. 메타 복원 로직이 `meta.viewMode === 'bubble'`에서만 bubbleParams를 복원하면, radial로 진입 후 bubble 토글 시 bubbleParams가 디폴트로 돌아간다.

## Why it matters
- 진입 경로별 일관성은 암묵 invariant — "같은 모드 + 같은 데이터 = 같은 결과"
- 사용자 인지 부하: "왜 똑같은 모드인데 다르지?"
- 일반화: state persistence 시 현재 view만 저장 X → 모든 view 누적

## How
```ts
// Bad — viewMode 분기로 한쪽 파라미터만 복원
useEffect(() => {
  const meta = await loadMeta(rootTopicId);
  if (meta.viewMode === 'bubble') {
    setBubbleParams(meta.graphParams as BubbleParams);
  } else if (meta.viewMode === 'radial-cluster') {
    setRadialParams(meta.graphParams as RadialParams);
  }
}, [rootTopicId]);

// Good — 두 모드 파라미터 동시 저장/복원
useEffect(() => {
  const meta = await loadMeta(rootTopicId);
  const params = meta.graphParams as { __bubble?: BubbleParams; __radial?: RadialParams };
  if (params.__bubble) setBubbleParams(params.__bubble);
  if (params.__radial) setRadialParams(params.__radial);
}, [rootTopicId]);

const payload = {
  ...currentFlat,  // 구 데이터 호환
  __bubble: bubbleParams,
  __radial: radialParams,
};
```

## Pitfalls
- useEffect 의존성에 viewMode 추가하면 무한 루프 위험 → 의도적 omit
- 구 데이터(flat) 호환을 위해 두 스키마 동시 지원 필요

## Related
- [[FE/d3-visualization/_concepts/d3-zoom-state-machine]] — 같은 sprint, zoom 상태 머신
- [[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]
- [[Projects/mindgraph/_INDEX]]

## Sources
- INP-107 후속 — 진입 경로별 렌더링 일관성
