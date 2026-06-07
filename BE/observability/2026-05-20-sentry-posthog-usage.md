---
title: Sentry + PostHog 운영 가이드 (MindGraph)
aliases: [sentry posthog mindgraph, 에러 모니터링 운영]
type: concept
status: budding
created: 2026-05-20
updated: 2026-05-25
tags: [be/observability, project/mindgraph, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[sentry]]"
  - "[[../../Projects/mindgraph/_INDEX]]"
source: ["INP-156", "INP-157", "plan ga-posthog-greedy-crayon.md"]
migrated-from: "MindGraph-TIL/05-Ops-and-Maintenance/2026-05-20-sentry-posthog-usage.md"
---

# Sentry + PostHog 운영 가이드 — 왜 + 무엇 + 어떻게

## 왜 이 두 도구 (한 문단)

PostHog 하나로 행동 분석 + replay + flag + 에러까지 다 되지만 **각 도메인의 최고는 아님**. 에러 stack trace 깊이(source map, release tracking, breadcrumb)는 Sentry가 압도적이라 분리. 그 외(사용자 행동/funnel/retention/replay) 는 PostHog 올인원으로 묶음. GA4/Amplitude/Datadog RUM은 PostHog와 중복 또는 consent UI 강제 → 제외. Vercel Analytics는 이미 박제됐고 Web Vitals 보조라 유지.

## 역할 분리 — 무엇을 어디서 캡처하나

| 도구 | 무엇을 캡처 | 어디서 동작 | 키 |
|------|------------|------------|-----|
| **Sentry** | 예외 / stack trace / breadcrumb / release tracking | server + edge + client | `NEXT_PUBLIC_SENTRY_DSN`, `SENTRY_AUTH_TOKEN` |
| **PostHog SDK** | 사용자 행동 — `signin_success`, `node_created`, `topic_opened`, `$pageview` | client only | `NEXT_PUBLIC_POSTHOG_KEY` |
| **PostHog Logs (OTLP)** | 서버 console.log/info/warn/error → PostHog Live events Logs 탭 | server only (edge 미지원) | `NEXT_PUBLIC_POSTHOG_KEY` (Authorization Bearer) |
| **Vercel Analytics** | 트래픽 / Web Vitals | 기본 | 없음 (Vercel auto) |

### 중복 방지 박제 (반드시 켜둘 것)
- Sentry session replay = **OFF** (`replaysSessionSampleRate: 0`) — PostHog Replay가 담당
- PostHog exception capture = **OFF** (`capture_exceptions: false`) — Sentry가 담당
- Sentry tracing = **10%** (`tracesSampleRate: 0.1`) — quota 절약
- PostHog person profile = `identified_only` — 미신원 user 는 anonymous

---

## Sentry 사용법

### 1. 진입점 4파일 구조 (Next.js 16 표준)

```
instrumentation.ts              ← 모든 runtime register() 진입
├─ sentry.server.config.ts     ← NEXT_RUNTIME === 'nodejs' 일 때 import
├─ sentry.edge.config.ts       ← NEXT_RUNTIME === 'edge' 일 때 import
└─ instrumentation-client.ts   ← 브라우저 자동 실행 (sentry.client.config.ts 는 deprecated)
```

`next.config.ts`는 `withSentryConfig(withNextIntl(nextConfig), { tunnelRoute, sourcemaps, ... })` 로 래핑.

### 2. 에러 캡처는 단일 진입점 `lib/error-reporter.ts`
컴포넌트/이벤트 핸들러에서 `Sentry.captureException()` 직접 호출 금지. 모두 `reportError()` 경유:

```typescript
import { reportError } from '@/lib/error-reporter';
reportError({ message: err.message, stack: err.stack, source: 'manual', metadata: { nodeId } });
```

`reportError()` 내부에서:
1. fingerprint dedup (5초 윈도우, 100개 캐시) → 같은 에러 폭주 차단
2. Sentry forward (`captureException` + tags + extra)
3. `/api/error-log` 보조 송신 (Vercel function 로그 용도, 권위 source는 Sentry)

### 3. 글로벌 에러는 자동 캡처
- `app/global-error.tsx` — App Router 글로벌 에러 boundary → `reportError`
- `components/global/error-boundary-reporter.tsx` — `window.onerror` + `unhandledrejection` 리스너 → `reportError`
- 의도적 throw 테스트: 콘솔에서 `throw new Error("sentry test")` → Issues에 도달

