---
title: passive event listener 누락 패턴
aliases: [passive event, scroll listener, passive true, touchmove passive]
type: concept
status: budding
created: 2026-04-24
updated: 2026-05-23
tags: [fe/perf, fe/browser, status/budding, career/fe, performance]
related:
  - "[[FE/react/_concepts/vercel-react-best-practices]]"
  - "[[FE/browser/_MOC]]"
source: []
migrated-from: MindGraph-TIL/02-Problem-Solving/2026-04-24-passive-event-listener.md
---

# passive event listener 누락 패턴

> TL;DR: `mousemove`·`touchmove`·`wheel`·`scroll`에 `{ passive: true }`를 명시하지 않으면 브라우저가 scroll-blocking을 가정해 메인 스레드 지연. 드래그/스크롤 UX 직격.

## What
브라우저는 일부 이벤트(특히 `touchmove`, `wheel`)에서 listener가 `preventDefault()` 호출 가능성을 항상 가정한다. 명시적으로 `passive: true`를 주지 않으면 listener 완료 전까지 scroll/drag 처리를 못 한다.

## Why it matters
- INP/스크롤 지연의 단골 원인
- D3 force-graph 드래그처럼 mousemove 핫 패스에서는 fps 직접 손실
- Lighthouse "Does not use passive listeners" 경고

## How
```ts
// Bad
element.addEventListener('mousemove', handler);

// Good
element.addEventListener('mousemove', handler, { passive: true });

// React 16+ — 합성 이벤트는 자동 passive지만 직접 ref + native listener 시 명시
useEffect(() => {
  const el = ref.current;
  el?.addEventListener('wheel', onWheel, { passive: true });
  return () => el?.removeEventListener('wheel', onWheel);
}, []);
```

## Pitfalls
- `preventDefault()`가 실제로 필요한 경우 `passive: true`면 무시되고 콘솔 경고
- 라이브러리 코드(D3 drag, react-dnd 등) 내부에서 native listener 등록하면 명시 못 함 → 라이브러리 버전 확인
- jsdom 테스트 환경은 passive 옵션 무시 — 실제 브라우저로만 검증

## Related
- [[FE/react/_concepts/vercel-react-best-practices]]
- [[FE/d3-visualization/_MOC]] — D3 드래그 적용 사례
- [[FE/performance/runtime-perf/_MOC]]

## Sources
- Vercel React Best Practices v1.0.0
- Chrome DevRel — passive event listener intervention
