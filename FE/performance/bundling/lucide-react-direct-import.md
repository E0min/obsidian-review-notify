---
title: lucide-react direct import (번들 다이어트)
aliases: [lucide barrel import, optimizePackageImports, icon library tree-shaking]
type: concept
status: budding
created: 2026-04-24
updated: 2026-05-23
tags: [fe/perf, fe/react, status/budding, career/fe, performance]
related:
  - "[[FE/react/_concepts/vercel-react-best-practices]]"
  - "[[FE/performance/_MOC]]"
  - "[[../core-web-vitals/웹-성능-측정]]"
source: []
migrated-from: MindGraph-TIL/02-Problem-Solving/2026-04-24-lucide-react-direct-import.md
---

# lucide-react direct import (번들 다이어트)

> TL;DR: barrel import `import { X } from 'lucide-react'`는 1,583 모듈을 로드해 콜드 스타트 200-800ms 추가. direct import 또는 `optimizePackageImports`로 해결.

## What
`lucide-react`처럼 큰 아이콘 라이브러리에서 barrel 패턴으로 import하면 트리쉐이킹이 충분히 안 돼 dev/prod 양쪽에서 콜드 스타트가 느려진다.

## Why it matters
- 콜드 스타트 200-800ms 단축 (페이지 첫 진입 LCP 직접 영향)
- dev 서버 HMR 속도 향상
- Vercel React Best Practices CRITICAL 항목

## How
```ts
// Bad
import { Link, Trash2, Plus } from 'lucide-react';

// Good (direct path)
import Link from 'lucide-react/dist/esm/icons/link';
import Trash2 from 'lucide-react/dist/esm/icons/trash-2';

// Better (Next.js 자동 최적화)
// next.config.ts
export default {
  experimental: {
    optimizePackageImports: ['lucide-react'],
  },
};
```

## Pitfalls
- `optimizePackageImports`는 Next.js 13.5+ 필요
- direct path는 라이브러리 내부 구조에 결합 — 메이저 버전 업 시 경로 깨질 수 있음 → `optimizePackageImports` 우선
- 적용 후 cold start 측정 (`next build && next start --profile`)으로 검증

## Related
- [[FE/react/_concepts/vercel-react-best-practices]] — 원천 가이드
- [[FE/performance/bundling/_MOC]]
- [[FE/performance/core-web-vitals/_MOC]] — LCP 개선 효과

## Sources
- Vercel React Best Practices v1.0.0
