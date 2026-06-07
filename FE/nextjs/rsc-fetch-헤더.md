---
title: RSC에서 fetch 헤더 수동 전달
aliases: [server component fetch header, RSC headers, cookie forwarding]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[서버-컴포넌트-클라이언트-컴포넌트]]"
  - "[[서버-액션-server-actions]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: 서버 컴포넌트 fetch 헤더"
---

# RSC에서 fetch 헤더 수동 전달

> TL;DR: Server Component는 브라우저 컨텍스트가 없어 `fetch()`가 자동으로 Cookie·Authorization 헤더를 보내지 않는다. `next/headers`의 `headers()`로 클라이언트 요청 헤더를 읽어 수동으로 전달해야 한다.

---

## What

클라이언트(브라우저)에서 `fetch()`를 호출하면 쿠키가 자동으로 함께 전송된다. 그러나 **서버 컴포넌트(RSC)** 에서 `fetch()`를 호출하면 브라우저 컨텍스트가 없으므로 쿠키나 인증 헤더가 자동으로 포함되지 않는다.

---

## Why it matters

```
브라우저 → Next.js 서버 (Cookie: session=xxx 포함)
                ↓
         RSC 내 fetch('/api/data') ← 쿠키 없음! 인증 실패
```

인증이 필요한 API를 RSC에서 호출할 때, 세션/토큰을 수동으로 전달하지 않으면 **401 Unauthorized** 응답을 받는다.

---

## How

### `next/headers`로 요청 헤더 읽기

```typescript
// app/dashboard/page.tsx (Server Component)
import { headers } from 'next/headers';

export default async function DashboardPage() {
  const clientHeaders = await headers(); // 클라이언트 요청의 헤더 객체

  const cookie = clientHeaders.get('Cookie');
  const authorization = clientHeaders.get('Authorization');

  // fetch에 헤더 수동 전달
  const res = await fetch('https://api.example.com/user/me', {
    headers: {
      Cookie: cookie ?? '',
      Authorization: authorization ?? '',
    },
  });

  if (!res.ok) {
    throw new Error('인증 실패');
  }

  const user = await res.json();
  return <div>{user.name}</div>;
}
```

### 헬퍼 함수로 추상화

```typescript
// lib/api.ts
import { headers } from 'next/headers';

export async function serverFetch(url: string, options?: RequestInit) {
  const clientHeaders = await headers();

  return fetch(url, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      Cookie: clientHeaders.get('Cookie') ?? '',
      Authorization: clientHeaders.get('Authorization') ?? '',
      ...options?.headers,
    },
  });
}

// 사용
const res = await serverFetch('/api/user/me');
```

---

## 패턴 비교

| 상황 | 해결책 |
|------|--------|
| RSC에서 쿠키 기반 인증 API 호출 | `headers()` → Cookie 전달 |
| RSC에서 Bearer 토큰 API 호출 | `headers()` → Authorization 전달 |
| Server Action에서 API 호출 | 동일 (`headers()`는 Server Action에서도 사용 가능) |
| 클라이언트 컴포넌트에서 API 호출 | 자동 전달 (브라우저 컨텍스트) |

---

## Pitfalls

- **`headers()`는 동적 함수**: 호출하는 순간 해당 페이지는 **동적 렌더링**으로 강제됨 → 정적 생성(SSG) 불가. 꼭 필요한 RSC에서만 사용.
- **`headers()`는 async**: Next.js 15부터 `await headers()`로 사용 (동기 사용은 deprecated).
- **Route Handler(`/api/`)는 해당 없음**: Route Handler는 Node.js HTTP 컨텍스트에서 동작하므로 `request.headers`로 직접 접근.
- **같은 도메인 내부 API 호출**: Next.js Route Handler(`/api/...`)를 RSC에서 호출할 때도 헤더 전달 필요. 내부 API라고 자동 인증되지 않음.

---

## Related

- [[_MOC]] — Next.js 전체 지도
- [[서버-컴포넌트-클라이언트-컴포넌트]] — RSC와 클라이언트 컴포넌트의 실행 환경 차이
- [[서버-액션-server-actions]] — Server Action에서도 동일 패턴 적용 가능

## Sources

- [Next.js — headers()](https://nextjs.org/docs/app/api-reference/functions/headers)
- [Next.js — Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
