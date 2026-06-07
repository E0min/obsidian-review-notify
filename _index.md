---
type: index
title: Dev — 세컨드 브레인
status: evergreen
updated: 2026-05-23
tags: [moc, home]
---

# Dev/ — Second Brain

> 평생 운영할 컴퓨터 공부 위키. 코드는 `~/깃허브/`에, 지식은 여기에.
> 구조: **Karpathy LLM-Wiki 3-Layer** + Andy Matuschak evergreen notes.

직무 준비: **FE / Product Engineer / Forward Deployed Developer / AI-Native Builder**

## 3-Layer Architecture (Karpathy LLM-Wiki)

```
Layer 1 — Raw Sources (immutable)    : _sources/
Layer 2 — The Wiki (LLM-owned)       : 9개 카테고리 _concepts/
Layer 3 — Schema (LLM 운영 메뉴얼)   : CLAUDE.md
```

- **`_sources/`** ([[_sources/_MOC]]) — 원본 자료. 수정 금지. LLM은 읽기만.
- **9 categories** — LLM이 sources에서 추출·통합·유지하는 atomic 노트.
- **`CLAUDE.md`** — wiki 운영 규칙 (한 새 source가 들어왔을 때 어떻게 처리할지).

## Now
- [[_now]] — 현재 sprint, 현재 학습 주제 (한 페이지로)

## 9 Categories (Map of Contents)

- [[CS/_MOC|CS]] — 알고리즘, 자료구조, 네트워크, OS, DB, 시스템 디자인
- [[FE/_MOC|FE]] — React, Next.js, performance, browser, D3
- [[BE/_MOC|BE]] — API design, auth, DB, infra, observability
- [[Product/_MOC|Product]] — discovery, metrics, strategy, case studies
- [[DESIGN/_MOC|DESIGN]] — design systems, typography, UX patterns
- [[AI-Native/_MOC|AI-Native]] — Claude Code, agents, prompts, spec-driven
- [[CodingTest/_MOC|CodingTest]] — 알고리즘 풀이, 패턴 atomic
- [[Projects/_MOC|Projects]] — 각 프로젝트의 지식 레이어 (decisions, retro, learnings)
- [[Blog/_MOC|Blog]] — 발행/draft 글, 시리즈

## Cross-cutting

- [[_journal/_MOC|_journal]] — 날짜 기반 TIL (카테고리 횡단 일지)
- `_templates/` — 8종 표준 템플릿
- `_attachments/` — 이미지/PDF

## 운영 규칙 (요약)

- **atomic note**: 한 노트 = 한 개념. 재사용 가능하면 `_concepts/`로.
- **status**: `seedling` → `budding` → `evergreen` (Andy Matuschak)
- **승격(promote)**: Journal 핵심을 atomic으로 추출 → 카테고리 `_concepts/`로
- **링크 의무**: 모든 atomic은 최소 2개 `[[wikilink]]` 보유
- **태그**: `#status/*`, `#type/*`, `#fe/*`, `#career/*` 등 (계층형)

## 라이프사이클 루틴

- **매일**: `_journal/YYYY-MM-DD-*.md`
- **매주 일요일**: journal → `_concepts/` 승격 심사
- **매월**: MOC 갱신, 그래프 뷰 캡처
- **분기**: evergreen 승격, Blog 발행 후보 추출

## Migration Status (from MindGraph-TIL)

- [ ] Week 1: 골격 + 템플릿 + MOC stub
- [ ] Week 2: 02-Problem-Solving → FE/BE
- [ ] Week 3: 03-D3 + Projects/mindgraph
- [ ] Week 4: 01-Workflow → AI-Native
- [ ] Week 5: Blog + 05-Ops + Projects 골격
- [ ] Week 6: 취업/JD + CodingTest
- [ ] Week 12: MindGraph-TIL archive
