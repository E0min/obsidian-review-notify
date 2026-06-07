---
title: D3 force simulation 동기 settle loop → rIC/rAF chunk runner
aliases: [chunk runner, requestIdleCallback, INP optimization, frame budget, settle async]
type: concept
status: evergreen
created: 2026-05-16
updated: 2026-05-23
tags: [fe/d3, fe/perf, status/evergreen, career/fe, career/product-engineer, inp, performance]
related:
  - "[[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]]"
  - "[[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]"
  - "[[AI-Native/tools/codex/pair-programming-root-fix]]"
  - "[[FE/performance/core-web-vitals/_MOC]]"
source: ["INP-146 commit 394078d"]
migrated-from: MindGraph-TIL/03-D3-Graph-Logic/2026-05-16-d3-chunk-runner-ric-raf.md
---

# D3 force simulation 동기 settle loop → rIC/rAF chunk runner

> TL;DR: D3 사전 안정화 동기 loop(`for (i; N) simulation.tick()`)은 100+ 노드에서 main thread 60-200ms 블록 → INP "Poor". `simulation.tick()` 직접 호출 + frame budget(6ms) + `requestIdleCallback` 양보 + `AbortSignal` cancellation.

## What
D3 force simulation의 동기 settle loop는 작은 그래프에선 체감 0이지만 큰 그래프에선 main thread를 블록한다. INP(Interaction to Next Paint) Core Web Vital의 적신호.

## Why it matters
- **INP는 Core Web Vital** — Google 검색 랭킹 직접 지표
- 같은 패턴은 D3 외부에도 적용: 큰 정렬/변환, virtual list 측정, canvas 일괄 렌더링, 마이그레이션 스크립트
- 핵심 추상화: "동기 N번 반복 + main thread 점유 위험" = chunk runner

## How

```ts
// Bad — main thread block 60-200ms
function setupSimulationMode(...) {
  const simulation = createSim();
  simulation.stop();
  for (let i = 0; i < PRE_STABILIZE_TICKS; i++) simulation.tick();  // 동기 600 tick
}

// Good — chunk runner + AbortSignal
async function settleBubbleLayoutAsync(
  simulation, ticks,
  { signal, chunkBudgetMs = 6 } = {},
) {
  let remaining = ticks;
  while (remaining > 0) {
    if (signal?.aborted) return;
    const deadline = await nextFrameDeadline();
    if (signal?.aborted) return;

    const chunkStart = performance.now();
    while (remaining > 0) {
      simulation.tick();
      remaining -= 1;
      const budgetExceeded = performance.now() - chunkStart >= chunkBudgetMs;
      const deadlineExpired = deadline.timeRemaining() <= 1;
      if (budgetExceeded || deadlineExpired) break;
    }
  }
}

function nextFrameDeadline(): Promise<IdleDeadline> {
  return new Promise((resolve) => {
    if (typeof requestIdleCallback === 'function') {
      requestIdleCallback((d) => resolve(d), { timeout: 50 });
      return;
    }
    // Safari fallback — 가상 16ms deadline
    requestAnimationFrame(() => {
      const start = performance.now();
      resolve({
        didTimeout: false,
        timeRemaining: () => Math.max(0, 16 - (performance.now() - start)),
      });
    });
  });
}
```

## 핵심 원칙
1. **rIC 우선, rAF fallback** — Safari 미지원이라 rAF + 가상 16ms deadline
2. **frame budget 6-10ms** — 60fps의 16.6ms 중 절반 미만, 다른 작업 여유
3. **AbortSignal로 stale job 취소** — viewMode/root 전환, unmount 시 차단
4. **첫 진입 + relayout 같은 함수 공유** — 결과 좌표 일치 보장

## Pitfalls
1. `simulation.stop()` 후에도 `simulation.tick()` 가능 — stop은 internal stepper만 중단
2. tick handler가 settle 중에도 발화 — idle guard 발동 vs 결함 명확히
3. `simulationRef` 박제 시점 — settle 전 즉시 박제 + stale 검출 패턴
4. rIC timeout 너무 길면 발화 안 됨 — `timeout: 50` 강제
5. **Web Worker가 항상 정답 아님** — D3 force는 mutable object graph + DOM 의존성. chunk runner가 1차 해법

## Related
- [[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]] — INP-145 root fix (chunk runner 직전)
- [[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]
- [[AI-Native/tools/codex/pair-programming-root-fix]] — 진단 출처
- [[FE/performance/core-web-vitals/_MOC]]

## Sources
- INP-146 commit 394078d
