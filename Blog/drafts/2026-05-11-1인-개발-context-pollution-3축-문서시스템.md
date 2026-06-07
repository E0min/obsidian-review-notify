---
date: 2026-05-11
project: mindgraph
category: 02-Problem-Solving
tags: [claude-code, workflow, single-developer, context-management, ai-swarm, document-system, frontmatter, hook, skill, custom-agent, 1인-개발, context-drift, information-architecture]
source: "2026-05-11 회고 — 1인 개발의 역설, context 오염 발견, frontmatter+hook+skill 3축 시스템 진화, sub-agent isolation 메커니즘"
related_post: ""
---

# 1인 개발의 역설 — context 오염에서 3축 문서 시스템까지

## 1. 1인 개발은 정말 부채가 없나

흔히 1인 개발은 커뮤니케이션 부채가 없다고 한다. A와 B가 다른 맥락에서 일할 일이 없으니 맞는 말이긴 하다. 그런데 한참 굴려 보니 빠진 게 있었다. 사람과 사람 사이의 부채가 없는 대신, 나 자신의 과거 맥락과 현재 맥락 사이의 부채가 쌓이고 있었다.

예를 들면 이런 식이다. PRD에는 v1.0이라고 적혀 있는데 나는 이미 v1.5 sprint를 진행 중이다. 머릿속으로는 당연히 1.5라는 걸 알고 있으니까 별 문제가 안 된다. 그런데 AI 에이전트가 끼면 얘기가 달라진다. PRD v1.0을 읽은 에이전트는 자기가 지금 1.5를 만지고 있다는 걸 모른다. 이미 끝난 요구사항을 다시 구현하거나, 더는 유효하지 않은 문서를 정성껏 참조해서 엉뚱한 결과물을 내놓는다.

지나간 결정이 현재 작업의 맥락을 뒤덮는 이 현상을 나는 context 오염이라고 부르게 됐다. 사람은 직관적으로 걸러내는 정보를 AI는 문서가 말하는 대로 그대로 받아들이기 때문이다.

---

## 2. 디렉토리에 정책이 들어오기 시작했다

처음 MindGraph는 평범한 코드 프로젝트였다.

```
mindgraph/
├── src/                    # Chrome Extension, Next.js
├── web/                    # 웹앱 코드
├── DOCS/                   # 문서 모두 여기
└── README.md
```

코드가 중심이고 문서는 `DOCS/` 한 폴더에 다 모여 있었다. 그러다가 프로젝트가 자라면서 폴더 안의 종류가 늘기 시작했다. 디자인 결정이 생기니 `DESIGN.md`와 `DESIGN_TOKENS.md`가 들어왔고, 기획이 깊어지니 `PRD.md`, `FEATURES.md`가 추가됐다. 운영 지침도 자리를 잡아 `DEPLOYMENT.md`, `CI_CD.md`가 합류했고, QA를 챙기다 보니 `TEST_GUIDE.md`, `QA_CHECKLIST.md`도 필요했다.

어느 순간 `DOCS/` 폴더를 열면 멀미가 났다. 기획·디자인·개발·운영이 한 폴더에 뒤섞여 있으니 어떤 문서가 누구 책임인지, 지금 sprint와 관계있는지 한눈에 들어오지 않았다. 그래서 그쯤에 부서 단위로 디렉토리를 잘랐다.

```
department/
├── product/docs/
├── design/docs/
├── dev/docs/
├── qa/docs/
├── ops/docs/
└── CLAUDE.md   # 전사 헌장
```

각 부서 폴더 안에 그 부서가 책임지는 문서를 넣고, 최상위에는 부서를 가로지르는 공유 문서만 남겼다. 부서별로 `CLAUDE.md`를 따로 둬서 에이전트가 그 부서 안에서 일할 때 그 부서의 규칙만 읽도록 했다. 폴더가 책임과 소유권을 표현할 수 있다는 걸 처음으로 코드가 아닌 문서에 적용해본 순간이었다. 다만 이걸로는 아직 한참 부족했다.

---

## 3. PRD v1.0과 sprint v1.5가 동시에 살아 있을 때

