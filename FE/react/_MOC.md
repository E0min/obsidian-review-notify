---
title: React MOC
aliases: [React Map of Contents, React 목차]
type: moc
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/react, status/budding, type/moc]
related:
  - "[[../FE_MOC]]"
  - "[[../nextjs/_MOC]]"
source: ["Notion: React"]
---

# React MOC

> React 핵심 개념 지도. SPA 등장 배경 → 컴포넌트 기초 → 상태/이벤트 → 훅 → 성능 최적화 → 고급 패턴 순으로 학습.

---

## 기초

| 노트 | 핵심 |
|------|------|
| [[MPA-SPA]] | MPA vs SPA, CSR의 등장 배경 |
| [[react-앱-만들기]] | CRA vs Vite, 프로젝트 구조 |
| [[react-app-구동원리]] | Virtual DOM, 재조정(Reconciliation), 렌더링 파이프라인 |
| [[컴포넌트-라이프사이클]] | Mount → Update → Unmount 3단계 |

## 상태 & 이벤트

| 노트 | 핵심 |
|------|------|
| [[props]] | Props 흐름, PropTypes, 기본값 |
| [[props로-state-전달]] | 자식→부모 콜백 패턴, 상태 끌어올리기 |
| [[state]] | useState 원리, 불변성, 배치 업데이트 |
| [[state-사용자-입력]] | controlled vs uncontrolled, form 패턴 |
| [[이벤트-처리]] | 합성 이벤트, 이벤트 위임 |

## 라이프사이클 & 사이드이펙트

| 노트 | 핵심 |
|------|------|
| [[lifecycle-useEffect]] | useEffect 의존성 배열, cleanup |
| [[useEffect-라이프사이클]] | 클래스 ↔ 함수형 라이프사이클 대응표 |

## 훅

| 노트 | 핵심 |
|------|------|
| [[useRef]] | DOM 참조, 렌더링 무관 값 저장 |
| [[useReducer]] | 복잡한 상태 로직, dispatch 패턴 |
| [[useReducer-vs-useState]] | 선택 기준 비교표 |
| [[context]] | createContext, Provider, useContext |
| [[커스텀훅]] | 로직 재사용, 네이밍 컨벤션 |

## 성능 최적화

| 노트 | 핵심 |
|------|------|
| [[React-memo]] | 불필요 리렌더링 방지, props 비교 |
| [[useMemo]] | 비싼 계산 메모이제이션 |
| [[useCallback]] | 함수 참조 안정화, deps 배열 |
| [[compiler/memo-불필요]] | React Compiler가 memo를 자동화하는 원리 |

## 라우팅 & 자산

| 노트 | 핵심 |
|------|------|
| [[라우팅]] | React Router v6, BrowserRouter, useNavigate |
| [[폰트-이미지]] | 정적 자산 최적화, font-display |

## 상태관리 심화

| 노트 | 핵심 |
|------|------|
| [[상태-분류]] | Local/Server/URL/Form/Derived 5가지 상태 |
| [[상태관리]] | 라이브러리 선택 전 결정 트리 |
| [[zustand-심화]] | selective subscription, persist/devtools/immer |
| [[jotai-심화]] | atom, derived atom, async + Suspense |
| [[redux-toolkit-심화]] | createSlice, createAsyncThunk, RTK Query |
| [[tanstack-query]] | 서버 상태, optimistic update, infinite query |
| [[상태관리-패턴]] | State Machine, Compound Component, URL↔Store sync |

---

## 학습 순서 (딥다이브 권장)

1. **기초** (4) — MPA-SPA → react-앱-만들기 → react-app-구동원리 → 컴포넌트-라이프사이클
2. **상태 & 이벤트** (5) — props → props로-state-전달 → state → state-사용자-입력 → 이벤트-처리
3. **라이프사이클 & 사이드이펙트** (2) — lifecycle-useEffect → useEffect-라이프사이클
4. **훅** (5) — useRef → useReducer → useReducer-vs-useState → context → 커스텀훅
5. **성능 최적화** (4) — React-memo → useMemo → useCallback → compiler/memo-불필요
6. **라우팅 & 자산** (2) — 라우팅 → 폰트-이미지
7. **상태관리 심화** (7) — 상태-분류 → 상태관리 → zustand → jotai → redux-toolkit → tanstack-query → 상태관리-패턴

총 32개. 약 14-20시간 (1-2주 분량).

### 학습 루틴 (한 노트당)

```
1. 노트 열기 → frontmatter 갱신:
   confidence: 1
   last-reviewed: <오늘>
   study-count: 1
2. 본문 읽기 (TL;DR → What → How → Pitfalls)
3. 코드 예제는 직접 타이핑·실행 (옵션)
4. 30초 안에 핵심 한 줄로 설명할 수 있는가?
   - 가능: confidence: 2~3
   - 불가: confidence: 1, [[review-queue]] 추가
5. 30일 후 재방문 (아래 "복습 필요" 블록에 자동 노출)
   → study-count +1, last-reviewed 갱신, confidence 재평가
```

→ frontmatter 필드 정의: [[../../CLAUDE]] §3

---

## 학습 진행률

```dataview
TABLE confidence as "익숙도", last-reviewed as "마지막 학습", study-count as "횟수"
FROM "FE/react"
WHERE confidence
SORT confidence ASC, last-reviewed ASC
```

## 복습 필요 (간격 반복)

`confidence`가 낮을수록 짧은 주기. 1→3일, 2→7일, 3→14일, 4→30일, 5→60일.

```dataview
TABLE confidence as "익숙도", last-reviewed as "마지막", (date(today) - date(last-reviewed)).day as "경과일"
FROM "FE/react"
WHERE confidence AND last-reviewed AND
  ((confidence = 1 AND date(today) - date(last-reviewed) > dur(3 days)) OR
   (confidence = 2 AND date(today) - date(last-reviewed) > dur(7 days)) OR
   (confidence = 3 AND date(today) - date(last-reviewed) > dur(14 days)) OR
   (confidence = 4 AND date(today) - date(last-reviewed) > dur(30 days)) OR
   (confidence = 5 AND date(today) - date(last-reviewed) > dur(60 days)))
SORT confidence ASC, last-reviewed ASC
```

## 최근 7일 수정된 노트

본문 보강·정정·심화 메모 추가 등 어떤 변경이든 잡힘 (`file.mtime` 기반).

```dataview
TABLE file.mtime as "파일 수정", updated as "frontmatter updated", confidence
FROM "FE/react"
WHERE file.mtime >= date(today) - dur(7 days) AND file.name != "_MOC"
SORT file.mtime DESC
```

## 아직 안 본 노트

```dataview
LIST FROM "FE/react"
WHERE !confidence AND file.name != "_MOC"
SORT file.name ASC
```

## 익숙도 분포

```dataview
TABLE WITHOUT ID confidence as "익숙도", length(rows) as "노트 수"
FROM "FE/react"
WHERE confidence
GROUP BY confidence
SORT confidence ASC
```

---

## Currently Learning

- React Compiler 심화 → `[[compiler/memo-불필요]]`

## Core Ideas (evergreen 후보)

- 불변성: 상태를 직접 변경하지 않는다
- 단방향 데이터 흐름: props 아래로, 이벤트 위로
- Virtual DOM → 재조정 → 최소 DOM 업데이트

---

## Related

- [[../nextjs/_MOC]] — React 위에 올라가는 SSR 프레임워크
- [[../_MOC]] — FE 전체 지도
- [[../../CS/_MOC]] — 브라우저·렌더링 원리
- [[../../CLAUDE]] — 학습 추적 frontmatter 필드 정의
