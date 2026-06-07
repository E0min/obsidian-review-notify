---
title: 해시 테이블 — O(1)의 원리
aliases: [hash table, 해시 테이블, hash map, 해시 함수, hash function, hash collision]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [cs/data-structure, status/budding]
related:
  - "[[../_MOC]]"
  - "[[../../CodingTest/_theory/해시-Set-Map]]"
  - "[[../../FE/javascript/Map-객체]]"
  - "[[../../FE/javascript/const-let-var]]"
source: []
migrated-from: ""
---

# 해시 테이블 — O(1)의 원리

> TL;DR: 해시 함수로 키 → 메모리 주소를 O(1)에 계산, RAM의 직접 접근(Direct Access)으로 위치를 한 번에 읽는다. 덕분에 데이터 크기와 무관하게 항상 일정한 시간이 걸린다.

---

## What

해시 테이블은 **키(Key)를 해시 함수에 통과시켜 인덱스로 변환**하고, 그 인덱스 위치에 값을 저장하는 자료구조.

JavaScript의 `Object`, `Map`, `Set`이 모두 해시 테이블 기반이다.

---

## Why it matters

배열로 값을 찾으려면 앞에서부터 순서대로 뒤져야 한다 → O(N).  
해시 테이블은 키만 알면 위치를 **즉시 계산**한다 → O(1).

| 자료구조 | 탐색 | 삽입 | 삭제 |
|---------|------|------|------|
| 배열 (순차 탐색) | O(N) | O(1) (끝) | O(N) |
| 정렬 배열 (이진 탐색) | O(log N) | O(N) | O(N) |
| **해시 테이블** | **O(1)** | **O(1)** | **O(1)** |

---

## How — 3단계 동작 원리

```
키(Key) 입력
    │
    ▼
해시 함수(Hash Function)
키를 고정 크기 정수(인덱스)로 변환
    │   예: hash("name") → 4829번지
    ▼
메모리 직접 접근(Direct Access)
RAM은 주소만 알면 O(1)로 해당 위치로 이동
    │
    ▼
값(Value) 읽기/쓰기
```

### 1. 해시 함수

키 문자열을 정수 인덱스로 바꾸는 공식. 단순화 예시:

```javascript
// 실제 엔진은 훨씬 복잡하지만 원리는 이것
function simpleHash(key, tableSize) {
  let hash = 0;
  for (const char of key) {
    hash = (hash + char.charCodeAt(0)) % tableSize;
  }
  return hash;
}

simpleHash("name", 100);  // → 예: 42
simpleHash("age", 100);   // → 예: 17
```

**핵심**: 입력 길이와 무관하게 연산 횟수가 **키 길이에만 비례** (키 길이는 보통 상수로 취급) → 사실상 O(1).

### 2. RAM 직접 접근 (O(1)의 물리적 근거)

RAM(메모리)은 **주소 → 값**의 배열. 주소만 알면 어느 위치든 동일한 시간에 접근 가능.

```
메모리 (단순화):
주소:  0    1    2  ...  42  ...  17  ...
값:   ...  ...  ...     "홍길동" ... 30  ...
```

해시 함수로 `"name" → 42`를 계산했으면, 메모리 42번지를 한 번에 읽는다.  
배열처럼 0, 1, 2 … 순서대로 훑지 않아도 된다.

### JavaScript에서의 실제 사용

```javascript
// Object — 문자열/심볼 키, 숫자 키는 자동 정렬
const lastSeen = {};
lastSeen['a'] = 5;    // hash('a') → 메모리 주소 → 5 저장
lastSeen['a'];        // hash('a') → 같은 주소 → 5 읽기 (O(1))

// Map — 모든 자료형 키 가능, 삽입 순서 보장
const map = new Map();
map.set('key', 42);   // O(1)
map.get('key');       // O(1)
map.has('key');       // O(1)
```

---

## 해시 충돌 (Hash Collision)

**서로 다른 키가 같은 주소로 계산되는 현상**.

```
hash("abc") → 42번지
hash("xyz") → 42번지  ← 충돌!
```

### 해결 방법 1: 체이닝 (Chaining)

같은 주소에 연결 리스트(또는 배열)를 붙여 여러 값을 저장.

```
42번지: ["abc": 1] → ["xyz": 2] → null
```

충돌이 많으면 리스트가 길어져 최악의 경우 O(N). 하지만 좋은 해시 함수 + 적당한 테이블 크기로 충돌을 최소화하면 평균 O(1) 유지.

### 해결 방법 2: 오픈 어드레싱 (Open Addressing)

충돌 시 다음 빈 슬롯을 찾아 저장. 메모리 효율적이지만 클러스터링 문제 발생 가능.

### V8(JavaScript 엔진)의 처리

V8은 객체 구조에 따라 내부 표현을 최적화한다:
- **Fast mode**: 고정된 프로퍼티 구조 → 숨겨진 클래스(Hidden Class)로 오프셋 직접 계산. 해시보다도 빠름
- **Dictionary mode**: 동적 프로퍼티 추가/삭제가 많을 때 → 해시 테이블로 폴백

```javascript
// Fast mode 유지 (권장)
const user = { name: '김철수', age: 30 }; // 구조 고정

// Dictionary mode로 폴백 (성능 저하 가능)
const obj = {};
obj.name = '김철수';
delete obj.name;       // delete는 Hidden Class 무효화
obj.age = 30;
```

---

## Pitfalls

- **Object vs Map 키 타입**: Object는 키가 항상 문자열/심볼로 강제 변환. Map은 모든 타입을 키로 사용 가능
- **`delete` 남용**: 프로퍼티 삭제는 V8 내부 최적화를 깨뜨림 → `undefined`로 설정하는 것이 나을 때도 있음
- **O(1)은 평균**: 해시 충돌이 극단적으로 많으면 O(N)까지 저하 가능 (실제 사용에서는 거의 발생 안 함)
- **순서 보장**: `Object`는 숫자 키를 먼저 정렬, 문자열 키는 삽입 순서. 순서가 중요하면 `Map` 사용

---

## Related

- [[../_MOC]] — CS 전체 지도
- [[../../CodingTest/_theory/해시-Set-Map]] — 코테에서 Set/Map 사용법 (O(1) 탐색 활용)
- [[../../CodingTest/_theory/시간복잡도와-디버그]] — O(1) vs O(N) 판단 기준
- [[../../FE/javascript/Map-객체]] — JS Map 객체 사용법 (해시 테이블의 실제 구현체)

## Sources

- [MDN — Map](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Map)
- [V8 Blog — Fast properties](https://v8.dev/blog/fast-properties)
