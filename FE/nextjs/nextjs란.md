---
title: Next.js란
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c5023838009b5c7f9df692136e2
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: Next.js란?(feat. 사전 렌더링)"
---

# Next.js란

> TL;DR: Next.js는 React의 CSR 한계(느린 초기 로딩, SEO 불리)를 서버 사이드 렌더링으로 보완하는 React 프레임워크다.

## What

Next.js는 **React.js의 프레임워크**다. 라이브러리와 프레임워크의 차이를 이해하는 것이 출발점이다.

| 구분 | 라이브러리 | 프레임워크 |
|------|-----------|-----------|
| 주도권 | 개발자 | 프레임워크 |
| 자유도 | 높음 | 낮음 |
| 기능 제공 | 최소 | 풍부 |
| 예시 | React, Lodash | Next.js, Angular |

## Why it matters

React는 기본적으로 **CSR(Client Side Rendering)** 방식으로 동작한다. 이 방식은 두 가지 문제가 있다.

1. **느린 초기 로딩**: 빈 HTML → JS 번들 다운로드 → JS 실행 후에야 화면이 보임
2. **SEO 불리**: 검색 엔진 크롤러가 수집할 때 빈 HTML만 보임

Next.js는 **SSR(Server Side Rendering)** 을 기본 제공하여 이 두 문제를 해결한다.

## How

### CSR 렌더링 과정 (React 기본)

```
접속 → 빈 HTML 반환 → JS 번들 다운로드 → JS 실행 → FCP(화면 표시)
```

- 사용자는 JS 실행 완료 전까지 흰 화면을 봄
- `<div id="root"></div>` 만 있는 HTML이 크롤러에 수집됨

### SSR 렌더링 과정 (Next.js)

```
접속 → 서버에서 HTML 생성 → 완성된 HTML 반환 → Hydration → TTI(인터랙션 가능)
```

- 사용자는 즉시 콘텐츠를 볼 수 있음 (빠른 FCP)
- 완성된 HTML이 크롤러에 수집됨 (SEO 유리)

### CSR vs SSR 비교

| 항목 | CSR (React) | SSR (Next.js) |
|------|------------|--------------|
| 렌더링 위치 | 클라이언트 (브라우저) | 서버 |
| 초기 로딩 속도 | 느림 | 빠름 |
| SEO | 불리 | 유리 |
| 서버 리소스 | 적음 | 많음 |
| 인터랙션 | 빠름 | Hydration 후 가능 |

## Pitfalls

- SSR이 항상 유리한 것은 아님. 서버 리소스 소비가 크므로, 유저 개인화 데이터가 많은 페이지는 CSR 혼합이 나을 수 있음
- Hydration 불일치(서버 HTML ≠ 클라이언트 렌더 결과)가 발생하면 콘솔 경고 및 레이아웃 깜빡임 유발
- `window`, `document` 같은 브라우저 API는 SSR 실행 중 접근 불가 → `useEffect` 또는 `typeof window !== 'undefined'` 가드 필요

## Related

- [[nextjs-시작하기]]
- [[page-router]]
- [[pre-fetching]]

## Sources

- Notion: Next.js란?(feat. 사전 렌더링)
- [Next.js 공식 문서](https://nextjs.org/docs)
