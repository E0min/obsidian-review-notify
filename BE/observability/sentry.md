---
title: Sentry — 에러 모니터링
aliases: [Sentry, 센트리, error monitoring, exception tracking, DSN, breadcrumb, fingerprint]
type: concept
status: budding
created: 2026-05-25
updated: 2026-05-25
tags: [be/observability, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[2026-05-20-sentry-posthog-usage]]"
  - "[[../../Projects/에러-이슈-기록]]"
source: ["MindGraph 운영 경험", "Sentry 공식 문서"]
migrated-from: ""
---

# Sentry — 에러 모니터링

> TL;DR: Sentry는 프로덕션 에러를 자동 캡처·그룹화·알림하는 에러 모니터링 플랫폼. DSN으로 연결하면 unhandled exception을 즉시 수집하고, source map으로 원본 TypeScript stack trace를 표시한다.

---

## What

개발 환경에서 재현되지 않는 프로덕션 에러를 **자동으로 캡처**하고, 발생 빈도·영향 유저 수·stack trace·breadcrumb을 통합해 원인 파악을 돕는 도구.

**핵심 가치**: "서버 로그만으로는 못 찾는 에러"를 찾아준다 — 특히 클라이언트 사이드 에러, 엣지 케이스 에러, 특정 브라우저/OS 에러.

---

## 핵심 개념

### DSN (Data Source Name)

```
https://<public_key>@<host>/sentry.io/<project_id>
예: https://abc123@o12345.ingest.sentry.io/67890
```

프로젝트별 고유 주소. SDK가 이 주소로 이벤트를 전송. `.env`에 박제, 브라우저 노출 OK (공개 키).

### Event vs Issue

| 개념 | 설명 |
|------|------|
| **Event** | 에러 1건 발생 = 이벤트 1개 |
| **Issue** | 같은 에러의 그룹 (fingerprint 기반 자동 묶음) |
| **Occurrence** | Issue 안의 이벤트 수 |

### Fingerprint (지문)

같은 에러끼리 자동 그룹화하는 기준. 기본은 stack trace + 에러 메시지. 커스터마이징 가능:

```javascript
Sentry.captureException(err, {
  fingerprint: ['database-timeout', err.code], // 직접 지정
});
```

### Breadcrumb (빵 부스러기)

에러 직전 사용자 행동 로그. SDK가 자동으로 수집:
- XHR/fetch 요청 (`url`, `status_code`)
- Console.log 호출
- UI 클릭/네비게이션
- 직접 추가: `Sentry.addBreadcrumb({ category: 'auth', message: 'login' })`

---

## SDK 초기화 — Next.js App Router

### 필수 4파일 구조

```
instrumentation.ts              ← 모든 runtime register() 진입점
├─ sentry.server.config.ts     ← Node.js runtime
├─ sentry.edge.config.ts       ← Edge runtime
└─ instrumentation-client.ts   ← 브라우저 (deprecated: sentry.client.config.ts)
```

```typescript
// sentry.server.config.ts
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  environment: process.env.NODE_ENV,          // production / development
  tracesSampleRate: 0.1,                      // 성능 트레이싱 10% — quota 절약
  sendDefaultPii: false,                      // 이메일/IP 자동 전송 차단
});
```

```typescript
// instrumentation-client.ts (브라우저)
import * as Sentry from '@sentry/nextjs';

Sentry.init({
  dsn: process.env.NEXT_PUBLIC_SENTRY_DSN,
  replaysSessionSampleRate: 0,    // Session Replay OFF (PostHog가 담당)
  replaysOnErrorSampleRate: 0,
  tracesSampleRate: 0.1,
});
```

```typescript
// next.config.ts
import { withSentryConfig } from '@sentry/nextjs';

export default withSentryConfig(nextConfig, {
  tunnelRoute: '/sentry-tunnel',              // ad-blocker 우회 (중요)
  sourcemaps: {
    disable: false,                           // source map 업로드 활성화
  },
  hideSourceMaps: true,                       // 프로덕션에서 .map 파일 숨김
});
```

---

## 에러 캡처 방법

### 1. 자동 캡처 (권장)

SDK가 자동으로 처리:
- `window.onerror` / `unhandledrejection`
- Next.js App Router `global-error.tsx`
- Server Component throw

```typescript
// app/global-error.tsx — App Router 전체 에러 경계
'use client';
import * as Sentry from '@sentry/nextjs';
import NextError from 'next/error';
import { useEffect } from 'react';

export default function GlobalError({ error }: { error: Error }) {
  useEffect(() => {
    Sentry.captureException(error);
  }, [error]);
  return <NextError statusCode={0} />;
}
```

### 2. 수동 캡처 — 단일 진입점 패턴

컴포넌트에서 `Sentry.captureException()` 직접 호출 **금지**. 래퍼 함수 경유:

