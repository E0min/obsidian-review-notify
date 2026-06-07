---
title: useActionState vs useAction
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18935c5023838049bebdeed8c0adbd37
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: useActionState vs useAction"
---

# useActionState vs useAction

> TL;DR: 폼 제출이면 `useActionState`, 버튼 클릭 등 이벤트 핸들러면 `useAction`을 사용한다.

## What

서버 액션(Server Action)을 클라이언트에서 실행할 때 두 가지 훅 중 상황에 맞는 것을 선택해야 한다.

| 구분 | `useActionState` | `useAction` |
|---|---|---|
| 폼 필요 여부 | ✅ 필요 | ❌ 불필요 |
| 실행 방식 | `form action` 자동 실행 | `execute()` 직접 호출 |
| 로딩 상태 | `isPending` | `pending` |
| 결과 접근 | `state` | `result` |
| 주요 용도 | 로그인 / 회원가입 / 일반 폼 | API 호출 / 버튼 이벤트 |

## Why it matters

서버 액션을 클라이언트에서 다루는 방법은 실행 트리거가 무엇인지에 따라 달라진다. 잘못 선택하면 폼 유효성 검사가 우회되거나, 불필요한 `<form>` 래퍼가 생기는 구조가 된다.

## How

### useActionState — 폼 제출에 사용

```typescript
"use client";
import { useActionState } from "react";
import { loginAction } from "./actions";

export default function LoginForm() {
  const [state, formAction, isPending] = useActionState(loginAction, null);

  return (
    <form action={formAction}>
      <input type="email" name="email" />
      <input type="password" name="password" />
      <button type="submit" disabled={isPending}>
        {isPending ? "로그인 중..." : "로그인"}
      </button>
      {state?.error && <p>{state.error}</p>}
    </form>
  );
}
```

### useAction — 이벤트 핸들러에 사용

```typescript
"use client";
import { useAction } from "next-safe-action/hooks"; // 또는 커스텀 훅
import { deleteItemAction } from "./actions";

export default function ItemCard({ id }: { id: string }) {
  const { execute, status, result, pending, reset } = useAction(deleteItemAction);

  return (
    <div>
      <button onClick={() => execute({ id })} disabled={pending}>
        {pending ? "삭제 중..." : "삭제"}
      </button>
      {result?.data && <p>삭제 완료</p>}
    </div>
  );
}
```

### 반환값 비교

```typescript
// useActionState 반환
const [state, formAction, isPending] = useActionState(action, initialState);

// useAction 반환 (next-safe-action 기준)
const { execute, status, result, pending, reset } = useAction(action);
```

## Pitfalls

- `useActionState`는 서버 액션 함수 시그니처가 반드시 `(prevState, formData)` 형태여야 한다.
- `useAction`은 Next.js 내장 훅이 아니라 `next-safe-action` 같은 라이브러리에서 제공하는 경우가 많다. 프로젝트마다 API가 다를 수 있다.
- 폼이 있는 UI에 `useAction` + `onClick`을 억지로 연결하면 접근성(a11y)이 저하된다. 폼이 있다면 `useActionState`가 더 적합하다.

## Related

- [[useActionState]] — useActionState 단독 개념
- [[서버-액션]] — Server Action 기본 개념
- [[프로그래머틱-form-제출]] — useRef로 폼을 직접 제출하는 패턴

## Sources

- [React 공식 문서 — useActionState](https://react.dev/reference/react/useActionState)
- Notion: Next.js
