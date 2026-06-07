---
title: Next.js MOC
type: moc
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/nextjs, type/moc, status/budding]
related:
  - "[[../FE/_MOC]]"
---

# Next.js MOC

> React 프레임워크. SSR/SSG/ISR 사전렌더링 + App Router + RSC + Server Actions.

## 개요
- [[nextjs란]] — CSR vs SSR, Next.js 등장 배경
- [[nextjs-시작하기]] — 프로젝트 생성, _app.tsx, _document.tsx, next.config.js

## Page Router
- [[page-router]] — 파일 기반 라우팅 시스템
- [[라우팅-설정하기]] — 동적 경로, [id].tsx, [...id].tsx
- [[page-router-네비게이팅]] — Link, useRouter, router.push
- [[pre-fetching]] — 프리페칭 동작 방식
- [[api-routes]] — pages/api/ 서버 API 구현
- [[스타일링]] — 글로벌 CSS, CSS 모듈, CSS-in-JS

### 사전 렌더링
- [[ssr-getServerSideProps]] — 요청마다 서버에서 HTML 생성
- [[ssg-정적경로]] — 빌드 타임 정적 생성, getStaticProps
- [[ssg-동적경로]] — getStaticPaths + fallback 옵션
- [[isr]] — Incremental Static Regeneration, revalidate
- [[seo-설정하기]] — Head, 메타태그, OG 태그
- [[page-router-장단점]] — Page Router 한계와 보완책

## App Router
- [[app-router]] — RSC 기반 새로운 라우팅, page.js/layout.js/error.js
- [[레이아웃-설정하기]] — layout.js, 중첩 레이아웃, 라우트 그룹 ()
- [[rsc-이해하기]] — React Server Components 개념, Hook 불가 이유
- [[rsc-주의사항]] — 브라우저 코드 금지, import 방향, 직렬화
- [[앱라우터-네비게이팅]] — RSC 페이로드, 프리페칭 차이

### 데이터 페칭 & 캐싱
- [[앱라우터-데이터페칭]] — 서버 컴포넌트에서 직접 fetch
- [[데이터-캐시]] — cache:'no-store', revalidate 옵션
- [[request-memoization]] — 동일 요청 중복 제거 (페이지 범위)
- [[풀라우트-캐시]] — 빌드 타임 정적 페이지 캐시, generateStaticParams
- [[라우트-세그먼트-옵션]] — dynamic, revalidate, fetchCache, runtime
- [[클라이언트-라우터-캐시]] — RSC 페이로드 클라이언트 캐싱

### 스트리밍 & 에러
- [[스트리밍]] — loading.tsx (페이지), Suspense (컴포넌트)
- [[에러-핸들링]] — error.tsx, reset / router.refresh / window.reload

### 서버 액션
- [[서버-액션]] — 'use server', API Route 없이 서버 작업
- [[재검증하기]] — revalidatePath, revalidateTag
- [[useActionState]] — 폼과 서버 액션 연결
- [[useActionState-vs-useAction]] — 폼 제출 vs 버튼 이벤트

## 고급 라우팅
- [[병렬-라우트]] — @slot 병렬 렌더링, 조건부 렌더링, 모달
- [[인터셉트-라우트]] — (.) (..) (...) 경로 가로채기

## 최적화
- [[이미지-최적화]] — next/image, Lazy Loading, WebP, blur placeholder
- [[검색-엔진-최적화]] — metadata, generateMetadata, JSON-LD
- [[프로그래머틱-form-제출]] — useRef, requestSubmit()

## Related
- [[../FE/_MOC]] — FE 전체 MOC
- [[../react/_MOC]] — React 기초
