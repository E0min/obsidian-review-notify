---
title: useCallback — 함수 재생성 방지
aliases: [useCallback, 함수 메모이제이션]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/6ab0db0fb3704be78c5089d2227dcf05
related:
  - "[[_MOC]]"
  - "[[useMemo]]"
  - "[[React-memo]]"
source: ["Notion: React"]
migrated-from: "Notion: useCallback — 함수 재생성 방지"
---

# useCallback — 함수 재생성 방지

> TL;DR: 리렌더링마다 함수가 새로 생성되는 것을 막아, 같은 함수 참조를 유지하는 훅. React.memo와 함께 써야 효과가 나온다.

## What

컴포넌트 리렌더링 시마다 함수가 새로 생성되는 것을 방지. 의존성이 바뀔 때만 새 함수 생성.

## Why it matters

JavaScript에서 함수는 매번 새로운 참조로 생성된다. `React.memo`로 감싼 자식 컴포넌트에 함수를 props로 전달하면, 부모가 리렌더링될 때마다 새 함수 참조가 전달되어 memo가 무의미해진다. `useCallback`으로 함수 참조를 고정하면 자식의 불필요한 리렌더링을 막을 수 있다.

## How

```javascript
const increment = useCallback(() => {
    setCount(prev => prev + 1);
}, []); // 의존성 없으면 항상 같은 함수 참조

const handleSearch = useCallback((query) => {
    fetchData(query);
}, [fetchData]); // fetchData가 바뀔 때만 갱신
```

## useCallback vs useMemo

```javascript
// useMemo: 값 반환
const memoVal = useMemo(() => compute(a, b), [a, b]);

// useCallback: 함수 반환 (useMemo로 함수 반환하는 것과 동일)
const memoFn = useCallback(() => doSomething(), []);
// 위와 동일: useMemo(() => () => doSomething(), [])
```

`useCallback(fn, deps)` 는 `useMemo(() => fn, deps)` 의 syntactic sugar.

## Pitfalls

- 모든 함수에 `useCallback` 적용 불필요 → 메모이제이션 비용 대비 효과를 고려
- `React.memo`된 자식에게 함수를 props로 전달할 때 필수
- 의존성 배열 관리 실수 시 stale closure 버그 발생

## Related

- [[useMemo]] — 값(연산 결과) 메모이제이션
- [[React-memo]] — 컴포넌트 단위 리렌더링 방지
- [[_MOC]]

## Sources

- [React 공식 문서 — useCallback](https://react.dev/reference/react/useCallback)
- Notion: React
