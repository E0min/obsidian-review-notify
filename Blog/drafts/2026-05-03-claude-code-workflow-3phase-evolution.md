---
title: Claude Code 워크플로우 3단계 진화 — tmux 대시보드 폐기에서 정체성별 폴더 분리까지
date: 2026-05-03
category: 02-Problem-Solving
tags:
  - claude-code
  - workflow
  - hooks
  - agents
  - sprint
  - ownership-docs
  - retrospective
  - 1인-개발
related_commits:
  - a4cdf98
  - ebede55
  - 8632fd1
  - 4a0dc53
  - e7bb068
  - f926a5d
  - 06f75d7
  - 42bda4b
status: published-ready
---

# Claude Code 워크플로우 3단계 진화 — tmux 대시보드 폐기에서 정체성별 폴더 분리까지

## 1. 22일과 6일

지난 한 달 사이 MindGraph 본 개발보다 워크플로우 인프라를 다듬는 데 더 많은 시간을 썼다. 22일을 들여 만든 tmux 9페인 에이전트 대시보드를 통째로 폐기하고, 그 뒤 6일 만에 hooks와 ownership-based DOCS와 `/sprint` 메타 스킬로 새 시스템을 짰다. 같은 한 달인데 결과물은 정반대였다. 앞쪽은 거의 다 버렸고, 뒤쪽은 모두 운영 중이다.

이 글은 그 22일과 6일 사이에 무슨 일이 있었는지 기록한 글이다. 1인 + AI swarm 환경에서 워크플로우 인프라가 어떻게 함정이 되는지, 그리고 그 함정에서 어떻게 빠져나왔는지를 담는다.

---

## 2. Phase 1 — 손수 스킬을 산발적으로 쓰던 때 (~2026-04-05)

이야기는 에이전트 시스템이 자리 잡기 전부터 시작한다.

처음에는 `/office-hours`, `/autoplan`, `/qa`, `/ship` 같은 gstack 스킬을 손으로 직접 호출했다. 매 작업마다 관련 에이전트 파일을 다시 읽고, CEO 같은 오케스트레이션 레이어 없이 부서 에이전트를 한 명씩 직접 부르는 방식이었다.

이 방식의 불편함은 세 가지였다. 첫째, 새 작업을 시작할 때마다 `.claude/CLAUDE.md`를 다시 읽혀야 했다. 컨텍스트 재부여 비용이 매번 들었다. 둘째, 에이전트 dispatching이 없으니 기획성 작업을 개발 에이전트가 받거나, 운영 작업이 기획 쪽으로 흘러가는 일이 종종 생겼다. 셋째, `CLAUDE.md`가 한 장짜리 평면 구조라서 전사 정책과 부서 정책과 기술 스택이 한 문서 안에 뒤섞여 있었다.

이 방식이 약 3주간 굴러갔다. 그 사이 마이크로 매니지먼트의 피로가 누적됐다. 한 번에 하나씩 챙기는 게 가능은 하지만 점점 머릿속에서 "이걸 자동화하면 좋을 텐데"라는 욕구가 자라기 시작했다. 그게 다음 단계의 출발점이 됐다.

---

## 3. Phase 2 — tmux 9페인 대시보드라는 함정 (2026-04-06 ~ 04-28)

### 3.1 어떻게 만들었나

2026년 4월 6일 commit `a4cdf98`에서 tmux 에이전트 대시보드를 도입했다. 구상은 이런 모양이었다.

```
┌─────────────────────────────────────┐
│      상태 모니터 (실시간)             │
├──────────────┬──────────────────────┤
│   CEO        │  Product Manager     │
├──────────────┼──────────────────────┤
│   UI/UX      │  Frontend Engineer   │
├──────────────┼──────────────────────┤
│   Backend    │  Marketing Strategist│
├──────────────┼──────────────────────┤
│   Ops        │  QA Engineer         │
└──────────────┴──────────────────────┘
```

