---
type: architecture
project: mindgraph
status: budding
updated: 2026-05-23
tags: [project/mindgraph, architecture]
---

# mindgraph — Architecture

> 시스템 구조 + 핵심 모듈 + 데이터 흐름. 코드 깊이 X, 구조 다이어그램과 의사결정 트레일.

## 상위 구성

```
┌─────────────────────┐    ┌──────────────────────┐    ┌──────────────────┐
│ Chrome Extension    │───▶│ Next.js 16 (App)     │◀──▶│ Supabase         │
│ (capture + sidebar) │    │ + D3 force sim       │    │ (Postgres + auth)│
└─────────────────────┘    └──────────────────────┘    └──────────────────┘
                                    │
                                    ▼
                           ┌──────────────────────┐
                           │ proxy.ts (i18n + auth)│ ← Next.js 16 standard
                           └──────────────────────┘
```

## 핵심 모듈

- **components/graph/** (~7,000줄) — D3 force simulation + 멀티 layout (bubble / radial / tree)
- **proxy.ts** — i18n 라우팅 + Supabase 세션 갱신 ([[FE/nextjs/middleware-proxy/nextjs-16-middleware-to-proxy]])
- **lib/d3/createClusterLayer** — opacity SSOT 통합 ([[FE/d3-visualization/_concepts/opacity-ssot-pattern]])
- **lib/d3/settleBubbleLayoutAsync** — chunk runner ([[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]])
- **lib/db/positions** — `position` (layout seed) + `layoutPinned` (force 무영향) 분리 ([[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]])

## 핵심 데이터 흐름

1. **진입** — `[locale]/page.tsx` → proxy.ts 라우팅 → graphCanvas mount
2. **layout 복원** — IndexedDB `loadMeta(rootTopicId)` → `__bubble` / `__radial` params 복원 ([[FE/d3-visualization/canvas-svg/canvas-meta-restore-viewmode]])
3. **force settle** — `settleBubbleLayoutAsync(simulation, signal)` → frame budget 6ms
4. **drag end** — `handleDragEnd` 즉시 `layoutPinned: true` 박제 + 1초 debounce로 나머지 저장
5. **zoom** — `zoom.on('zoom')` → `computeCircleOpacity()` SSOT 호출

## 핵심 invariant

- **fx/fy 한 필드 = 한 의미** — DB 좌표 복원은 `position`만, force 무영향은 `layoutPinned: true`일 때만 fx/fy
- **opacity는 SSOT만 set** — `computeCircleOpacity()` 외에는 어디서도 attr('opacity') X
- **모드 전환만 fit** — 슬라이더/리사이즈는 zoom 보존
- **passive listener 필수** — mousemove/wheel/touchmove

## See also
- [[_INDEX]]
- [[Projects/mindgraph/links-to-code]]
- [[decisions/_MOC]]
