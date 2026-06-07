---
title: SEO 설정하기 (Page Router)
aliases: [SEO, 메타태그, Head컴포넌트]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c50238380709d05e9dd4c7c8809
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: SEO 설정하기 (Page Router)"
---

# SEO 설정하기 (Page Router)

> TL;DR: Next.js Page Router에서는 `next/head`의 `Head` 컴포넌트로 페이지별 메타태그를 설정하며, `fallback: true` 사용 시 `router.isFallback` 체크로 SEO 누락을 방지한다.

## What

**SEO(Search Engine Optimization)** 를 위해 각 페이지에 고유한 `<title>`, `<meta>` 태그를 설정해야 한다. Next.js Page Router에서는 `next/head`에서 제공하는 `Head` 컴포넌트를 사용해 페이지별로 메타태그를 주입한다.

## Why it matters

검색엔진 크롤러와 SNS 공유 시 Open Graph 태그가 없으면 페이지 제목·설명·썸네일이 제대로 표시되지 않는다. SSR/SSG로 서버에서 HTML에 메타태그를 포함시켜야 크롤러가 실제 콘텐츠를 인식할 수 있다.

## How

### 기본 메타태그 설정

```javascript
// pages/posts/[id].js
import Head from 'next/head';

export default function PostPage({ data }) {
  return (
    <>
      <Head>
        {/* 페이지 제목 */}
        <title>{data.title}</title>

        {/* 검색 결과 설명 */}
        <meta name="description" content={data.description} />

        {/* Open Graph (SNS 공유용) */}
        <meta property="og:title" content={data.title} />
        <meta property="og:description" content={data.description} />
        <meta property="og:image" content={data.image} />
        <meta property="og:url" content={`https://example.com/posts/${data.id}`} />

        {/* Twitter Card */}
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content={data.title} />
        <meta name="twitter:image" content={data.image} />
      </Head>

      <article>
        <h1>{data.title}</h1>
      </article>
    </>
  );
}
```

### fallback: true 사용 시 SEO 문제 해결

`getStaticPaths`에서 `fallback: true`를 사용하면, 아직 생성되지 않은 경로 요청 시 컴포넌트가 데이터 없이 렌더링된다. 이때 메타태그도 비어있어 SEO에 불리하다.

**해결 방법 1: `router.isFallback` 체크 후 기본 메타태그 제공**

```javascript
import Head from 'next/head';
import { useRouter } from 'next/router';

export default function PostPage({ data }) {
  const router = useRouter();

  // fallback 상태: 임시 메타태그로 SEO 최소 보장
  if (router.isFallback) {
    return (
      <>
        <Head>
          <title>로딩 중...</title>
          <meta name="description" content="페이지를 불러오는 중입니다." />
        </Head>
        <div>Loading...</div>
      </>
    );
  }

  return (
    <>
      <Head>
        <title>{data.title}</title>
        <meta name="description" content={data.description} />
        <meta property="og:image" content={data.image} />
      </Head>
      <article><h1>{data.title}</h1></article>
    </>
  );
}
```

**해결 방법 2: `fallback: 'blocking'` 사용**

HTML이 완성된 후 응답하므로 fallback 상태가 없어 SEO 문제가 발생하지 않는다.

```javascript
export async function getStaticPaths() {
  return {
    paths: [],
    fallback: 'blocking', // SEO + 동적 경로 동시 해결
  };
}
```

**해결 방법 3: `fallback: false`로 모든 경로 사전 생성**

경로 수가 적다면 모든 경로를 빌드 시 생성한다.

## Pitfalls

- `Head` 안에 중복 태그가 여러 컴포넌트에 있을 경우, **나중에 렌더링된 것이 우선** 적용됨
- `fallback: true` 상태에서 메타태그 데이터가 `undefined`이면 OG 태그가 빈 값으로 크롤링됨
- `_app.js`의 전역 `Head`와 페이지별 `Head`가 충돌할 수 있으므로 `key` prop으로 중복 제거

```javascript
// key prop으로 전역/페이지별 메타태그 충돌 방지
<meta key="og-title" property="og:title" content={title} />
```

## Related

- [[ssg-동적경로]]
- [[ssr-getServerSideProps]]
- [[isr]]
- [[page-router-장단점]]

## Sources

- [Next.js 공식 문서 - next/head](https://nextjs.org/docs/api-reference/next/head)
- Notion: SEO 설정하기 (Page Router)
