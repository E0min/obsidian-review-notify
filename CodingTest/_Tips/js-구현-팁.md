---
title: JavaScript 코딩테스트 구현 팁
aliases:
  - js 코테 팁
  - 자바스크립트 코딩테스트
  - js coding test tips
type: concept
status: seedling
created: 2026-05-25
updated: 2026-05-25
tags:
  - codingtest
  - javascript
  - status/seedling
related:
  - "[[_MOC]]"
  - "[[출력조건-구조파악]]"
  - "[[../_strategy/풀이순서]]"
  - "[[../_strategy/공부법]]"
  - "[[../_theory/two-pointer]]"
  - "[[../../FE/javascript/배열-메소드]]"
source: []
migrated-from: "CodingTest/_strategy/js-구현-팁.md"
---

# JavaScript 코딩테스트 구현 팁

> TL;DR: 알고리즘보다 한 단계 아래 — JS 문법 선택과 사고 패턴으로 구현 속도를 올리는 실전 팁 모음.

---

## 사고 패턴

### 출력이 Yes/No면 → 여사건으로 접근

→ **상세: [[출력조건-구조파악]]** (a/~a, a/b, 다중 구조 판별 + 코딩 템플릿)

요약: 실패 조건 하나 발견 즉시 `return "No"`. 성공 조건 전체를 직접 증명하려 하지 말 것.

### 결과값이 배열 → map / filter / reduce 먼저 고려

| 목적 | 메서드 | 패턴 |
|------|--------|------|
| 각 요소 변환, 길이 동일 | `map` | `arr.map(x => 변환)` |
| 조건 충족 요소만 추출 | `filter` | `arr.filter(x => 조건)` |
| 단일 값으로 누산 | `reduce` | `arr.reduce((acc, x) => acc + x, 0)` |
| 변환 후 필터 | `map` + `filter` | 체이닝 |

```javascript
// 예: 양수만 뽑아서 두 배로
arr.filter(x => x > 0).map(x => x * 2);

// 예: 전체 합
arr.reduce((sum, x) => sum + x, 0);
```

`for`문도 맞지만 의도가 명확한 메서드가 실수가 적다.  
단, `break`가 필요하면 `for`문 사용 (`forEach`는 `break` 불가).

---

## 배열 조작

### 원본 보존이 필요할 때 → 스프레드로 복사 후 조작

```javascript
// sort()는 원본 변경 — 원본 필요하면 복사 먼저
const sorted = [...arr].sort((a, b) => a - b);

// 2D 배열 복사 (얕은 복사 — 내부 배열은 공유됨에 주의)
const copy = arr.map(row => [...row]);
```

### 배열 초기화

```javascript
// 길이 n, 모두 0
Array(n).fill(0)

// 길이 n, 인덱스값
Array.from({ length: n }, (_, i) => i)

// 2D 배열 n×m, 모두 false  
Array.from({ length: n }, () => Array(m).fill(false))
// ❌ Array(n).fill([]) — 내부 배열이 동일 참조라 전부 연결됨
```

### 스프레드로 인자 펼치기

```javascript
// Math.max에 배열 못 넘김 → 스프레드
Math.max(...arr)
Math.min(...arr)

// 배열 병합
const merged = [...a, ...b];
```

---

## 숫자 / 문자열

### 정수 변환

```javascript
parseInt('42')      // 10진수 파싱
+'42'               // 단항 + (빠름, 간결)
Number('42')        // 명시적, NaN 안전
Math.floor(n)       // 소수 버림
```

### 자릿수 / 자리 분해

```javascript
// 각 자릿수 배열로
String(n).split('').map(Number)  // [1, 2, 3, ...]

// 각 자릿수 합
String(n).split('').reduce((sum, d) => sum + +d, 0)
```

---

## 해시 (Map / Set)

### 빈도 카운트

```javascript
const freq = new Map();
for (const x of arr) {
    freq.set(x, (freq.get(x) ?? 0) + 1);
}
```

### 중복 제거

```javascript
const unique = [...new Set(arr)];
```

### 존재 여부 O(1)

```javascript
const seen = new Set(arr);
if (seen.has(target)) { ... }
```

---

## 정렬

```javascript
// 숫자 오름차순 (비교함수 필수 — 없으면 유니코드 정렬)
arr.sort((a, b) => a - b);

// 내림차순
arr.sort((a, b) => b - a);

// 문자열 한국어 포함
arr.sort((a, b) => a.localeCompare(b));

// 객체 배열: 특정 필드 기준
arr.sort((a, b) => a.score - b.score);
```

---

## 조기 종료

```javascript
// for...of는 break 가능
for (const x of arr) {
    if (조건) break;
}

// some — 하나라도 조건 충족하면 즉시 true 반환 (break 역할)
arr.some(x => x > 10);

// every — 하나라도 false면 즉시 중단
arr.every(x => x > 0);
```

---

## 주의사항

- `==` 대신 `===` — 타입 강제 변환 방지
- `Array(n).fill([])` 금지 — 레퍼런스 공유
- 숫자 정렬에 비교함수 없으면 문자열 정렬 (`[10, 9, 2].sort()` → `[10, 2, 9]`)
- `forEach`에서 `return`은 외부 함수로 전달 안 됨 (for문으로 교체)

---

## Related

- [[출력조건-구조파악]] — 사고 패턴 (a/~a, a/b, 다중) SSOT
- [[../_strategy/풀이순서]] — 제약 조건 → 알고리즘 선택 프로세스
- [[../_strategy/공부법]] — 학습 루프
- [[../_theory/two-pointer]] — 투포인터 패턴
- [[../../FE/javascript/배열-메소드]] — map/filter/reduce 상세
