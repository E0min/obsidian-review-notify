---
date: 2026-05-20
project: MindGraph
category: 도입기/Observability
tags: [draft, observability, sentry, posthog, opentelemetry, decision-log, 1-dev-swarm]
status: draft
target: Velog 발행 후보
source: "INP-156 · INP-157 · commit a5b7dd6"
---

# 1인 개발자가 관측성 스택 5개 중 2개만 고른 이유 — Sentry + PostHog

> 출시 직전, "GA / PostHog / Amplitude / Sentry / Datadog RUM 다 깔면 뭔가 잘 보이겠지" 라는 유혹을 이기고 **2개만** 골랐다. 어떻게 좁혔고, 어떻게 박제했는지 기록.

## 0. 문제 — 출시 전인데 보이는 게 없다

MindGraph 는 AI 답변을 그래프로 모으는 Chrome Extension + Next.js 웹앱이다. 출시 직전 상태였다. 그런데 다음 sprint 우선순위를 정하려고 "사용자가 어디서 막히지?" 묻는 순간 깨달았다 — **답할 데이터가 없다**. Vercel Analytics 의 트래픽 숫자만 보이고, funnel/이탈/에러 stack 은 전혀 측정 안 되고 있었다.

그래서 관측성 스택을 박제하기로 했다. 처음 떠올린 후보:

- **GA4** — 마케팅 표준
- **PostHog** — funnel/retention/replay/flag 올인원
- **Amplitude** — 고전 제품 분석
- **Sentry** — 에러 stack 의 표준
- **Datadog RUM** — 백엔드 APM 과 통합

다 깔면 뭔가 잘 보일 것 같았다. 그게 함정이었다.

## 1. "다 깔자" 가 함정인 이유 — 중복 도메인

각 도구를 카테고리로 매핑해 보면:

| 도구 | 트래픽 | Funnel | 에러 | RUM | Replay | Flag |
|------|:---:|:---:|:---:|:---:|:---:|:---:|
| Vercel Analytics | ◎ | × | × | △ | × | × |
| GA4 | ◎ | △ | × | × | × | × |
| PostHog | ○ | ◎ | ○ | × | ◎ | ◎ |
| Amplitude | △ | ◎ | × | × | △ | ○ |
| Sentry | × | × | ◎ | △ | ○ | △ |
| Datadog RUM | △ | × | ○ | ◎ | ○ | × |

5개를 다 깔면:
- **트래픽** 을 3개 도구 (Vercel + GA4 + PostHog) 가 동시에 측정 → 숫자 불일치 → 의사결정 혼란
- **제품 분석** 을 PostHog + Amplitude 둘 다 → 100% 중복
- **에러** 를 Sentry + PostHog + Datadog 셋이 동시에 → 어디서 봐야 진실?
- **Session Replay** 를 3개 도구가 동시에 → 데이터 분산

월 비용도 비용이지만, **"어느 숫자가 진실인지" 매번 디버깅** 해야 하는 인지 비용이 더 컸다. 1인 + AI swarm 으로 sprint 돌리는 환경에선 이 인지 비용이 sprint 안정성을 무너뜨린다.

## 2. 결정 기준 5개 — 가장 압축된 형태

후보들을 거를 때 실제로 작동한 질문 5개:

1. **Cookie consent UI 를 이번 sprint 에 만들 거냐?**
   → 아니라면 GA/Amplitude/Datadog 모두 탈락. 셋 다 cookie consent 강제다.
2. **Google Ads 캠페인 집행 중이냐?**
   → 아니라면 GA4 의 attribution 가치 = 0. 마케팅 시작 시점에 도입 트리거로 박제만.
3. **유료 결제 미루고 싶냐?**
   → Datadog RUM 은 첫날부터 카드. 나머지는 무료 시작.
4. **백엔드 모니터링을 Datadog 으로 통일할 계획이냐?**
   → 아니라면 Datadog RUM 의 시너지 = 0. ROI 음수.
5. **셀프호스트 옵션이 미래에 필요할 가능성?**
   → PostHog + Sentry 만 가능. 나머지는 SaaS lock-in.

내 경우 1~5 모두 "지금은 아님" → **PostHog + Sentry** 로 좁혀졌다.

## 3. 왜 둘 다 — 한 도구로 안 되나?

PostHog 만 깔면 funnel + replay + flag + 에러까지 다 된다. 한 stack 으로 끝나면 다이어트 원칙에 가장 부합한다.