지금 유효한 문서가 무엇인지 묻는 질문에 나는 그냥 기억으로 답한다. AI는 그러지 못한다. 참조하는 모든 문서를 동등한 권위로 본다.

이런 상황을 떠올려 보면 좋다. v1.0이 끝났다. 당시 PRD는 "root-topic UI는 카드 그리드 + 무한 스크롤"이라고 적혀 있었고 이미 그 모양대로 구현돼 있다. v1.5에서는 프로필 페이지와 북마크 기능을 새로 넣기로 했고 v1.5용 PRD를 별도 파일에 적었다. 여기서 AI에게 "홈페이지 리팩토링해" 하고 시키면 어떻게 될까. AI는 v1.0 PRD를 읽으면서 카드 그리드 + 무한 스크롤이라는 옛 명세를 끌어오고, 곧이어 v1.5 PRD를 읽으면서 프로필 페이지 얘기를 함께 본다. 둘이 충돌하는 부분에서 판단을 못 하거나, 옛 명세를 다시 구현하거나, 두 버전을 어색하게 섞어버린다.

더 미묘한 경우도 있다. v1.0 PRD가 여전히 `active` 폴더에 남아 있고 v1.5가 `drafts` 폴더에 가 있다면, AI는 "active가 권위 있는 위치"라고 합리적으로 추측한다. 결과는 v1.0을 기준으로 일을 진행하는 것. 사람은 머릿속에서 "v1.0은 이미 끝난 거니까 참조 금지"라는 규칙을 암묵적으로 갖고 있지만 AI에게는 그 암묵 규칙이 없다. 문서는 평등하고 시간 개념도 없다.

팀 프로젝트라면 PM이 옆자리에서 "지금 v1.5 작업해, 1.0 PRD는 보지 마"라고 일일이 말해 줄 텐데, 나 + AI 조합에서는 그 역할을 해 줄 사람이 없다. 결국 문서가 스스로 자기 유효 범위를 말해야 한다는 결론에 도달했다.

---

## 4. 첫 번째 답이 잘못된 답이었다 — 3주짜리 오버엔지니어링

이 불편을 인지하고 나니 자체 시스템을 만들어 보고 싶어졌다. 문서와 코드의 버전을 항상 동기화하는 인프라가 필요하다고 판단했다.

그렇게 그려본 설계는 이런 모양이었다. 모든 문서의 메타데이터(버전, 의존성, 상태, 마지막 갱신일)를 Python과 SQLite로 관리하고, tmux 대시보드 위에 문서 상태와 에이전트 상태, sprint 진행률을 실시간으로 띄운다. 거기에 8명짜리 가상 에이전트를 자동으로 할당하는 dispatcher를 붙이고, LangGraph 스타일로 "사용자 요청 → CEO 에이전트 → 부서별 위임 → 상태 추적"이 흐르도록 orchestration 레이어를 얹는다.

그렇게 3주를 쏟았다. 그 기간 동안 commit이 100개를 넘었는데, 다시 들여다 보니 거의 전부 인프라였다. MindGraph라는 원래 만들고 싶던 제품은 거의 진전이 없고, MindGraph를 만들기 위한 도구만 자라고 있었다. 어느 날 갑자기 한 가지 의심이 들었다. "잠깐, Claude Code 자체가 이미 AI agent 아닌가?"

내가 만들려던 건 LangGraph로 agent orchestration을 짓는 일이었는데, 이미 Claude Code가 그 역할을 하고 있었다. 비유하자면 Python 위에 또 하나의 Python을 짓는 셈이었다. 결국 인프라는 통째로 폐기했다. 다만 그 3주가 완전히 헛은 아니었던 게, 문제 자체는 분명히 실재한다는 것만은 확신을 갖게 됐다. 답이 잘못됐을 뿐이지 질문은 맞았다.

---

## 5. 두 번째 답 — frontmatter, hook, skill 세 부품

폐기 이후 방향을 거꾸로 잡았다. 거대한 시스템을 짓지 않고 Claude Code가 이미 가진 기능 위에 얇은 레이어만 얹기로 했다. 그렇게 추려진 부품이 frontmatter, hook, skill 세 개였다.

### 5.1 문서가 자기 의존성을 선언한다

