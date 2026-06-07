---
title: this 바인딩
aliases: [this, this binding, 자바스크립트 this, call apply bind]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/javascript, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[화살표함수-this]]"
  - "[[원시타입-객체타입]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: 3. this"
---

# this 바인딩

> TL;DR: `this`는 **호출 방식**에 따라 동적으로 결정된다 — 전역·일반 함수·메서드·콜백·생성자 각각 다른 `this`를 가지며, `call/apply/bind`로 명시적으로 고정할 수 있다.

---

## What

`this`는 현재 실행 중인 함수가 어디에 속하는지를 나타내는 특수 키워드. 자바스크립트에서 `this`는 **선언 시점이 아니라 호출 시점**에 결정된다 (화살표 함수 제외).

---

## How — 5가지 컨텍스트

### A. 전역 컨텍스트 — `this = window / global`

```javascript
// 브라우저
console.log(this); // window

// Node.js
console.log(this); // global (또는 모듈 스코프에서는 {})
```

최상위 스코프에서 `this`는 전역 객체를 가리킨다.

---

### B. 메서드 컨텍스트 — `this = 호출한 객체`

```javascript
const user = {
  name: '영민',
  greet() {
    console.log(this.name); // '영민' ← user가 호출 주체
  }
};

user.greet(); // '영민' ✅
```

**메서드는 점(.) 앞의 객체가 `this`다.**

```javascript
// 주의: 메서드를 변수에 꺼내면 호출 주체가 사라짐
const fn = user.greet;
fn(); // undefined (strict) 또는 window.name (non-strict) ❌
```

---

### C. 일반 함수 컨텍스트 — `this = 전역 / undefined`

```javascript
function show() {
  console.log(this);
}

show();           // window (non-strict) | undefined (strict mode)
```

`'use strict'` 적용 시 독립 함수 호출의 `this`는 `undefined`.

```javascript
function outer() {
  console.log(this); // window

  function inner() {
    console.log(this); // 역시 window (중첩 함수도 독립 호출로 취급)
  }
  inner();
}
outer();
```

---

### D. 콜백 컨텍스트 — `this`가 바뀌는 함정

```javascript
const timer = {
  count: 0,
  start() {
    setTimeout(function() {
      this.count++; // ❌ this = window, count가 없음
      console.log(this.count); // NaN 또는 undefined
    }, 1000);
  }
};
timer.start();
```

콜백 함수는 **직접 호출**이므로 `this`가 전역으로 바뀐다.

**해결책 1: 화살표 함수 (바깥 `this` 캡처)**
```javascript
start() {
  setTimeout(() => {
    this.count++; // ✅ 화살표 함수 → 바깥 start()의 this = timer
    console.log(this.count);
  }, 1000);
}
```

**해결책 2: `self` 변수로 캡처 (ES5 방식)**
```javascript
start() {
  const self = this; // this = timer
  setTimeout(function() {
    self.count++; // ✅ 클로저로 캡처
  }, 1000);
}
```

---

### E. 생성자 컨텍스트 — `this = 새 인스턴스`

```javascript
function Person(name, age) {
  this.name = name; // 새로 생성된 인스턴스에 프로퍼티 추가
  this.age = age;
}

const me = new Person('영민', 28);
console.log(me.name); // '영민'
console.log(me.age);  // 28
```

`new` 키워드로 호출하면:
1. 빈 객체 생성
2. `this`가 그 객체를 가리킴
3. 함수 실행 후 `this`(새 객체) 자동 반환

---

## call / apply / bind — 명시적 this 고정

### `call(thisArg, ...args)` — 즉시 호출

```javascript
function introduce(job, hobby) {
  console.log(`${this.name}, ${job}, ${hobby}`);
}

const person = { name: '영민' };

introduce.call(person, '개발자', '코딩');
// '영민, 개발자, 코딩' ← this를 person으로 고정
```

### `apply(thisArg, [args])` — 즉시 호출, 인자는 배열

```javascript
introduce.apply(person, ['개발자', '코딩']);
// '영민, 개발자, 코딩'

// 활용: Math.max에 배열 전달
const nums = [1, 5, 3, 2];
Math.max.apply(null, nums); // 5
// ES6부터는 스프레드가 더 간결
Math.max(...nums);           // 5
```

### `bind(thisArg, ...args)` — this 고정된 새 함수 반환 (지연 실행)

```javascript
const boundIntroduce = introduce.bind(person, '개발자');
boundIntroduce('코딩'); // '영민, 개발자, 코딩'

// 이벤트 핸들러에서 자주 사용
class Button {
  constructor(label) {
    this.label = label;
    this.handleClick = this.handleClick.bind(this); // ← 미리 bind
  }
  handleClick() {
    console.log(this.label); // ✅ this가 Button 인스턴스로 고정
  }
}
```

| | `call` | `apply` | `bind` |
|--|--------|---------|--------|
| 실행 방식 | 즉시 | 즉시 | 나중에 (새 함수) |
| 인자 전달 | 쉼표 나열 | 배열 | 쉼표 나열 (부분 적용 가능) |
| 반환값 | 함수 실행 결과 | 함수 실행 결과 | 새 함수 |

---

## Pitfalls

- **메서드를 콜백으로 넘기면 `this`가 사라진다** — `setTimeout(obj.method, 1000)` 대신 `setTimeout(() => obj.method(), 1000)`
- **화살표 함수로 메서드 선언 금지** — 바깥 스코프의 `this`(전역)가 캡처됨 → [[화살표함수-this]] 참고
- **strict mode에서 독립 함수 호출의 `this`는 `undefined`** — `window`가 아님을 주의
- **이벤트 핸들러에서 일반 함수의 `this`는 이벤트 타겟 요소** (DOM 조작이 필요한 경우 유용)

```javascript
// 실수 사례
const team = {
  name: '드림팀',
  members: ['영민', '지수'],
  list() {
    this.members.forEach(function(m) {
      console.log(this.name + ': ' + m); // ❌ this.name = undefined
    });
  }
};
// 수정: forEach 콜백을 화살표 함수로 교체
```

---

## 요약 — 한눈에 보기

| 호출 방식 | `this` |
|-----------|--------|
| 전역 | `window` (브라우저) / `global` (Node.js) |
| 일반 함수 `fn()` | `window` (non-strict) / `undefined` (strict) |
| 메서드 `obj.fn()` | `obj` |
| 콜백 (일반 함수) | `window` / `undefined` ← 함정! |
| 콜백 (화살표 함수) | 바깥 스코프의 `this` |
| 생성자 `new Fn()` | 새 인스턴스 |
| `fn.call(x)` | `x` |
| `fn.apply(x)` | `x` |
| `fn.bind(x)()` | `x` |

---

## Related

- [[_MOC]] — JavaScript 전체 지도
- [[화살표함수-this]] — 화살표 함수에서 this가 어떻게 달라지는지 (map 콜백 중심)
- [[원시타입-객체타입]] — 참조 타입과 스코프 이해

## Sources

- [MDN — this](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Operators/this)
- [MDN — Function.prototype.call](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Function/call)
- [MDN — Function.prototype.bind](https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Function/bind)
