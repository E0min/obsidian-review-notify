---
title: Linear Done 자동 차단 hook — one-shot marker + env var 우회
aliases: [linear done gate, ticket auto-done block, pre-tool-use exit 2, one-shot approval]
type: concept
status: evergreen
created: 2026-05-04
updated: 2026-05-23
tags: [ai/claude-code, ai/agent-pattern, status/evergreen, career/ai-native, hook, workflow]
related:
  - "[[AI-Native/agents/swarm-workflow-real-issues]]"
  - "[[AI-Native/agents/inp-tracker-followup-pattern]]"
  - "[[AI-Native/_concepts/5-layer-backpropagation]]"
  - "[[AI-Native/claude-code/workflows/build-pr-block-backpropagation]]"
source: ["v1.9.3 sprint — AI 자동 Done 전환 사고 방지"]
migrated-from: MindGraph-TIL/01-Workflow-and-Harness/2026-05-04-linear-done-gate-hook-pattern.md
---

# Linear Done 자동 차단 hook — one-shot marker + env var 우회

> TL;DR: AI가 ticket을 자동으로 Done 처리하면 잘못된 "출시 가능" 신호. PreToolUse(`mcp__linear__linear_updateIssue`) hook으로 `exit 2` 차단. 우회: ①one-shot marker(다음 1회만) ②`LINEAR_DONE_GATE=off`(bulk).

## What
PreToolUse hook이 `mcp__linear__linear_updateIssue` 호출의 `stateId`를 검사. Done state ID와 일치하면 `exit 2`로 도구 호출 거부. 사용자 명시 승인은 marker 또는 env var로.

## Why it matters
- AI 자체 검증으로 Done 처리 = "AC 충족 ≠ UX 검증" 함정 (모바일, 디자인, 성능 회귀 못 잡음)
- "되돌리기 비용 큰 액션"(배포/머지/외부 알림)에 적용 가능한 일반 패턴
- 5층 역전파의 레벨 4 (Hook = constraint layer) 실 사례

## How
```bash
#!/bin/bash
# .claude/hooks/linear-done-gate.sh — PreToolUse
set -e

# bulk 우회
if [[ "${LINEAR_DONE_GATE:-enforce}" == "off" ]]; then exit 0; fi

# one-shot marker (사용 후 자동 삭제)
APPROVAL_MARKER="/tmp/claude-linear-done-approved"
if [[ -f "$APPROVAL_MARKER" ]]; then
  rm -f "$APPROVAL_MARKER"
  exit 0
fi

INPUT="$(cat 2>/dev/null || true)"
TOOL_NAME=$(echo "$INPUT" | jq -r '.tool_name // empty')
STATE_ID=$(echo "$INPUT" | jq -r '.tool_input.stateId // empty')
DONE_STATE_ID="aaa781b7-..."  # Linear team Done state

if [[ "$TOOL_NAME" == "mcp__linear__linear_updateIssue" ]] \
   && [[ "$STATE_ID" == "$DONE_STATE_ID" ]]; then
  echo "[BLOCKED] Done 전환 차단 — 사용자 시각 검증 게이트" >&2
  echo "필수: localhost:3000 시각 검증 후 'touch /tmp/claude-linear-done-approved'" >&2
  exit 2
fi
exit 0
```

`.claude/settings.json`:
```json
{
  "hooks": {
    "PreToolUse": [{
      "matcher": "mcp__linear__linear_updateIssue",
      "hooks": [{ "type": "command", "command": "bash .claude/hooks/linear-done-gate.sh" }]
    }]
  }
}
```

## 3가지 통행 경로

1. **기본 차단** (`exit 2`) — AI Done 호출 자동 거부
2. **one-shot 승인** — `touch /tmp/claude-linear-done-approved` → 다음 1회만 통과 → 자동 삭제
3. **bulk 우회** — `LINEAR_DONE_GATE=off` (chore/docs/ops 다수)

## Pitfalls
- Done state ID는 Linear team마다 다름 — 사전 조회 후 박제
- env var는 부주의 방지를 위해 명시적 설정만
- one-shot이 env보다 좁은 권한 — 가능하면 one-shot 우선
- 같은 패턴이 적용 가능한 케이스: 자동 commit, vault 자동 저장, INP 자동 발급

## Related
- [[AI-Native/agents/swarm-workflow-real-issues]] — 결함 1
- [[AI-Native/agents/inp-tracker-followup-pattern]] — 같은 5층 패턴
- [[AI-Native/claude-code/workflows/build-pr-block-backpropagation]] — 더 정교한 5층
- [[AI-Native/_concepts/5-layer-backpropagation]]

## Sources
- v1.9.3 sprint commit 743d01f
- Memory: `feedback_linear_done_user_gate.md`
