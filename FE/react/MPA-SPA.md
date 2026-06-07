---
title: MPA vs SPA
aliases: [MPA, SPA, CSR, SSR, Single Page Application, Multi Page Application]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/b5fb6f6397f74f0683a20ecb53684863
related:
  - "[[_MOC]]"
  - "[[라우팅]]"
source: ["Notion: React"]
migrated-from: "Notion: MPA vs SPA"
---

# MPA vs SPA

> TL;DR: MPA는 페이지마다 서버에서 HTML을 새로 받고, SPA는 첫 로드 이후 JS로 화면을 동적으로 업데이트한다. React는 기본적으로 SPA 방식이다.

## What

- **MPA** (Multi-Page Application): 페이지 이동 시 서버에서 새 HTML 전체 로드
- **SPA** (Single-Page Application): 첫 로드 후 JS로 동적 업데이트, 페이지 전환 없음

## Why it matters

아키텍처 선택에 따라 SEO, 초기 로딩 속도, 사용자 경험, 개발 방식이 모두 달라진다. React 프로젝트를 시작할 때 어떤 렌더링 전략을 선택할지 이해하는 기초 개념.

## How

| 항목 | MPA | SPA |
|------|-----|-----|
| 렌더링 방식 | SSR (서버 사이드) | CSR (클라이언트 사이드) |
| 페이지 전환 | 전체 새로고침 | JS 동적 업데이트 |
| SEO | 유리 | 불리 (SSR로 보완 가능) |
| 초기 로딩 | 빠름 | 느릴 수 있음 |
| 이후 인터랙션 | 매 요청마다 서버 통신 | 빠른 클라이언트 전환 |
| 적합한 서비스 | 쇼핑몰, 블로그, 뉴스 | 대시보드, SNS, 메일 앱 |

React는 기본적으로 SPA 방식 → `react-router-dom`으로 클라이언트 사이드 라우팅 구현.

## Pitfalls

- SPA의 SEO 문제 → Next.js SSR/SSG로 해결
- SPA 첫 로딩 느림 → Code Splitting(`React.lazy` + `Suspense`)으로 해결
- SPA에서 뒤로가기/북마크 처리 → 라우터 라이브러리 필수

## Related

- [[라우팅]] — React SPA에서 라우팅 구현 방법
- [[_MOC]]

## Sources

- [React 공식 문서 — Start a New React Project](https://react.dev/learn/start-a-new-react-project)
- Notion: React
