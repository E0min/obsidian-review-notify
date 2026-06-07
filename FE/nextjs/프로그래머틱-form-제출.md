---
title: 프로그래머틱 Form 제출
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18c35c5023838085b97cd76de9213dca
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: 프로그래머틱 Form 제출"
---

# 프로그래머틱 Form 제출

> TL;DR: `useRef`로 폼을 참조하고 `requestSubmit()`을 호출하면 버튼이 아닌 외부 요소에서도 폼을 제출할 수 있다.

## What

폼 제출 버튼(`<button type="submit">`) 이외의 요소(예: `<div>`, 커스텀 UI)에서 폼을 제출해야 할 때, `useRef`로 폼 요소를 참조하고 `requestSubmit()`을 호출하는 패턴이다.

## Why it matters

서버 액션이나 `onSubmit` 핸들러가 연결된 폼을 클릭 이벤트로 직접 트리거해야 하는 경우가 있다. 예를 들어 커스텀 디자인된 카드나 아이콘 버튼에서 삭제·수정 액션을 실행할 때 유용하다.

## How

### 기본 패턴

```typescript
"use client";
import { useRef } from "react";
import { deleteAction } from "./actions";

export default function DeleteCard() {
  const formRef = useRef<HTMLFormElement>(null);

  return (
    <form ref={formRef} action={deleteAction}>
      <input type="hidden" name="id" value="123" />
      {/* 커스텀 UI 요소로 폼 제출 */}
      <div
        onClick={() => formRef.current?.requestSubmit()}
        style={{ cursor: "pointer" }}
      >
        삭제하기
      </div>
    </form>
  );
}
```

### 분리된 핸들러 함수

```typescript
const handleSubmit = () => {
  formRef.current?.requestSubmit();
};

return (
  <form ref={formRef} action={deleteAction}>
    <CustomButton onClick={handleSubmit} />
  </form>
);
```

### requestSubmit() vs submit() 비교

| 메서드 | 유효성 검사 | onsubmit 핸들러 | 서버 액션 |
|---|---|---|---|
| `requestSubmit()` | ✅ 실행됨 | ✅ 트리거됨 | ✅ 작동 |
| `submit()` | ❌ 건너뜀 | ❌ 트리거 안 됨 | ⚠️ 미작동 가능 |

서버 액션과 `useActionState`를 함께 쓸 때는 반드시 `requestSubmit()`을 사용한다.

## Pitfalls

- `<div onClick>`보다는 `<button type="submit">`을 사용하는 것이 접근성(a11y) 측면에서 권장된다. 키보드 내비게이션, 스크린 리더 호환성이 자동으로 지원된다.
- `submit()`은 폼 유효성 검사를 우회하고 `onsubmit` 이벤트도 발생시키지 않는다. 서버 액션과 함께 쓰면 예상대로 동작하지 않을 수 있다.
- `formRef.current`는 컴포넌트가 마운트된 이후에만 접근 가능하다. `onClick` 내에서 `?.` 옵셔널 체이닝으로 안전하게 접근한다.
- 폼 외부에서 `requestSubmit()`을 호출할 경우, 폼이 DOM에 렌더링되어 있지 않으면 작동하지 않는다.

### 개선 권장 예시

```typescript
// 권장: <div> 대신 <button> 사용
<form action={deleteAction}>
  <button type="submit" className="custom-delete-btn">
    삭제하기
  </button>
</form>
```

## Related

- [[useActionState]] — 폼과 서버 액션 상태 연결
- [[useActionState-vs-useAction]] — 폼 제출 vs 이벤트 핸들러 선택
- [[서버-액션]] — 'use server' 서버 액션 기본

## Sources

- [MDN — HTMLFormElement.requestSubmit()](https://developer.mozilla.org/en-US/docs/Web/API/HTMLFormElement/requestSubmit)
- Notion: Next.js