각 페인에서 `run`, `ask`, `log`, `status` 같은 명령을 직접 칠 수 있었다. 곁들여 보조 도구도 세 개를 짰다. `agent-dispatch.sh`로 단일 또는 브로드캐스트 작업을 지시하고, `agent-pipeline.sh`로 feature/bugfix/deploy 같은 사전 정의 워크플로우를 흘려 보내고, `.claude/agent-state/`에 각 에이전트 상태 파일을 동기화했다. 상태는 3초마다 자동 갱신됐고, 화면은 마치 작은 회의실을 한눈에 내려다보는 듯한 느낌이었다.

### 3.2 왜 멋져 보였나

지금 돌이켜 보면 이 시스템이 멋져 보였던 이유는 본질이 아니라 미감 쪽에 가까웠다. 8명 에이전트가 동시에 일하는 모습이 한 화면에 들어오니 작은 회사를 운영하는 듯한 환상이 있었고, 누가 무엇을 하고 어떤 상태인지 실시간으로 추적되는 게 통제감을 줬다. 거기에 tmux와 bash로만 짜진 구성이 개발자스러운 미학을 더했다. commit 메시지는 늘 야심 차 보였다.

### 3.3 왜 함정이었나

문제는 22일치 통계를 다시 들여다본 순간이었다. 그 기간 동안 commit이 109개 쌓였는데, MindGraph 본 개발에 해당하는 양이 사실상 3일 분량이었고 나머지 19일이 전부 인프라였다. 비율로 따지면 86~91%가 워크플로우를 만들기 위한 워크플로우였던 셈이다.

변경 비용도 만만치 않았다. 6개의 skill(`agent-dispatch`, `cross-doc-validation`, `integrity-sync`, `kickoff`, `spec-gate`, `sprint`)과 5개의 shell 도구(`agent-dashboard`, `discover`, `dispatch`, `pipeline`, `spawn`)와 상태 파일들이 서로 얽혀 있어서, 하나를 손대면 3~4개가 영향받았다. 다이어그램 하나 바꾸려고 해도 `dashboard.sh`와 `dispatch.sh`와 state 파일 세 곳을 동시에 만져야 했다.

2주차쯤부터 "다음 주에 고칠 것" 항목이 매주 누적되기 시작했다. 3주차에는 결국 구조를 두 번 재설계했다(commit `2428d11`). 대시보드는 관찰만 하는 도구인데, 유지보수 비용은 실제 코드만큼 비쌌다.

### 3.4 폐기 결단

2026년 4월 28일, commit `ebede55`에서 한꺼번에 정리했다. 메시지는 이랬다.

> ops(v1.9.1): 구 인프라 정리 + DOCS 1차 초안 보강
>
> - 구 인프라 삭제 (Phase 7-doc 구조로 대체됨)
>   · .claude/skills/{agent-dispatch,cross-doc-validation,integrity-sync,kickoff,spec-gate,sprint}
>   · tools/agent-{dashboard,discover,dispatch,pipeline,spawn}.sh

6개 skill과 5개 shell 도구를 일괄 삭제했다. 상태 파일도 정리했다. 약 700줄의 shell과 JavaScript가 사라졌다. 그 자리에 들어선 새 접근이 "Phase 7-doc 구조"였다. 문서와 폴더 구조와 hooks를 조합해서 자동화는 살리되, 시각화는 버리기로 했다.

### 3.5 남은 교훈

대시보드는 "우리가 뭘 하고 있는지 본다"는 환상을 준다. 그런데 자동화는 본래 관찰을 배제한다. 강제된 정책이 자동으로 흐름을 정렬해 주면 사람은 굳이 들여다보지 않아도 된다. 1인 팀에서는 이 차이가 더 크게 작용한다. 다른 팀원과 소통할 일이 없으니 "지금 뭘 하나"보다 "제대로 움직이는가"가 훨씬 중요하다.

결국 관찰 가능한 시스템보다 관찰할 필요 없는 시스템이 더 우월하다는 게 22일치 학습의 한 줄 결론이었다.

---

## 4. Phase 3-A — Ownership-based DOCS (2026-04-29 ~ 05-01)

### 4.1 옛 구조의 한계

대시보드를 폐기하고 나서 남은 게 문서 구조였다. 당시 DOCS는 이런 모양이었다.

