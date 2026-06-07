---
title: Request Memoization
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c502383808881a4f80af82acd5a
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: Request Memoization"
---

# Request Memoization
> TL;DR: 한 렌더링 사이클 내에서 동일한 URL의 fetch 요청을 자동으로 중복 제거해 한 번만 실제 네트워크 요청을 보내는 메커니즘.

## What
한 페이지를 렌더링하는 동안 여러 서버 컴포넌트가 동일한 API 엔드포인트로 fetch 요청을 보낼 때, Next.js가 자동으로 중복 요청을 제거하고 실제 네트워크 요청은 딱 한 번만 보낸다. 결과는 메모리에 임시 보관되었다가 페이지 렌더링이 완료되면 모두 소멸된다.

- 서버 컴포넌트에서만 작동
- 개발자가 별도 설정 없이 자동 적용
- 범위: 단일 페이지 렌더링 사이클 (페이지 이동·새로고침 시 초기화)

## Why it matters
Next.js App Router의 핵심 패턴인 **"fetch data where it's needed"** — 각 컴포넌트가 필요한 데이터를 직접 fetch하도록 설계할 때, 공통 데이터를 여러 컴포넌트가 각각 요청해도 성능 문제가 생기지 않는다. Props drilling 없이 각 컴포넌트가 독립적으로 데이터를 선언할 수 있다.

## How

```javascript
// ComponentA와 ComponentB가 동일한 URL을 fetch해도
// 실제 네트워크 요청은 한 번만 발생

async function ComponentA() {
  const data = await fetch('https://api.example.com/data').then(res => res.json());
  return <div>{data.title}</div>;
}

async function ComponentB() {
  const data = await fetch('https://api.example.com/data').then(res => res.json());
  return <div>{data.description}</div>;
}

// 두 컴포넌트가 동일 URL fetch → 한 번만 실제 요청
```

내부적으로 React는 렌더 트리를 순회할 때 동일 URL·옵션의 fetch를 감지하면 캐시에서 꺼내 반환한다.

## Pitfalls
- **클라이언트 컴포넌트에는 적용되지 않는다.** `'use client'` 선언 컴포넌트는 브라우저에서 실행되므로 이 메커니즘이 작동하지 않는다.
- **Request Memoization ≠ 데이터 캐시**: 요청 메모이제이션은 렌더링 범위 내 임시 중복 제거이고, 데이터 캐시(Data Cache)는 서버 전역에서 거의 영구적으로 보관된다. 혼동하지 않도록 주의.
- URL이나 옵션(headers, method 등)이 조금이라도 다르면 별개의 요청으로 취급된다.

## Related
- [[풀라우트-캐시]] — 빌드 타임 정적 페이지 캐싱 (데이터 캐시와 연동)
- [[클라이언트-라우터-캐시]] — 클라이언트 측 RSC 페이로드 캐싱
- [[라우트-세그먼트-옵션]] — 페이지 단위 캐시 동작 제어

## Sources
- [Next.js 공식 문서 — Caching: Request Memoization](https://nextjs.org/docs/app/building-your-application/caching#request-memoization)
- Notion: Next.js
