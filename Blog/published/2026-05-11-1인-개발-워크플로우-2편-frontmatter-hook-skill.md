---
title: "1인 개발 워크플로우 진화 2편 — Frontmatter + Hook + Skill로 짓는 시스템"
date: 2026-05-11
category: 02-Problem-Solving
series: "1인 + AI swarm 워크플로우 진화"
series_index: 2
tags:
  - claude-code
  - workflow
  - single-developer
  - ai-swarm
  - frontmatter
  - hook
  - skill
  - sub-agent
  - context-isolation
  - ownership-docs
  - 1인-개발
related_commits:
  - 8632fd1
  - 4a0dc53
  - e7bb068
  - f926a5d
  - 06f75d7
  - 42bda4b
status: published-ready
related_post: "[[2026-05-11-1인-개발-워크플로우-1편-context-오염과-22일-폐기]]"
---

# 1인 개발 워크플로우 진화 2편 — Frontmatter + Hook + Skill로 짓는 시스템

> 이 글은 2부작 시리즈의 2편이다. 1편 「Context 오염과 22일짜리 오버엔지니어링」에서는 1인 + AI swarm 환경에서 마주친 문제와 거기에 잘못 답하느라 22일을 태운 이야기를 다뤘다. 2편에서는 폐기 이후 6일 동안 자리 잡은 시스템을 구체적으로 본다. 1편을 읽지 않은 독자를 위해 짧게 요약하면 이렇다. 1인 개발에는 커뮤니케이션 부채 대신 자기 과거 맥락과의 동기화 부채가 있다. AI 에이전트는 옛 PRD를 새 PRD와 동등한 권위로 본다. 이 문제를 풀려고 tmux 대시보드와 Python 기반 orchestration을 짓다가 22일을 태우고 폐기했다. 결론은 Claude Code 위에 얇은 레이어만 얹기로 한 것. 그 얇은 레이어가 이 글에서 다루는 frontmatter, hook, skill이다.

## 1. 세 부품 — frontmatter, hook, skill

폐기 이후 새로 짠 시스템은 세 가지로 정리된다. frontmatter는 문서가 자기 의존성을 스스로 선언하게 한다. hook은 그 선언을 바탕으로 정책을 자동 강제한다. skill은 반복되는 워크플로우의 리듬을 한 번에 묶는다. 셋 다 Claude Code가 이미 가진 기능 위에 얹는 얇은 layer고, 따로 새 framework를 짓지 않는다.

---

## 2. Frontmatter — 문서가 자기 의존성을 선언한다

### 2.1 7필드 다이어트

처음에는 frontmatter에 13~15개 필드를 달고 있었다.

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
last_updated: 2026-05-11
depends_on:
  - path: RULES/PROJECT_STRUCTURE.md
    hash: 554628d51bb4
impacts:
  - department/dev/docs/FRONT/FRONTEND.md