```
DOCS/
├── Phase1_Product/
├── Phase2_Design/
├── Phase3_Engineering/
├── Phase4_Quality/
├── Phase5_Operations/
└── Phase6_GTM/
```

이건 시간축으로 자른 분류였다. 책임축이 아니었다. 1인 + AI swarm 환경에서는 "이 문서 누가 관리해?"라는 질문에 답하는 축이 부서(team)인데, Phase 분류로는 그게 안 잡혔다. 8명 에이전트가 동시에 여러 Phase 폴더를 만지면 ownership이 모호해지고 수정 충돌이 생긴다. 게다가 "지금 어느 Phase냐"는 질문 자체가 동적이다. v2.0 기획을 하면서 v1.9 버그도 고치고 있는 상황이 흔한데, Phase 폴더는 그걸 표현하지 못했다.

### 4.2 ownership-based 재구조화

2026년 4월 29일 commit `8632fd1`에서 대대적으로 옮겼다.

```
department/product/docs/
├── active/
│   ├── PRD.md
│   ├── FEATURES.md
│   ├── SRS.md
│   └── RELEASE_PLAN.md
├── playbook/
│   ├── BEACHHEAD-V2.md
│   ├── POSITIONING.md
│   └── COMPETITIVE_ANALYSIS.md
└── archive/
    ├── KPI_METRICS.md
    └── discovery/

department/design/docs/
department/dev/docs/
department/ops/docs/
department/qa/docs/
```

이 구조에서 핵심은 폴더 자체가 lifecycle의 SSOT가 된다는 점이었다. `active/`는 living(자주 변경), `playbook/`은 standard(운영 방식 정의), `artifacts/`는 immutable(시점 박제, 배포 시 생성), `drafts/`는 exploration(임시), `archive/`는 frozen(과거 참조용, 수정 불가)을 의미한다. lifecycle 정보를 frontmatter 필드로 따로 둘 필요가 없어졌다. 위치 자체가 정책을 표현하니까.

### 4.3 frontmatter 다이어트

commit `e7bb068`(2026-05-02)에서 frontmatter도 함께 줄였다.

이전에는 13~15개 필드를 달고 있었다.

```yaml
---
doc_type: PRD
team: product
scope: shared
lifecycle: draft
cumulative: false
phase: 1
version: v1.9
last_updated: 2026-04-20
---
```

이걸 7개로 줄였다.

```yaml
---
doc_type: PRD
team: product
status: APPROVED
owner: product-manager
last_updated: 2026-05-02
depends_on: [...]
impacts: [...]
---
```

폐기한 필드는 `scope`, `lifecycle`, `cumulative`, `phase`, `version`이다. 이들이 하던 일을 폴더 위치가 대신했다. 73개 파일에서 일괄로 빼냈고, `strip-legacy-fields.ts`라는 작은 CLI를 만들어 자동화했다.

### 4.4 메모리 피드백 한 줄

이 결정의 배경에는 미리 적어둔 메모리 노트가 있었다. `feedback_doc_architecture.md`의 한 문장이 길게 남았다.

> 위치가 정책을 표현 — frontmatter 따로 만들 필요 없음.
> 1인 + AI swarm에서는 새 SSOT를 만들지 않는다. Linear 이미 있고, SPRINT.md 있고, git history 있고, CHANGELOG 있다. 5번째 SSOT(frontmatter 상태 필드)를 만들면 동기화 비용이 5배가 된다.

phase-based에서 ownership-based로 옮긴 진짜 이유가 여기에 있었다.

---

## 5. Phase 3-B — Hooks 네 가지로 자동화 (2026-04-29 ~ 05-03)

대시보드를 버리고 나면 자연스러운 질문이 따라온다. 그럼 자동화는 어떻게 하나? 답이 hook이었다. 네 개의 hook이 특정 순간마다 강제로 정책을 집행하도록 했다.

### 5.1 spec-gate.sh — 코드 작성을 차단한다

PreToolUse 단계, 즉 Write나 Edit이 호출되는 순간에 발동한다. 작성하려는 영역에 대응하는 필수 문서가 `status:APPROVED` 상태인지 확인한다. 영역 매핑은 이런 식이다.