근데 **각 도메인의 최고가 PostHog 인 건 아니다.** 특히 에러 stack 추적은:
- source map 적용된 원본 TypeScript stack
- release 단위 회귀 추적 (어느 commit 에서 회귀 들어왔나)
- breadcrumb (에러 직전 사용자 행동 시퀀스)

Sentry 가 압도적이다. PostHog 의 exception tracking 은 "있긴 한데 깊지 않다" 수준.

그래서 **깊이 필요한 도메인은 분리(Sentry), 나머지는 올인원(PostHog) 으로 묶기** — 이 패턴이 다이어트 + 깊이 둘 다 잡는 방법이라는 결론.

## 4. 박제할 때 가장 중요했던 패턴 — 중복 OFF 옵션

두 도구를 다 깔면 자동으로 중복 영역이 생긴다:
- Sentry 도 session replay 됨 (`replaysSessionSampleRate`)
- PostHog 도 exception 캡처됨 (`capture_exceptions`)

이걸 **명시적으로 OFF** 하지 않으면 어느 날 청구서가 비싸진다.

```typescript
// sentry — session replay 끔 (PostHog Replay 가 담당)
Sentry.init({
  replaysSessionSampleRate: 0,
  replaysOnErrorSampleRate: 1.0,  // 에러 시점만 캡처
  tracesSampleRate: 0.1,           // 초기 10% 만
});

// posthog — exception 끔 (Sentry 가 담당)
posthog.init(key, {
  capture_exceptions: false,
  cookieless_mode: 'on_reject',    // consent UI 없이 안전
  person_profiles: 'identified_only',
});
```

이 4줄이 없으면 같은 영역을 2개 도구가 동시에 측정하다가 **숫자 불일치 + 비용 폭증** 한다.

## 5. 단일 진입점 박제 — 컴포넌트가 SDK 를 직접 import 하지 않음

PostHog SDK 를 컴포넌트에서 직접 import 하면:
1. 테스트할 때 mock 어려움
2. 이벤트 이름 문자열 오타 → 컴파일 통과 → PostHog dashboard 에서 분실
3. 나중에 SDK 교체 시 전체 코드 grep

그래서 단일 진입점 + 타입 안전 이벤트 카탈로그:

```typescript
// lib/analytics/events.ts — 이벤트 이름 상수
export const AnalyticsEvent = {
  SIGNIN_SUCCESS: 'signin_success',
  NODE_CREATED: 'node_created',
  TOPIC_OPENED: 'topic_opened',
} as const;

// lib/analytics/posthog-client.ts — 래퍼
export function track<E extends AnalyticsEventName>(
  event: E,
  properties?: AnalyticsEventProps[E],
): void { ... }

// 컴포넌트에서 — SDK 직접 import 금지
import { track } from '@/lib/analytics/posthog-client';
import { AnalyticsEvent } from '@/lib/analytics/events';
track(AnalyticsEvent.NODE_CREATED, { node_type: 'page', depth: 1, is_root: false });
```

`AnalyticsEventProps` 인터페이스가 각 이벤트의 권장 properties 타입을 강제 → 오타/누락 시 컴파일 에러.

에러 리포팅도 같은 패턴 — `lib/error-reporter.ts` 의 `reportError()` 가 fingerprint dedup + Sentry forward 단일 진입점. `Sentry.captureException` 을 컴포넌트에서 직접 호출하지 않는다.

## 6. 환경변수 가드 — 빌드는 항상 통과해야 함

dev/PR preview/CI 환경에서 키가 없을 수 있다. 그래도 빌드가 깨지면 안 된다.

```typescript
// instrumentation.ts
if (process.env.NEXT_PUBLIC_SENTRY_DSN) {
  await import('./sentry.server.config');
}
if (process.env.NEXT_PUBLIC_POSTHOG_KEY) {
  await import('./posthog.server.config');
}

// posthog-client.ts
const key = process.env.NEXT_PUBLIC_POSTHOG_KEY;
if (!key) return null;  // SDK init 자체를 skip
```

이 패턴 덕에 production 키 없이 PR preview 가 돌아간다. + 의도치 않은 production 누수도 차단.

## 7. "지금 안 함" 을 영구가 아니라 트리거로 박제

GA4 / Amplitude / Datadog 을 **영구 제외**로 두면 6개월 뒤 "왜 안 깔았지?" 라는 자문이 다시 든다. 그래서 *조건부 도입 트리거* 로 박제:

