---
title: 5층 역전파 패턴 — AI 워크플로 규칙의 강제력 격차 메우기
aliases: [5 layer backprop, hook conversation memory CLAUDE skill, enforce hierarchy]
type: concept
status: evergreen
created: 2026-05-23
updated: 2026-05-23
tags: [ai/agent-pattern, ai/claude-code, status/evergreen, career/ai-native, career/product-engineer, meta-pattern]
related:
  - "[[AI-Native/claude-code/hooks/linear-done-gate]]"
  - "[[AI-Native/claude-code/workflows/build-pr-block-backpropagation]]"
  - "[[AI-Native/agents/inp-tracker-followup-pattern]]"
  - "[[AI-Native/agents/swarm-workflow-real-issues]]"
source: ["MindGraph v1.9.3 / v2.0 sprint 인시던트 패턴 종합"]
---

# 5층 역전파 패턴 — AI 워크플로 규칙의 강제력 격차 메우기

> TL;DR: AI agent에 단일 layer 박제(특히 memory)는 다음 세션에서 누락 가능. **L1 대화 + L2 memory + L3 CLAUDE/RULES + L4 SKILL + L5 Hook**의 5층 동시 박제로 강제력 격차를 메우는 메타 패턴. 적용 사례: Linear Done, build PR, INP reuse, vault log.

## What
AI agent가 규칙을 어기는 케이스의 공통 원인 = **단일 layer 강제력 부족**. 5층 동시 박제로 안전망 구축.

## Why it matters
- memory(L2)만 박제 = "AI가 능동 참조한다" 가정에 의존 → 가정 깨지면 누락 재발
- L5 Hook은 다른 4층의 모든 누락을 잡는 안전망 — OS 레벨 거부는 AI 판단과 무관
- 적용 가능 액션: 되돌리기 비용 큰 모든 자동화 (배포, 머지, 외부 알림, 자동 발급)

## How — 5층 매핑

| 층 | 위치 | 강제력 | 역할 | 예시 |
|----|------|--------|------|------|
| L1 | Conversation | 약 (휘발) | 인시던트 즉시 정정 | "PR 아니라 직접 머지" |
| L2 | `memory/feedback_*.md` | 중 (참조 의존) | 다음 세션 컨텍스트 | `feedback_pr_only_for_ship.md` |
| L3 | CLAUDE.md / RULES | 중-강 (spec-gate) | 정책 권위 | `GIT_CONVENTIONS §1.7` |
| L4 | SKILL.md (Anti-patterns) | 강 (실행 흐름) | 단계마다 강제 | `/sprint build` step3 |
| L5 | `.claude/hooks/*.sh` `exit 2` | 최강 (OS 거부) | AI 위반 명령 시 차단 | `build-pr-block.sh` |

## 적용 사례

| 케이스 | L4 SKILL | L5 Hook | Hook 종류 |
|--------|----------|---------|-----------|
| Linear Done 자동화 | `/sprint qa` | `linear-done-gate.sh` | PreToolUse (`exit 2`) |
| 워커→트렁크 PR | `/sprint build` step3 | `build-pr-block.sh` | PreToolUse (`exit 2`) |
| INP 무분별 발급 | (없음) | `inp-reuse-suggest.sh` | UserPromptSubmit (stderr 주입, 차단 X) |
| Vault 기록 누락 | (없음) | `vault-log-suggest.sh` | PostToolUse (Bash, stderr 주입) |

## Hook 종류 선택 가이드

- **PreToolUse + `exit 2`** = 되돌리기 비용 큰 액션 (배포/머지/Done/자동 발급) — 차단
- **UserPromptSubmit + stderr** = 사용자 메시지 패턴 감지 (결함 키워드) — 컨텍스트 주입
- **PostToolUse + stderr** = commit/build 같은 결과 이벤트 — 체크리스트 자동 출현
- **융통성 보존** = 우회 경로 2종 (env var bulk + one-shot marker)

## Pitfalls
- L5만 박제 = "왜 차단되지?" 사용자 인지 X → L2/L3에도 박제 필수
- 우회 경로 없는 L5 = 정당한 케이스도 막힘 → env var + marker 2종 권장
- L4 강제력 과대평가 — SKILL.md는 `/sprint` 호출 시만 발동, 항상 보지 않음

## Related
- [[AI-Native/claude-code/hooks/linear-done-gate]] — one-shot marker + bulk env
- [[AI-Native/claude-code/workflows/build-pr-block-backpropagation]] — 가장 정교한 5층
- [[AI-Native/agents/inp-tracker-followup-pattern]] — UserPromptSubmit hook 변형
- [[AI-Native/agents/swarm-workflow-real-issues]] — 5층 패턴 도출 원천

## Sources
- v1.9.3 / v2.0 sprint 인시던트 (linear-done, build-pr 정정)
- 합성 노트 — atomic들에서 추출한 메타 패턴