```bash
case "$REL" in
  department/dev/web/lib/storage/*)
    required_doc="department/dev/docs/BACK/DATABASE_SCHEMA.md" ;;
  department/dev/web/components/graph/*)
    required_doc="department/dev/docs/FRONT/FRONTEND.md" ;;
  department/dev/src/content/*)
    required_doc="department/dev/docs/FRONT/FRONTEND.md" ;;
  department/dev/src/background/*)
    required_doc="department/dev/docs/BACK/BACKEND.md" ;;
  department/dev/src/popup/*)
    required_doc="department/dev/docs/FRONT/FRONTEND.md" ;;
  *)
    exit 0 ;;
esac
```

대응 문서가 DRAFT 상태라면 hook이 `exit 2`를 반환하고, Claude Code는 그 도구 호출을 거부한다. 도그푸딩 중에 이게 너무 빡빡하게 느껴지면 `SPEC_GATE_MODE=warn`을 걸어 차단을 경고로 낮출 수 있다.

### 5.2 integrity-sync.sh — 후행 문서를 STALE로 알린다

PostToolUse 단계, 문서 작성이 끝난 직후에 발동한다. 수정된 문서의 frontmatter에서 `impacts[]`를 파싱해서 후행 문서들을 STALE 후보로 안내한다. 폴더 위치에 따라 알림 강도가 갈린다.

```bash
case "$REL" in
  */archive/*|*/drafts/*)
    # frozen 또는 exploration — STALE 전파 OFF
    exit 0 ;;
  */artifacts/*)
    # immutable — 변경 자체 차단 (git tracked면)
    >&2 echo "[integrity-sync] artifact 변경 차단"
    exit 2 ;;
  */playbook/*)
    # standard — 변경 알림만 (약한 전파)
    >&2 echo "[integrity-sync] playbook 변경 후행 알림"
    exit 0 ;;
  *)
    # living — 강한 전파, STALE 마킹 권고
    >&2 echo "[integrity-sync] living doc 변경 — 후행 $N개 STALE 후보"
    ;;
esac
```

여기서 일부러 자동 마킹은 하지 않는다. 사용자 결정을 보존하기 위해서다. 대신 "이 문서를 손댔으니 저기도 영향이 갈 것"이라는 신호만 명확히 주는 식이다.

### 5.3 dept-doc-sync.sh — cross-tree 참조를 보여준다

`department/*/docs/`에 변경이 생기면 RULES와 HANDBOOK과 다른 부서 문서에서 이 파일을 참조하는 곳을 훑어 안내한다. 예를 들어 `department/dev/docs/FRONT/FRONTEND.md`를 손대면 `RULES/CODE_CONVENTIONS.md`와 `HANDBOOK/02_DOCS_SYSTEM.md`가 이 문서를 인용하고 있다는 사실이 stderr로 떠오른다. 부서 경계는 부서 경계대로 두면서 cross-tree 가시성을 동시에 챙기는 장치다.

### 5.4 stale-warn.sh — STALE 누적을 경고한다

UserPromptSubmit, 그러니까 사용자가 prompt를 입력하는 매 순간에 발동한다. frontmatter의 `status:STALE`을 카운트해서 5개를 넘으면 prompt 앞에 한 줄 경고를 붙인다.

```
⚠️  [stale-warn] STALE 문서 8개 — 우선 처리하거나 `skip stale` 입력으로 무시
```

skip 키워드를 다섯 가지(`skip stale`, `stale ok`, `ignore stale`, `proceed`, `force`) 인식하도록 둬서, 일단 무시하고 진행해야 하는 상황도 말로 풀 수 있게 했다. 임계는 `STALE_WARN_THRESHOLD=5`로 조절하고, `STALE_WARN_BLOCK=true`를 걸면 경고가 아니라 차단이 된다.

### 5.5 git hooks 두 가지

commit `e7bb068`에서 git hook도 두 개 추가했다.

