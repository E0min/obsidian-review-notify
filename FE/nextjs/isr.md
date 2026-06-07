---
title: 사전렌더링 - ISR (Incremental Static Regeneration)
aliases: [ISR, 점진적정적재생성]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c50238380df9f35c952eea6dd6a
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: 사전렌더링 - ISR (Incremental Static Regeneration)"
---

# 사전렌더링 - ISR (Incremental Static Regeneration)

> TL;DR: ISR은 `revalidate` 옵션으로 정적 페이지를 주기적으로 백그라운드 재생성해 SSG의 속도와 SSR의 데이터 최신성을 동시에 달성한다.

## What

**ISR(Incremental Static Regeneration)** 은 SSG의 빠른 응답 속도를 유지하면서, 지정한 주기마다 페이지를 백그라운드에서 재생성해 최신 데이터를 반영하는 방식이다.

`getStaticProps`의 반환 객체에 `revalidate` 옵션(초 단위)을 추가하는 것만으로 동작한다.

## Why it matters

| 방식 | 속도 | 데이터 최신성 |
|------|------|-------------|
| SSG | 매우 빠름 | 빌드 시점 고정 |
| SSR | 상대적으로 느림 | 항상 최신 |
| **ISR** | **빠름** | **주기적으로 최신화** |

블로그, 뉴스, 상품 페이지처럼 데이터가 자주 바뀌지만 실시간 최신성이 절대적으로 필요하지 않은 경우에 최적이다.

## How

### 기본 ISR (주기적 재생성)

```javascript
// pages/products.js
export async function getStaticProps() {
  const res = await fetch('https://api.example.com/products');
  const data = await res.json();

  return {
    props: { data },
    revalidate: 10, // 10초마다 백그라운드에서 재생성
  };
}
```

**동작 방식:**
1. 첫 요청 → 빌드 시 생성된 캐시 페이지 즉시 반환
2. `revalidate` 시간 경과 후 요청이 오면 → 캐시된 페이지 반환 + 백그라운드에서 새 페이지 생성
3. 재생성 완료 → 다음 요청부터 새 페이지 반환

### On-Demand ISR (즉시 재생성, Next.js 12.1+)

특정 이벤트(CMS 콘텐츠 발행, 데이터 업데이트 등)가 발생했을 때 즉시 재생성한다.

```javascript
// pages/api/revalidate.js
export default async function handler(req, res) {
  // 보안 토큰으로 무단 재생성 방지
  if (req.query.secret !== process.env.MY_SECRET_TOKEN) {
    return res.status(401).json({ message: 'Invalid token' });
  }

  try {
    // 재생성할 경로 지정
    await res.revalidate('/products');
    return res.json({ revalidated: true });
  } catch (err) {
    return res.status(500).send('Error revalidating');
  }
}
```

호출 예시:
```
POST /api/revalidate?secret=MY_SECRET_TOKEN
```

### ISR vs On-Demand ISR 비교

| 항목 | ISR | On-Demand ISR |
|------|-----|--------------|
| 재생성 트리거 | 시간 주기 | 외부 이벤트 |
| 최신성 보장 | 주기 내 지연 가능 | 즉시 반영 |
| 적합한 상황 | 주기적 업데이트 콘텐츠 | CMS, 웹훅 연동 |

## Pitfalls

- `revalidate: 0`은 **매 요청마다 재생성**을 의미하지 않음. SSR처럼 동작하려면 `getServerSideProps` 사용
- 재생성 중 에러 발생 시 **이전 캐시 페이지를 계속 서빙**함 (안정적이나 갱신 지연 발생)
- On-Demand ISR 보안 토큰은 반드시 환경 변수로 관리. 평문 하드코딩 금지
- Vercel 외 자체 호스팅 환경에서는 ISR을 위한 추가 서버 설정이 필요할 수 있음

## Related

- [[ssg-정적경로]]
- [[ssg-동적경로]]
- [[ssr-getServerSideProps]]
- [[page-router-장단점]]

## Sources

- [Next.js 공식 문서 - Incremental Static Regeneration](https://nextjs.org/docs/basic-features/data-fetching/incremental-static-regeneration)
- Notion: 사전렌더링 - ISR (Incremental Static Regeneration)
