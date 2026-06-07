---
type: links-to-code
project: mindgraph
updated: 2026-05-23
tags: [project/mindgraph]
---

# mindgraph — Links to Code

> 옵시디언 노트와 실제 코드의 양방향 포인터. 코드 절대 복사하지 않음 — 경로 + 1줄 설명만.

## 핵심 파일 (`~/깃허브/mindgraph/`)

| 경로 | 설명 | 관련 atomic |
|------|------|------|
| `proxy.ts` | Next.js 16 라우팅 hook (i18n + Supabase 세션) | [[FE/nextjs/middleware-proxy/nextjs-16-middleware-to-proxy]] |
| `components/graph/GraphCanvas.tsx` | 최상위 캔버스 컨테이너 — zoom + mode 전환 + fit | [[FE/d3-visualization/_concepts/d3-zoom-state-machine]] |
| `lib/d3/createClusterLayer.ts` | `computeCircleOpacity` SSOT 통합 | [[FE/d3-visualization/_concepts/opacity-ssot-pattern]] |
| `lib/d3/settleBubbleLayoutAsync.ts` | rIC/rAF chunk runner | [[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]] |
| `lib/d3/setupSimulationMode.ts` | force simulation 진입점 (settle + ref 박제) | [[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]] |
| `lib/d3/setupCircleDragBehavior.ts` | drag start/end + dragStateRef 동기화 | [[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]] |
| `components/graph/handlers/handleNodeClick.ts` | panTo + mousedown.hover-cancel | [[FE/d3-visualization/_concepts/d3-react-hover-stale]] |
| `lib/db/positions.ts` | `position` + `layoutPinned` 컬럼 (의미 분리) | [[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]] |
| `lib/db/graphMeta.ts` | `__bubble` / `__radial` params 누적 저장 | [[FE/d3-visualization/canvas-svg/canvas-meta-restore-viewmode]] |
| `messages/{en,ko}.json` | next-intl messages (hot-reload 이슈 주의) | [[FE/nextjs/_concepts/next-intl-hot-reload-cache]] |
| `next.config.ts` | `optimizePackageImports: ['lucide-react']` | [[FE/performance/bundling/lucide-react-direct-import]] |
| `department/dev/web/AGENTS.md` | "This is NOT the Next.js you know" 가드 | [[AI-Native/claude-code/_MOC]] |

## Sprint 단위 commit 추적

| Commit | Sprint | 변경 |
|--------|--------|------|
| `5b07918` | INP-145 | fx/fy 의미 분리 |
| `6e15df7` | INP-116/118 | opacity SSOT |
| `394078d` | INP-146 | chunk runner |

## See also
- [[_INDEX]]
- [[architecture]]
- [[decisions/_MOC]]
