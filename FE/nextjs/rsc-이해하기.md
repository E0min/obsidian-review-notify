---
title: React Server Components (RSC) 이해하기
aliases: [RSC, 리액트 서버 컴포넌트, React Server Components]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c502383808780e6c3833cee46fa
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: React Server Components (RSC) 이해하기"
---

# React Server Components (RSC) 이해하기

> TL;DR: 상호작용이 불필요한 컴포넌트를 서버에서만 렌더링해 JS 번들에서 제외함으로써, 번들 크기와 불필요한 Hydration 비용을 줄이는 React 아키텍처다.

## What

RSC는 컴포넌트를 **서버 컴포넌트**와 **클라이언트 컴포넌트** 두 종류로 나누는 개념이다.

| 구분 | 서버 컴포넌트 | 클라이언트 컴포넌트 |
|------|-------------|----------------|
| 실행 위치 | 서버만 | 서버(초기 SSR) + 클라이언트 |
| 선언 방법 | 기본값 (디렉티브 불필요) | 파일 상단에 `'use client'` |
| JS 번들 포함 | 포함 안 됨 | 포함됨 |
| DB 직접 접근 | 가능 | 불가 |
| Hook 사용 | 불가 | 가능 |
| 이벤트 핸들러 | 불가 | 가능 |
| SEO | 유리 | SSR 초기 HTML은 유리 |

## Why it matters

React 앱이 커질수록 두 가지 문제가 누적된다.

1. **JS 번들 크기 증가**: 인터랙션이 없는 단순 표시용 컴포넌트도 클라이언트 JS에 포함됨
2. **불필요한 Hydration**: 서버에서 렌더링된 HTML을 클라이언트에서 다시 처리(Hydration)해야 하는데, 정적 콘텐츠에도 이 비용이 발생함

RSC는 "상호작용이 없는 컴포넌트는 서버에서만 실행하고 클라이언트에는 결과 HTML만 전달한다"는 원칙으로 이 두 문제를 동시에 해결한다.

## How

### 서버 컴포넌트에서 Hook을 쓸 수 없는 이유

서버는 요청마다 컴포넌트를 실행하고 HTML을 생성한 뒤 **즉시 종료**한다. Hook이 전제하는 세 가지 조건이 서버에 없다.

1. **'기억' 공간 없음**: `useState`는 렌더링 사이에 값을 기억해야 하는데, 서버는 HTML 생성 후 종료되므로 state를 저장할 곳이 없음
2. **'타이밍' 없음**: `useEffect`는 "렌더링 후" 실행되는 훅인데, 서버에는 "렌더링 후"라는 시점 자체가 없음 — 렌더링이 곧 끝임
3. **'상호작용' 없음**: `useState`의 setter로 re-render를 유발하는 개념이 서버에는 없음

**비유**:
- 클라이언트 컴포넌트 = 칠판: 쓰고 지우고 다시 쓸 수 있음 (상태 변경, re-render)
- 서버 컴포넌트 = 종이 인쇄: 한 번 찍으면 끝, 수정 불가 (요청당 1회 실행)

### 서버 컴포넌트 예시 (DB 직접 접근)

```javascript
// app/posts/page.js — 서버 컴포넌트 (기본값, 'use client' 없음)
import { db } from '@/lib/db';

export default async function PostsPage() {
  // 서버에서 직접 DB 쿼리 — 클라이언트에 DB 로직 노출 없음
  const posts = await db.query('SELECT * FROM posts');
  return (
    <ul>
      {posts.map(post => <li key={post.id}>{post.title}</li>)}
    </ul>
  );
}
```

### 클라이언트 컴포넌트 예시

```javascript
'use client'; // 클라이언트 컴포넌트 선언

import { useState } from 'react';

export default function LikeButton({ initialCount }) {
  const [count, setCount] = useState(initialCount);
  return (
    <button onClick={() => setCount(c => c + 1)}>
      좋아요 {count}
    </button>
  );
}
```

### 혼합 패턴 (권장)

```javascript
// app/post/[id]/page.js — 서버 컴포넌트
import LikeButton from '@/components/LikeButton'; // 클라이언트 컴포넌트 import

export default async function PostPage({ params }) {
  const post = await fetchPost(params.id); // 서버에서 데이터 페칭
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
      {/* 인터랙티브한 부분만 클라이언트 컴포넌트 */}
      <LikeButton initialCount={post.likes} />
    </article>
  );
}
```

## Pitfalls

- 서버 컴포넌트에서 `window`, `document` 등 브라우저 API 사용 시 `ReferenceError` 발생 → 클라이언트 컴포넌트로 이동
- 클라이언트 컴포넌트도 **초기 렌더링 시 서버에서 실행됨** (SSR). `'use client'`는 "클라이언트에서도 실행된다"는 의미지 "서버에서 실행 안 된다"가 아님
- 클라이언트 컴포넌트에서 서버 컴포넌트를 직접 import하면 서버 컴포넌트가 클라이언트 번들로 끌려들어감 → `children` prop으로 전달하는 패턴 사용
- 기본 원칙: **가능하면 서버 컴포넌트, 꼭 필요한 경우에만 클라이언트 컴포넌트**

## Related

- [[app-router]]
- [[rsc-주의사항]]
- [[앱라우터-데이터페칭]]
- [[nextjs란]]

## Sources

- Notion: React Server Components (RSC) 이해하기
- [Next.js 공식 문서 - Server Components](https://nextjs.org/docs/app/building-your-application/rendering/server-components)