모든 문서 머리에 메타데이터를 박아 둔다. 7개 필드면 충분했다.

```yaml
---
doc_type: PRD
team: product
status: APPROVED          # DRAFT | REVIEW | APPROVED | STALE | DEPRECATED
owner: product-manager
last_updated: 2026-05-11
depends_on:
  - path: RULES/PROJECT_STRUCTURE.md
    hash: 554628d51bb4
impacts:
  - department/dev/docs/FRONT/FRONTEND.md
---
```

핵심은 `status`, `depends_on`, `impacts` 세 필드다. `status`가 STALE이거나 DEPRECATED이면 AI는 그 문서를 권위 있는 출처로 받아들이지 않는다. `depends_on`은 이 문서가 어떤 상위 문서를 전제로 깔고 있는지를, `impacts`는 이 문서가 바뀌면 함께 흔들리는 후행 문서가 어디인지를 가리킨다. 의존성 그래프가 frontmatter 안에 자기서술 형태로 들어 있는 셈이다.

이제 v1.0 PRD에는 `status: ARCHIVED`를 박고 v1.5 PRD에는 `APPROVED`를 박는다. 완벽한 마법은 아니지만, 적어도 AI가 어떤 문서가 살아 있고 어떤 문서가 죽었는지 신호를 받을 수 있게 된다.

### 5.2 정책을 자동으로 강제한다

문서가 메타데이터를 선언하면 시스템이 무결성을 자동으로 점검할 수 있다. `.claude/hooks/`에 두는 셸 스크립트가 그 역할을 한다. 지금 9개를 쓰고 있는데, 가장 자주 발동하는 건 다음 셋이다.

`spec-gate.sh`는 코드 파일을 작성하기 직전 PreToolUse 단계에서 발동한다. 작성하려는 영역에 대응하는 필수 문서가 APPROVED 상태인지 확인하고, 아니면 `exit 2`로 작성을 막는다. 문서 없이 코드부터 짜는 흐름을 차단하는 게이트다.

`integrity-sync.sh`는 문서를 수정한 직후 PostToolUse에서 발동한다. 수정된 문서의 `impacts[]`를 읽어 후행 문서들을 STALE 후보로 알려준다. "이 문서가 흔들렸으니 저 문서도 같이 봐야 할 것"이라는 신호다.

`commit-user-gate.sh`는 `git commit` 명령 자체를 막는다. AI가 시각 검증 없이 commit으로 직행하는 흐름을 차단하고, 내가 명시 승인한 경우에만 marker 파일이나 환경변수로 한 번 풀어 준다.

나머지 hook도 비슷한 결이다. Linear 이슈 Done 전환 차단, 후속 결함을 기존 이슈에 묶도록 유도, 부서 간 교차 참조 안내, STALE 누적 경고, sprint 트렁크 PR 차단. 각각이 한 가지 정책만 강제하는 작은 스크립트인데, 9개가 동시에 돌면서 큰 시스템을 만들지 않고도 비슷한 효과를 낸다.

### 5.3 반복되는 워크플로우를 패턴으로 묶는다

Hook이 정책을 강제하면, skill은 반복되는 작업의 리듬을 묶는다. 현재 두 개만 있다.

`/sprint`는 6단계 메타스킬이다. `research → plan → build → qa → ship → retro` 순서로 sprint 한 사이클이 흐르고, 각 단계마다 어떤 gstack 스킬을 호출하고 어떤 산출물을 어디에 박제하는지가 SKILL.md에 박혀 있다. 1주 단위 sprint가 매번 비슷한 리듬으로 흘러가는 걸 한 스킬에 압축한 셈이다.

`/promote-design-doc`은 draft 산출물을 정식 위치(RULES 최상위 또는 부서 artifacts)로 승격시키는 스킬이다. 대화형으로 최종 위치를 고르고 frontmatter를 자동으로 갱신해 준다. 손으로 옮기다 frontmatter `promoted_from`을 빠뜨리는 실수를 줄이려고 만들었다.

---

## 6. 디렉토리 세 축 — 누가 읽는가로 갈라놓기