`pre-commit`은 7개 검증을 모두 통과해야 통과한다. schema(frontmatter 형식), cycle(순환 의존), dangling(참조 끊김), hash-drift(선행 doc이 변경됐는데 hash 미갱신), orphan(폴더 정책 위반), folder-policy(잘못된 lifecycle 폴더), legacy-field+path(옛 필드명 또는 옛 경로 인용). 한 항목이라도 에러가 잡히면 commit이 막힌다. 여기에 commit `06f75d7`에서 HANDBOOK drift 검사를 한 단계 더 얹었다. `.claude/CLAUDE.md`나 `.claude/hooks/`나 `scripts/docs/`나 `SYSTEM/schemas/` 같은 시스템 파일이 staged 됐는데 `HANDBOOK/`은 손대지 않았다면 경고가 뜬다(`HANDBOOK_DRIFT_MODE=enforce|off|warn`로 강도 조절).

`commit-msg`는 Conventional Commits 형식을 강제한다. `dev(web/storage): 기능 요약` 같은 형태가 아니면 commit이 거부된다. 워커 브랜치(`inp-*`) commit에서는 `(refs INP-XX)` footer까지 강제한다. sprint trunk나 팀 브랜치, chore commit은 면제다.

---

## 6. Phase 3-C — `/sprint` 메타 스킬로 1주 사이클을 묶다

Phase 3에서 마지막으로 자리 잡은 큰 도구가 `/sprint` 메타 스킬이다. commit `4a0dc53`에서 첫 골격을 잡았다.

### 6.1 6단계 구조

sprint 한 사이클이 늘 비슷한 리듬으로 흐른다는 걸 인지하고, 그 리듬을 한 스킬에 압축했다.

```
/sprint research → 백로그 탐색 + 리스크 분석
        ↓
/sprint plan     → Linear Cycle 생성 + INP 이슈 등록 + SPRINT.md 자동 작성
        ↓
/sprint build    → 워커 브랜치(inp-*) 작업 + 트렁크 머지
        ↓
/sprint qa       → 4-tier QA (회귀 + review + cso + benchmark)
        ↓
/sprint ship     → 배포 + 릴리스 노트 + INP Done 일괄 전환
        ↓
/sprint retro    → 회고 박제 (artifacts/sprints/v{X.Y}/RETRO.md)
```

각 단계는 그 자체가 새 스킬이 아니라, gstack 풀에 이미 있는 스킬들(`office-hours`, `autoplan`, `as-build`, `qa`, `review`, `cso`, `benchmark`, `ship`, `land-and-deploy`, `canary`, `document-release`, `retro` 등)을 호출하는 wrapper에 가깝다. 새 도구를 짓지 않고 기존 도구를 엮은 셈이다.

### 6.2 SSOT 네 곳을 한 번에 동기화한다

sprint를 운영하다 보면 정보가 네 곳에 흩어진다. `SPRINT.md`(루트, 지금 뭘 하나), Linear Cycle(거울, 누가 뭘 맡았나), Git history(추적, 뭘 했나), CHANGELOG와 tag(가시, 사용자에게 뭘 알릴까). 각각 한 가지 일만 한다는 점이 중요하다. 동기화 비용은 `/sprint`가 흡수한다. 사람은 어느 한 곳에만 정보를 적어 두고, 나머지로의 전파는 스킬이 떠맡는다.

### 6.3 prerequisite 4 옵션

각 단계마다 선행 조건이 있는데, 그 선행 조건을 어떻게 만족시킬지 네 가지 분기를 둔다.

```
/sprint build 호출
  ↓
"plan 단계 완료했나?"
  ├─ 자동 실행 (plan 산출물이 형성돼 있으면 인정)
  ├─ 사용자 주장 (plan 대화는 했는데 산출물 미작성 → 자동 마킹)
  ├─ 대화 분석 (최근 대화 기반 추론)
  └─ 강제 (무시하고 진행)
```

여기서 "사실상 했다"의 판단 기준을 산출물 형성 여부로 잡았다. PLAN.md나 Linear Cycle이 만들어졌으면 인정하고, 말로만 결정한 건 인정하지 않는다. 입으로 "계획 끝났어"라고 한다고 해서 plan 단계가 완료된 게 아니라, 그게 어딘가에 박제됐을 때만 다음 단계로 넘어간다는 규칙이다.

### 6.4 사람이 직접 하는 일은 세 가지뿐

