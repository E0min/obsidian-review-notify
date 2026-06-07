---
title: React Server Components 주의사항
aliases: [RSC 주의사항, RSC pitfalls, 서버 컴포넌트 주의사항]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c50238380119f4ccf4b40b18618
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: React Server Components 주의사항"
---

# React Server Components 주의사항

> TL;DR: RSC는 브라우저 API 금지, 클라이언트 컴포넌트의 SSR 실행 이해, 컴포넌트 import 방향 제한, JSON 직렬화 가능한 props만 전달 — 이 4가지 규칙을 지켜야 런타임 오류를 피할 수 있다.

## What

RSC(React Server Components)를 사용할 때 흔히 오해하거나 실수하는 4가지 규칙. [[rsc-이해하기]]의 개념을 숙지한 뒤 실제 코드에 적용할 때 필요한 실전 제약 사항이다.

## Why it matters

RSC는 서버/클라이언트 경계가 코드 레벨에서 관리되기 때문에, 경계를 잘못 이해하면 `ReferenceError`, 클라이언트 번들 크기 폭증, 런타임 직렬화 에러 등이 발생한다. 오류 메시지만으로는 원인을 파악하기 어려운 경우가 많아 사전에 규칙을 익혀두는 것이 중요하다.

## How

### 규칙 1: 서버 컴포넌트에 브라우저 코드 사용 금지

`window`, `document`, `localStorage` 등은 브라우저 전용 API다. 서버 환경에는 존재하지 않으므로 서버 컴포넌트에서 사용하면 `ReferenceError`가 발생한다.

```javascript
// ❌ 서버 컴포넌트에서 브라우저 API 접근
export default function BadComponent() {
  const width = window.innerWidth; // ReferenceError: window is not defined
  return <div>{width}</div>;
}

// ✅ 클라이언트 컴포넌트로 이동
'use client';
import { useState, useEffect } from 'react';

export default function GoodComponent() {
  const [width, setWidth] = useState(0);
  useEffect(() => {
    setWidth(window.innerWidth);
  }, []);
  return <div>{width}</div>;
}
```

### 규칙 2: 클라이언트 컴포넌트도 서버에서 실행됨

`'use client'`는 "클라이언트에서도 실행된다"는 의미이지, "서버에서 실행 안 된다"는 의미가 아니다. 초기 페이지 로드 시 SSR(HTML 생성)을 위해 서버에서도 실행된다.

```
초기 접속 흐름:
1. 서버: 클라이언트 컴포넌트 SSR → HTML 생성
2. 클라이언트: 이미 렌더된 HTML을 Hydration → 인터랙션 가능
```

따라서 클라이언트 컴포넌트에서도 `window`를 조건 없이 쓰면 SSR 단계에서 오류가 난다.

```javascript
'use client';
import { useEffect, useState } from 'react';

export default function SafeClientComponent() {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    // useEffect는 클라이언트에서만 실행 → 브라우저 API 안전 사용 가능
    setMounted(true);
  }, []);

  if (!mounted) return null;
  return <div>{window.location.href}</div>;
}
```

### 규칙 3: 클라이언트 컴포넌트에서 서버 컴포넌트 import 불가

클라이언트 컴포넌트가 서버 컴포넌트를 import하면, 서버 컴포넌트가 클라이언트 번들로 끌려 들어가 서버 전용 코드(DB 쿼리 등)가 클라이언트에 노출된다.

```javascript
// ❌ 클라이언트 컴포넌트에서 서버 컴포넌트 직접 import
'use client';
import ServerComponent from './ServerComponent'; // 위험!

export default function ClientParent() {
  return <ServerComponent />;
}
```

```javascript
// ✅ 올바른 패턴: 서버 컴포넌트가 클라이언트 컴포넌트를 children으로 감싸기

// app/page.js (서버 컴포넌트)
import ClientWrapper from './ClientWrapper';
import ServerContent from './ServerContent';

export default function Page() {
  return (
    <ClientWrapper>
      <ServerContent /> {/* children prop으로 전달 */}
    </ClientWrapper>
  );
}
```

### 규칙 4: 서버 → 클라이언트 Props는 JSON 직렬화 가능한 타입만

서버 컴포넌트에서 클라이언트 컴포넌트로 props를 전달할 때, 데이터는 네트워크를 통해 **JSON 직렬화**되어 전달된다. 직렬화 불가능한 타입은 런타임 에러가 발생한다.

| 전달 가능 | 전달 불가 |
|----------|---------|
| `string`, `number`, `boolean` | 함수 (Function) |
| `array`, `plain object` | `Date` 객체 |
| `null`, `undefined` | 클래스 인스턴스 |
| `BigInt` | `Map`, `Set` |

```javascript
// ❌ 함수 전달 불가
export default function ServerPage() {
  const handleClick = () => console.log('클릭'); // 함수는 직렬화 불가
  return <ClientButton onClick={handleClick} />; // 에러
}

// ✅ 함수는 클라이언트 컴포넌트 내부에서 정의
'use client';
export default function ClientButton() {
  const handleClick = () => console.log('클릭'); // 클라이언트 내부에서 정의
  return <button onClick={handleClick}>클릭</button>;
}
```

```javascript
// ❌ Date 객체 직접 전달 불가
export default async function ServerPage() {
  const post = await fetchPost();
  return <ClientCard createdAt={post.createdAt} />; // Date 객체 → 에러
}

// ✅ ISO 문자열로 변환 후 전달, 클라이언트에서 복원
export default async function ServerPage() {
  const post = await fetchPost();
  return <ClientCard createdAt={post.createdAt.toISOString()} />; // string으로 변환
}

'use client';
export default function ClientCard({ createdAt }) {
  const date = new Date(createdAt); // 클라이언트에서 Date 복원
  return <span>{date.toLocaleDateString('ko-KR')}</span>;
}
```

## Pitfalls

- `'use client'`를 파일 최상단(import 전)에 써야 함 — 중간에 쓰면 무시됨
- 서버 컴포넌트에서 서버 전용 패키지(예: `fs`, `crypto`)는 사용 가능하지만, 해당 컴포넌트가 실수로 `'use client'`가 붙은 파일에서 import되면 번들에 포함되어 보안 문제 발생
- `Date` 직렬화 문제는 `superjson` 라이브러리로 우회 가능하지만, 공식 권장 방법은 ISO 문자열 변환

## Related

- [[rsc-이해하기]]
- [[app-router]]
- [[앱라우터-데이터페칭]]

## Sources

- Notion: React Server Components 주의사항
- [Next.js 공식 문서 - Passing data from Server to Client](https://nextjs.org/docs/app/building-your-application/rendering/composition-patterns#passing-props-from-server-to-client-components-serialization)