### 4. Tunnel route — ad-blocker 우회
`tunnelRoute: "/sentry-tunnel"` 옵션 → 브라우저는 `*.sentry.io` 대신 1P 도메인 `/sentry-tunnel` 호출. Network 탭에서 직접 sentry.io 호출 0건이어야 정상.

### 5. Source map 업로드
`SENTRY_AUTH_TOKEN` 박제 시 `next build`가 자동으로 source map 업로드 → Issues 페이지에 원본 TypeScript stack 표시. 토큰 없으면 build skip (빌드 자체는 통과).

### 6. User identify — auth-context.tsx 박제 위치
```typescript
// supabase onAuthStateChange 콜백
if (event === 'SIGNED_IN' && s?.user) {
  Sentry.setUser({ id: s.user.id });
}
if (event === 'SIGNED_OUT') {
  Sentry.setUser(null);
}
```
이메일/이름은 보내지 말 것 — `sendDefaultPii: false` 유지.

---

## PostHog SDK (브라우저 행동 분석) 사용법

### 1. 단일 진입점 — `lib/analytics/posthog-client.ts`
`posthog-js` 직접 import 금지. 항상 래퍼 경유:

```typescript
import { track, identifyUser, resetUser } from '@/lib/analytics/posthog-client';
import { AnalyticsEvent } from '@/lib/analytics/events';
```

### 2. 타입 안전 이벤트 카탈로그 — `lib/analytics/events.ts`
이벤트 이름 문자열 직박제 금지. 항상 상수 import:

```typescript
export const AnalyticsEvent = {
  SIGNIN_SUCCESS: 'signin_success',
  SIGNOUT_SUCCESS: 'signout_success',
  NODE_CREATED: 'node_created',
  TOPIC_OPENED: 'topic_opened',
} as const;
```

각 이벤트의 권장 properties는 `AnalyticsEventProps` 인터페이스에 박제 → 오타/누락 시 컴파일 에러.

### 3. 호출 지점 3곳

```typescript
// 1) 노드 생성 — lib/storage/cached-cloud-repository/node-create.ts
track(AnalyticsEvent.NODE_CREATED, {
  node_type: 'page',
  depth: childNode.depth,
  is_root: false,
  has_source: Boolean(source),
});

// 2) 캔버스 진입 — app/[locale]/canvas/[topicId]/page.tsx
useEffect(() => {
  track(AnalyticsEvent.TOPIC_OPENED, { topic_id: topicId });
}, [topicId]);

// 3) 로그인 — lib/supabase/auth-context.tsx (onAuthStateChange)
track(AnalyticsEvent.SIGNIN_SUCCESS, { provider: 'email' });
```

### 4. identify / reset — Supabase 이벤트와 동기
```typescript
if (event === 'SIGNED_IN' && s?.user) identifyUser(s.user.id);
if (event === 'SIGNED_OUT')           resetUser();
if (event === 'TOKEN_REFRESHED' && s?.user) identifyUser(s.user.id);
```
- `identify` 호출 시 이전 anonymous distinct_id 가 user.id 로 alias → 가입 전 행동 보존
- `reset` 호출 시 다음 이벤트부터 새 anonymous id

### 5. Provider 위치 — providers.tsx 안쪽
```
ThemeProvider
└─ AuthProvider                ← user.id 가 여기서 잡힘
   └─ PostHogProvider           ← AuthProvider 안쪽 (identify 가능)
      └─ StorageProvider
         └─ AuthGuard → children
```

### 6. cookieless 모드
`cookieless_mode: 'on_reject'` + `person_profiles: 'identified_only'` → consent UI 없이도 PIPA/GDPR 안전. 익명 트래픽은 server-side hash 로 추적 (cookie 미사용).

### 7. Reverse proxy — `/ingest` 경로
`next.config.ts` rewrites: `/ingest/:path*` → `us.i.posthog.com`. Network 탭에서 직접 posthog.com 호출 0건. ad-blocker 우회 + Safari 3rd-party cookie 차단 회피.

---

## PostHog Logs (OpenTelemetry, 서버 로그) 사용법

