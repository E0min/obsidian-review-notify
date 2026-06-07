---
title: Hydration 에러 — 브라우저 확장 프로그램 원인
aliases: [hydration error, suppressHydrationWarning, hydration mismatch]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[서버-컴포넌트-클라이언트-컴포넌트]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: hydration 에러"
---

# Hydration 에러 — 브라우저 확장 프로그램 원인

> TL;DR: 브라우저 확장 프로그램이 `<html>` 태그에 속성을 주입해 서버 HTML과 클라이언트 DOM이 불일치한다. `suppressHydrationWarning`으로 해결한다.

---

## What

Next.js에서 hydration은 서버에서 렌더링된 HTML에 React 이벤트 핸들러를 연결하는 과정. 서버 HTML과 클라이언트 렌더링 결과가 다르면 **Hydration Mismatch** 에러가 발생한다.

---

## Why it matters

개발 환경에서 코드 변경 없이도 다음 에러가 콘솔에 반복 출력될 수 있다:

```
Error: Hydration failed because the initial UI does not match what was rendered on the server.
```

이 에러는 실제 코드 문제가 아니어도 발생하므로 **원인 파악이 먼저**.

---

## How — 원인과 해결

### 원인: 브라우저 확장 프로그램의 DOM 조작

브라우저 확장 프로그램(번역기, 비밀번호 관리자, Grammarly 등)이 `<html>` 또는 `<body>` 태그에 속성을 자동으로 추가한다.

```html
<!-- 서버가 보낸 HTML -->
<html lang="ko">

<!-- 브라우저 확장이 수정한 HTML (클라이언트) -->
<html lang="ko" data-locator-hook-status-message="ok" data-lt-installed="true">
```

React는 두 DOM이 다르다고 판단해 hydration 에러를 발생시킨다.

### 해결: `suppressHydrationWarning`

```tsx
// app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" suppressHydrationWarning>
      {/*                 ↑ 이 속성이 핵심 */}
      <body>{children}</body>
    </html>
  );
}
```

`suppressHydrationWarning`은 해당 요소의 속성 불일치 경고를 무시하도록 React에 지시한다. **자식 컴포넌트에는 적용되지 않으므로** `<html>` 태그에만 추가하면 된다.

---

## Pitfalls

- **`suppressHydrationWarning`을 남용하지 말 것** — 진짜 코드 버그(서버/클라이언트 데이터 불일치)도 숨겨버린다. `<html>` 태그처럼 확장 프로그램 영향을 받는 요소에만 사용.
- **다른 hydration 에러 원인들**:
  - `Date.now()`, `Math.random()` 등 서버/클라이언트 실행 시점이 다른 값
  - `typeof window !== 'undefined'` 분기
  - 서버에서 가져온 데이터와 클라이언트 초기 상태가 다른 경우
  → 이런 경우는 `suppressHydrationWarning`이 아닌 코드 수정이 필요

---

## Related

- [[_MOC]] — Next.js 전체 지도
- [[서버-컴포넌트-클라이언트-컴포넌트]] — RSC/Client Component 렌더링 차이

## Sources

- [Next.js — suppressHydrationWarning](https://nextjs.org/docs/messages/react-hydration-error)
- [React — Hydration](https://react.dev/reference/react-dom/client/hydrateRoot)
