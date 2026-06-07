---
title: Map 객체
aliases: [Map, JavaScript Map, Map vs Object, 맵]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/javascript, status/budding]
related:
  - "[[_MOC]]"
  - "[[원시타입-객체타입]]"
  - "[[배열-메소드]]"
  - "[[../../CS/data-structures/hash-table]]"
  - "[[../../CodingTest/_theory/해시-Set-Map]]"
source: []
migrated-from: ""
---

# Map 객체

> TL;DR: 키-값 쌍을 저장하는 해시 테이블. Object와 달리 **모든 자료형을 키로** 쓸 수 있고, **삽입 순서를 보장**하며, 크기를 `.size`로 즉시 확인. 탐색·삽입·삭제 모두 O(1).

---

## What

`Map`은 ES6에서 추가된 키-값 컬렉션. 내부적으로 해시 테이블로 구현되어 모든 연산이 O(1).

---

## Why it matters — Object와의 차이

| 비교 항목 | `Object` | `Map` |
|-----------|---------|-------|
| 키 타입 | 문자열, 심볼만 (나머지는 `.toString()` 강제 변환) | **모든 자료형** (함수, 객체, NaN도 가능) |
| 순서 보장 | 숫자 키 먼저 정렬, 그 다음 삽입 순서 | **삽입 순서 100% 보장** |
| 크기 확인 | `Object.keys(obj).length` | **`map.size`** (즉시) |
| 순회 | `for...in` (프로토타입 포함 위험) | `for...of`, `.forEach` (안전) |
| 직렬화 | `JSON.stringify` 바로 됨 | ❌ 별도 변환 필요 |
| 성능 | 단순 데이터 저장에 빠름 | 잦은 추가/삭제에 더 최적화 |

### 키 타입 차이가 핵심

```javascript
// Object — 객체를 키로 쓰면 "[object Object]"로 덮어씌워짐
const obj = {};
const keyA = { id: 1 };
const keyB = { id: 2 };
obj[keyA] = 'A';
obj[keyB] = 'B';
console.log(obj); // { '[object Object]': 'B' } ← 충돌!

// Map — 객체 자체가 키 (참조 기준)
const map = new Map();
map.set(keyA, 'A');
map.set(keyB, 'B');
console.log(map.get(keyA)); // 'A' ✅
console.log(map.get(keyB)); // 'B' ✅
```

---

## How — 주요 메서드

### 생성

```javascript
// 빈 Map
const map = new Map();

// 초기값으로 생성 — [키, 값] 쌍의 배열
const map2 = new Map([
  ['name', '홍길동'],
  ['age', 30],
  ['active', true],
]);
```

### CRUD

```javascript
const map = new Map();

// 추가/수정
map.set('key', 'value');      // Map 반환 → 체이닝 가능
map.set('a', 1).set('b', 2).set('c', 3);

// 읽기
map.get('key');               // 'value'
map.get('없는키');            // undefined

// 존재 확인
map.has('key');               // true
map.has('없는키');            // false

// 삭제
map.delete('key');            // true (성공), false (키 없음)

// 전체 삭제
map.clear();

// 크기
map.size;                     // O(1)
```

### 순회

```javascript
const map = new Map([['a', 1], ['b', 2], ['c', 3]]);

// for...of (가장 일반적)
for (const [key, value] of map) {
  console.log(key, value); // 'a' 1, 'b' 2, 'c' 3 (삽입 순서)
}

// forEach
map.forEach((value, key) => {
  console.log(key, value); // 주의: 콜백 인자 순서가 (value, key)
});

// 키만, 값만
for (const key of map.keys()) { ... }
for (const value of map.values()) { ... }

// 배열로 변환
const entries = [...map];           // [['a',1], ['b',2], ['c',3]]
const keys = [...map.keys()];       // ['a', 'b', 'c']
const values = [...map.values()];   // [1, 2, 3]
```

### Object 변환

```javascript
// Object → Map
const obj = { name: '홍길동', age: 30 };
const map = new Map(Object.entries(obj));

// Map → Object
const obj2 = Object.fromEntries(map);

// Map → JSON (직렬화)
JSON.stringify(Object.fromEntries(map));
```

---

## 코딩 테스트 활용 패턴

### 빈도 카운팅

```javascript
function countChars(s) {
  const freq = new Map();
  for (const char of s) {
    freq.set(char, (freq.get(char) ?? 0) + 1);
  }
  return freq;
}
// 'banana' → Map { 'b': 1, 'a': 3, 'n': 2 }
```

### 마지막 등장 인덱스 추적 (← 142086 패턴)

```javascript
const lastSeen = new Map();
for (let i = 0; i < s.length; i++) {
  const char = s[i];
  const dist = lastSeen.has(char) ? i - lastSeen.get(char) : -1;
  lastSeen.set(char, i);
}
```

### 그래프 인접 리스트

```javascript
const graph = new Map();
graph.set('A', ['B', 'C']);
graph.set('B', ['D']);
// 노드가 문자열/숫자 혼합이거나 객체일 때 Map이 안전
```

---

## Pitfalls

- **`forEach` 인자 순서**: `map.forEach((value, key) => ...)` — 배열의 `(item, index)`와 반대. 헷갈리면 `for...of [key, value]` 사용
- **JSON 직렬화 안 됨**: `JSON.stringify(map)` → `'{}'`. `Object.fromEntries(map)`으로 변환 후 직렬화
- **`get` 실패 시 `undefined`**: 존재 확인 없이 `map.get(key) + 1` 하면 `NaN` 발생 → `?? 0` 또는 `has()` 먼저
- **Object가 더 나은 경우**: 키가 항상 문자열이고 JSON 직렬화가 필요하면 Object가 심플

---

## 실무에서 Object vs Map 선택 기준

```
키가 문자열/심볼이고 JSON 직렬화 필요?
  └─ Yes → Object  (API 응답, config, DTO)
  └─ No  →
        키가 문자열이 아닌 타입?         → Map
        순서가 중요한가?                  → Map
        잦은 추가/삭제가 있는가?          → Map
        그냥 키-값 저장/탐색만?           → 둘 다 OK (Map이 의도 명확)
```

| 상황 | 추천 |
|------|------|
| API 응답 파싱, config 객체 | `Object` |
| 코딩테스트 — 빈도 카운팅, 인덱스 추적 | `Map` |
| 객체/함수를 키로 써야 할 때 | `Map` (Object는 불가) |
| 순서가 보장돼야 할 때 | `Map` |
| 크기를 자주 확인할 때 | `Map` (`.size`) |
| 프로퍼티 삭제가 잦을 때 | `Map` (`delete`가 V8 최적화 안 깸) |

---

## Related

- [[_MOC]] — JavaScript 전체 지도
- [[원시타입-객체타입]] — 참조 타입 이해 (Map 키도 참조 기준 비교)
- [[배열-메소드]] — 배열과 Map 변환 (`Object.entries`, spread)
- [[../../CS/data-structures/hash-table]] — Map이 O(1)인 원리 (해시 테이블 내부 구조)
- [[../../CodingTest/_theory/해시-Set-Map]] — 코테에서 Map/Set 활용 패턴

## Sources

- [MDN — Map](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Map)
