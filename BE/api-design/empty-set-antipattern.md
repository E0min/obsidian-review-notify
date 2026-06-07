---
title: 빈 Set의 의미 분기 안티패턴 — "필터 미적용" vs "필터 활성 + 매치 0"
aliases: [empty set antipattern, empty collection ambiguity, filter zero match]
type: concept
status: budding
created: 2026-05-04
updated: 2026-05-23
tags: [be/api, fe/react, status/budding, career/fdd, career/product-engineer, antipattern]
related:
  - "[[FE/d3-visualization/_concepts/opacity-ssot-pattern]]"
  - "[[AI-Native/claude-code/hooks/linear-done-gate]]"
  - "[[BE/api-design/_MOC]]"
source: ["INP-118 매치 0개 fallback 버그"]
migrated-from: MindGraph-TIL/02-Problem-Solving/2026-05-04-empty-set-api-antipattern.md
---

# 빈 Set의 의미 분기 안티패턴

> TL;DR: 컬렉션 API에서 `size === 0`이 "필터 미적용"인지 "필터 활성 + 매치 0"인지 단일 시그니처로 표현 불가. 별도 `mode` 또는 `hasFilter` 플래그로 의도를 명시.

## What
`setHighlightedNodes(ids: Set<string>)` 같은 API가 빈 컬렉션을 받으면 두 가지 의미가 모두 자연스럽다:
1. **필터 미적용** → 전체 활성 복원
2. **필터 활성 + 매치 0** → 모두 dim (결과 없음 시각화)

단일 매개변수가 두 의미를 표현 못 하면 사용자 의도와 정반대 결과가 나간다. 가장 흔한 패턴: `if (ids.size > 0) dim(); else restoreAll();` → 매치 0 시 자동 fallback으로 필터가 안 먹은 것처럼 보임.

## Why it matters
- 컬렉션 size로 의도를 추론하면 **Empty / None / All-Filtered**가 한 동작에 묶임
- API 계약이 호출자 의도를 잃어버림 → 디버깅 시 "필터 코드는 맞는데 안 먹어요" 미스리딩
- 같은 안티패턴: GraphQL `null` vs `undefined` vs `[]`, REST `404` vs `200 + []`

## How

```ts
// Bad — 빈 Set이 fallback 으로 해석됨
setHighlightedNodes(ids: Set<string>) {
  const hasHighlight = ids.size > 0;
  nodeSel.attr('opacity', d =>
    !hasHighlight ? 1 : (ids.has(d.id) ? 1 : 0.12)
  );
}
// 사용자: AND 필터 매치 0 → 빈 ids → 전체 활성. "필터가 안 먹는다"

// Good — 호출자가 의도를 명시
setHighlightedNodes(ids: Set<string>, hasFilter?: boolean) {
  const filterActive = hasFilter ?? (ids.size > 0);
  if (!filterActive) { nodeSel.attr('opacity', 1); return; }
  if (filterActive && ids.size === 0) {
    nodeSel.attr('opacity', 0.12);  // 매치 0 → 모두 dim
    return;
  }
  nodeSel.attr('opacity', d => ids.has(d.id) ? 1 : 0.12);
}

// Alt — mode enum으로 분기
setHighlightDim(activeIds: Set<string>, duration: number, mode?: 'restore' | 'dim-all')
```

## Pitfalls
- `Set | null`로 풀려는 시도는 또 다른 모호함 (`null` = 미적용? 미정의?)
- mode enum이 많아지면 readonly union으로 묶어 타입 검사 강제
- HTTP 404 vs 200+[] 도 같은 패턴 — "리소스 없음" vs "필터 결과 없음"

## Related
- [[FE/d3-visualization/_concepts/opacity-ssot-pattern]] — 같은 sprint에서 발견한 자매 패턴
- [[BE/api-design/_MOC]]
- [[AI-Native/claude-code/hooks/linear-done-gate]] — 같은 cycle 작업

## Sources
- INP-118 매치 0개 fallback 버그 (mindgraph)
