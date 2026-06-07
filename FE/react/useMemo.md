---
title: useMemo — 같은 연산 반복 방지
aliases: [useMemo, memoization, 메모이제이션, 연산 최적화]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/cc1880bb426948caaa307fc7c42c1e2a
related:
  - "[[_MOC]]"
  - "[[React-memo]]"
  - "[[useCallback]]"
source: ["Notion: React"]
migrated-from: "Notion: useMemo — 같은 연산 반복 방지"
---

# useMemo — 같은 연산 반복 방지

> TL;DR: 비싼 계산 결과를 캐싱해두고, 의존성이 바뀔 때만 재연산하는 훅. 불필요한 연산을 줄여 렌더링 성능을 최적화한다.

## What

비싼 계산 결과를 메모이제이션하여 의존성이 변경될 때만 재연산.

## Why it matters

리렌더링이 발생할 때마다 컴포넌트 내부의 모든 코드가 다시 실행된다. 무거운 연산(대용량 배열 필터링, 복잡한 수식 등)이 매 렌더링마다 실행되면 성능 저하로 이어진다. `useMemo`는 결과값을 기억해두고 의존성이 바뀔 때만 재계산하여 불필요한 연산을 방지한다.

## How

```javascript
const memoizedValue = useMemo(() => {
    return expensiveCalculation(a, b);
}, [a, b]); // a나 b가 변할 때만 재계산
```

```javascript
// 배열 필터링 최적화
const filteredItems = useMemo(() => {
    return items.filter(item => item.includes(filter));
}, [items, filter]);
```

## useMemo vs useCallback vs React.memo

| | useMemo | useCallback | React.memo |
|--|---------|------------|-----------|
| 대상 | 값 | 함수 | 컴포넌트 |
| 목적 | 연산 결과 캐싱 | 함수 참조 유지 | 리렌더링 방지 |

## Pitfalls

- 모든 값에 useMemo 남용 금지 → 메모이제이션 자체도 비용(메모리 + 비교 연산)이 발생
- 의존성 배열에 필요한 값을 빠뜨리면 stale 값을 반환하는 버그 발생
- 단순한 연산에는 오히려 오버헤드가 더 클 수 있음 → 진짜 비싼 연산에만 적용

## Related

- [[React-memo]] — 컴포넌트 단위 메모이제이션
- [[useCallback]] — 함수 참조 메모이제이션
- [[_MOC]]

## Sources

- [React 공식 문서 — useMemo](https://react.dev/reference/react/useMemo)
- Notion: React