`/sprint`가 자리 잡고 나서 보니, 사람이 의식적으로 해야 하는 행동은 세 가지로 줄어들었다. commit prefix에 `dev-feat`, `dev-fix` 같은 보조 태그를 붙이는 일, 워커 브랜치 commit에서 `(refs INP-XX)` footer를 넣는 일, `/sprint research` 산출물(draft estimate)을 검토해서 승인하는 일. 그 외에는 Linear cycle 생성, INP 이슈 일괄 생성, area 라벨 매핑, SPRINT.md 작성과 동기, PR review 통합, Done 일괄 전환, CHANGELOG 갱신, tag 생성, 릴리스 노트 작성 모두 자동으로 흐른다.

---

## 7. Phase 3 Finale — 정체성별로 폴더를 갈랐다 (2026-05-03)

### 7.1 폴더 이름이 너무 광범위했다

Phase 3가 자리 잡으면서 또 다른 불편이 슬슬 보이기 시작했다.

```
graph/
├── DOCS/                     ← "문서" 일반명사
│   ├── AGENT_INSTRUCTIONS.md (에이전트가 따라야 할 규칙)
│   ├── HANDBOOK/             (사람이 읽는 운영 매뉴얼)
│   ├── _meta/                (시스템 메타데이터)
│   └── ...
├── department/docs/          ← 부서별 doc
```

`DOCS/`라는 이름이 너무 광범위했다. 최상위 `DOCS/`와 `department/docs/`의 이름이 충돌했고, 한 폴더 안에 성격이 다른 세 종류의 파일이 섞여 있었다. 에이전트가 의사결정에 참고하는 규칙, 사람이 운영할 때 읽는 매뉴얼, 시스템이 검증할 때 읽는 메타데이터가 모두 한 곳에 들어 있었다. 그러다 보니 새 문서를 만들 때마다 "이거 어디다 두지?"라는 작은 갈등이 매번 생겼다.

commit `f926a5d`(2026-05-03)에서 이름을 갈랐다.

> docs(structure): DOCS → RULES rename — ownership clarity 회복

### 7.2 분리 전후

전에는 한 폴더에 다 들어 있었다.

```
DOCS/
├── AGENT_INSTRUCTIONS.md     (규칙)
├── GIT_CONVENTIONS.md         (규칙)
├── HANDBOOK/                  (매뉴얼)
├── _meta/                     (메타)
└── ...
```

이걸 세 폴더로 갈라 냈다.

```
RULES/                         (에이전트가 따라야 할 규칙 8개)
├── AGENT_INSTRUCTIONS.md
├── GIT_CONVENTIONS.md
├── CODE_CONVENTIONS.md
├── PROJECT_STRUCTURE.md
├── DESIGN-LANGUAGE.md
├── SECURITY_POLICY.md
├── CLAUDE.md
└── INDEX.md

HANDBOOK/                      (사람이 읽는 운영 매뉴얼)
├── 01_SYSTEM_OVERVIEW.md
├── 02_DOCS_SYSTEM.md
├── 03_SPRINT_WORKFLOW.md
├── 04_TROUBLESHOOTING.md
├── 05_GIT_WORKFLOWS.md
└── README.md

SYSTEM/                        (시스템이 읽는 메타데이터)
├── schemas/
│   ├── frontmatter-schema.json
│   └── doc-type-registry.yaml
└── cache/
    └── .docs-index.db (gitignore)
```

### 7.3 폴더 이름이 정체성이 됐다

이렇게 갈라 놓고 보니 폴더 이름이 곧 그 안에 든 문서의 정체성이 됐다. RULES는 에이전트가 따라야 할 규칙이고, HANDBOOK은 사람이 읽는 운영 지침이고, SYSTEM은 시스템이 읽는 메타데이터고, department는 부서 owner가 관리하는 결과물이다. 새 문서를 만들 때 "이게 규칙인가, 매뉴얼인가, 메타인가, 산출물인가?"를 한 번만 자문하면 위치가 자동으로 결정된다. 그 갈등이 사라진 게 가장 컸다.

