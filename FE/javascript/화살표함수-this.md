---
title: 화살표 함수와 this 바인딩
aliases: [arrow function, 화살표함수, this binding, this 바인딩, lexical this]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/javascript, status/budding]
related:
  - "[[_MOC]]"
  - "[[배열-메소드]]"
  - "[[원시타입-객체타입]]"
source: []
migrated-from: ""
---

# 화살표 함수와 this 바인딩

> TL;DR: 일반 함수의 `this`는 **호출 시점**에 결정되고, 화살표 함수의 `this`는 **선언 시점** 바깥 스코프에서 상속된다. `map` 안에서 `this`가 필요하면 화살표 함수를 써야 한다.

---

## What — 두 가지 차이

화살표 함수와 일반 함수의 차이는 크게 두 가지다.

| | 일반 함수 `function() {}` | 화살표 함수 `() => {}` |
|--|--------------------------|----------------------|
| **`this` 결정 시점** | 호출할 때 (동적) | 선언할 때 바깥 스코프 (정적) |
| **`this` 값** | 누가 호출하느냐에 따라 달라짐 | 항상 바깥의 `this` |
| **`arguments` 객체** | 있음 | 없음 |
| **생성자로 사용** | 가능 (`new`) | 불가 |
| **암묵적 return** | 없음 (반드시 `return`) | 중괄호 없으면 자동 return |

---

## Why it matters — `map` 안에서 무슨 일이?

### 일반 함수를 쓰면 `this`가 바뀐다

```javascript
const team = {
  name: '드림팀',
  members: ['영민', '지수', '민준'],

  greet() {
    // 여기서 this = team 객체 ✅
    return this.members.map(function(member) {
      // 여기서 this = ??? ← 문제 발생!
      return `${this.name}: ${member}`; // TypeError 또는 undefined
    });
  }
};

team.greet(); // ['undefined: 영민', 'undefined: 지수', 'undefined: 민준']
```

**이유**: `map`에 넘긴 `function`은 `map`이 내부적으로 호출한다.  
호출하는 주체가 `map`(or 엔진)이 되므로 `this`가 `undefined`(strict mode) 또는 `window`(non-strict)로 바뀐다.

### 화살표 함수를 쓰면 `this`가 고정된다

```javascript
const team = {
  name: '드림팀',
  members: ['영민', '지수', '민준'],

  greet() {
    // 여기서 this = team 객체 ✅
    return this.members.map(member => {
      // 화살표 함수는 자체 this가 없어서 바깥 this(= team)를 그대로 씀 ✅
      return `${this.name}: ${member}`;
    });
  }
};

team.greet(); // ['드림팀: 영민', '드림팀: 지수', '드림팀: 민준'] ✅
```

---

## How — `this` 결정 원리

### 일반 함수: 호출 방식에 따라 `this`가 결정됨

```javascript
function show() {
  console.log(this);
}

show();           // window (non-strict) / undefined (strict)
obj.show();       // obj
new show();       // 새로 생성된 인스턴스
show.call(other); // other
```

→ 같은 함수라도 **누가 호출하느냐**에 따라 `this`가 달라진다.

### 화살표 함수: 선언된 위치의 `this`를 캡처

```javascript
const obj = {
  value: 42,
  regular: function() {
    // 이 function 안에서 this = obj
    const arrow = () => {
      // 화살표 함수: 바깥(regular)의 this를 캡처 → obj
      console.log(this.value); // 42 ✅
    };
    arrow();
  }
};
```

화살표 함수는 **자기 자신의 `this`를 아예 갖지 않는다**.  
`this`를 참조하면 스코프 체인을 타고 올라가서 가장 가까운 일반 함수(또는 전역)의 `this`를 쓴다.

---

## 문법 차이 — 화살표 함수 축약 규칙

```javascript
// 일반 함수
[1, 2, 3].map(function(n) { return n * 2; });

// 화살표 함수 — 매개변수가 1개면 괄호 생략 가능
[1, 2, 3].map(n => { return n * 2; });

// 중괄호 없으면 return 자동 (암묵적 return)
[1, 2, 3].map(n => n * 2);  // ✅ 가장 짧은 형태

// 매개변수 없거나 2개 이상은 괄호 필수
[1, 2, 3].map((n, i) => `${i}: ${n}`);
[1, 2, 3].map(() => 0);

// 객체를 반환할 때는 소괄호로 감싸야 함 (중괄호가 함수 바디로 해석되는 것 방지)
[1, 2, 3].map(n => ({ value: n })); // ✅
[1, 2, 3].map(n => { value: n });   // ❌ undefined 반환 (바디로 해석됨)
```

---

## Pitfalls

### 메서드를 화살표 함수로 선언하면 `this`가 전역이 됨

```javascript
const obj = {
  name: '철수',
  // ❌ 메서드를 화살표 함수로 만들면 this가 전역(window/undefined)
  greet: () => {
    console.log(this.name); // undefined
  },
  // ✅ 메서드는 일반 함수(또는 축약 메서드)로
  greet() {
    console.log(this.name); // '철수'
  }
};
```

### 이벤트 핸들러에서 `this`가 필요하면 일반 함수 사용

```javascript
button.addEventListener('click', function() {
  console.log(this); // 클릭된 button 요소 ✅
});

button.addEventListener('click', () => {
  console.log(this); // window (또는 undefined) ❌ — 화살표 함수는 this 없음
});
```

### 객체를 반환하는 암묵적 return 실수

```javascript
// 중괄호를 쓰면 return이 있어야 함
[1, 2, 3].map(n => { n * 2 });     // [undefined, undefined, undefined] ❌
[1, 2, 3].map(n => { return n * 2; }); // [2, 4, 6] ✅
[1, 2, 3].map(n => n * 2);             // [2, 4, 6] ✅ (암묵적 return)
```

---

## 언제 무엇을 쓸까

```
map / filter / reduce 콜백
  └─ this가 필요 없음 → 화살표 함수 (간결)
  └─ this가 필요함   → 화살표 함수 (바깥 this 캡처)

객체 메서드 정의
  └─ 항상 일반 함수 (또는 축약 메서드)

이벤트 핸들러
  └─ this(이벤트 대상 요소)가 필요 → 일반 함수
  └─ 바깥 class/컴포넌트의 this 필요 → 화살표 함수
```

---

## Related

- [[_MOC]] — JavaScript 전체 지도
- [[this-바인딩]] — this가 결정되는 5가지 컨텍스트 전체 정리 (call/apply/bind 포함)
- [[배열-메소드]] — map에서 화살표 함수 실전 사용
- [[원시타입-객체타입]] — 참조 타입과 스코프 이해

## Sources

- [MDN — Arrow functions](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Functions/Arrow_functions)
- [MDN — this](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/this)