세 부품이 자리 잡으면서 디렉토리 구조 자체도 바뀌었다. 처음에는 부서별 분류만 있었는데, 어느 시점부터 "누가 이 문서를 읽는가"라는 축이 더 본질적이라는 느낌이 들었다. 그래서 최상위를 세 축으로 갈랐다.

```
mindgraph/
├── SYSTEM/                     # 기계가 읽음
│   ├── schemas/                # frontmatter-schema.json, doc-type-registry.yaml
│   └── cache/                  # .docs-index.db (SQLite, gitignore)
│
├── RULES/                      # 에이전트가 읽음 (8명 전체 또는 4+ 부서)
│   ├── AGENT_INSTRUCTIONS.md   # 에이전트 헌장
│   ├── GIT_CONVENTIONS.md      # Git 정책
│   ├── CODE_CONVENTIONS.md     # 코드 스타일
│   ├── PROJECT_STRUCTURE.md    # 아키텍처
│   ├── DESIGN-LANGUAGE.md      # StyleSeed Golden Rules
│   ├── SECURITY_POLICY.md      # 보안 정책
│   ├── CLAUDE.md               # 문서 헌장
│   └── INDEX.md                # 글로벌 토픽 맵
│
├── HANDBOOK/                   # 사람이 읽음
│   ├── 01_SYSTEM_OVERVIEW.md ~ 05_TROUBLESHOOTING.md
│   └── README.md
│
├── department/                 # 부서별 owner doc (lifecycle = 폴더)
│   ├── product / design / dev / ops / qa / marketing
│   │   └── docs/{active|playbook|artifacts|drafts|archive}/
│   ├── docs/                   # 메타 코디네이션
│   │   └── artifacts/sprints/v{X.Y}/{RESEARCH,PLAN,QA,RETRO}.md
│   └── CLAUDE.md               # 전사 헌장
│
└── .claude/
    ├── hooks/  (9)
    ├── skills/ (2)
    ├── agents/ (11)
    └── settings.json
```

`SYSTEM/`은 frontmatter 스키마와 의존성 그래프 캐시가 들어 있는 곳이다. 사람이 읽을 일은 거의 없고 검증 스크립트가 참조한다. `RULES/`는 에이전트가 자기 행동을 결정할 때 읽는 규칙들이다. 헌장, 컨벤션, 보안 정책 같은 것들이 모여 있고 4개 이상의 부서가 공통으로 읽거나 오케스트레이션상 필수인 문서만 여기에 둔다. `HANDBOOK/`은 그 반대편이다. "어떻게 이걸 써?" "문제 났을 때 어디부터 봐?"라는 사람의 질문에 답하는 실용 가이드라서, AI는 거의 안 읽고 사람만 본다.

`department/{team}/docs/` 아래에는 부서별 owner 문서가 들어가고, 그 안은 다시 `active / playbook / artifacts / drafts / archive` 다섯 폴더로 lifecycle을 표현한다. lifecycle을 frontmatter 필드로 두지 않고 폴더 위치로 박은 이유는 단순하다. 두 군데에 적으면 어차피 어긋난다. 위치만으로 의미가 통하면 그게 가장 단순하다.

처음에는 `DOCS/` 한 폴더가 있었고, 다음 단계에서는 부서별로 갈렸고, 마지막에는 읽는 주체별로 한 번 더 갈렸다. 폴더 위치만 봐도 그 문서가 누구에게 말하고 있는지가 자명해졌다.

---

## 7. 사용자 정의 에이전트가 컨텍스트를 아낀다

마지막 한 조각이 남는다. `.claude/agents/`에는 지금 11개의 사용자 정의 에이전트가 있다. CEO, Product Manager, UI/UX Designer, Frontend Engineer, Backend Engineer, Marketing Strategist, Ops Engineer, QA Engineer, FE QA, BE QA, 그리고 Knowledge Logger. 이 글 자체도 사실 메인 AI가 쓴 게 아니라 Knowledge Logger 에이전트에게 위임한 결과다.

처음에는 이렇게까지 분할할 필요가 있나 싶었다. 결국 깨달은 건 컨텍스트 윈도우를 자원처럼 다뤄야 한다는 것이었다.