같은 날 commit `06f75d7`에서 HANDBOOK도 의존성 그래프에 편입시켰다. 시스템 파일(`.claude/CLAUDE.md`, `hooks/`, `scripts/`)이 변경되면 HANDBOOK 문서가 자동으로 STALE 전파 후보가 된다. commit `42bda4b`에서는 SYSTEM 분리도 마무리해서 `schemas/`와 `cache/`의 폴더 정책을 따로 두었다.

---

## 8. 22일 vs 6일을 숫자로

| 지표 | Phase 2 (대시보드) | Phase 3 (hooks + ownership) |
|------|-------------------|---------------------------|
| 기간 | 22일 (04-06 ~ 04-28) | 6일 (04-28 ~ 05-03) |
| 총 commit | 109개 | 약 30개 (인프라만) |
| 인프라 비중 | 86~91% | 20~33% |
| 본 개발 시간 | 약 3일 | 약 3~4일 |
| 산출물 폐기율 | 100% (`ebede55`에서 일괄 삭제) | 0% (모두 운영 중) |
| 관리 대상 | skill 6개 + shell 도구 5개 + state 파일 | hook 4개 + frontmatter 7필드 + lifecycle 폴더 5종 |
| 정책 1개 수정 시 영향 | 3~4개 파일 | 1개 파일 또는 1개 폴더 |

가장 인상적이었던 건 본 개발에 쓴 시간이 거의 같았다는 점이다. 22일짜리 Phase 2도 본 개발은 3일이었고, 6일짜리 Phase 3도 본 개발은 3~4일이었다. 인프라 시간만 19일에서 1~2일로 줄었다. 같은 결과물인데 비용이 한 자릿수 차이로 떨어진 셈이다.

`v1.9.2` retro에는 이런 구절이 있다.

> 2.1 "본문 검증 후 hash만 갱신" 패턴이 핵심 가속기.
> 기존 가정은 hash-drift가 본문이 outdated된 결과라고 봤다. 그래서 본문과 hash를 둘 다 갱신해야 한다고 봤고, 시간을 4~5시간 잡았다. 실제로는 SRS/SAD/IA 본문이 모두 v1.9.x 코드와 이미 일치했다. drift는 옛 hash가 frozen된 결과였다. 결과적으로 patch sprint의 70% 시간을 절감했다. 본문 갱신은 별도 sprint로 분리할 수 있다는 게 사실로 확인됐다.

작은 패턴 하나를 정확히 잡으니 시간이 절반 이상 줄어든다. Phase 3가 그런 패턴들의 집합이었다.

---

## 9. 1인 + AI swarm 다이어트 네 가지 원칙

전체를 정리하면서 남은 인식을 네 가지로 묶었다.

첫째, 새 SSOT를 만들지 않는다. 이미 Linear가 "누가 뭘 맡았나"를 들고 있고, SPRINT.md가 "지금 뭘 하나"를 들고 있고, git history가 "뭘 했나"를 들고 있고, CHANGELOG가 "사용자에게 뭘 알릴까"를 들고 있다. 여기에 다섯 번째 SSOT(상태 필드든, 모니터링 대시보드든)를 더 얹으면 동기화 비용이 그대로 N배가 된다. 그래서 새 doc을 추가하기 전에 한 번 자문한다. 이거 Linear로 충분하지 않나?

둘째, 위치가 정책을 표현한다. lifecycle을 frontmatter 필드로 두지 않고 폴더로 표현하면, 두 군데에 같은 정보를 적느라 어긋날 일이 사라진다. `active`에 있으면 living이고, `playbook`에 있으면 standard고, `artifacts`에 있으면 immutable이고, `archive`에 있으면 frozen이다. 위치가 곧 의미다.

셋째, 정체성이 위치를 결정한다. RULES는 에이전트가 읽고, HANDBOOK은 사람이 읽고, SYSTEM은 도구가 읽고, department는 부서 owner가 읽는다. 한 폴더에 다 두면 누구든 다 읽어야 하는 것처럼 보이지만, 갈라 놓으면 각자 자기 자리만 보면 된다. 컨텍스트가 그만큼 가벼워진다.

