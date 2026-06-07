---
title: 사전렌더링 - SSG (정적 경로)
aliases: [SSG, 정적사이트생성, getStaticProps]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c50238380f39440ec9f04bd59d7
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: 사전렌더링 - SSG (정적 경로)"
---

# 사전렌더링 - SSG (정적 경로)

> TL;DR: SSG는 빌드 시점에 HTML을 미리 생성해 CDN에서 즉시 서빙하므로 가장 빠르지만, 실시간 데이터 반영이 어렵다.

## What

**SSG(Static Site Generation)** 는 `next build` 시점에 HTML 파일을 미리 생성하는 방식이다. 빌드된 HTML은 CDN에 캐싱되어 사용자 요청 시 서버 처리 없이 즉시 반환된다.

`getStaticProps`를 사용해 빌드 시점에 외부 데이터를 가져와 페이지에 주입한다.

## Why it matters

SSR의 주요 단점인 **서버 부하, 응답 지연, 비용 증가** 문제를 해결한다.

| 항목 | SSR | SSG |
|------|-----|-----|
| HTML 생성 시점 | 요청 시마다 | 빌드 시 1회 |
| 데이터 최신성 | 항상 최신 | 빌드 시점 |
| 응답 속도 | 상대적으로 느림 | 매우 빠름 |
| 서버 의존성 | 높음 | 없음 (정적 파일) |

자주 변경되지 않는 콘텐츠(블로그 포스트, 제품 목록, 마케팅 페이지 등)에 적합하다.

## How

### 기본 사용법

```typescript
// pages/products.tsx
import { GetStaticProps, InferGetStaticPropsType } from 'next';

type Product = {
  id: string;
  name: string;
};

export default function ProductsPage({
  products,
}: InferGetStaticPropsType<typeof getStaticProps>) {
  return (
    <ul>
      {products.map((p) => (
        <li key={p.id}>{p.name}</li>
      ))}
    </ul>
  );
}

export async function getStaticProps() {
  const res = await fetch('https://api.example.com/products');
  const products: Product[] = await res.json();

  return {
    props: { products },
  };
}
```

### 정적 페이지 context에서 사용 가능한 속성

SSG의 context는 빌드 타임 정보만 포함한다. 요청 기반 정보는 사용할 수 없다.

| 속성 | 사용 가능 여부 |
|------|--------------|
| `params` | 가능 (동적 경로에서) |
| `locale` | 가능 |
| `query` | **불가** |
| `req` | **불가** |
| `res` | **불가** |

> 쿼리 스트링이 필요한 경우 CSR(클라이언트 사이드 렌더링)을 사용한다.

## Pitfalls

- **데이터 갱신 어려움**: 빌드 후 데이터가 바뀌어도 재빌드 전까지 반영 안 됨 → [[isr]]로 해결
- **빌드 시간 증가**: 페이지 수가 많을수록 빌드 시간이 길어짐
- **실시간 데이터 부적합**: 주가, 뉴스, 사용자별 맞춤 데이터에는 부적합
- `getStaticProps`는 서버 컨텍스트가 없으므로 `req.cookies` 등 요청 정보 접근 불가

## Related

- [[ssg-동적경로]]
- [[isr]]
- [[ssr-getServerSideProps]]
- [[page-router-장단점]]

## Sources

- [Next.js 공식 문서 - getStaticProps](https://nextjs.org/docs/basic-features/data-fetching/get-static-props)
- Notion: 사전렌더링 - SSG (정적 경로)
