---
title: App Router
aliases: [앱라우터, app router]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c502383802e801ff81df9fa7d13
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: App Router"
---

# App Router

> TL;DR: Next.js 13에서 도입된 `app/` 디렉토리 기반 라우팅 방식으로, RSC를 기본 지원하고 파일 역할별 컨벤션으로 레이아웃·로딩·에러를 선언적으로 관리한다.

## What

Next.js 13부터 도입된 새로운 라우팅 시스템. 기존 `pages/` 디렉토리 대신 `app/` 디렉토리를 사용하며, **React Server Components(RSC)를 기본값**으로 채택했다.

파일 이름 자체가 역할을 결정한다.

| 파일명 | 역할 |
|--------|------|
| `page.js` | 해당 경로의 기본 UI 컴포넌트 |
| `layout.js` | 하위 경로를 감싸는 공통 레이아웃 |
| `loading.js` | 데이터 로딩 중 보여줄 UI (Suspense 자동 래핑) |
| `error.js` | 에러 발생 시 폴백 UI (Error Boundary 자동 래핑) |
| `not-found.js` | 404 UI |

## Why it matters

Page Router의 한계를 해소한다.

1. **props drilling 제거**: 데이터 페칭을 최상단에서만 할 필요 없이, 필요한 서버 컴포넌트에서 직접 fetch
2. **JS 번들 최소화**: 서버 컴포넌트는 클라이언트 JS를 생성하지 않음
3. **중첩 레이아웃**: `layout.js`를 각 디렉토리에 배치해 URL 계층과 UI 계층을 일치시킴
4. **선언적 로딩/에러 처리**: `loading.js`, `error.js` 파일 하나로 해당 세그먼트 전체 커버

## How

### 디렉토리 구조 예시

```
app/
├── layout.js          → 루트 레이아웃 (필수)
├── page.js            → /
├── about/
│   └── page.js        → /about
├── blog/
│   ├── layout.js      → /blog/* 공통 레이아웃
│   ├── page.js        → /blog
│   └── [id]/
│       ├── page.js    → /blog/:id
│       └── loading.js → /blog/:id 로딩 UI
└── (marketing)/
    └── page.js        → / (URL에 marketing 미포함)
```

### 서버 컴포넌트에서 비동기 데이터 페칭

```javascript
// app/blog/[id]/page.js — 서버 컴포넌트 (기본값)
export default async function Page({ params }) {
  const data = await fetch(`https://api.example.com/posts/${params.id}`)
    .then(res => res.json());
  return <div>{data.title}</div>;
}
```

### 동적 경로 + 정적 생성

```javascript
// generateStaticParams로 빌드 타임에 경로 사전 생성
export async function generateStaticParams() {
  const posts = await fetch('https://api.example.com/posts').then(res => res.json());
  return posts.map(post => ({ id: String(post.id) }));
}
```

### 클라이언트 컴포넌트 선언

```javascript
'use client'; // 이 디렉티브가 있어야 클라이언트 컴포넌트

import { useState } from 'react';

export default function Counter() {
  const [count, setCount] = useState(0);
  return <button onClick={() => setCount(c => c + 1)}>{count}</button>;
}
```

### Pages Router vs App Router 비교

| 항목 | Pages Router | App Router |
|------|-------------|-----------|
| 도입 버전 | Next.js 초기 | Next.js 13 |
| 디렉토리 | `pages/` | `app/` |
| 기본 컴포넌트 타입 | 클라이언트 | 서버 (RSC) |
| 레이아웃 | `_app.tsx` 단일 | `layout.js` 중첩 가능 |
| 데이터 페칭 | `getStaticProps` / `getServerSideProps` | `async` 컴포넌트 직접 fetch |
| 로딩 UI | 직접 구현 | `loading.js` 자동 Suspense |
| 에러 처리 | 직접 구현 | `error.js` 자동 ErrorBoundary |
| 서버 컴포넌트 | 미지원 | 기본 지원 |
| 권장 여부 | 레거시 | 신규 프로젝트 권장 |

## Pitfalls

- `app/`과 `pages/` 디렉토리를 동시에 사용 가능하지만, 같은 경로가 충돌하면 `app/`이 우선됨
- 서버 컴포넌트(기본)에서는 `useState`, `useEffect`, 이벤트 핸들러 사용 불가 → 인터랙션이 필요한 부분만 `'use client'` 추가
- `error.js`는 반드시 클라이언트 컴포넌트여야 함 (`'use client'` 필수)
- `loading.js`는 `page.js`와 같은 디렉토리에 있어야 해당 세그먼트에만 적용됨
- 동적 경로 `[id]`는 폴더명으로 만들어야 함 (Page Router는 파일명)

## Related

- [[page-router]]
- [[레이아웃-설정하기]]
- [[rsc-이해하기]]
- [[앱라우터-네비게이팅]]
- [[앱라우터-데이터페칭]]

## Sources

- Notion: App Router
- [Next.js 공식 문서 - App Router](https://nextjs.org/docs/app)
