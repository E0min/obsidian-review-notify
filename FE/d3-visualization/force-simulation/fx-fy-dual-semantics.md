---
title: D3 force simulation의 fx/fy 의미 이중 사용 함정
aliases: [fx fy dual semantics, layout seed vs pinned, semantic overload, position layoutPinned]
type: concept
status: evergreen
created: 2026-05-16
updated: 2026-05-23
tags: [fe/d3, fe/react, status/evergreen, career/fe, career/fdd, force-simulation, root-cause]
related:
  - "[[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]]"
  - "[[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]"
  - "[[AI-Native/tools/codex/pair-programming-root-fix]]"
  - "[[Projects/mindgraph/decisions/001-fx-fy-dual-semantics]]"
source: ["INP-145 commit 5b07918"]
migrated-from: MindGraph-TIL/03-D3-Graph-Logic/2026-05-16-fx-fy-dual-semantics.md
---

# D3 force simulation의 fx/fy 의미 이중 사용 함정

> TL;DR: `fx/fy` 한 필드에 두 의미(① DB 저장 좌표 복원 = layout seed, ② 사용자 드래그 고정 = force 무영향)를 박제하면 3개 symptom(첫 진입 위치 X, CPU 영구 소모, 600 tick 동기 블록)이 모두 한 root에서 파생. 의미 분리: `position` + `layoutPinned`.

## What
D3 `fx/fy`는 의미상 **"force 무영향 고정 좌표"** — 단일 의미. 도메인에서 두 의미를 같이 박제하면 첫 진입 시 layout이 안 풀리고, idle CPU 100%가 되며, 동기 settle이 main thread 블록.

## Why it matters
이건 **"한 필드 = 한 의미"** 원칙의 교과서적 사례. 비슷한 함정: enum overloading, magic number, sentinel value. 한 root cause에서 3개 다른 symptom이 파생 → 각각만 보고 fix 시도하면 모두 revert.

## How

```ts
// Bad — 의미 이중 사용
if (restoreSavedPositions) {
  for (const node of simulation.nodes()) {
    const saved = node.data.position;
    if (saved) {
      node.x = saved.x; node.y = saved.y;
      node.fx = saved.x; node.fy = saved.y;  // ❌ DB 좌표를 force 무영향으로 박제
    }
  }
}

simulation.on('tick', () => {
  const hasFixedNode = nodes.some(n => n.fx != null);  // ❌ 영구 통과
  const isActive = simulation.alpha() > 0.005;
  if (!hasFixedNode && !isActive) simulation.stop();
});

// Good — 의미 분리
interface UnifiedNode {
  position?: { x: number; y: number };  // ✅ layout seed (모든 노드)
  layoutPinned?: boolean;                // ✅ force 무영향 (드래그 노드만)
}

if (restoreSavedPositions) {
  for (const node of simulation.nodes()) {
    const saved = node.data.position;
    if (saved) {
      node.x = saved.x; node.y = saved.y;
      if (node.data.layoutPinned === true) {
        node.fx = saved.x; node.fy = saved.y;
      }
    }
  }
}

const dragStateRef = useRef<{ active: boolean }>({ active: false });
simulation.on('tick', () => {
  const isDragging = dragStateRef.current.active;
  if (!isDragging && simulation.alpha() <= 0.005) simulation.stop();
});
```

## Symptom diagnostic 트리

한 root에서 3개 symptom 파생:
1. **첫 진입 위치 ≠ relayout 결과** — 사용자 보고 1차
2. **CPU 영구 소모(idle 100%)** — `hasFixedNode` 무한 tick
3. **600 tick 동기 = main thread block** — 100+ 노드 60-200ms

각각 다른 fix 시도(alpha(0.3), alphaMin=0, tick 수 줄임) 모두 revert → **fix 3번 revert가 root 신호**.

## Race conditions (의미 분리 후 발견)

### Race 1 — drag end 좌표 stale
```ts
// Bad — mouseup 즉시 alpha=0 → 마지막 tick 못 받음 → stale 좌표 저장
.on('end', (_event, d) => {
  options?.onDragEnd?.(d.id, d.x, d.y);  // d.x는 한 tick 뒤
});

// Good — fx/fy로 강제 동기화
.on('end', (_event, d) => {
  if (d.fx != null) d.x = d.fx;
  if (d.fy != null) d.y = d.fy;
  options?.onDragEnd?.(d.id, d.x, d.y);
});
```

### Race 2 — debounce + 페이지 이탈
drag end → 1초 debounce 저장 → 1초 안 이탈 시 `layoutPinned` 없이 저장 → 다음 진입 시 fx/fy 복원 X.

**Fix**: drag end 즉시 단일 노드 박제 + 1초 debounce는 나머지 노드만.

## Related
- [[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]] — symptom 3 해결책
- [[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]
- [[AI-Native/tools/codex/pair-programming-root-fix]] — 진단 방법론
- [[Projects/mindgraph/decisions/001-fx-fy-dual-semantics]] — ADR

## Sources
- INP-145 commit 5b07918
- D3 docs: https://d3js.org/d3-force/simulation#simulation_force
