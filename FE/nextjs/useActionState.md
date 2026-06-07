---
title: useActionState
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18935c50238380f0a518cd71ac340399
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: useActionState"
---

# useActionState

> TL;DR: 서버 액션 실행 후 반환 상태를 관리하는 React 훅으로, 폼(form)과 함께 사용한다.

## What

`useActionState`는 서버 액션(Server Action)을 폼과 연결하고, 실행 결과 상태와 로딩 여부를 클라이언트에서 관리하는 React 훅이다.

```typescript
const [state, formAction, isPending] = useActionState(action, "초기 상태");
```

| 반환값 | 설명 |
|---|---|
| `state` | 서버 액션이 반환한 최신 상태값 |
| `formAction` | `<form>`의 `action` 속성에 연결하는 함수 |
| `isPending` | 서버 액션 실행 중 여부 (`boolean`) |

## Why it matters

Next.js App Router에서 서버 액션은 API Route 없이 서버 로직을 실행할 수 있게 해준다. 그러나 클라이언트에서 "실행 결과"와 "로딩 상태"를 추적하려면 별도 상태 관리가 필요하다. `useActionState`는 이 두 가지를 하나의 훅으로 해결한다.

## How

### 기본 사용 예시

```typescript
// actions.ts
"use server";
export async function action(prevState: string, formData: FormData) {
  const input = formData.get("message") as string;
  return `서버에서 받은 데이터: ${input}`;
}
```

```typescript
// page.tsx
"use client";
import { useActionState } from "react";
import { action } from "./actions";

export default function Page() {
  const [state, formAction, isPending] = useActionState(action, "초기 상태");

  return (
    <div>
      <p>결과: {state}</p>
      <form action={formAction}>
        <input type="text" name="message" />
        <button type="submit" disabled={isPending}>
          {isPending ? "처리 중..." : "전송"}
        </button>
      </form>
    </div>
  );
}
```

### 흐름 정리

1. 사용자가 폼을 제출하면 `formAction`이 서버 액션을 호출한다.
2. 실행 중에는 `isPending`이 `true`가 된다.
3. 서버 액션이 값을 반환하면 `state`가 업데이트된다.
4. `action` 함수의 첫 번째 인자(`prevState`)로 이전 상태를 받을 수 있다.

## Pitfalls

- `useActionState`는 `"use client"` 컴포넌트에서만 사용 가능하다.
- 서버 액션 함수의 시그니처는 반드시 `(prevState, formData)` 형태여야 한다.
- `useActionState` vs `useFormStatus`: `useActionState`는 전체 상태(반환값, 로딩)를 관리하고, `useFormStatus`는 폼 내부 자식 컴포넌트에서 제출 상태만 확인할 때 사용한다.
- React 18 이하에서는 `useFormState`(react-dom)를 사용해야 하며, React 19부터 `useActionState`로 통합되었다.

## Related

- [[useActionState-vs-useAction]] — 폼 vs 이벤트 핸들러 선택 기준
- [[서버-액션]] — Server Action 개념 및 'use server' 지시문
- [[재검증하기]] — 서버 액션 후 revalidatePath / revalidateTag

## Sources

- [React 공식 문서 — useActionState](https://react.dev/reference/react/useActionState)
- Notion: Next.js
