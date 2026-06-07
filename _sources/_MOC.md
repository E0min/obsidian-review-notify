---
type: moc
title: _sources — Raw Sources Layer
status: budding
updated: 2026-05-23
tags: [moc, sources]
---

# _sources — Layer 1 (Raw, Immutable)

> Karpathy LLM-Wiki의 **Raw Sources** 레이어. 원본 자료를 그대로 보관.
> **수정 금지** — LLM은 읽기만, 추출된 지식은 `<카테고리>/_concepts/`에 atomic으로.

## Sub-areas
- [[articles/_MOC|articles]] — 블로그/뉴스레터 스크랩
- [[papers/_MOC|papers]] — 논문 PDF + 요약
- [[videos/_MOC|videos]] — 영상 URL + 트랜스크립트
- [[books/_MOC|books]] — 책 노트
- [[screenshots/_MOC|screenshots]] — UI/디자인 영감, 에러 화면
- [[raw-notes/_MOC|raw-notes]] — 정제 안 된 메모 (나중에 atomic으로 추출)

## 운영 규칙
1. 새 source 추가 시 파일명: `YYYY-MM-DD-<slug>.md` 또는 `<author>-<title>.<ext>`
2. 메타 frontmatter: `source-type`, `url`, `accessed-date`, `author`, `extracted-to:` (어떤 _concepts로 추출됐는지)
3. 절대 본문 수정 금지 — 보정/요약은 별도 노트로

## See also
- [[../CLAUDE.md]] — wiki schema (운영 규칙)
- [[../_index]]
