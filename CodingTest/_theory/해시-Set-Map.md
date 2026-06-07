---
title: 해시 (Set, Map)
aliases: [hash, Set, Map, HashMap, HashSet, 해시, 해시 테이블]
type: concept
status: budding
created: 2026-05-23
updated: 2026-05-24
tags: [cs/algorithm, codingtest, status/budding, 자료구조]
notion-url: https://www.notion.so/Set-Map-11135c50238380c79370c8f7db5e9431
related:
  - "[[_MOC]]"
  - "[[그래프]]"
  - "[[트리]]"
  - "[[../../CS/data-structures/hash-table]]"
source: ["Notion: 코딩 테스트 알고리즘 이론"]
migrated-from: "Notion: 해시(Set, Map)"
---

# 🎶 해시 (Set, Map)

> TL;DR: Set은 중복 없는 값 집합(O(1) 삽입/탐색), Map은 모든 자료형을 키로 쓰는 키-값 쌍(O(1) 연산). 둘 다 해시 테이블 기반. Map은 삽입 순서 보장, Object는 숫자 키 정렬됨.

---

`Set`과 `Map`은 ES6에서 도입된 데이터 구조로, **해시 테이블** 기반으로 동작하는 매우 효율적인 자료구조이다.

---

# 1. Set

**중복 없는 값들의 집합**. 동일한 값은 한 번만 저장. 삽입 순서 유지. 모든 자료형 지원.

## Set의 주요 메서드

| 메서드 | 설명 | 시간복잡도 |
|--------|------|-----------|
| `new Set()` | Set 인스턴스 생성 | — |
| `add(value)` | 값 추가 (중복 무시) | O(1) |
| `has(value)` | 값 존재 여부 확인 | O(1) |
| `delete(value)` | 값 삭제 | O(1) |
| `clear()` | 모든 값 삭제 | O(n) |
| `size` | Set 크기 반환 | O(1) |
| `forEach(fn)` | 모든 값에 콜백 호출 | O(n) |
| `values()` | Iterator 반환 | O(1) |

## Set 사용 예시

```javascript
const set = new Set([1, 2, 3, 4, 4]); // 중복 4는 하나만 저장
console.log(set);       // Set { 1, 2, 3, 4 }
console.log(set.size);  // 4

set.add(5);
set.add(5); // 중복 무시
console.log(set);       // Set { 1, 2, 3, 4, 5 }

set.delete(1);
console.log(set.has(1)); // false

set.forEach(value => console.log(value)); // 2, 3, 4, 5

// 배열에서 중복 제거
const arr = [1, 2, 2, 3, 3, 4];
const unique = [...new Set(arr)]; // [1, 2, 3, 4]
```

---

# 2. Map

**모든 자료형을 키로** 사용할 수 있는 키-값 쌍 자료구조. 삽입 순서 유지. 해시 테이블 기반 O(1) 연산.

## Map의 주요 메서드

| 메서드 | 설명 | 시간복잡도 |
|--------|------|-----------|
| `new Map()` | Map 인스턴스 생성 | — |
| `set(key, value)` | 키-값 설정 (기존 키면 덮어쓰기) | O(1) |
| `get(key)` | 키에 해당하는 값 반환 | O(1) |
| `has(key)` | 키 존재 여부 확인 | O(1) |
| `delete(key)` | 키-값 쌍 삭제 | O(1) |
| `clear()` | 모든 키-값 삭제 | O(n) |
| `size` | 키-값 쌍 개수 | O(1) |
| `forEach(fn)` | 모든 쌍에 콜백 호출 (value, key 순서) | O(n) |
| `keys()` / `values()` / `entries()` | Iterator 반환 | O(1) |

## Map 사용 예시

```javascript
const map = new Map();
map.set('name', 'John');
map.set(1, 'one');
map.set(true, 'boolean');
map.set({}, 'object key도 가능');

console.log(map.get('name')); // 'John'
console.log(map.has(1));      // true
console.log(map.size);        // 4

map.delete('name');
console.log(map.has('name')); // false

map.forEach((value, key) => console.log(key, value));
// 1 'one'
// true 'boolean'
// {} 'object key도 가능'
```

---

# 3. Map vs 객체(Object) 비교

| 특징 | Map | 객체(Object) |
|------|-----|------------|
| **키의 자료형** | **모든 자료형** (객체, 함수 포함) | 문자열 또는 심볼만 |
| **순서 보장** | **삽입 순서 보장** | 숫자 키는 정렬됨, 나머지는 삽입 순서 |
| **메서드** | set/get/has/delete/size 제공 | 없음, 수동 조작 |
| **성능** | 해시 테이블 기반 **평균 O(1)** | 비슷하지만 특정 상황 느릴 수 있음 |
| **크기 확인** | `map.size` | `Object.keys(obj).length` |
| **직렬화** | JSON.stringify 미지원 | JSON.stringify 지원 |
| **용도** | 키 다양성, 대량 데이터, 순서 중요 | 단순 구조, JSON 표현, 프로토타입 활용 |

## 핵심 차이 — 키 자료형

```javascript
// Map: 모든 자료형 키 가능
const map = new Map();
map.set('string', 1);
map.set(42, 2);
map.set(true, 3);
map.set({}, 4);      // 객체 키
map.set(() => {}, 5); // 함수 키

// Object: 자동으로 문자열 변환
const obj = {};
obj[1] = 'one';       // '1'로 변환
obj[{}] = 'obj';      // '[object Object]'로 변환 — 충돌!
obj[() => {}] = 'fn'; // '[object Object]'로 변환 — 충돌!
console.log(obj);     // { '1': 'one', '[object Object]': 'fn' }
```

## 핵심 차이 — 순서

```javascript
// Map: 삽입 순서 그대로
const map = new Map();
map.set('second', 2); map.set('first', 1); map.set(3, 'three'); map.set(1, 'one');
// Map { 'second' => 2, 'first' => 1, 3 => 'three', 1 => 'one' }

// Object: 숫자 키 먼저 정렬
const obj = {};
obj['second'] = 2; obj['first'] = 1; obj[3] = 'three'; obj[1] = 'one';
console.log(obj);
// { '1': 'one', '3': 'three', second: 2, first: 1 } ← 숫자 키가 앞으로
```

---

# 4. 코딩 테스트 활용 패턴

```javascript
// 빈도 카운팅 (Map)
function countFreq(arr) {
    const freq = new Map();
    for (const x of arr) {
        freq.set(x, (freq.get(x) || 0) + 1);
    }
    return freq;
}

// 중복 제거 (Set)
const unique = [...new Set([1, 2, 2, 3, 3])]; // [1, 2, 3]

// 방문 여부 체크 (Set — O(1) has)
const visited = new Set();
visited.add(nodeId);
if (visited.has(nodeId)) { /* 이미 방문 */ }

// 두 배열의 교집합 (Set)
const a = new Set([1, 2, 3]);
const intersection = [4, 5, 2, 3].filter(x => a.has(x)); // [2, 3]
```

---

## Related
- [[_MOC]]
- [[그래프]] — 방문 체크에 Set 사용 (BFS/DFS)
- [[Dynamic-Programming]] — 메모이제이션에 Map 사용

## Sources
- [Notion 원본](https://www.notion.so/Set-Map-11135c50238380c79370c8f7db5e9431)