---
```

폐기한 필드는 `scope`, `lifecycle`, `cumulative`, `phase`, `version`이다. 이들이 하던 일을 폴더 위치가 대신했다(자세한 폴더 정책은 §6에서 다룬다). 73개 파일에서 일괄로 빼냈고, `strip-legacy-fields.ts`라는 작은 CLI를 만들어 자동화했다.

### 2.2 핵심은 status / depends_on / impacts

남긴 7필드 중에서도 핵심은 세 개다. `status`는 현재 유효성을 표현한다(`DRAFT | REVIEW | APPROVED | STALE | DEPRECATED`). STALE이거나 DEPRECATED이면 AI는 그 문서를 출처로 받아들이지 않는다. `depends_on`은 이 문서가 어떤 상위 문서를 전제로 깔고 있는지를, `impacts`는 이 문서가 바뀌면 함께 흔들리는 후행 문서가 어디인지를 가리킨다. 의존성 그래프가 frontmatter 안에 자기서술 형태로 들어 있는 셈이다.

이제 v1.0 PRD에는 `status: DEPRECATED`를 박고 v1.5 PRD에는 `APPROVED`를 박는다. 완벽한 해결은 아니지만, 적어도 AI가 어떤 문서가 살아 있고 어떤 문서가 죽었는지 신호를 받을 수 있게 된다. 1편에서 다룬 context 오염을 막는 첫 번째 자물쇠다.

`depends_on`에 hash가 들어 있는 게 또 한 가지 장치다. 선행 문서가 변경되면 hash가 어긋나고, hook이 그 어긋남을 잡아서 "이 문서를 다시 검토해야 한다"는 신호를 띄운다. 단순한 link만으로는 안 잡히는 후행 영향을 hash가 추적한다.

---

## 3. Hook — 정책을 자동으로 강제한다

문서가 메타데이터를 선언하면 시스템이 무결성을 자동으로 점검할 수 있다. `.claude/hooks/`에 두는 셸 스크립트가 그 역할을 한다. 지금 9개를 쓰고 있는데, 가장 자주 발동하는 것부터 본다.

### 3.1 spec-gate.sh — 코드 작성을 차단한다

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

대응 문서가 DRAFT 상태라면 hook이 `exit 2`를 반환하고, Claude Code는 그 도구 호출을 거부한다. 도그푸딩 중에 이게 너무 빡빡하게 느껴지면 `SPEC_GATE_MODE=warn`을 걸어 차단을 경고로 낮출 수 있다. 문서 없이 코드부터 짜는 흐름을 차단하는 게이트다.

### 3.2 integrity-sync.sh — 후행 문서를 STALE로 알린다

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

### 3.3 dept-doc-sync.sh — cross-tree 참조를 보여준다

`department/*/docs/`에 변경이 생기면 RULES와 HANDBOOK과 다른 부서 문서에서 이 파일을 참조하는 곳을 훑어 안내한다. 예를 들어 `department/dev/docs/FRONT/FRONTEND.md`를 손대면 `RULES/CODE_CONVENTIONS.md`와 `HANDBOOK/02_DOCS_SYSTEM.md`가 이 문서를 인용하고 있다는 사실이 stderr로 떠오른다. 부서 경계는 부서 경계대로 두면서 cross-tree 가시성을 동시에 챙기는 장치다.

### 3.4 stale-warn.sh — STALE 누적을 경고한다

UserPromptSubmit, 그러니까 사용자가 prompt를 입력하는 매 순간에 발동한다. frontmatter의 `status:STALE`을 카운트해서 5개를 넘으면 prompt 앞에 한 줄 경고를 붙인다.

```
⚠️  [stale-warn] STALE 문서 8개 — 우선 처리하거나 `skip stale` 입력으로 무시
```

skip 키워드를 다섯 가지(`skip stale`, `stale ok`, `ignore stale`, `proceed`, `force`) 인식하도록 둬서, 일단 무시하고 진행해야 하는 상황도 말로 풀 수 있게 했다.

### 3.5 나머지 다섯 hook — 두 가지 결로 갈린다

이외에 다섯 개가 더 있는데, 성격이 둘로 나뉜다. 사용자 검증을 강제하는 게이트 둘과, 의사결정 시점에 정보를 한 줄 띄워 주는 보조 셋이다.

먼저 게이트 두 개. `commit-user-gate`는 `git commit` 명령 자체를 막는다. AI가 시각 검증 없이 곧장 commit으로 직행하는 흐름을 차단하고, 내가 명시 승인한 경우에만 한 번 풀어 주는 우회 장치를 둔다. `linear-done-gate`는 같은 결로 이슈 트래커에서 Done 전환을 막는다. AI의 코드 검증으로는 "Done 후보"까지만이고, 실제 Done 전환은 내가 dev 서버에서 화면을 본 뒤에만 한다. 두 hook 다 "AI가 자체 판단으로 외부 영향을 끼쳤다가 잘못된 상태로 진행돼 버린" 사고가 누적된 직후에 박혔다.

나머지 셋은 차단보다는 신호에 가깝다. `vault-log-suggest`는 의미 있는 수정 commit이 끝난 직후에 학습 노트로 남길 가치가 있는지 평가하는 체크리스트를 한 줄 띄운다. 일반화 가능한 패턴인지, 비자명한 메커니즘인지를 commit 직후에 한 번 점검하게 만든다. `inp-reuse-suggest`는 후속 결함 보고가 들어오면 신규 이슈로 발급하지 말고 기존 이슈에 묶으라고 자동 제안한다. 같은 문제에 새 이슈를 자꾸 만들면서 트래커가 부풀어 오르는 걸 막는 장치다. `build-pr-block`은 머지 흐름이 잘못된 형태로 갈 때 막는다. 1인 + AI swarm 환경에서는 워커 브랜치에서 sprint 트렁크로는 직접 머지하고, sprint 트렁크에서 main으로만 PR을 쓰는 게 정책인데, 이 순서가 어긋나려 하면 hook이 잡는다.

각각이 한 가지 정책만 강제하는 작은 스크립트다. 9개가 동시에 돌면서 큰 시스템을 만들지 않고도 비슷한 효과를 낸다. 이게 1편에서 폐기한 22일치 시스템이 하려던 일을 대신하는 핵심 메커니즘이다.

### 3.6 git hooks 두 개

bash hook 외에 git hook도 두 개 추가했다. 하나는 commit 자체를 막는 검증, 다른 하나는 commit 메시지 형식 강제다.

`pre-commit`은 frontmatter 무결성을 일곱 항목으로 점검한다. 묶어 보면 세 가지 결이다. 형식 검증(스키마가 맞는가, 옛 필드나 옛 경로를 인용하고 있지 않은가), 의존성 검증(선행 문서를 가리키는 link가 끊겨 있지 않은가, 순환 의존이 생기지 않았는가, 선행 문서가 바뀌었는데 hash가 갱신되지 않았는가), 폴더 정책 검증(문서가 active/playbook/archive 같은 lifecycle 폴더 규칙을 따르고 있는가). 한 항목이라도 에러가 잡히면 commit이 막힌다. 여기에 매뉴얼 drift 검사를 한 단계 더 얹어서, 시스템 설정 파일을 손댔는데 사람이 읽는 매뉴얼(HANDBOOK)을 함께 갱신하지 않았다면 경고가 뜬다.

`commit-msg`는 commit 메시지 형식을 강제한다. Conventional Commits 형식이 아니면 commit이 거부되고, 워커 브랜치에서 만든 commit에는 어느 이슈를 다루는지 footer로 명시하도록 강제한다. sprint 트렁크나 팀 브랜치의 통합 commit, 단순 chore commit은 면제다.

---

## 4. Skill — `/sprint` 메타 스킬로 1주 사이클을 묶다

Hook이 정책을 강제하면, skill은 반복되는 작업의 리듬을 묶는다. 현재 두 개만 있다. `/sprint`와 `/promote-design-doc`이다. `/sprint`가 메인이라 그쪽을 자세히 본다.

### 4.1 6단계 구조

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

### 4.2 SSOT 네 곳을 한 번에 동기화한다

sprint를 운영하다 보면 정보가 네 곳에 흩어진다. `SPRINT.md`(루트, 지금 뭘 하나), Linear Cycle(거울, 누가 뭘 맡았나), Git history(추적, 뭘 했나), CHANGELOG와 tag(가시, 사용자에게 뭘 알릴까). 각각 한 가지 일만 한다는 점이 중요하다. 동기화 비용은 `/sprint`가 흡수한다. 사람은 어느 한 곳에만 정보를 적어 두고, 나머지로의 전파는 스킬이 떠맡는다.

### 4.3 prerequisite 4 옵션과 "사실상 했다" 판정 기준

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

### 4.4 사람이 직접 하는 일은 세 가지뿐

`/sprint`가 자리 잡고 나서 보니, 사람이 의식적으로 해야 하는 행동은 세 가지로 줄어들었다. commit prefix에 `dev-feat`, `dev-fix` 같은 보조 태그를 붙이는 일, 워커 브랜치 commit에서 `(refs INP-XX)` footer를 넣는 일, `/sprint research` 산출물(draft estimate)을 검토해서 승인하는 일. 그 외에는 Linear cycle 생성, INP 이슈 일괄 생성, area 라벨 매핑, SPRINT.md 작성과 동기, PR review 통합, Done 일괄 전환, CHANGELOG 갱신, tag 생성, 릴리스 노트 작성 모두 자동으로 흐른다.

---

## 5. Ownership-based DOCS — 71개에서 7개로

세 부품이 자리 잡으면서 문서 구조도 같이 바뀌었다.

이전에는 시간축으로 폴더를 잘랐다. `Phase1_Product/`, `Phase2_Design/`, `Phase3_Engineering/` 식이다. 1인 + AI swarm 환경에서는 "이 문서 누가 관리해?"라는 질문에 답하는 축이 부서(team)인데, Phase 분류로는 그게 안 잡혔다. 8명 에이전트가 동시에 여러 Phase 폴더를 만지면 ownership이 모호해지고 수정 충돌이 생긴다. 게다가 "지금 어느 Phase냐"는 질문 자체가 동적이다. v2.0 기획을 하면서 v1.9 버그도 고치고 있는 상황이 흔한데, Phase 폴더는 그걸 표현하지 못했다.

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

이 구조에서 핵심은 폴더 자체가 lifecycle의 SSOT가 된다는 점이었다. `active/`는 living(자주 변경), `playbook/`은 standard(운영 방식 정의), `artifacts/`는 immutable(시점 박제, 배포 시 생성), `drafts/`는 exploration(임시), `archive/`는 frozen(과거 참조용, 수정 불가)을 의미한다. lifecycle 정보를 frontmatter 필드로 따로 둘 필요가 없어졌다(2.1에서 폐기한 `lifecycle` 필드가 이래서 사라진 거다). 위치 자체가 정책을 표현하니까.

이 마이그레이션으로 active 상태로 살아 있는 문서가 71개에서 7개로 줄었다. 나머지 64개는 archive나 playbook이나 drafts로 옮겨 갔다. 매일 갱신해야 한다고 생각했던 문서 대부분이 사실은 frozen 상태로 두면 충분한 것들이었다.

---

## 6. 정체성별 폴더 분리 — RULES / HANDBOOK / SYSTEM / department

### 6.1 폴더 이름이 너무 광범위했다

ownership 마이그레이션이 자리 잡고 나서 또 다른 불편이 슬슬 보이기 시작했다.

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

### 6.2 분리 전후

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

### 6.3 폴더 이름이 정체성이 됐다

이렇게 갈라 놓고 보니 폴더 이름이 곧 그 안에 든 문서의 정체성이 됐다. RULES는 에이전트가 따라야 할 규칙이고, HANDBOOK은 사람이 읽는 운영 지침이고, SYSTEM은 시스템이 읽는 메타데이터고, department는 부서 owner가 관리하는 결과물이다. 새 문서를 만들 때 "이게 규칙인가, 매뉴얼인가, 메타인가, 산출물인가?"를 한 번만 자문하면 위치가 자동으로 결정된다. 그 갈등이 사라진 게 가장 컸다.

같은 날 commit `06f75d7`에서 HANDBOOK도 의존성 그래프에 편입시켰다. 시스템 파일(`.claude/CLAUDE.md`, `hooks/`, `scripts/`)이 변경되면 HANDBOOK 문서가 자동으로 STALE 전파 후보가 된다. commit `42bda4b`에서는 SYSTEM 분리도 마무리해서 `schemas/`와 `cache/`의 폴더 정책을 따로 두었다.

---

## 7. 사용자 정의 에이전트 — 컨텍스트를 자원으로 다루기

마지막 한 조각이 남는다. `.claude/agents/`에는 지금 11개의 사용자 정의 에이전트가 있다. CEO, Product Manager, UI/UX Designer, Frontend Engineer, Backend Engineer, Marketing Strategist, Ops Engineer, QA Engineer, FE QA, BE QA, 그리고 Knowledge Logger다. 사실 이 시리즈의 초기 draft 자체도 메인 AI가 직접 쓴 게 아니라 Knowledge Logger 에이전트에 위임한 결과를 받아서, 메인이 다시 다듬어 1편/2편으로 재구성한 것이다.

처음에는 이렇게까지 에이전트를 나눠 둘 필요가 있나 싶었다. 같은 모델 위에 시스템 프롬프트만 다른 11개를 두는 셈이라, 그냥 메인 AI 하나가 다 처리하면 되지 않나 싶었다. 운영해 보고 깨달은 건 두 가지 효과가 동시에 따라온다는 점이었다. 하나는 명시적인 효과, 하나는 부수 효과인데 부수 쪽이 생각보다 컸다.

명시적인 효과는 역할 분담이다. 각 에이전트가 자기 도메인의 시스템 프롬프트와 도구 셋과 모델(상황에 따라 sonnet/opus/haiku)을 따로 가진다. Frontend Engineer는 React/D3/Content Script 관련 문서를 자기 컨텍스트의 일부로 들고 시작하고, Backend Engineer는 IndexedDB/Supabase/storage 레이어 문서를 들고 시작한다. 메인이 매번 "이건 프론트 작업이니까 이 문서를 먼저 읽어"라고 컨텍스트를 다시 부여할 필요가 없다.

부수 효과가 컨텍스트 격리다. Claude Code에서 sub-agent를 호출하면 그 작업은 별도 컨텍스트 윈도우에서 돌아가고, 메인에는 sub-agent의 final 응답만 돌아온다. sub-agent가 중간에 읽은 파일, 호출한 도구, 시도하다 실패한 접근, 디버깅 과정의 로그 — 이런 것들이 메인 컨텍스트에 들어오지 않는다.

이게 어떤 차이를 만드는지는 같은 작업을 두 가지 방식으로 해 보면 보인다. 메인이 직접 한 시간짜리 디버깅을 한다면 그 한 시간치 도구 호출 결과(`grep`, `cat`, 실패한 `Edit`, 다시 시도한 `Edit`, 추가 `Read`)가 메인 컨텍스트에 누적된다. 다음 작업으로 넘어갈 때 그 누적이 그대로 따라온다. 같은 디버깅을 Frontend Engineer 에이전트에 위임하면 메인에는 "버그 고쳤어요, 원인은 X, 커밋은 Y"라는 한 줄짜리 보고만 돌아온다. 30분짜리 도구 호출 흔적은 sub-agent 컨텍스트에서 끝나고 사라진다.

위임이 만능은 아니다. 메인이 직접 수행한 일(나의 Read/Write/Edit/Bash 호출 결과)은 그대로 메인 컨텍스트에 누적된다. 그래서 어떤 작업을 직접 할지 어떤 작업을 위임할지가 작은 설계 결정이 된다. 빠른 한두 줄 수정은 직접 하고, 디버깅이 길어질 것 같거나 산출물 작성처럼 도구 호출이 많이 쌓일 작업은 위임하는 식이다. 이 글의 초기 draft를 Knowledge Logger에 위임한 것도 같은 맥락이다. 글 한 편 쓰는 동안 사용된 Read/Write 호출과 검토 흔적이 모두 sub-agent 안에서 끝나도록.

이런 관점에서 보면 11개 에이전트는 역할 분담만을 위한 것도, 컨텍스트 격리만을 위한 것도 아니다. 둘이 같이 따라온다. 처음에는 역할 분담만 떠올렸는데, 운영해 보니 컨텍스트 격리 쪽이 1인 + LLM swarm 환경에서 의외로 큰 자원이라는 사실이 점점 분명해졌다.

---

## 8. 22일과 6일을 숫자로

전체를 다시 정리하면 1편의 22일과 이 글의 6일이 어떻게 갈렸는지 표 한 장에 들어온다.

| 지표 | Phase 2 (대시보드) | Phase 3 (hooks + ownership) |
|------|-------------------|---------------------------|
| 기간 | 22일 (04-06 ~ 04-28) | 6일 (04-28 ~ 05-03) |
| 총 commit | 109개 | 약 30개 (인프라만) |
| 인프라 비중 | 86~91% | 20~33% |
| 본 개발 시간 | 약 3일 | 약 3~4일 |
| 산출물 폐기율 | 100% (`ebede55`에서 일괄 삭제) | 0% (모두 운영 중) |
| 관리 대상 | skill 6 + shell 도구 5 + state 파일 | hook 9 + frontmatter 7필드 + lifecycle 폴더 5종 |
| 정책 1개 수정 시 영향 | 3~4개 파일 | 1개 파일 또는 1개 폴더 |

가장 인상적이었던 건 본 개발에 쓴 시간이 거의 같았다는 점이다. 22일짜리 Phase 2도 본 개발은 3일이었고, 6일짜리 Phase 3도 본 개발은 3~4일이었다. 인프라 시간만 19일에서 1~2일로 줄었다. 같은 결과물인데 비용이 한 자릿수 차이로 떨어진 셈이다.

어떻게 시간이 그렇게 줄었는지는 작은 사례 하나를 보면 잡힌다. 어느 sprint에서 frontmatter의 hash 정보가 어긋난 문서들이 잔뜩 발견된 적이 있다. hash가 어긋난다는 건 선행 문서가 바뀌었는데 후행 문서가 그걸 따라잡지 못했다는 신호다(§2.2의 hash 메커니즘). 처음엔 후행 문서들의 본문이 코드와 따로 놀고 있는 거라고 가정했고, 본문을 일일이 검토하고 다시 쓰는 데 네다섯 시간을 잡았다.

막상 문서들을 열어 보니 본문은 모두 이미 코드와 일치하고 있었다. 어긋난 건 본문이 아니라 hash 값 자체였다. 그래서 본문은 손대지 않고 hash만 새로 박는 식으로 정리했더니 작업이 30분 만에 끝났다. "본문이 outdated돼서 hash가 어긋났을 것"이라는 가정 하나를 잘못 잡았다가 정확히 잡은 것뿐인데, 작업 시간이 70% 줄었다.

이런 작은 패턴 하나하나가 쌓이면서 인프라 시간이 19일에서 1~2일로 줄었다. Phase 3가 한 일은 거대한 도구를 짓는 게 아니었다. 이런 자잘한 가정들을 한 번씩 정확히 잡고, 잡힌 패턴을 hook이나 폴더 정책으로 박아 두는 일의 반복이었다.

---

## 9. 다이어트 네 가지 원칙

전체를 정리하면서 남은 인식을 네 가지로 묶었다.

첫째, 새 SSOT를 만들지 않는다. 이미 Linear가 "누가 뭘 맡았나"를 들고 있고, SPRINT.md가 "지금 뭘 하나"를 들고 있고, git history가 "뭘 했나"를 들고 있고, CHANGELOG가 "사용자에게 뭘 알릴까"를 들고 있다. 여기에 다섯 번째 SSOT(상태 필드든, 모니터링 대시보드든)를 더 얹으면 동기화 비용이 그대로 N배가 된다. 그래서 새 doc을 추가하기 전에 한 번 자문한다. 이거 Linear로 충분하지 않나?

둘째, 위치가 정책을 표현한다. lifecycle을 frontmatter 필드로 두지 않고 폴더로 표현하면, 두 군데에 같은 정보를 적느라 어긋날 일이 사라진다. `active`에 있으면 living이고, `playbook`에 있으면 standard고, `artifacts`에 있으면 immutable이고, `archive`에 있으면 frozen이다. 위치가 곧 의미다.

셋째, 정체성이 위치를 결정한다. RULES는 에이전트가 읽고, HANDBOOK은 사람이 읽고, SYSTEM은 도구가 읽고, department는 부서 owner가 읽는다. 한 폴더에 다 두면 누구든 다 읽어야 하는 것처럼 보이지만, 갈라 놓으면 각자 자기 자리만 보면 된다. 컨텍스트가 그만큼 가벼워진다.

넷째, 시각화보다 자동화가 낫다. 대시보드는 "지금 뭘 하네"라는 정보를 줄 뿐이지만, hook은 "이건 해야 돼, 저건 안 돼"를 강제한다. 1인 팀에서는 정보가 부족해서 망하는 일보다 강제가 부족해서 망하는 일이 훨씬 잦았다. 1편에서 22일을 들여 그걸 확인했다.

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

처음부터 hook을 9개 다 만들 필요는 없다. spec-gate 하나만 있어도 "문서 없이 코드 못 짜는 흐름"은 잡힌다. integrity-sync까지 두 개면 후행 영향까지 보인다. 그 다음에 commit-user-gate처럼 안전 게이트를 한두 개 더 얹는 식으로 키워 가면 된다. `/sprint` 같은 메타 스킬은 한참 뒤에 와도 된다. 손으로 sprint를 한두 번 돌려 보면서 어떤 단계가 매번 똑같이 반복되는지 보고 나서 묶는 게 자연스럽다.

더 깊이 파고들고 싶으면 `.claude/CLAUDE.md`의 §12~14(hooks, git hooks, skills 레지스트리)와 `RULES/GIT_CONVENTIONS.md`의 commit prefix와 branch strategy 부분을 같이 보는 걸 권한다.

---

## 11. 마무리 — 1인의 강점 회복

1편에서 폐기한 대시보드는 "조직처럼 보이고 싶다"는 욕망에서 나왔다. 그런데 1인 + AI swarm의 본질적 강점은 큰 조직처럼 보이는 게 아니라 정반대다. 의사결정권이 한 곳에 있어서 합의가 빠르고, 설명할 팀원이 없어서 커뮤니케이션 부채가 0이고, 재검토할 단계가 없어서 즉시 실행할 수 있다. 대시보드와 회의실 미감은 이 강점을 침식한다. 강제된 정책과 명확한 위치가 1인의 생산성을 더 잘 끌어낸다.

작은 팀은 큰 팀처럼 보일 필요가 없다. 빠르고 정확하면 그걸로 충분하다. 그게 22일과 6일 사이에서 배운 한 줄 결론이다.

---

## 관련 노트

- [[2026-05-11-1인-개발-워크플로우-1편-context-오염과-22일-폐기]] — 1편: 문제 인지와 22일 폐기
- [[2026-05-04-ai-swarm-workflow-real-issues]] — 운영하면서 발견한 5가지 결함
- [[2026-05-04-linear-done-gate-hook-pattern]] — Linear Done 자동 차단 hook 패턴
- [[2026-05-10-build-pr-block-5-layer-backpropagation]] — 정책을 코드까지 박제하는 다층 안전망

## 참고 commit

- `8632fd1` — Phase 3-A ownership-based DOCS 마이그레이션
- `e7bb068` — frontmatter 다이어트 + git hooks
- `4a0dc53` — `/sprint` 6단계 메타 스킬
- `f926a5d` — RULES/HANDBOOK/SYSTEM 분리 (정체성별 폴더)
- `06f75d7` — HANDBOOK 의존성 그래프 편입
- `42bda4b` — SYSTEM 폴더 분리 완료
