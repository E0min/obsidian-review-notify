---
title: AI agent 이슈 추적기 운영 — 후속 자동 흡수 + 5층 역전파
aliases: [INP reuse default, ticket reuse, auto-absorb followup, tracker inflation]
type: concept
status: evergreen
created: 2026-05-04
updated: 2026-05-23
tags: [ai/agent-pattern, ai/claude-code, status/evergreen, career/ai-native, career/product-engineer, workflow]
related:
  - "[[AI-Native/claude-code/hooks/linear-done-gate]]"
  - "[[AI-Native/claude-code/workflows/build-pr-block-backpropagation]]"
  - "[[AI-Native/agents/inp-hierarchy-skip-pattern]]"
  - "[[AI-Native/_concepts/5-layer-backpropagation]]"
source: ["INP-120 → INP-107 흡수 사용자 피드백 + 5층 역전파 박제"]
migrated-from: MindGraph-TIL/01-Workflow-and-Harness/2026-05-04-ai-agent-inp-tracker-followup-pattern.md
---

# AI agent 이슈 추적기 운영 — 후속 자동 흡수 + 5층 역전파

> TL;DR: AI가 검증 발견 결함마다 신규 ticket 발급하면 트래커 인플레이션. **후속/보강 = 기존 ticket 코멘트 + commit `(refs INP-NN)`** 가 default. 단순 memory 박제는 자주 누락 → Hook + CLAUDE.md 이중 안전망 필수.

## What
AI agent가 외부 시스템(Linear/JIRA/GitHub Issues)에 쓰기 권한을 가질 때 발견 결함마다 신규 ticket 발급하는 행동은 **트래커 인플레이션 + 추적성 분산**을 낳는다. 후속 자동 흡수 패턴을 5층 역전파로 강제.

## Why it matters
- AI 자동 발급은 sprint 회계 왜곡 (같은 도메인이 N개 ticket으로 분산)
- "후속은 기존 ticket" 정책은 memory 박제만으론 자주 누락 — 다음 세션에서 AI가 능동 참조 안 함
- 일반화: 외부 쓰기 권한 가진 agent에 항상 적용

## How — 5단계 운영 절차

| 단계 | 동작 | 도구 |
|------|------|------|
| 1. 결함 보고 수신 | 결함/보강 키워드 + ticket 명시 여부 분석 | UserPromptSubmit hook |
| 2. 기존 ticket 식별 | 명시 → 그대로 / 모호 → `git log -5` grep `(refs INP-NN)` → 사용자 1줄 확인 | `AskUserQuestion` |
| 3. 코멘트로 scope 박제 | 기존 ticket에 가설/수정 방향 코멘트 | `mcp__linear__linear_createComment` |
| 4. worker 위임 | "INP-XX 후속" 명시 + commit footer `(refs INP-XX)` 강제 | `Agent(run_in_background=true)` |
| 5. 사용자 검증 → Done | one-shot marker 우회 → updateIssue | [[AI-Native/claude-code/hooks/linear-done-gate]] |

## How — 5층 역전파 매핑

| 레이어 | 위치 | 강제력 |
|--------|------|--------|
| 1. Conversation | 대화 turn | 약(휘발) |
| 2. Memory | `memory/feedback_inp_reuse_default.md` | 중(다음 세션 자동 로드) |
| 3. CLAUDE.md / SKILL.md | `.claude/CLAUDE.md §14` + `sprint/SKILL.md step3` | 강(system prompt 상시) |
| 4. Hook | `.claude/hooks/inp-reuse-suggest.sh` UserPromptSubmit | 강(stderr 자동 주입) |
| 5. Skill | `/sprint build` 안에 흐름 박제 | 중(사용자 호출 시) |

## How — Hook 예시
```bash
# .claude/hooks/inp-reuse-suggest.sh
DEFECT_KEYWORDS='에러|버그|결함|문제|이상|안[[:space:]]*됨|풀림|stale|회귀'
if echo "$PROMPT" | grep -qE 'INP[-]?[0-9]+'; then exit 0; fi
if ! echo "$PROMPT" | grep -qE "$DEFECT_KEYWORDS"; then exit 0; fi

RECENT_INPS=$(git log -5 --pretty=%B | grep -oE '\(refs INP-[0-9]+\)' | sort -u)
[[ -z "$RECENT_INPS" ]] && exit 0

cat >&2 <<EOF
[INP-REUSE-SUGGEST] 결함 키워드 감지 + ticket 명시 X.
최근 commits: ${RECENT_INPS}
판단: 같은 도메인 → 기존 ticket 코멘트 / 모호 → 사용자 확인
EOF
```

## Pitfalls
- memory만 박제하면 다음 세션에서 AI가 자체 권장 흐름으로 또 신규 발급
- Hook의 stderr 메시지는 **차단 X, 컨텍스트 주입만** — AI 무시 불가 + 융통성 보존
- 5층 역전파는 다른 정책(Done 차단, vault 기록, build PR 차단)에도 동일 적용

## Related
- [[AI-Native/claude-code/hooks/linear-done-gate]] — 같은 5층 패턴 (one-shot marker)
- [[AI-Native/claude-code/workflows/build-pr-block-backpropagation]] — 가장 정교한 5층 예
- [[AI-Native/agents/inp-hierarchy-skip-pattern]] — cross-INP 의존성 패턴
- [[AI-Native/_concepts/5-layer-backpropagation]] — 일반화 패턴

## Sources
- INP-120 archive + 후속 흡수 사용자 피드백
