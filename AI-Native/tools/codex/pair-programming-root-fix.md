---
title: Codex 페어 프로그래밍 — 단계적 root fix 흐름
aliases: [claude codex pair, multi-agent root cause, semantic vs mechanic, multi-round review]
type: concept
status: evergreen
created: 2026-05-16
updated: 2026-05-23
tags: [ai/codex, ai/agent-pattern, status/evergreen, career/ai-native, career/product-engineer, career/fdd, root-cause]
related:
  - "[[AI-Native/tools/codex/leftover-attach-pattern]]"
  - "[[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]]"
  - "[[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]]"
  - "[[AI-Native/agents/_MOC]]"
source: ["INP-145 commit 5b07918"]
migrated-from: MindGraph-TIL/01-Workflow-and-Harness/2026-05-16-codex-pair-programming-root-fix.md
---

# Codex 페어 프로그래밍 — 단계적 root fix 흐름

> TL;DR: Claude + Codex 페어의 진가는 "두 번째 의견"이 아니라 **진단 → 설계 → 박제 → 리뷰 → race 추적**의 단계적 분업. 다른 reasoning trace + 다른 학습 데이터를 가진 모델이 의미적 결함을 잡는다 (Claude=mechanic 강점, Codex=semantic + strict typing 강점).

## What
1인 + AI swarm에서 LLM 2회 호출은 같은 blind spot 반복. **다른 모델**을 페어로 쓰면 한쪽이 놓친 결함을 다른 쪽이 잡는다. Codex가 INP-145의 `fx/fy` 의미 이중 사용 root cause를 진단 — Claude가 6번 fix 시도 다 revert한 케이스에서.

## Why it matters
- 같은 LLM 2회 = 동일 편향 강화
- 다른 LLM 페어 = semantic ↔ mechanic 결함 교차 검출
- ROI: 6번 revert + 사용자 wasted time보다 Codex 토큰(~2M) 저렴

## How — 5단계 분업

| 단계 | 주관 | 산출 |
|------|------|------|
| 1. 진단 (Codex consult) | Codex | root cause + 6 findings + AC 설계 |
| 2. 박제 (Claude implement) | Claude | 12 파일 + migration |
| 3. 1차 리뷰 (Codex review) | Codex | 4 findings (P1.1 drag end stale, P1.2 영속화, P2.3 interrupted drag, P2.4 semantics 충돌) |
| 4. fix + race 추적 (Claude) | Claude | drag end 즉시 박제 (debounce race 차단) |
| 5. 사용자 시각 검증 | 사용자 | 6 시나리오 통과 |

각 단계의 산출이 **다음 단계 입력** = 명시적 transition. 한 모델이 다 하면 단계 사이 의미 손실.

## How — Race 추적

Codex 1차 리뷰 P1.1 (drag end 좌표 stale): Claude가 의미 분리 후 만든 **debounce 1초 race** 결함. Codex가 즉시 진단:
> "mouseup 즉시 active=false + alpha=0 = simulation 즉시 stop → 마지막 tick 못 받음 → d.x/d.y stale"

Claude 단독이면 사용자 결함 보고 후에야 발견.

## How — Cost-aware 사용

매 task review = 토큰 부담 (~296k / consult). balance:
- **큰 변경** (semantic, architectural) → Codex consult/review 필수
- **작은 변경** (refactor, naming) → Codex skip
- INP-145 ROI = consult 1 + review 1 = ~2M tokens (6번 revert보다 저렴)

## How — Codex CLI 사용 패턴

```bash
codex exec -s read-only \
  -c 'model_reasoning_effort="high"' \
  --enable web_search_cached --json
```

## Pitfalls
- 단계 분업이 명확하지 않으면 단계 사이 transition에서 의미 손실
- Cost 무시하고 매 commit review = 부담 폭증 → semantic 변경만
- "두 번째 의견"으로만 쓰면 단순 비용 — **단계 분업이 진짜 가치**

## Related
- [[AI-Native/tools/codex/leftover-attach-pattern]] — multi-round 박제
- [[FE/d3-visualization/force-simulation/fx-fy-dual-semantics]] — root fix 결과
- [[FE/d3-visualization/_concepts/d3-chunk-runner-ric-raf]] — round 2 후속

## Sources
- INP-145 commit 5b07918
- Codex CLI docs
