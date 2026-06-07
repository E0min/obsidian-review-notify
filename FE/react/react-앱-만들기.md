---
title: React 앱 만들기 (Vite)
aliases: [Vite React, npm create vite, React 프로젝트 생성]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding]
notion-url: https://www.notion.so/bd2dad7a316048e0ac8aa7ef4cc61668
related:
  - "[[_MOC]]"
  - "[[react-app-구동원리]]"
source: ["Notion: React"]
migrated-from: "Notion: React 앱 만들기 (Vite)"
---

# React 앱 만들기 (Vite)

> TL;DR: `npm create vite@latest`로 프로젝트 생성 후 `npm i` → `npm run dev`로 시작. `public/`은 정적 파일, `src/assets/`는 캐싱 최적화 이미지용.

## What

Vite를 사용해 React 프로젝트를 생성하고 개발 서버를 실행하는 표준 절차.

## Why it matters

Vite는 ESM 기반 HMR로 CRA 대비 빠른 개발 환경을 제공하며, 현재 React 생태계의 사실상 표준 빌드 도구다.

## How

```shell
npm init                    # Node.js 패키지 생성
npm create vite@latest      # Vite로 React 앱 생성
# framework: React, variant: JavaScript
npm i                       # 의존성 설치
npm run dev                 # 개발 서버 실행
```

**디렉토리 구조**:
- `public/` — 정적 파일 (폰트, favicon 등). 새로고침 시 매번 재로딩
- `src/` — 코드. `assets/` 이미지는 브라우저 캐싱됨
- `src/assets/` vs `public/`: assets는 import 필요, 캐싱 최적화됨

## Pitfalls

- `package.json`에 `"dev": "vite"` scripts 확인 필수
- `npm run dev` 안 될 때 위 스크립트 누락 확인

## Related

- [[_MOC]]
- [[react-app-구동원리]]

## Sources

- Notion: React 앱 만들기 (Vite)
