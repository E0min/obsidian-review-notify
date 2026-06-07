---
title: Pre-fetching
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c5023838052b3f7f7e8f374d127
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: Pre-fetching"
---

# Pre-fetching

> TL;DR: 사용자가 이동하기 전에 다음 페이지 리소스를 미리 로드하는 기법으로, `<Link>`는 기본 활성화, `router.push`는 수동 구현이 필요하다.

## What

Pre-fetching(프리페칭)이란 사용자가 **아직 이동하지 않은 페이지의 JS 번들을 미리 다운로드**하는 기법이다. 링크를 클릭하는 순간 이미 리소스가 준비되어 있어 페이지 전환이 즉각적으로 느껴진다.

## Why it matters

Next.js는 페이지별 코드 스플리팅을 적용해 현재 페이지에 필요한 JS만 로드한다. 덕분에 초기 로딩은 빠르지만, 다음 페이지로 이동 시 번들을 새로 받아야 한다. 프리페칭은 이 지연을 숨기는 전략이다.

## How

### `<Link>` 컴포넌트 — 기본 프리페칭 활성화

뷰포트 안에 `<Link>`가 들어오면 자동으로 해당 페이지 번들을 프리페칭한다.

```javascript
import Link from 'next/link';

// 기본: 프리페칭 활성화
<Link href="/about">About</Link>

// 프리페칭 비활성화 (성능이 낮은 환경, 유료 데이터 고려)
<Link href="/about" prefetch={false}>About</Link>
```

---

### `useRouter` — 수동 프리페칭

`router.push`는 기본 프리페칭이 없다. 필요한 경우 `router.prefetch()`를 직접 호출한다.

```javascript
import { useRouter } from 'next/router';
import { useEffect } from 'react';

export default function Page() {
  const router = useRouter();

  // 컴포넌트 마운트 시 다음 페이지 미리 로드
  useEffect(() => {
    router.prefetch('/next-page');
  }, [router]);

  const handleClick = () => {
    router.push('/next-page'); // 이미 프리페치된 번들 사용
  };

  return <button onClick={handleClick}>다음 페이지</button>;
}
```

---

### 동작 방식 요약

| 방법 | 기본 프리페칭 | 수동 제어 |
|------|-------------|---------|
| `<Link href="...">` | 자동 (뷰포트 진입 시) | `prefetch={false}` |
| `router.push()` | 없음 | `router.prefetch()` 필요 |

## Pitfalls

- **개발 모드(`next dev`)에서는 프리페칭이 작동하지 않는다.** 반드시 프로덕션 빌드(`next build && next start`) 또는 `next build` 후 확인
- `prefetch={false}`를 남용하면 페이지 전환이 느껴질 수 있음 — 실제 데이터 사용량 문제가 있는 경우에만 비활성화
- 프리페칭은 사용자 인터넷 연결이 `save-data` 모드이거나 느린 경우 자동으로 비활성화됨 (브라우저가 판단)
- `router.prefetch()`는 클라이언트 컴포넌트에서만 사용 가능

## Related

- [[page-router-네비게이팅]]
- [[page-router]]
- [[nextjs란]]

## Sources

- Notion: Pre-fetching
- [Next.js 공식 문서 - Prefetching](https://nextjs.org/docs/pages/building-your-application/routing/linking-and-navigating#prefetching)