새 sprint를 시작했다고 해 보자. 메인 AI 하나가 모든 단계를 직접 수행한다면, sprint 동안 코드를 짜고 에러를 보고 디버깅하고 PRD를 갱신하고 테스트를 돌리고 회고까지 쓰는 모든 과정이 메인 컨텍스트에 차곡차곡 쌓인다. 그 다음 작업으로 넘어가려고 하면 이미 컨텍스트가 무겁다. 이전 sprint의 디버깅 로그가 머릿속에서 안 지워지는 사람과 비슷한 상태가 된다.

sub-agent에 위임하면 흐름이 반대로 흐른다. Frontend Engineer 에이전트가 D3 zoom 이벤트 이중 바인딩 버그를 디버깅한다고 했을 때, 그 디버깅 과정 전체는 Frontend Engineer 자신의 격리된 컨텍스트 안에서만 일어난다. 메인에는 결과만 돌아온다. "버그 고쳤어요, 커밋 해시 XXXX, 원인은 reactStrictMode가 true라서 useEffect가 두 번 돌고 있었음." 그게 끝이다.

그 디버깅이 일반화할 가치가 있는 패턴이라면 Knowledge Logger가 이어받는다. 또 격리된 컨텍스트에서 Obsidian 노트를 쓰고 메인에 다시 결과만 보고한다. 메인 컨텍스트는 sprint 동안 거의 깨끗하게 유지되고, 다음 작업으로 넘어갈 때 부채 없이 시작할 수 있다.

이런 관점에서 보면 11개 에이전트는 역할 분담을 위한 게 아니라 컨텍스트 격리를 위한 장치다. 1인 + LLM swarm 구성에서 컨텍스트를 아키텍처처럼 설계하는 가장 작은 단위다.

---

## 8. 정리하며

3주의 오버엔지니어링을 폐기하고 다시 짜면서 남은 인식 세 가지가 있다.

첫째, 1인 개발에는 커뮤니케이션 부채 대신 자기 과거와의 동기화 부채가 있다. 사람과 사람 사이 메시지를 주고받을 일이 없어진 자리에, 어제의 결정이 오늘의 작업 맥락을 오염시키는 문제가 들어선다. 사람은 직관으로 거르지만 AI는 못 거르고 문서를 평등하게 본다. 그래서 문서가 자기 유효 범위를 frontmatter로 직접 말하도록 만든 게 첫 번째 답이었다.

둘째, 새 시스템을 짓지 말고 기존 인프라를 얇게 강화하는 편이 거의 항상 옳았다. tmux 대시보드와 Python + SQLite와 LangGraph 스타일 orchestration은 멋있어 보였지만, Claude Code가 이미 agent라는 사실 위에서는 잉여였다. frontmatter 7필드와 hook 9개와 skill 2개로 같은 효과를 더 적은 코드로 낼 수 있었다.

셋째, 컨텍스트 윈도우는 자원이고, 폴더 구조와 sub-agent는 그 자원을 효율화하는 아키텍처다. 폴더는 "이 문서가 누구에게 말하는가"를 표현해서 잘못된 참조를 줄여 주고, sub-agent는 "이 작업의 맥락을 어디까지 격리할 것인가"를 결정해서 메인 컨텍스트의 오염을 줄여 준다. 1인 개발자에게 컨텍스트 오염은 결국 멀티태스킹 오버헤드와 같은 비용이라서, 두 가지 다 그 비용을 깎는 장치였다.

이 글을 쓴 시점이 마침 v2.0-sprint-1을 D-2로 조기 마감하고 다음 sprint research draft를 띄워 둔 직후다. 같은 구조가 다음 사이클에서 어떻게 더 다듬어지는지는 또 다른 회고에서 적어 보려고 한다.

---

## 관련 노트

- [[2026-05-03-claude-code-workflow-3phase-evolution|Claude Code 워크플로우 3단계 진화]] — 같은 진화를 시스템 비용/편익 측면에서 본 글
- [[2026-05-04-ai-swarm-workflow-real-issues]] — 실제 운영하면서 발견한 5가지 결함
- [[2026-05-04-linear-done-gate-hook-pattern]] — Linear Done 자동 차단 hook의 5층 역전파
- [[2026-05-10-build-pr-block-5-layer-backpropagation]] — 정책을 코드까지 박제하는 5층 패턴
