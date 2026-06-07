---
title: Vercel React Best Practices 기반 리팩토링 포인트
aliases: [vercel react guide, react best practices, components/graph audit]
type: concept
status: budding
created: 2026-04-24
updated: 2026-05-23
tags: [fe/react, fe/perf, status/budding, career/fe, performance, refactoring]
related:
  - "[[FE/performance/bundling/lucide-react-direct-import]]"
  - "[[FE/react/compiler/memo-불필요]]"
  - "[[FE/browser/passive-event-listener]]"
  - "[[FE/react/_MOC]]"
source: ["Vercel React Best Practices v1.0.0"]
migrated-from: MindGraph-TIL/02-Problem-Solving/2026-04-24-vercel-react-best-practices-리팩토링-포인트.md
---

# Vercel React Best Practices 기반 리팩토링 포인트

> TL;DR: MindLink `components/graph/`(~7,000줄)를 Vercel React Best Practices 40+ 규칙으로 감사한 결과 8 카테고리 23+ 개선점 발견. 핵심: 번들 다이어트, passive listener, Map/Set 자료구조.

## What
Vercel이 정리한 React 모범사례 가이드의 핵심 항목을 실제 코드베이스에 적용한 감사 보고서. CRITICAL/HIGH/MEDIUM 우선순위로 분류.

## Why it matters
- Next.js 환경에서 가장 신뢰성 있는 React 규칙 모음
- 단일 atomic이 너무 커서 항목별로 [[FE/performance/bundling/lucide-react-direct-import]] / [[FE/browser/passive-event-listener]] / [[FE/react/compiler/memo-불필요]]로 분할 승격됨

## How

### CRITICAL — 번들 사이즈
1. **lucide-react barrel import** (5+ 곳) — `import { X } from 'lucide-react'`이 1,583 모듈 로드, 콜드 스타트 200-800ms 지연. 자세히: [[FE/performance/bundling/lucide-react-direct-import]]
2. **MarkdownEditor 직접 import** — Tiptap 에디터 lazy-load 안 됨. dynamic import + Suspense로.

### HIGH — 이벤트 리스너
3. **mousemove에 `{ passive: true }` 누락** (5 곳) — 드래그 성능. 자세히: [[FE/browser/passive-event-listener]]

### MEDIUM — 데이터 구조
4. **반복 `.find()` 호출** — `treeNodes` 8+ 곳 O(n). `Map`으로 O(1).
5. **`.includes()` 대신 `Set`** — 태그 필터링 O(n²) → O(1).
6. **`.sort()` 대신 `.toSorted()`** (4 곳) — 배열 뮤테이션 위험.

### MEDIUM — Derived state
7. **`useState + useEffect`로 파생 상태 동기화** → `useMemo` 또는 render 중 계산.

### LOW — Type safety / Lint
- 매직 넘버 상수화
- ESLint `react-compiler` 룰셋 활성화

## 코드 예시

```ts
// Before — barrel import (CRITICAL)
import { Link, Trash2, Plus } from 'lucide-react';

// After — direct import
import Link from 'lucide-react/dist/esm/icons/link';

// Before — repeated .find() O(n)
const target = treeNodes.find(tn => tn.node.id === nodeId);

// After — Map O(1)
const nodeMap = new Map(treeNodes.map(tn => [tn.node.id, tn]));
const target = nodeMap.get(nodeId);

// Before — derived state
const [highlightIds, setHighlightIds] = useState<string[]>([]);
useEffect(() => {
  setHighlightIds(results.map(r => r.node.id));
}, [results]);

// After — computed during render
const highlightIds = useMemo(() => results.map(r => r.node.id), [results]);
```

## Pitfalls
- React Compiler 활성 시 수동 memo는 대부분 불필요 — [[FE/react/compiler/memo-불필요]]
- `useMemo`로 referential equality 잡아도 **로직 비용(compute(data))** 은 데이터 구조로 풀어야

## Related
- [[FE/performance/bundling/lucide-react-direct-import]] — 승격된 자식
- [[FE/browser/passive-event-listener]] — 승격된 자식
- [[FE/react/compiler/memo-불필요]] — 승격된 자식
- [[Projects/mindgraph/_INDEX]] — 적용 대상 프로젝트

## Sources
- Vercel React Best Practices v1.0.0
