---
title: useEffect로 라이프 사이클 조절하기
aliases: [useEffect lifecycle, componentDidMount useEffect, componentWillUnmount useEffect]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/2fae87df75574feabc3209b14725509a
related:
  - "[[_MOC]]"
  - "[[lifecycle-useEffect]]"
  - "[[컴포넌트-라이프사이클]]"
source: ["Notion: React"]
migrated-from: "Notion: useEffect로 라이프 사이클 조절하기"
---

# useEffect로 라이프 사이클 조절하기

> TL;DR: useEffect의 의존성 배열 패턴으로 마운트/업데이트/언마운트를 세밀하게 제어. cleanup 반환값은 반드시 함수여야 함.

## What

useEffect의 의존성 배열과 cleanup 반환을 활용해 컴포넌트 라이프사이클 각 단계를 함수형으로 제어하는 방법.

## Why it matters

클래스형 componentDidMount / componentWillUnmount를 함수형에서 동일하게 구현하고, 최초 렌더링 제외 등 세밀한 제어도 가능.

## How

```javascript
// 1. 마운트 시 1회 실행 (componentDidMount)
useEffect(() => {
    // API 호출, 이벤트 리스너 설정
    return () => { /* 언마운트 정리 */ };
}, []);

// 2. 특정 state 변경 시 실행 (componentDidUpdate)
useEffect(() => {
    console.log('count 변경:', count);
}, [count]);

// 3. 매 렌더링마다 실행 (의존성 배열 없음)
useEffect(() => {
    console.log('렌더링');
}); // 배열 없음

// 언마운트 시 스크롤 리스너 제거
useEffect(() => {
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
}, []);
```

**최초 렌더링 제외하고 실행**:
```javascript
const isFirst = useRef(false);
useEffect(() => {
    if (!isFirst.current) {
        isFirst.current = true;
        return;
    }
    // 실제 로직
});
```

## Pitfalls

- 반환값은 반드시 함수 또는 아무것도 없어야 함. 다른 값 반환 시 에러:
  `Error: An effect function must not return anything besides a function`

## Related

- [[lifecycle-useEffect]]
- [[컴포넌트-라이프사이클]]
- [[useRef]]

## Sources

- Notion: React
