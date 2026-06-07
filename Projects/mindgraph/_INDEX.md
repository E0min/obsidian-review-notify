---
type: project-index
status: active
created: 2026-05-23
last-touched: 2026-05-23
repo: ~/깃허브/mindgraph
tags: [project/mindgraph, status/active]
---

# mindgraph

> AI 지식 그래프 시각화 — Next.js 16 + D3 force simulation + Supabase + Chrome Extension.
> 직무 포폴 핵심 프로젝트 (FE / Product Engineer / AI-Native Builder 모두에 어필).

## Status
- 활성 sprint: INP-140 시리즈 (INP-145/146 완료)
- 최근 결정: [[decisions/002-opacity-ssot-pattern]]
- 다음 액션: Week 3+ — sprint 회고 + 다음 시리즈 plan

## Map
- [[architecture]] — 시스템 구조 + 데이터 흐름
- [[Projects/mindgraph/links-to-code]] — `~/깃허브/mindgraph` 핵심 파일 포인터
- [[roadmap]] — 마일스톤
- [[decisions/_MOC]] — ADR 모음
- [[retro/_MOC]] — sprint 회고
- [[learnings/_MOC]] — atomic 학습 (재사용 가능하면 FE/_concepts로 승격)

## 최근 ADR
- [[decisions/001-fx-fy-dual-semantics]] — fx/fy 의미 분리 (INP-145)
- [[decisions/002-opacity-ssot-pattern]] — opacity SSOT 통합 (INP-116/118)

## 학습 → 카테고리 승격 (이미 승격된 atomic)
- [[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]]
- [[FE/d3-visualization/force-simulation/fx-fy-alpha-mechanism]]
- [[FE/d3-visualization/_concepts/opacity-ssot-pattern]]
- [[FE/d3-visualization/_concepts/d3-zoom-state-machine]]
- [[FE/d3-visualization/_concepts/d3-react-hover-stale]]
- [[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]]
- [[FE/d3-visualization/canvas-svg/canvas-meta-restore-viewmode]]
- [[FE/react/_concepts/vercel-react-best-practices]]
- [[FE/nextjs/middleware-proxy/nextjs-16-middleware-to-proxy]]
- [[FE/nextjs/_concepts/next-intl-hot-reload-cache]]

## 외부 링크
- 깃허브: https://github.com/(user)/mindgraph
- Linear: INP 프로젝트
- 배포: (TBD)

## 직무 어필 포인트
- **FE**: D3 + React + Next.js 16 통합, INP 최적화 (chunk runner), state machine 설계
- **Product Engineer**: opacity SSOT 같은 근본 해결 vs patch 누적 의사결정
- **AI-Native Builder**: Claude Code + Codex 페어 프로그래밍 워크플로 ([[AI-Native/tools/codex/pair-programming-root-fix]])
