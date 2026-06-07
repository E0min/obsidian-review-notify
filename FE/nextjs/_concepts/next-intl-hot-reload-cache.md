---
title: next-intl messages hot-reload 미작동 — .next 캐시 완전 삭제
aliases: [next-intl hot reload, MISSING_MESSAGE, turbopack cache, messages json reload]
type: concept
status: budding
created: 2026-05-04
updated: 2026-05-23
tags: [fe/nextjs, fe/perf, status/budding, career/fe, turbopack, i18n]
related:
  - "[[FE/nextjs/middleware-proxy/nextjs-16-middleware-to-proxy]]"
  - "[[FE/nextjs/_MOC]]"
source: ["INP-118 i18n 라벨 변경 후 raw key 노출"]
migrated-from: MindGraph-TIL/02-Problem-Solving/2026-05-04-next-intl-messages-hot-reload-cache.md
---

# next-intl messages hot-reload 미작동 — .next 캐시 완전 삭제

> TL;DR: `messages/{locale}.json` 변경이 Next.js 16 + Turbopack dev에서 HMR로 안 잡힘. 단순 dev 재시작 X, **`.next` 디렉토리 완전 삭제 후 재시작**으로 해결.

## What
`messages/en.json` 같은 i18n 메시지 파일에 새 키 추가 → UI에 `MISSING_MESSAGE: Could not resolve canvas.tagFilterModeAnd` raw 노출. JSON 자체는 정상 파싱되는데도 next-intl이 옛 messages를 캐시.

## Why it matters
- Turbopack module evaluation cache가 JSON import 결과까지 보존
- next-intl plugin이 빌드 타임에 messages를 evaluate → dev cache에 박힘
- 같은 패턴: dev 서버에서 JSON/YAML/CSV 데이터 파일 변경 후 raw key 노출 시 동일 처방

## How
```bash
# Bad — 단순 재시작 (여전히 MISSING_MESSAGE)
kill $(lsof -ti :3000)
npm run dev

# Good — .next 완전 삭제 후 재시작
kill $(lsof -ti :3000)
rm -rf .next          # 핵심
npm run dev
```

## 진단 순서
1. `node -e "require('./messages/en.json').canvas.tagFilterModeAnd"` — JSON syntax 정상 확인
2. namespace tree 위치 확인 (key 경로가 실제 JSON 구조와 일치)
3. dev 서버 로그에서 `MISSING_MESSAGE` 검색
4. `.next` 삭제 + 재시작

## Pitfalls
- `next dev --turbo` 일 때 더 잘 재현 — webpack 모드는 hot-reload 잡힐 수 있음
- `rm -rf .next/cache`만으로는 부족 — 디렉토리 전체 삭제 필요
- CI/배포 환경에서는 빌드마다 재생성이라 발생 안 함 — dev 한정 이슈

## Related
- [[FE/nextjs/middleware-proxy/nextjs-16-middleware-to-proxy]] — 같은 sprint
- [[FE/nextjs/_MOC]]
- [[FE/tooling/_MOC]] — Turbopack 캐시 일반론

## Sources
- INP-118 i18n 라벨 변경 후 raw key 노출 (mindgraph)
