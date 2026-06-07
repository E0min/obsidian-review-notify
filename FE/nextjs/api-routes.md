---
title: API Routes
aliases: []
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, status/budding]
notion-url: https://www.notion.so/18135c50238380ab80d8eab5debaab7b
related:
  - "[[_MOC]]"
source: ["Notion: Next.js"]
migrated-from: "Notion: API Routes"
---

# API Routes

> TL;DR: `pages/api/` 폴더에 파일을 만들면 별도 서버 없이 Next.js 앱 안에서 백엔드 API 엔드포인트를 구성할 수 있다.

## What

Next.js의 API Routes는 `pages/api/` 디렉토리에 파일을 생성하는 것만으로 **서버 사이드 API 엔드포인트**가 자동 생성되는 기능이다. Express 같은 별도 서버 없이 동일한 Next.js 앱에서 API를 제공할 수 있다.

## Why it matters

프론트엔드와 API 서버를 별도로 운영하지 않아도 되므로 소규모 프로젝트나 BFF(Backend For Frontend) 패턴 구현에 적합하다. 클라이언트 번들에 포함되지 않으므로 서버 전용 로직(DB 접근, 시크릿 키 사용)을 안전하게 처리할 수 있다.

## How

### 기본 구조

```javascript
// pages/api/time.ts
import type { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const date = new Date();
  res.json({ time: date.toLocaleString() });
}
```

접근 URL: `/api/time`

---

### HTTP 메서드 분기

`req.method`로 GET / POST / PUT / DELETE를 구분한다.

```typescript
// pages/api/posts.ts
import type { NextApiRequest, NextApiResponse } from "next";

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  switch (req.method) {
    case "GET":
      // 데이터 조회
      res.status(200).json({ posts: [] });
      break;

    case "POST":
      // 데이터 생성
      const body = req.body; // 요청 본문
      res.status(201).json({ created: true, data: body });
      break;

    case "DELETE":
      res.status(200).json({ deleted: true });
      break;

    default:
      // 허용하지 않는 메서드
      res.setHeader("Allow", ["GET", "POST", "DELETE"]);
      res.status(405).end(`Method ${req.method} Not Allowed`);
  }
}
```

---

### 쿼리 파라미터 처리

```typescript
// pages/api/search.ts
// 요청: GET /api/search?keyword=nextjs

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { keyword } = req.query; // 쿼리 파라미터 추출
  res.json({ results: `"${keyword}" 검색 결과` });
}
```

---

### 동적 API 라우트

```typescript
// pages/api/posts/[id].ts
// 요청: GET /api/posts/123

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { id } = req.query;
  res.json({ post: { id, title: `포스트 ${id}` } });
}
```

---

### 미들웨어 수동 추가

Next.js API Routes는 Express 미들웨어를 기본 지원하지 않으므로 직접 래핑한다.

```typescript
// utils/middleware.ts — 미들웨어 헬퍼 예시
import type { NextApiRequest, NextApiResponse } from "next";
import type { NextHandler } from "next-connect";

export function authMiddleware(
  req: NextApiRequest,
  res: NextApiResponse,
  next: NextHandler
) {
  const token = req.headers.authorization;
  if (!token) {
    return res.status(401).json({ error: "Unauthorized" });
  }
  next();
}
```

## Pitfalls

- API Routes 파일은 **클라이언트 번들에 포함되지 않음** — DB 연결 정보나 시크릿 키를 직접 사용해도 노출되지 않음
- `req.body`를 사용하려면 요청의 `Content-Type`이 `application/json`이어야 하며, Next.js는 자동으로 파싱함
- 파일 업로드 등 커스텀 body 파싱이 필요한 경우 기본 파서를 비활성화해야 함:
  ```typescript
  export const config = {
    api: {
      bodyParser: false,
    },
  };
  ```
- App Router에서는 `pages/api/` 대신 `app/api/route.ts` (Route Handlers) 방식 사용
- CORS 처리는 수동으로 헤더를 설정해야 함

## Related

- [[page-router]]
- [[nextjs-시작하기]]
- [[라우팅-설정하기]]

## Sources

- Notion: API Routes
- [Next.js 공식 문서 - API Routes](https://nextjs.org/docs/pages/building-your-application/routing/api-routes)
