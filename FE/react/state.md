---
title: State와 useState
aliases: [state, useState, 상태, 리렌더링]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/a38402b2f5834877adfb3dc104324ddc
related:
  - "[[_MOC]]"
  - "[[props]]"
  - "[[props로-state-전달]]"
source: ["Notion: React"]
migrated-from: "Notion: State와 useState"
---

# State와 useState

> TL;DR: `useState`는 컴포넌트의 동적 데이터를 관리하는 훅. state 변경 시 자동 리렌더링. `setState(값)` 직접 호출 금지 — 반드시 화살표 함수로 래핑.

## What

컴포넌트의 동적 데이터를 관리하는 변수. 변경 시 자동으로 컴포넌트 리렌더링.

## Why it matters

일반 변수 변경은 React가 감지 못해 UI 미갱신 → useState 필수.

## How

```javascript
import { useState } from 'react';

const [state, setState] = useState(초기값);
// state: 현재 값
// setState: 값 변경 함수 (호출 시 리렌더링 트리거)
```

```javascript
const [count, setCount] = useState(0);
const [light, setLight] = useState("ON");

// 버튼 클릭 시 증가
<button onClick={() => setCount(count + 1)}>click</button>

// 토글
<button onClick={() => setLight(light === "ON" ? "OFF" : "ON")}>{light}</button>
```

**리렌더링 조건 3가지**:
1. `useState`로 state 변경
2. 전달받은 props 변경
3. 부모 컴포넌트 리렌더링

**주의**: `<button onClick={setState(state+1)}>` (X) → 렌더링 시 즉시 실행, 무한루프
→ `onClick={() => setState(state+1)}` (O)

## Pitfalls

- state 직접 수정 불가 (`state.count++` X) → setState 함수 사용
- `useState`가 반환하는 배열: `[현재값, 업데이트함수]`

## Related

- [[_MOC]]
- [[props]]
- [[props로-state-전달]]
- [[state-사용자-입력]]
- [[이벤트-처리]]

## Sources

- Notion: State와 useState
