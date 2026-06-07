---
title: 1인 + AI Swarm 워크플로우 실증 — 5가지 결함과 해법
aliases: [ai swarm 5 defects, claude code workflow incidents, sprint v1.9.3 retro]
type: concept
status: evergreen
created: 2026-05-04
updated: 2026-05-23
tags: [ai/agent-pattern, ai/claude-code, status/evergreen, career/ai-native, career/product-engineer, workflow, retro]
related:
  - "[[AI-Native/claude-code/hooks/linear-done-gate]]"
  - "[[AI-Native/claude-code/workflows/build-pr-block-backpropagation]]"
  - "[[AI-Native/agents/inp-tracker-followup-pattern]]"
  - "[[AI-Native/_concepts/5-layer-backpropagation]]"
  - "[[Blog/series/_MOC]]"
source: ["v1.9.3 sprint 실사용 중 발견 5가지 결함"]
migrated-from: MindGraph-TIL/01-Workflow-and-Harness/2026-05-04-ai-swarm-workflow-real-issues.md
---

# 1인 + AI Swarm 워크플로우 실증 — 5가지 결함과 해법

> TL;DR: 2주 전 Phase 3 시스템 설계를 완성 후 v1.9.3 sprint 실사용 중 발견한 5가지 결함의 패턴: AI 자동 Done, 인간 기준 capacity, 리뷰어 없는 폐쇄 루프, 학습 휘발, 스킬 파일 인플레이션. 공통 해법: **5층 역전파 + 기존 강화 우선** + Hook 강제.

## What
**합성 노트** — 5가지 결함은 각각 별 atomic으로 승격됨. 이 노트는 5가지를 한 흐름으로 묶는 retro 형식. 발행 시점 글이라 더 자세한 분해는 자식 atomic 참고.

## 5가지 결함 요약

| # | 결함 | 핵심 원인 | 해법 |
|---|------|-----------|------|
| 1 | AI가 Linear ticket 자동 Done 처리 | "Done"의 정의가 모호 — AC 충족 ≠ UX 검증 | [[AI-Native/claude-code/hooks/linear-done-gate]] |
| 2 | Sprint capacity가 인간(14h/주) 기준 | AI swarm은 시간 capacity 변수 없음, 병목은 사용자 검증 횟수 | priority-first + backlog-all SPRINT.md |
| 3 | 리뷰어 없는 폐쇄 루프 (생성=검증) | 같은 AI가 만들고 검증 → 편향/보안/성능 결함 | Worker-Reviewer 4축 ([[AI-Native/agents/_MOC]]) |
| 4 | 학습 휘발 — Vault 진입구 없음 | sprint 끝나면 인사이트 사라짐 | PostToolUse `vault-log-suggest.sh` 체크리스트 주입 |
| 5 | 스킬 파일 인플레이션 — 새 파일 욕망 | Phase 2의 22파일 폐기 재현 위험 | "기존 강화 우선" 원칙 (AND 3개 충족 시만 신규) |

## Why it matters
- "시스템은 만드는 게 아니라 쓰면서 완성된다" — 설계와 운용 사이의 간격이 항상 있다
- 5가지 결함의 공통 해법: **MEMORY → SKILL/Hook → Vault → Commit** 사이클
- 새 파일 추가 = 인지 부하 ↑ + 발견 비용 ↑ → 기존 강화가 1차 안

## How — 발견-박제-학습 사이클

```
사고 발생 (운용 중)
 → 원인 분석 + Why 정리
 → MEMORY 박제 (feedback_*.md)
 → 코드/설정 변경 (Hook / SKILL.md / CLAUDE.md)
 → Git commit 박제 (추적성)
 → Vault 기록 (블로그 발행 원천)
 → 재발 방지 테스트
```

박제의 3-tier:
1. **MEMORY** — 세션 간 지속 (15~20줄)
2. **CLAUDE.md / SKILL.md** — 에이전트 런타임 규칙
3. **Hooks (sh)** — 코드 레벨 강제 (`exit 2` 차단)

## Pitfalls
- 단일 layer 박제는 다음 세션에서 누락 가능
- 새 파일 추가의 신설 기준 3개 (AND): ①기존 어디에도 안 맞는 책임 ②월 3회+ 독립 호출 ③기존 추가 시 책임 모호
- AI swarm의 capacity는 시간 X, **사용자 검증 횟수**가 진짜 변수

## Related
- [[AI-Native/claude-code/hooks/linear-done-gate]] — 결함 1
- [[AI-Native/agents/inp-tracker-followup-pattern]] — 결함 1 + 4 일반화
- [[AI-Native/claude-code/workflows/build-pr-block-backpropagation]] — 같은 5층 패턴
- [[AI-Native/_concepts/5-layer-backpropagation]] — 메타 패턴
- [[Blog/published/2026-05-11-1인-개발-워크플로우-1편-context-오염과-22일-폐기]]
- [[Blog/published/2026-05-11-1인-개발-워크플로우-2편-frontmatter-hook-skill]]

## Sources
- v1.9.3 sprint 종료 직후 (2026-05-04)
- Commits: 743d01f, 0a7ee32, 3a543f1
