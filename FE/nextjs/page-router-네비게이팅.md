---
title: Page Router 네비게이팅
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c502383809badf1cf4513739cec
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: Page Router 네비게이팅"
---

# Page Router 네비게이팅

> TL;DR: `<a>` 태그 대신 `<Link>` 컴포넌트나 `router.push()`를 사용해야 전체 페이지 새로고침 없이 CSR 방식으로 이동한다.

## What

Next.js Page Router에서 페이지 간 이동을 처리하는 세 가지 방법: HTML `<a>` 태그, `<Link>` 컴포넌트, `useRouter` 훅.

## Why it matters

`<a>` 태그로 이동하면 서버에 새 요청을 보내 전체 페이지를 다시 로드한다. Next.js의 CSR 네비게이션 이점(빠른 전환, 상태 유지)을 활용하려면 전용 방법을 사용해야 한다.

## How

### `<a>` 태그 (비권장)

```html
<!-- 서버 요청 발생 → 전체 페이지 새로고침 -->
<a href="/about">About</a>
```

- 브라우저가 서버에 새 HTTP 요청을 보냄
- 페이지 전체를 다시 파싱하고 렌더링
- React 상태(전역 스토어 등)가 초기화됨

---

### `<Link>` 컴포넌트 (선언적 이동)

클릭 가능한 링크 요소에 사용한다. CSR 방식으로 이동하며 서버 요청이 발생하지 않는다.

```javascript
import Link from 'next/link';

export default function Nav() {
  return (
    <nav>
      <Link href="/about">About</Link>
      <Link href="/blog/1">블로그 포스트 1</Link>

      {/* 동적 경로 */}
      <Link href={`/blog/${postId}`}>포스트 {postId}</Link>

      {/* 객체 형태로 쿼리 파라미터 전달 */}
      <Link href={{ pathname: '/search', query: { keyword: 'next' } }}>
        검색
      </Link>
    </nav>
  );
}
```

---

### `useRouter` — 프로그래매틱 이동

버튼 클릭, 폼 제출 후 리다이렉트 등 **이벤트 핸들러 안에서** 이동할 때 사용한다.

```javascript
import { useRouter } from 'next/router';

export default function LoginForm() {
  const router = useRouter();

  const handleLogin = async () => {
    // 로그인 처리 후...
    router.push('/home');           // 앞으로 이동 (히스토리 추가)
    // router.replace('/home');     // 현재 히스토리 교체 (뒤로가기 불가)
    // router.back();               // 이전 페이지로 이동
  };

  return <button onClick={handleLogin}>로그인</button>;
}
```

### `router.push` vs `router.replace`

| 메서드 | 히스토리 | 뒤로가기 |
|--------|---------|---------|
| `router.push('/home')` | 히스토리에 추가 | 가능 |
| `router.replace('/home')` | 현재 항목 교체 | 불가 |

## Pitfalls

- `<Link>` 컴포넌트 내부에 `<a>` 태그를 중첩하지 말 것 (Next.js 13+ 에서는 불필요)
- `useRouter`는 **클라이언트 컴포넌트에서만** 사용 가능 (서버 컴포넌트 불가)
- `router.push`는 기본적으로 프리페칭을 하지 않으므로 성능이 중요한 경우 수동 프리페칭 필요 → [[pre-fetching]] 참조
- `router.query`는 초기 렌더 시 빈 객체일 수 있음 (`router.isReady` 확인)

## Related

- [[page-router]]
- [[라우팅-설정하기]]
- [[pre-fetching]]

## Sources

- Notion: Page Router 네비게이팅
- [Next.js 공식 문서 - Linking and Navigating](https://nextjs.org/docs/pages/building-your-application/routing/linking-and-navigating)