```typescript
// lib/error-reporter.ts
import * as Sentry from '@sentry/nextjs';

const recentErrors = new Map<string, number>(); // dedup 캐시

export function reportError({
  message, stack, source, metadata,
}: {
  message: string;
  stack?: string;
  source: 'manual' | 'boundary' | 'global';
  metadata?: Record<string, unknown>;
}) {
  // 5초 윈도우 내 같은 에러 dedup
  const key = `${message}:${source}`;
  const last = recentErrors.get(key) ?? 0;
  if (Date.now() - last < 5000) return;
  recentErrors.set(key, Date.now());

  const err = new Error(message);
  err.stack = stack;

  Sentry.captureException(err, {
    tags: { source },
    extra: metadata,
  });
}
```

### 3. 사용자 식별 연동

```typescript
// Supabase onAuthStateChange 콜백
if (event === 'SIGNED_IN' && session?.user) {
  Sentry.setUser({ id: session.user.id }); // ID만 — 이메일/이름 X
}
if (event === 'SIGNED_OUT') {
  Sentry.setUser(null);
}
```

---

## Source Map — TypeScript stack 표시

빌드 시 `.map` 파일을 Sentry 서버에 업로드 → Issues 페이지에 원본 TS 파일명·라인 표시 (minified 코드 아님).

```bash
# 환경변수 박제 시 next build가 자동 업로드
SENTRY_AUTH_TOKEN=sntrys_...  # 개인 키 (커밋 금지)
SENTRY_ORG=your-org
SENTRY_PROJECT=your-project
```

`SENTRY_AUTH_TOKEN` 없으면 source map 업로드만 skip, 런타임 에러 캡처는 정상 동작.

---

## Tunnel Route — ad-blocker 우회

```
브라우저 → /sentry-tunnel (1P 도메인) → Sentry 서버
```

`tunnelRoute: '/sentry-tunnel'` 설정 시 브라우저가 `*.sentry.io` 직접 호출 대신 자사 도메인 경유. Network 탭에서 `sentry.io` 직접 요청 0건이어야 정상.

---

## Release & Environment

```typescript
Sentry.init({
  release: process.env.NEXT_PUBLIC_VERCEL_GIT_COMMIT_SHA, // 커밋 SHA
  environment: process.env.NEXT_PUBLIC_VERCEL_ENV,         // production / preview
});
```

- **Release**: 어느 배포에서 발생한 에러인지 추적. "이번 배포 이후 새로 생긴 에러" 필터 가능
- **Environment**: production/staging/preview 분리 — 개발 중 에러 노이즈 차단

---

## Alerts 설정 (권장)

Sentry 대시보드 > Alerts > Create Alert Rule:

```
조건: event.unhandled = true AND times_seen ≥ 5 (5분 안에)
액션: 이메일/Slack/PagerDuty
```

첫 발생 즉시 알림보다 **임계값 기반 알림**이 알림 피로 방지에 효과적.

---

## 성능 모니터링 (tracing)

```typescript
// API route에서 수동 트랜잭션
import * as Sentry from '@sentry/nextjs';

const transaction = Sentry.startTransaction({
  name: 'process-user-data',
  op: 'task',
});
// ... 작업 수행
transaction.finish();
```

`tracesSampleRate: 1.0`이면 100% 추적 → 프로덕션에서 0.1~0.2 권장 (비용).

---

## 검증 체크리스트

```
□ throw new Error("sentry test") → Issues 페이지 도달 확인
□ Network 탭에서 /sentry-tunnel 경유 (직접 *.sentry.io 0건)
□ npm run build → source map 업로드 로그 확인
□ 로그인 후 Issue 페이지에서 user.id 박제 확인 (이메일 없음)
□ Environment 필터로 production/preview 분리 확인
```

---

## Pitfalls

- **`sendDefaultPii: true` 설정**: 이메일·IP가 Sentry 서버에 저장 → GDPR/PIPA 위반 가능
- **Session Replay + PostHog 중복**: `replaysSessionSampleRate: 0` 미설정 시 비용 2배
- **fingerprint 미설정으로 과다 그룹화**: 동적 URL이 포함된 에러 메시지는 수천 개 별개 Issue로 분리 → fingerprint 직접 지정 필요
- **`captureException` 직접 호출 분산**: 로직 중복 + dedup 불가 → 단일 `reportError` 래퍼 패턴 필수
- **SENTRY_AUTH_TOKEN 커밋**: source map에 원본 코드 경로가 포함되므로 `.env.local`에만 보관

---

## Related

- [[2026-05-20-sentry-posthog-usage]] — MindGraph 프로젝트 Sentry + PostHog 실전 운영 가이드
- [[../../Projects/에러-이슈-기록]] — 에러 기록 워크플로

## Sources

- [Sentry Next.js SDK 공식](https://docs.sentry.io/platforms/javascript/guides/nextjs/)
- [Sentry 성능 모니터링](https://docs.sentry.io/product/performance/)
- [Source Maps 설정](https://docs.sentry.io/platforms/javascript/sourcemaps/)