### 1. server-only — 클라이언트 사용 금지
`lib/analytics/posthog-logger.ts` 는 `import 'server-only'` 박제. API route / server action / instrumentation 진입점에서만 사용.

```typescript
import { logInfo, logWarn, logError } from '@/lib/analytics/posthog-logger';

logInfo('embedding queue tick', { batchSize: 32, pending: 5 });
logWarn('rate limit close', { remaining: 12 });
logError('embedding API failed', { nodeId, err: err.message });
```

### 2. 자동 init — instrumentation.ts
`NEXT_RUNTIME === 'nodejs'` + `NEXT_PUBLIC_POSTHOG_KEY` 박제 시 `posthog.server.config.ts` 자동 import → OTLP exporter + LoggerProvider 초기화 + 전역 박제 (`logs.setGlobalLoggerProvider`).

### 3. 어디서 보이나
PostHog dashboard → Activity → Logs 탭. service.name `mindgraph` + Vercel commit SHA(`service.version`) 로 필터.

### 4. PII 정책 (필수 준수)
- 사용자 콘텐츠 (노드 본문, 답변 텍스트) 절대 body/attributes에 넣지 말 것
- userId 만 안전 (Sentry/PostHog SDK와 일관)
- 비밀번호/토큰 절대 X

### 5. edge runtime 미지원
OTLP HTTP exporter는 node:fetch 의존 → edge function에서 logger 호출 시 no-op. edge 에러는 Sentry가 담당.

---

## 환경변수 (.env.local)

```bash
# Sentry (DE 리전)
NEXT_PUBLIC_SENTRY_DSN=https://...@o....ingest.de.sentry.io/...
SENTRY_ORG=c22824800e5c
SENTRY_PROJECT=mindgraph
SENTRY_AUTH_TOKEN=...  # 비면 source map skip, 런타임 캡처는 정상

# PostHog (US 리전)
NEXT_PUBLIC_POSTHOG_KEY=phc_...     # phc_ = Project API Key (SDK용)
NEXT_PUBLIC_POSTHOG_HOST=/ingest    # next.config.ts rewrites 경유
POSTHOG_LOGS_ENDPOINT=https://us.i.posthog.com/otlp/v1/logs
```

### 키 종류 구분
- `phc_...` Project API Key — SDK 이벤트 전송 + OTLP Bearer 양쪽 사용
- `phx_...` Personal API Key — MCP server 인증 (`.env.local` 아닌 `claude mcp add` 헤더로 박제)
- `NEXT_PUBLIC_` prefix = 브라우저 노출 OK (의도된 공개 키만)
- prefix 없으면 server-only

---

## 검증 체크리스트

### Sentry
- [ ] 콘솔에서 `throw new Error("test")` → Issues 페이지에 도달 + source map 적용된 stack
- [ ] Network 탭에 `/sentry-tunnel` 경유 (직접 `*.sentry.io` 0건)
- [ ] `npm run build` 시 source map 업로드 로그 (SENTRY_AUTH_TOKEN 박제 시)
- [ ] 로그인/로그아웃 → Issue 의 user 정보가 user.id 로만 박제 (이메일 없음)

### PostHog SDK
- [ ] 로그아웃 상태 홈 진입 → Live Events `$pageview` (anonymous distinct_id)
- [ ] 로그인 → `signin_success` + 같은 세션이 user.id 로 identify
- [ ] 노드 생성 → `node_created` + props (`depth`, `is_root`, `has_source`)
- [ ] 캔버스 진입 → `topic_opened` + `topic_id`
- [ ] 로그아웃 → `signout_success` + 다음 이벤트가 새 anonymous id
- [ ] Network 탭에 `/ingest/e/` 경유 (직접 posthog.com 0건)

### PostHog Logs
- [ ] API route 에서 `logInfo('hello')` 호출 → PostHog Activity → Logs 탭에 도달
- [ ] service.name = `mindgraph`, service.version = commit SHA 로 필터링 가능

---

## 관련 노트
- Linear INP-156 (Sentry) · INP-157 (PostHog)
- `~/.claude/plans/ga-posthog-greedy-crayon.md` — 선정 근거 + GA4/Datadog/Amplitude 제외 사유
- `~/.claude/projects/.../memory/feedback_linear_done_user_gate.md` — Sentry issue link = 시각 검증 evidence
