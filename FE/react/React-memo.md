---
title: React.memo — 불필요한 리렌더링 방지
aliases: [React.memo, memo, HOC, 고차 컴포넌트]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/dafccc37b5004d2098f8f166141dddd7
related:
  - "[[_MOC]]"
  - "[[useMemo]]"
  - "[[useCallback]]"
source: ["Notion: React"]
migrated-from: "Notion: React.memo — 불필요한 리렌더링 방지"
---

# React.memo — 불필요한 리렌더링 방지

> TL;DR: props가 변경되지 않으면 자식 컴포넌트의 리렌더링을 건너뛰는 고차 컴포넌트(HOC). 부모가 자주 리렌더링되는 상황에서 자식 컴포넌트를 보호한다.

## What

props가 변경되지 않으면 자식 컴포넌트 리렌더링 방지하는 고차 컴포넌트(HOC).

## Why it matters

React는 기본적으로 부모가 리렌더링되면 자식도 무조건 리렌더링된다. 자식 컴포넌트가 무거운 렌더링 작업을 수행하거나, 변경이 없는 props를 받는다면 불필요한 렌더링이 낭비된다. `React.memo`로 감싸면 props가 바뀌지 않는 한 자식 렌더링을 스킵한다.

## How

```javascript
const ChildComponent = React.memo(function ChildComponent({ count }) {
    return <div>Child Count: {count}</div>;
});
```

부모가 리렌더링돼도 `count` prop이 같으면 `ChildComponent` 재렌더링 안 함.

**참조 타입 문제** (객체/배열/함수는 매 렌더링마다 새 참조 생성):

```javascript
// 해결 1: useCallback으로 함수 메모이제이션
const handleClick = useCallback((id) => {
    console.log(id);
}, []);

// 해결 2: areEqual 커스텀 비교 함수
const ListItem = React.memo(function ListItem({ item, onClick }) {
    return <li onClick={() => onClick(item.id)}>{item.text}</li>;
}, (prev, next) => {
    return prev.item.id === next.item.id && prev.onClick === next.onClick;
});
```

## Pitfalls

- 기본 비교는 얕은 비교(shallow equality) → 객체/배열/함수 props는 매번 새 참조이므로 memo가 무효화됨
- `React.memo` + `useCallback` 세트로 사용해야 함수 props에서 효과적
- `areEqual` 커스텀 비교 함수: `true` 반환 시 리렌더링 스킵, `false` 반환 시 리렌더링

## Related

- [[useMemo]] — 값(연산 결과) 메모이제이션
- [[useCallback]] — 함수 참조 메모이제이션
- [[_MOC]]

## Sources

- [React 공식 문서 — memo](https://react.dev/reference/react/memo)
- Notion: React
