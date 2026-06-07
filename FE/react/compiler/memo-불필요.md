---
title: React Compiler에서 useMemo 불필요 패턴
aliases: [react compiler, automatic memoization, forget compiler, useMemo deprecated]
type: concept
status: budding
created: 2026-04-24
updated: 2026-05-23
tags: [fe/react, fe/perf, status/budding, career/fe]
related:
  - "[[FE/react/_concepts/vercel-react-best-practices]]"
  - "[[FE/react/_MOC]]"
source: []
migrated-from: MindGraph-TIL/02-Problem-Solving/2026-04-24-react-compiler-memo-불필요.md
---

# React Compiler에서 useMemo 불필요 패턴

> TL;DR: React Compiler(구 React Forget)가 켜져 있으면 `useMemo`·`useCallback`·`React.memo` 대부분 자동 처리. 수동 메모는 가독성만 해치고 효과 없음.

## What
React 19+에서 React Compiler가 컴파일 타임에 컴포넌트의 reactive value를 분석해 자동 memoization 코드를 삽입한다. 따라서 개발자가 수동으로 `useMemo`/`useCallback`을 도배하는 패턴은 사라진다.

## Why it matters
- 코드 가독성 회복 — `useCallback(() => fn, [deps])` 보일러플레이트 제거
- deps 배열 누락/오기재로 인한 stale closure 버그 감소
- 그러나 **데이터 구조 최적화(O(n) → O(1))는 컴파일러가 못 함** — 별개 문제

## How
```tsx
// React 18 (수동 메모 필요)
const handleClick = useCallback(() => setX(x + 1), [x]);
const expensive = useMemo(() => compute(data), [data]);

// React 19 + Compiler (수동 메모 불필요)
const handleClick = () => setX(x + 1);
const expensive = compute(data);
```

활성화: Next.js 16에서 `experimental.reactCompiler: true` 또는 React 19 자동.

## Pitfalls
- 컴파일러는 **referential equality**만 자동화. **로직 비용**(`compute(data)` 실행 자체)은 데이터 구조 바꿔 해결해야 함 — Map/Set으로 O(1) 룩업, derived state는 render 중 계산
- 컴파일러 off / 외부 라이브러리에 컴포넌트 넘길 때는 여전히 수동 메모 필요 가능성
- ESLint `react-compiler` 룰셋으로 위반 패턴 자동 감지 권장

## Related
- [[FE/react/_concepts/vercel-react-best-practices]]
- [[FE/react/rendering/_MOC]]
- [[FE/react/hooks/_MOC]]

## Sources
- Vercel React Best Practices v1.0.0
- React 19 release notes
