---
title: fetch vs axios
aliases: [fetch, axios, HTTP 요청, XMLHttpRequest]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [fe/javascript, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[../../BE/api-design/zod]]"
  - "[[../../FE/nextjs/_MOC]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: fetch vs axios"
---

# fetch vs axios

> TL;DR: `fetch`는 브라우저/Node.js 내장 API로 별도 설치 없이 사용. `axios`는 JSON 자동 파싱·에러 처리·타임아웃·인터셉터 등 편의 기능이 풍부. 간단한 요청엔 fetch, 복잡한 API 레이어엔 axios.

---

## What

HTTP 요청을 보내는 두 가지 주요 방법:
- **`fetch`**: 브라우저 내장 Web API (Node.js 18+에서도 내장). Promise 기반.
- **`axios`**: 써드파티 라이브러리 (`npm install axios`). XMLHttpRequest 기반 (브라우저) + http 모듈 (Node.js).

---

## How

### GET 요청

```javascript
// fetch
const res = await fetch('https://api.example.com/users');
if (!res.ok) throw new Error(`HTTP error: ${res.status}`); // ← 수동 에러 처리
const data = await res.json();                              // ← JSON 파싱 별도

// axios
const { data } = await axios.get('https://api.example.com/users');
// JSON 파싱 자동, HTTP 에러(4xx/5xx)는 자동으로 throw
```

### POST 요청

```javascript
// fetch
const res = await fetch('/api/users', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' }, // ← 헤더 수동 설정
  body: JSON.stringify({ name: '영민', age: 28 }),  // ← JSON.stringify 필요
});
const data = await res.json();

// axios
const { data } = await axios.post('/api/users', { name: '영민', age: 28 });
// Content-Type: application/json 자동, JSON 직렬화 자동
```

---

## 비교 표

| 항목 | `fetch` | `axios` |
|------|---------|---------|
| **설치** | 불필요 (내장) | `npm install axios` |
| **JSON 파싱** | 수동 (`await res.json()`) | 자동 (`response.data`) |
| **에러 처리** | 4xx/5xx도 `ok: false`만 — throw 안 함 | 4xx/5xx에서 자동 throw |
| **타임아웃** | `AbortController` 수동 구현 | `timeout: 5000` 옵션 |
| **인터셉터** | 없음 | `axios.interceptors` (요청/응답 전처리) |
| **요청 취소** | `AbortController` | `AbortController` 또는 `CancelToken` |
| **Node.js 지원** | Node 18+ (내장) / 이전 버전은 `node-fetch` | 내장 (`http` 모듈 사용) |
| **번들 크기** | 0 KB | ~14 KB |
| **파일 업로드** | `FormData` 직접 | `FormData` + 자동 Content-Type |

---

## 에러 처리 패턴

```javascript
// fetch — 4xx/5xx를 직접 처리해야 함
async function getUser(id) {
  const res = await fetch(`/api/users/${id}`);
  if (!res.ok) {
    throw new Error(`Request failed: ${res.status} ${res.statusText}`);
  }
  return res.json();
}

// axios — catch로 바로 잡힘
async function getUser(id) {
  try {
    const { data } = await axios.get(`/api/users/${id}`);
    return data;
  } catch (error) {
    if (error.response) {
      // 서버가 응답했지만 4xx/5xx
      console.error(error.response.status, error.response.data);
    } else if (error.request) {
      // 요청은 보냈지만 응답 없음 (네트워크 오류)
    }
    throw error;
  }
}
```

---

## axios 인터셉터 — 공통 처리

```javascript
// 모든 요청에 Authorization 헤더 자동 추가
axios.interceptors.request.use(config => {
  config.headers.Authorization = `Bearer ${getToken()}`;
  return config;
});

// 401 응답 시 자동 로그아웃
axios.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      logout();
    }
    return Promise.reject(error);
  }
);
```

---

## fetch 타임아웃 — AbortController

```javascript
async function fetchWithTimeout(url, ms = 5000) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), ms);

  try {
    const res = await fetch(url, { signal: controller.signal });
    return await res.json();
  } finally {
    clearTimeout(timeout);
  }
}
```

---

## Next.js에서 fetch 확장

Next.js의 `fetch`는 Web API를 확장해 캐싱 옵션을 제공한다:

```typescript
// 정적 캐싱 (SSG처럼)
fetch('/api/data', { cache: 'force-cache' });

// 캐시 없음 (SSR처럼, 항상 최신)
fetch('/api/data', { cache: 'no-store' });

// ISR — 60초마다 재검증
fetch('/api/data', { next: { revalidate: 60 } });

// 태그 기반 On-demand Revalidation
fetch('/api/data', { next: { tags: ['data'] } });
// → revalidateTag('data') 호출 시 해당 캐시만 무효화
```

---

## Pitfalls

- **fetch는 네트워크 오류에서만 reject** — 4xx/5xx 응답은 `res.ok === false`로 확인 필요. 이를 모르면 에러 처리 없이 통과됨
- **fetch는 자동 JSON 파싱 없음** — `await res.json()` 누락 시 Response 객체를 받아 버그 유발
- **axios는 `data`에서 꺼내야 함** — `const data = await axios.get(url)` → 이미 `{ data, status, headers }` 구조. `data.data` 참조 실수 주의
- **Next.js의 fetch는 Server Component에서만 캐싱 옵션 동작** — 클라이언트에서 `next: { revalidate }` 써도 무시됨

---

## Related

- [[_MOC]] — JavaScript 전체 지도
- [[../../BE/api-design/zod]] — API 응답 데이터 검증 (fetch/axios 결과 파싱 후 Zod로 검증)
- [[../../FE/nextjs/_MOC]] — Next.js fetch 캐싱 전략

## Sources

- [MDN — fetch](https://developer.mozilla.org/ko/docs/Web/API/Fetch_API/Using_Fetch)
- [axios 공식 문서](https://axios-http.com/docs/intro)
