---
title: useEffect 사용하기
aliases: [useEffect, side effect, 사이드 이펙트]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/f348a3d2344b47faad7cdc559ad4ccb8
related:
  - "[[_MOC]]"
  - "[[컴포넌트-라이프사이클]]"
  - "[[useRef]]"
source: ["Notion: React"]
migrated-from: "Notion: useEffect 사용하기"
---

# useEffect 사용하기

> TL;DR: 함수형 컴포넌트에서 부수 효과를 처리하는 훅. 의존성 배열로 실행 시점을 제어.

## What

함수형 컴포넌트에서 부수 효과(데이터 fetching, DOM 조작, 구독 등)를 처리하는 훅.

## Why it matters

`useState`의 setter는 비동기 → 핸들러에서 바로 변경된 값 접근 불가. useEffect는 렌더링 후 실행되므로 최신값 보장.

## How

```javascript
useEffect(() => {
    // 실행할 로직
    return () => {
        // cleanup (언마운트 또는 다음 effect 실행 전)
    };
}, [dependencies]); // 의존성 배열
```

**의존성 배열 3가지 패턴**:
```javascript
useEffect(fn);         // 매 렌더링마다 실행
useEffect(fn, []);     // 마운트 시 1번만
useEffect(fn, [dep]);  // dep 변경 시마다
```

## Why not event handler?

```javascript
// 문제: handleClick에서 setCount 후 바로 count 로그 → 이전값 출력
// 해결: useEffect([count])에서 처리
```

## Pitfalls

- cleanup 함수에서 함수 외 값 반환 시 에러
- 무한 루프 주의: 의존성 배열에 effect 내에서 변경하는 state 포함하면 루프

## Related

- [[컴포넌트-라이프사이클]]
- [[useEffect-라이프사이클]]
- [[useRef]]

## Sources

- Notion: React
