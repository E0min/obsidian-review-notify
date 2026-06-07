---
title: useRef
aliases: [useRef, DOM 참조, 렌더링 무관 변수]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/fa27a96bf6c94eb3b89f4ba86db13900
related:
  - "[[_MOC]]"
  - "[[state]]"
  - "[[lifecycle-useEffect]]"
source: ["Notion: React"]
migrated-from: "Notion: useRef"
---

# useRef

> TL;DR: 렌더링을 트리거하지 않고 값을 유지하는 훅. DOM 요소 접근과 리렌더링 없이 유지해야 하는 변수에 사용.

## What

렌더링과 무관하게 값을 유지하는 훅. DOM 요소 접근 + 리렌더링 없이 유지되는 변수.

## Why it matters

일반 변수는 리렌더링 시 초기화됨. 전역 변수는 컴포넌트 인스턴스 간 공유 문제. useRef가 둘을 해결.

## How

```javascript
const ref = useRef(초기값); // { current: 초기값 } 반환
ref.current; // 값 접근
ref.current = 새값; // 값 변경 (리렌더링 없음)
```

**DOM 접근**:
```javascript
const inputRef = useRef();
<input ref={inputRef} />
inputRef.current.focus(); // DOM 직접 조작
```

**렌더링 무관 변수**:
```javascript
const timerRef = useRef(null);
timerRef.current = setInterval(...); // 리렌더링 없이 타이머 ID 저장
clearInterval(timerRef.current);
```

## useState vs useRef 비교

| | useState | useRef |
|--|---------|--------|
| 값 변경 시 리렌더링 | O | X |
| 렌더링 간 값 유지 | O | O |
| 용도 | UI에 반영할 상태 | DOM 참조, 타이머 ID 등 |

## Pitfalls

- useRef 변경은 리렌더링 안 함 → UI 반영 필요하면 useState 사용
- 일반 변수(`var count`)를 useRef 대신 쓰면 리렌더링 시 초기화

## Related

- [[state]]
- [[lifecycle-useEffect]]
- [[useEffect-라이프사이클]]

## Sources

- Notion: React
