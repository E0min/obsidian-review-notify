---
title: 사전렌더링 - SSR (getServerSideProps)
aliases: [SSR, 서버사이드렌더링]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c50238380e39a15c11069dd69e1
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: 사전렌더링 - SSR (getServerSideProps)"
---

# 사전렌더링 - SSR (getServerSideProps)

> TL;DR: SSR은 사용자 요청 시마다 서버에서 HTML을 동적으로 생성하며, `getServerSideProps`를 통해 요청 컨텍스트(쿠키, 쿼리 등)에 접근할 수 있다.

## What

**SSR(Server-Side Rendering)** 은 사용자가 페이지를 요청할 때마다 서버가 HTML을 새로 생성해 반환하는 방식이다. 빌드 시 미리 생성하는 SSG와 달리, 매 요청마다 최신 데이터를 반영할 수 있다.

## Why it matters

로그인 상태, 사용자별 맞춤 데이터, 실시간으로 바뀌는 콘텐츠처럼 **요청 시점의 최신 데이터**가 필요한 페이지에 적합하다. 동시에 HTML을 서버에서 완성해 내려주므로 SEO에도 유리하다.

## How

### 기본 흐름

```
요청 → getServerSideProps 실행 → HTML 생성 → 클라이언트 전달 → Hydration
```

### 기본 사용법

```typescript
// pages/product/[id].tsx
import { GetServerSideProps, InferGetServerSidePropsType } from 'next';

type Product = {
  id: string;
  name: string;
};

// InferGetServerSidePropsType으로 props 타입 자동 추론
type Props = InferGetServerSidePropsType<typeof getServerSideProps>;

export default function ProductPage({ product }: Props) {
  return <h1>{product.name}</h1>;
}

export const getServerSideProps: GetServerSideProps = async (context) => {
  const { params, query, req, res } = context;

  const response = await fetch(`https://api.example.com/products/${params?.id}`);
  const product: Product = await response.json();

  return {
    props: { product },
  };
};
```

### context 객체 주요 속성

| 속성 | 설명 |
|------|------|
| `params` | 동적 라우트 파라미터 (`[id]` → `params.id`) |
| `query` | 쿼리 스트링 파라미터 |
| `req` | HTTP 요청 객체 (쿠키 등 접근 가능) |
| `res` | HTTP 응답 객체 |
| `locale` | 현재 locale |
| `preview`, `previewData` | 프리뷰 모드 관련 |

### 쿠키 접근

```typescript
export const getServerSideProps: GetServerSideProps = async ({ req }) => {
  const token = req.cookies['auth-token'];

  if (!token) {
    return {
      redirect: {
        destination: '/login',
        permanent: false,
      },
    };
  }

  return { props: {} };
};
```

### 병렬 데이터 패칭

여러 API를 동시에 호출할 때 `Promise.all()`로 병렬 처리해 응답 시간을 단축한다.

```typescript
export const getServerSideProps: GetServerSideProps = async () => {
  const [userRes, postsRes] = await Promise.all([
    fetch('https://api.example.com/user'),
    fetch('https://api.example.com/posts'),
  ]);

  const [user, posts] = await Promise.all([
    userRes.json(),
    postsRes.json(),
  ]);

  return { props: { user, posts } };
};
```

## Pitfalls

- `getServerSideProps`는 **서버에서만 실행**되므로 `window`, `document` 같은 브라우저 API 사용 불가
- `export` 키워드를 반드시 붙여야 Next.js가 인식함 (빠뜨리면 일반 함수로 취급되어 SSR 미적용)
- 요청마다 서버를 거치므로 **응답 속도가 SSG보다 느리고 서버 비용이 증가**함
- 반환 객체는 반드시 `{ props: {...} }` 형태여야 하며, `props`는 JSON 직렬화 가능해야 함

## Related

- [[ssg-정적경로]]
- [[ssg-동적경로]]
- [[isr]]
- [[seo-설정하기]]
- [[page-router-장단점]]

## Sources

- [Next.js 공식 문서 - getServerSideProps](https://nextjs.org/docs/basic-features/data-fetching/get-server-side-props)
- Notion: 사전렌더링 - SSR (getServerSideProps)