넷째, 시각화보다 자동화가 낫다. 대시보드는 "지금 뭘 하네"라는 정보를 줄 뿐이지만, hook은 "이건 해야 돼, 저건 안 돼"를 강제한다. 1인 팀에서는 정보가 부족해서 망하는 일보다 강제가 부족해서 망하는 일이 훨씬 잦았다. 22일을 들여 그걸 확인했다.

---

## 10. 따라할 수 있는 시작점

혹시 다른 1인 개발자가 이 워크플로우 일부를 도입해 보고 싶다면, 여기서 시작하면 무난하다.

hook은 단순한 골격이면 충분하다. spec-gate는 다섯 줄로 시작할 수 있다.

```bash
FILE_PATH="$1"
case "$FILE_PATH" in
  src/storage/*) required="docs/DATABASE_SCHEMA.md" ;;
  *) exit 0 ;;
esac
# 필수 doc의 status:APPROVED 확인 후 exit 0 또는 2
```

integrity-sync도 비슷하게 짧게 시작할 수 있다.

```bash
FILE_PATH="$1"
# frontmatter impacts[] 파싱
for doc in "${IMPACTS[@]}"; do
  echo "STALE 후보: $doc"
done
```

frontmatter 7필드 스키마는 이 모양이다.

```yaml
---
doc_type: PRD        # 또는 FEATURE, DESIGN, SAD, TEST 등
team: product        # 또는 design, dev, ops, qa, marketing
status: APPROVED     # DRAFT | REVIEW | APPROVED | STALE | DEPRECATED
owner: pm-name
last_updated: YYYY-MM-DD
depends_on:          # 선행 문서 (hash로 추적)
  - path: department/product/docs/FEATURES.md
    hash: abc123def456
impacts:             # 후행 문서 (자동 STALE 전파)
  - department/dev/docs/FRONT/FRONTEND.md
---
```

ownership 폴더 구조는 이렇게 잡으면 그대로 시작할 수 있다.

```
department/product/docs/
├── active/           (living — 자주 변경)
│   ├── PRD.md
│   └── FEATURES.md
├── playbook/         (standard — 운영 방식)
│   └── POSITIONING.md
├── artifacts/        (immutable — 배포 박제)
│   └── v{X.Y}/
└── archive/          (frozen — 과거 참조)
    └── KPI_METRICS.md
```

더 깊이 파고 들고 싶으면 HANDBOOK의 01번 문서(시스템 오버뷰)와 `.claude/CLAUDE.md`의 §12~14(hooks, git hooks, skills 레지스트리)와 `RULES/GIT_CONVENTIONS.md`의 commit prefix와 branch strategy 부분을 같이 보는 걸 권한다.

---

## 11. 마무리

Phase 2의 대시보드는 "조직처럼 보이고 싶다"는 욕망에서 나왔다. 그런데 1인 + AI swarm의 본질적 강점은 큰 조직처럼 보이는 게 아니라 정반대다. 의사결정권이 한 곳에 있어서 합의가 빠르고, 설명할 팀원이 없어서 커뮤니케이션 부채가 0이고, 재검토할 단계가 없어서 즉시 실행할 수 있다. 대시보드와 회의실 미감은 이 강점을 침식한다. 강제된 정책과 명확한 위치가 1인의 생산성을 더 잘 끌어낸다.

작은 팀은 큰 팀처럼 보일 필요가 없다. 빠르고 정확하면 그걸로 충분하다.

---

## 참고 자료

- Commit `a4cdf98` — Phase 2 대시보드 도입
- Commit `ebede55` — Phase 2 폐기
- Commit `8632fd1` — Phase 3-A ownership-based DOCS
- Commit `e7bb068` — Phase 3-B frontmatter 다이어트와 git hooks
- Commit `4a0dc53` — Phase 3-C `/sprint` 메타 스킬
- Commit `f926a5d` — Phase 3 Finale RULES/HANDBOOK/SYSTEM 분리
- Commit `06f75d7` — HANDBOOK 의존성 그래프 편입
- Commit `42bda4b` — SYSTEM 폴더 분리 완료
- RETRO v1.9.2 — `/sprint` 메타 스킬 첫 검증 회고
- HANDBOOK 01 — 시스템 오버뷰와 다이어트 철학
