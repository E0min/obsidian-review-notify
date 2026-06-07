---
title: Page Router란
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c50238380b8a795c818316cf0f4
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: Page Router란"
---

# Page Router란

> TL;DR: `pages/` 디렉토리의 파일 구조가 곧 URL 경로가 되는 파일 기반 라우팅 시스템이다.

## What

Next.js의 전통적인 라우팅 방식으로, `pages/` 디렉토리 안의 파일 이름과 URL 경로를 **자동으로 1:1 매핑**한다. 별도의 라우터 설정 없이 파일을 만들기만 해도 라우트가 생성된다.

## Why it matters

파일 기반 라우팅은 설정 파일 없이 직관적으로 URL 구조를 파악할 수 있게 한다. 팀 협업 시 라우트 충돌을 줄이고, 코드 스플리팅이 자동으로 적용되어 페이지별 번들 최적화가 이루어진다.

## How

### 기본 디렉토리 구조

```
pages/
├── index.tsx          → /
├── about.tsx          → /about
├── blog/
│   ├── index.tsx      → /blog
│   └── [id].tsx       → /blog/:id  (동적 경로)
└── api/
    └── hello.ts       → /api/hello  (API 라우트)
```

### 주요 특징

| 특징 | 설명 |
|------|------|
| 파일 기반 라우팅 | 파일 생성 = 라우트 생성 |
| 자동 코드 스플리팅 | 페이지별 번들 분리 |
| 동적 라우팅 | `[id].tsx` 형식 파일명 사용 |
| API 라우팅 | `pages/api/` 폴더 내 파일이 엔드포인트 |
| 특수 파일 | `_app.tsx`, `_document.tsx`, `404.tsx` |

### Pages Router vs App Router 비교

| 항목 | Pages Router | App Router |
|------|-------------|-----------|
| 도입 버전 | Next.js 초기 | Next.js 13 |
| 디렉토리 | `pages/` | `app/` |
| 레이아웃 | `_app.tsx` | `layout.tsx` (중첩 가능) |
| 데이터 페칭 | `getStaticProps` / `getServerSideProps` | `async` 컴포넌트 / `fetch` |
| 서버 컴포넌트 | 미지원 | 기본 지원 |
| 스트리밍 | 미지원 | 지원 |
| 안정성 | 안정 (레거시) | 권장 (최신) |

### 페이지 컴포넌트 기본 구조

```typescript
// pages/about.tsx
import type { NextPage } from 'next';

const AboutPage: NextPage = () => {
  return (
    <div>
      <h1>About 페이지</h1>
    </div>
  );
};

export default AboutPage;
```

## Pitfalls

- `pages/` 와 `app/` 디렉토리를 동시에 사용할 수 있으나, 같은 경로가 중복되면 `app/`이 우선됨
- 파일명에 대문자 사용 가능하나 URL은 소문자로 처리됨 — 일관성을 위해 소문자/kebab-case 권장
- `pages/api/` 파일은 클라이언트 번들에 포함되지 않음 (서버 전용)
- Next.js 신규 프로젝트는 App Router 사용 권장 — Page Router는 레거시 지원 상태

## Related

- [[nextjs란]]
- [[nextjs-시작하기]]
- [[라우팅-설정하기]]
- [[page-router-네비게이팅]]
- [[api-routes]]

## Sources

- Notion: Page Router란
- [Next.js 공식 문서 - Pages Router](https://nextjs.org/docs/pages)
