---
title: 메인 AI 자체 권장 흐름 표준 외 — 5층 역전파로 박제
aliases: [build pr block, 5 layer backpropagation, AI standard divergence, sprint trunk merge]
type: concept
status: evergreen
created: 2026-05-10
updated: 2026-05-23
tags: [ai/claude-code, ai/agent-pattern, status/evergreen, career/ai-native, career/product-engineer, hook, workflow]
related:
  - "[[AI-Native/claude-code/hooks/linear-done-gate]]"
  - "[[AI-Native/agents/inp-tracker-followup-pattern]]"
  - "[[AI-Native/_concepts/5-layer-backpropagation]]"
  - "[[AI-Native/agents/swarm-workflow-real-issues]]"
source: ["v2.0-sprint-1 PR #1 close + 직접 머지 정정 인시던트"]
migrated-from: MindGraph-TIL/01-Workflow-and-Harness/2026-05-10-build-pr-block-5-layer-backpropagation.md
---

# 메인 AI 자체 권장 흐름 표준 외 — 5층 역전파로 박제

> TL;DR: 1인 + AI swarm에서 PR 형식은 가치 0(검토자 = 사용자 본인). 메인 AI가 학습 데이터 일반 패턴("PR이 git 표준")으로 우리 환경의 특수 정책을 덮어쓸 위험. **L1 대화 + L2 memory + L3 RULES + L4 SKILL.md + L5 Hook `exit 2`** 5층 동시 박제.

## What
워커(`inp-*`) → sprint 트렁크(`sprint/v{X.Y}`) 머지에 메인 AI가 PR을 권장한 인시던트. memory(L2) 박제만으로는 다음 세션에서 AI가 능동 참조 안 함. L5 Hook이 안전망 역할.

## Why it matters
이 패턴은 **L1~L5 강제력 격차의 교과서적 예**. AI 자율성을 깎지 않으면서 잘못된 자동화의 비용이 큰 액션만 OS 레벨 게이트.

## How — 5층 박제

| 층 | 위치 | 강제력 | 역할 |
|----|------|--------|------|
| L1 | 대화 1회 정정 | 약 (휘발) | 인시던트 즉시 |
| L2 | memory `feedback_pr_only_for_ship.md` | 중 (참조 의존) | 다음 세션 컨텍스트 |
| L3 | RULES `GIT_CONVENTIONS §1.7` | 중-강 (spec-gate 대상) | 정책 단일 권위 |
| L4 | `/sprint` SKILL.md step3 + Anti-patterns | 강 (실행 흐름) | 단계마다 강제 |
| L5 | Hook `build-pr-block.sh` `exit 2` | 최강 (OS 거부) | AI 위반 명령 시 |

## How — L5 Hook (`.claude/hooks/build-pr-block.sh`)

```bash
#!/usr/bin/env bash
set -e

if [[ "${BUILD_PR_BLOCK:-enforce}" == "off" ]]; then exit 0; fi

INPUT="$(cat 2>/dev/null || true)"
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# gh pr create 아니면 통과
if [[ ! "$CMD" =~ gh[[:space:]]+pr[[:space:]]+create ]]; then exit 0; fi

BASE=$(echo "$CMD" | grep -oE -- '--base[[:space:]]+[^[:space:]]+' | head -1 | awk '{print $2}')
HEAD=$(echo "$CMD" | grep -oE -- '--head[[:space:]]+[^[:space:]]+' | head -1 | awk '{print $2}')

# head 가 inp-* 면 sprint trunk PR 위험
if [[ -z "$BASE" ]] && [[ "$HEAD" =~ ^inp- ]]; then
  echo "[BLOCKED] base 미지정 + head=$HEAD. 직접 머지: git merge --ff-only $HEAD" >&2
  exit 2
fi

# 외부 트렁크 PR 통과 (ship 단계 정상)
if [[ "$BASE" == "main" ]] || [[ "$BASE" == "develop" ]]; then exit 0; fi

# 차단 패턴: base=sprint/* + head=inp-*
if [[ "$BASE" =~ ^sprint/ ]] && [[ "$HEAD" =~ ^inp- ]]; then
  echo "[BLOCKED] build PR 차단 — direct merge: git checkout $BASE && git merge --ff-only $HEAD" >&2
  exit 2
fi
exit 0
```

## How — L3 RULES (`GIT_CONVENTIONS.md §1.7`)

| 머지 | 형식 | 게이트 |
|------|------|--------|
| 워커 (inp-*) → sprint 트렁크 | 직접 머지 (PR X) | `/sprint qa` 4-tier |
| sprint 트렁크 → main | PR 필수 | `/sprint ship` |
| 시스템 정비 → main | 직접 머지 (`--ff-only`) | 사용자 명시 승인 |

## Pitfalls
- L2 memory만으로 의존하면 다음 세션에서 또 누락 (능동 참조 가정 깨짐)
- L5 우회 2종 (env var, 외부 트렁크) = 정당한 케이스 보호
- 같은 패턴이 적용 가능한 케이스: 자동 commit, 자동 vault 저장, INP 무분별 발급

## Related
- [[AI-Native/claude-code/hooks/linear-done-gate]] — 동일 패턴, one-shot marker 우회
- [[AI-Native/agents/inp-tracker-followup-pattern]] — UserPromptSubmit hook 변형
- [[AI-Native/_concepts/5-layer-backpropagation]] — 메타 패턴
- [[AI-Native/agents/swarm-workflow-real-issues]] — 관련 결함 종합

## Sources
- commit beaaa97 (chore(harness): build 단계 PR 차단)
- `RULES/GIT_CONVENTIONS.md §1.7`
