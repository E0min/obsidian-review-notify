---
title: Next.js 16 — middleware.ts → proxy.ts rename
aliases: [next 16 proxy, middleware deprecated, proxy.ts, NotAllowedRootHTTPFallbackError]
type: concept
status: budding
created: 2026-05-03
updated: 2026-05-23
tags: [fe/nextjs, status/budding, career/fe, breaking-change, next-intl]
related:
  - "[[FE/nextjs/_concepts/next-intl-hot-reload-cache]]"
  - "[[AI-Native/claude-code/_MOC]]"
  - "[[FE/nextjs/_MOC]]"
source: ["v1.9.3 sprint dev 서버 띄우기 작업"]
migrated-from: MindGraph-TIL/02-Problem-Solving/2026-05-03-nextjs-16-middleware-to-proxy.md
---

# Next.js 16 — middleware.ts → proxy.ts rename

> TL;DR: Next.js 16에서 `middleware.ts`는 deprecated. `proxy.ts`로 파일명·export 함수명 둘 다 `proxy`. 학습 cutoff 이전 가이드대로 middleware.ts 만들면 `Both middleware and proxy detected` 충돌.

## What
Next.js 16에서 라우팅 전 가로채기 hook이 `middleware` → `proxy`로 rename됐다. 파일명도 `proxy.ts`, default export 또는 named export `proxy` 함수.

## Why it matters
- **AI 어시스턴트 학습 cutoff 함정**: Next.js 16은 2025+ 출시 — 대부분 LLM이 모름. 자동완성/제안이 outdated
- 기존 `proxy.ts` 있는데 LLM이 `middleware.ts` 새로 만들면 충돌 → 404 + `NotAllowedRootHTTPFallbackError`
- 다른 Next.js 16 breaking 변경(App Router/Server Actions/캐싱)의 단서

## How

### Before (Next.js 15 — 더 이상 동작 안 함)
```ts
// middleware.ts
import createMiddleware from 'next-intl/middleware';
import { routing } from './i18n/routing';

export default createMiddleware(routing);

export const config = {
  matcher: ['/((?!api|_next|_vercel|.*\\..*).*)'],
};
```

### After (Next.js 16 — 표준)
```ts
// proxy.ts (파일명 + export 함수명 둘 다 'proxy')
import createMiddleware from 'next-intl/middleware';
import { routing } from '@/i18n/routing';
import { updateSession } from '@/lib/supabase/middleware';
import { type NextRequest } from 'next/server';

const intlMiddleware = createMiddleware(routing);

export async function proxy(request: NextRequest) {
  // Supabase 세션 갱신 + intl 라우팅
}
```

## Pitfalls
- LLM 자동완성은 `middleware.ts`를 만들려 함 — 작업 시 `node_modules/next/package.json`의 `version` 먼저 확인
- 두 파일 동시 존재하면 dev 서버가 unhandledRejection으로 죽음
- `app/`, `pages/`, `middleware.ts`, `proxy.ts` 동시 존재 여부 grep 필수
- "404 + NotAllowedRootHTTPFallbackError"를 i18n middleware 부재로 오진하지 말 것

## 진단 체크리스트
1. `cat node_modules/next/package.json | jq .version`
2. `ls app/ pages/ middleware.ts proxy.ts 2>/dev/null`
3. dev 서버 출력의 `unhandledRejection` 메시지
4. 학습 데이터 기준 코드 작성 전 `node_modules/next/dist/docs/` README 확인

## Related
- [[FE/nextjs/_concepts/next-intl-hot-reload-cache]] — 같은 sprint에서 발견
- [[FE/nextjs/middleware-proxy/_MOC]]
- [[AI-Native/claude-code/_MOC]] — AGENTS.md "This is NOT the Next.js you know" 가드 패턴

## Sources
- `node_modules/next/dist/docs/` (Next.js 16 official)
- v1.9.3 sprint plan / dev 서버 트러블슈팅
