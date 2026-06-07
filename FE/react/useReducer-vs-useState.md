---
title: useReducer vs useState
aliases: [useReducer useState 비교, 상태 관리 선택]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/12f35c5023838003a7f9d54659bf2c75
related:
  - "[[_MOC]]"
  - "[[useReducer]]"
  - "[[state]]"
source: ["Notion: React"]
migrated-from: "Notion: useReducer vs useState"
---

# useReducer vs useState

> TL;DR: 상태 1~2개·독립적이면 useState, 상태 3개 이상·서로 연관되면 useReducer.

## What

두 훅의 차이와 선택 기준.

## Why it matters

잘못된 선택은 코드 복잡도를 높임. useState 남발 시 setter가 분산되고, useReducer 과용 시 보일러플레이트 과다.

## How

| 항목 | useState | useReducer |
|------|---------|-----------|
| 적합 상황 | 단순 독립 상태 | 복잡하게 얽힌 다수 상태 |
| 코드 가독성 | 상태 많으면 분산 | 리듀서에 로직 집중 |
| 상태 추적 | 어려움 (여러 setter) | 액션 타입으로 명확 |
| 업데이트 효율 | 각각 개별 호출 | dispatch로 일괄 처리 |

**선택 기준**:
- 상태가 1~2개, 독립적 → **useState**
- 상태 3개+, 서로 연관, 업데이트 로직 복잡 → **useReducer**

```javascript
// useState - 상태가 많으면 분산
const [email, setEmail] = useState("");
const [password, setPassword] = useState("");
const [loading, setLoading] = useState(false);

// useReducer - 한 곳에서 관리
const [state, dispatch] = useReducer(reducer, { email: "", password: "", loading: false });
dispatch({ type: "LOGIN_REQUEST" }); // loading:true, error 초기화 한번에
```

## Pitfalls

- 단순한 상태에 useReducer 쓰면 불필요한 보일러플레이트 증가
- 전역 상태가 필요하면 useReducer 단독이 아닌 Context API 또는 Redux와 결합

## Related

- [[useReducer]]
- [[state]]

## Sources

- Notion: React