```markdown
## B 조합 승급 트리거 (GA4 + Consent UI 도입 시점)
- [ ] Google Ads 캠페인 집행 시작
- [ ] 유료 사용자 100명 돌파 또는 EU 트래픽 10% 초과 (GDPR 강제)
- [ ] SEO 트래픽이 의미 있는 채널이 됨
- [ ] Product Hunt / 외부 launch 1주일 전
```

미래의 나(또는 다른 협업자) 가 같은 질문을 다시 던질 때, 답이 이미 박제되어 있다. **"왜 안 깔았지?" → "이 트리거 4개 중 충족된 게 있나? 없으면 그대로."** 의사결정 비용을 1번 치르고 끝.

## 8. 일반화 — 도구 선택 의사결정의 6가지 원칙

이번 결정을 회고하며 일반화한 패턴:

1. **올인원 vs 도메인 분리** — 깊이 필요한 도메인만 분리, 나머지는 묶기.
2. **Consent UI 비용은 도구 선택의 1순위 제약** — cookie 기반 도구는 모두 banner UI 작업 1주 추가.
3. **중복 도메인 = anti-pattern** — 명시적 OFF 옵션 박제로 차단.
4. **"지금 안 함" 을 트리거로 박제** — 영구 제외보다 조건부 도입 트리거.
5. **환경변수 가드 = 빌드 안전** — 키 없이도 빌드/dev 가 돌아야 함.
6. **단일 진입점 + 타입 안전 카탈로그** — 컴포넌트가 SDK 를 직접 import 하지 않음.

## 9. 결과 — 무엇이 보이게 됐나

박제 끝:
- **Sentry**: 콘솔에서 의도적 throw → Issue 도달 + 원본 TypeScript stack + breadcrumb
- **PostHog**: 로그인/노드 생성/캔버스 진입 모두 Live events 도달 + Supabase user.id 로 identify
- **PostHog Logs (OpenTelemetry)**: 서버 console.log → PostHog Activity Logs 탭

이제 다음 sprint 우선순위를 데이터로 정할 수 있다. *어디서 이탈하는지 보이고, 어떤 에러가 가장 자주 터지는지 보인다.*

## 10. 비용 — 무료 시작점 박제

| 도구 | Free tier | 유료 진입점 |
|------|----------|------------|
| Vercel Analytics | 무한(Hobby) | Pro 부터 |
| Sentry | 5K errors/월 | 5K 초과 시 |
| PostHog | 1M events/월 + 1M replay min/월 | 1M 초과 시 |

지금 MindGraph 트래픽으론 한참 무료. 트래픽 늘면 sprint 단위로 quota 모니터링.

---

## 마무리

처음에 "관측성 풀세트 깔자" 라고 생각했을 때 들어간 비용 추정:
- 도구 5개 학습 + 통합 = 2 sprint
- Consent UI = 1 sprint
- 월 비용 = $200+ (Datadog 만으로도)
- 숫자 불일치 디버깅 = 매 sprint 1-2 시간

실제 박제한 비용:
- 도구 2개 통합 = 1 sprint
- 월 비용 = $0 (무료 tier)
- 의사결정 비용 = 1회 박제 (Plan + Vault note)

**"무엇을 안 깔 것인가" 가 도구 선택의 절반.** 1인 + AI swarm 환경에선 더 그렇다.

---

## 발행 전 체크리스트

- [ ] 코드 예시 4개 검증 (실제 박제된 코드와 1:1 매칭)
- [ ] 비용 추정치 출처 박제 (Sentry/PostHog free tier 공식 페이지)
- [ ] PostHog Logs (OpenTelemetry) 섹션을 별 글로 분리할지 결정 — 너무 깊으면 2편으로
- [ ] 제목 후보 검토:
  - 현재: "1인 개발자가 관측성 스택 5개 중 2개만 고른 이유"
  - 대안 A: "관측성 풀세트가 함정인 이유 — Sentry + PostHog 만 고른 1인 개발자의 선택"
  - 대안 B: "다 깔지 마라 — 1인 개발자의 관측성 스택 다이어트"
- [ ] 옵시디언 → Velog 발행 가능 형식으로 다듬기 (코드 블록 syntax highlight 등)

## 관련 노트
- `~/Obsidian/MindGraph-TIL/05-Ops-and-Maintenance/2026-05-20-sentry-posthog-usage.md` — 사용법 가이드 (참조용)
- `~/.claude/plans/ga-posthog-greedy-crayon.md` — 의사결정 플랜 원본
- Linear INP-156 (Sentry) · INP-157 (PostHog)
- commit a5b7dd6 (main 머지)
