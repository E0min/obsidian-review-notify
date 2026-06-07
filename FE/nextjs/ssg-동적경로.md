---
title: 사전렌더링 - SSG (동적 경로)
aliases: [getStaticPaths, 동적SSG]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c50238380a8a1e6dc1b9d747c63
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: 사전렌더링 - SSG (동적 경로)"
---

# 사전렌더링 - SSG (동적 경로)

> TL;DR: `getStaticPaths`로 빌드 시 생성할 경로를 정의하고, `getStaticProps`로 각 경로의 데이터를 가져와 동적 URL을 정적 파일로 사전 생성한다.

## What

`/posts/[id]` 같은 동적 라우트 페이지를 SSG로 만들려면 **어떤 경로를 미리 생성할지** 알려줘야 한다. `getStaticPaths`가 그 역할을 담당하고, `getStaticProps`가 각 경로에 필요한 데이터를 가져온다.

## Why it matters

동적 URL이 수천 개인 블로그나 e-commerce 사이트에서 모든 상품·게시글 페이지를 정적으로 서빙할 수 있다. 빌드 타임에 HTML을 생성해두므로 CDN 캐싱과 SEO 최적화가 동시에 가능하다.

## How

### 기본 구조

```typescript
// pages/posts/[id].tsx
import { GetStaticPaths, GetStaticProps } from 'next';

type Post = {
  id: string;
  title: string;
  content: string;
};

export default function PostPage({ post }: { post: Post }) {
  return (
    <article>
      <h1>{post.title}</h1>
      <p>{post.content}</p>
    </article>
  );
}

// 1. 빌드 시 생성할 경로 목록을 정의
export const getStaticPaths: GetStaticPaths = async () => {
  const res = await fetch('https://api.example.com/posts');
  const posts: Post[] = await res.json();

  const paths = posts.map((post) => ({
    params: { id: post.id },
  }));

  return {
    paths,
    fallback: false, // 목록에 없는 경로는 404
  };
};

// 2. 각 경로별 데이터 fetch
export const getStaticProps: GetStaticProps = async ({ params }) => {
  const res = await fetch(`https://api.example.com/posts/${params?.id}`);
  const post: Post = await res.json();

  return {
    props: { post },
  };
};
```

### fallback 옵션 비교

| fallback 값 | 동작 | 적합한 상황 |
|-------------|------|------------|
| `false` | 목록 외 경로 → 404 | 경로가 고정적, SEO 중요, 재빌드로 추가 |
| `true` | 첫 요청 시 로딩 화면 표시 후 동적 생성, 이후 캐싱 | 데이터가 방대해 빌드 시간 단축이 필요할 때 |
| `'blocking'` | 첫 요청 시 HTML 완성 후 반환 (로딩 화면 없음) | SEO + 사용자 경험 모두 중요할 때 |

### fallback: true 사용 시 로딩 처리

```typescript
import { useRouter } from 'next/router';

export default function PostPage({ post }: { post: Post }) {
  const router = useRouter();

  // fallback 상태일 때 로딩 UI 표시
  if (router.isFallback) {
    return <div>Loading...</div>;
  }

  return <article><h1>{post.title}</h1></article>;
}
```

### SSG context에서 사용 가능한 속성

빌드 타임 정보(params)만 포함하며, 요청 기반 정보(query, req, res)는 사용 불가.

```typescript
export const getStaticProps: GetStaticProps = async ({ params, locale }) => {
  // params.id: 동적 라우트 파라미터
  // locale: 현재 locale
  // query, req, res → 불가
};
```

## Pitfalls

- `fallback: true` + SEO 조합: fallback 상태에서 메타태그 데이터가 없어 SEO 누락 → [[seo-설정하기]] 참고
- `getStaticPaths`와 `getStaticProps`는 **반드시 함께** export해야 함. 하나만 있으면 오류
- 경로 수가 매우 많을 경우 `fallback: 'blocking'`으로 빌드 시간과 SEO를 동시에 확보
- `params` 값은 항상 **문자열**임. 숫자가 필요하면 `Number(params.id)`로 변환 필요

## Related

- [[ssg-정적경로]]
- [[isr]]
- [[seo-설정하기]]
- [[ssr-getServerSideProps]]
- [[page-router-장단점]]

## Sources

- [Next.js 공식 문서 - getStaticPaths](https://nextjs.org/docs/basic-features/data-fetching/get-static-paths)
- Notion: 사전렌더링 - SSG (동적 경로)
