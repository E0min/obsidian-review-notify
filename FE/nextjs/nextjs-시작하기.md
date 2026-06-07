---
title: Next.js 시작하기
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c502383806886dfc45f5912afef
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: Next.js 시작하기"
---

# Next.js 시작하기

> TL;DR: `create-next-app`으로 프로젝트를 생성하고, `_app.tsx` · `_document.tsx` · `next.config.js` 세 파일이 앱 전체의 뼈대를 구성한다.

## What

Next.js 프로젝트를 처음 설정할 때 알아야 할 CLI 명령어와 핵심 설정 파일들이다.

## Why it matters

프로젝트 초기 설정을 올바르게 이해하면 전역 레이아웃, 공통 스타일, HTML 문서 구조를 일관되게 관리할 수 있다. 잘못된 파일에 코드를 넣으면 SSR/CSR 전환에서 오류가 발생한다.

## How

### 프로젝트 생성

```bash
npx create-next-app@14 [프로젝트 이름]
```

생성 시 선택 옵션:

| 옵션 | 설명 |
|------|------|
| TypeScript | 타입 안정성 확보 |
| ESLint | 코드 품질 관리 |
| Tailwind CSS | 유틸리티 우선 CSS |
| `src/` 디렉토리 | 소스 파일 분리 |
| App Router | 권장 (Next.js 13+) |
| Page Router | 레거시 방식 |
| import alias | `@/` 등 절대 경로 별칭 |

---

### `_app.tsx` — 루트 컴포넌트

모든 페이지를 감싸는 최상위 컴포넌트. 클라이언트/서버 모두에서 실행된다.

```typescript
// pages/_app.tsx
import type { AppProps } from 'next/app';
import '../styles/globals.css'; // 전역 스타일

export default function App({ Component, pageProps }: AppProps) {
  return (
    // 공통 레이아웃, 상태 관리 Provider 등을 여기에 배치
    <Component {...pageProps} />
  );
}
```

주요 props:

- `Component` — 현재 활성화된 페이지 컴포넌트
- `pageProps` — `getStaticProps` / `getServerSideProps`에서 전달된 데이터

---

### `_document.tsx` — HTML 문서 구조

`<html>`, `<head>`, `<body>` 태그를 커스터마이징할 때 사용. **서버에서만 실행**되므로 이벤트 핸들러나 `useState` 사용 불가.

```typescript
// pages/_document.tsx
import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="ko">
      <Head>
        {/* 공통 메타태그, 폰트 링크 등 */}
      </Head>
      <body>
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
```

---

### `next.config.js` — Next.js 설정

```javascript
// next.config.js
/** @type {import('next').NextConfig} */
const nextConfig = {
  reactStrictMode: true,          // React 엄격 모드
  images: {
    domains: ['example.com'],     // 외부 이미지 허용 도메인
  },
  i18n: {
    locales: ['ko', 'en'],        // 다국어 지원
    defaultLocale: 'ko',
  },
  async redirects() {             // 리다이렉트 설정
    return [
      { source: '/old', destination: '/new', permanent: true },
    ];
  },
  env: {
    CUSTOM_KEY: process.env.CUSTOM_KEY, // 환경 변수 노출
  },
};

module.exports = nextConfig;
```

## Pitfalls

- `_app.tsx`에 무거운 로직을 넣으면 모든 페이지 렌더링에 영향을 줌
- `_document.tsx`는 서버 전용이므로 브라우저 API 호출 금지
- `next.config.js` 변경 후에는 반드시 개발 서버 재시작 필요
- App Router 사용 시 `_app.tsx`, `_document.tsx`는 사용하지 않음 → `app/layout.tsx`로 대체

## Related

- [[nextjs란]]
- [[page-router]]
- [[api-routes]]

## Sources

- Notion: Next.js 시작하기
- [Next.js 공식 문서 - Getting Started](https://nextjs.org/docs/getting-started)
