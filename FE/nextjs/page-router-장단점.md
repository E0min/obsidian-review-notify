---
title: Page Router 장단점
aliases: [Pages Router, 페이지라우터]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c502383805f8d7afd9636d92b2a
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: Page Router 장단점"
---

# Page Router 장단점

> TL;DR: Page Router는 파일 기반 라우팅과 다양한 렌더링 전략(SSR/SSG/ISR)이 장점이지만, 레이아웃 관리와 데이터 페칭 집중으로 인한 props drilling, 번들 최적화의 한계가 단점이다.

## What

Next.js **Page Router**는 `pages/` 디렉토리 구조가 그대로 URL이 되는 파일 시스템 기반 라우팅 시스템이다. `pages/about.js` → `/about`, `pages/posts/[id].js` → `/posts/:id`처럼 파일명과 URL이 1:1 대응된다.

## Why it matters

App Router(Next.js 13+)와의 비교 맥락에서 Page Router의 특성을 이해하면, 기존 프로젝트 유지보수나 마이그레이션 결정 시 근거가 된다.

## How

### 장점

#### 1. 파일 시스템 기반 간편한 라우팅

파일을 생성하는 것만으로 라우트가 만들어진다. 별도 라우터 설정이 필요 없어 직관적이다.

```
pages/
├── index.js          →  /
├── about.js          →  /about
├── posts/
│   ├── index.js      →  /posts
│   └── [id].js       →  /posts/:id
└── api/
    └── hello.js      →  /api/hello (API Route)
```

#### 2. 다양한 사전 렌더링 방식 제공

페이지 특성에 맞게 렌더링 전략을 선택할 수 있다.

| 전략 | 함수 | 적합한 상황 |
|------|------|------------|
| SSR | `getServerSideProps` | 실시간 데이터, 인증 필요 |
| SSG | `getStaticProps` | 변경 빈도 낮은 콘텐츠 |
| ISR | `getStaticProps` + `revalidate` | 주기적 업데이트 콘텐츠 |

### 단점

#### 1. 페이지별 레이아웃 설정 번거로움

각 페이지마다 다른 레이아웃이 필요하면 `getLayout` 패턴을 수동으로 구현해야 한다.

```javascript
// pages/_app.js
export default function App({ Component, pageProps }) {
  // 페이지별로 getLayout이 정의되어 있으면 사용, 없으면 기본 렌더링
  const getLayout = Component.getLayout ?? ((page) => page);
  return getLayout(<Component {...pageProps} />);
}

// pages/dashboard.js
DashboardPage.getLayout = function getLayout(page) {
  return <DashboardLayout>{page}</DashboardLayout>;
};
```

#### 2. 데이터 페칭이 페이지 컴포넌트에 집중 → props drilling

`getServerSideProps` / `getStaticProps`는 페이지 최상단 컴포넌트에서만 실행된다. 깊은 컴포넌트에 데이터를 전달하려면 props drilling이 불가피하다.

```javascript
// 페이지에서 받은 data를 여러 단계를 거쳐 전달해야 함
export default function Page({ user, posts, comments }) {
  return <Layout user={user}><PostList posts={posts} comments={comments} /></Layout>;
}
```

#### 3. 불필요한 컴포넌트도 JS 번들에 포함

처음부터 필요하지 않은 무거운 컴포넌트도 초기 번들에 포함되어 LCP(Largest Contentful Paint)에 영향을 줄 수 있다. `dynamic import`로 해결한다.

```javascript
import dynamic from 'next/dynamic';

// 필요할 때만 로드 (코드 스플리팅)
const HeavyComponent = dynamic(() => import('../components/HeavyComponent'), {
  loading: () => <p>Loading...</p>,
  ssr: false, // 서버 사이드 렌더링 제외 (브라우저 전용 라이브러리 등)
});

export default function Page() {
  return (
    <div>
      <HeavyComponent />
    </div>
  );
}
```

## Pitfalls

- `getLayout` 패턴 없이 페이지별 레이아웃을 컴포넌트 내부에서 처리하면, 페이지 전환 시 레이아웃이 언마운트·리마운트되어 상태가 초기화됨
- `dynamic import`에 `ssr: false`를 설정한 컴포넌트는 서버 HTML에 포함되지 않아 SEO에 영향을 줄 수 있음
- App Router 전환 시 `getServerSideProps` / `getStaticProps` API는 그대로 사용 불가 (Server Component + fetch로 대체)

## Related

- [[ssr-getServerSideProps]]
- [[ssg-정적경로]]
- [[ssg-동적경로]]
- [[isr]]
- [[seo-설정하기]]
- [[스타일링]]

## Sources

- [Next.js 공식 문서 - Pages Router](https://nextjs.org/docs/pages)
- Notion: Page Router 장단점
