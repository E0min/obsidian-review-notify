---
title: Firebase Firestore — CRUD
aliases: [firebase, firestore, firebase database, NoSQL]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [be/databases, status/budding]
notion-url: ""
related:
  - "[[_MOC]]"
  - "[[prisma]]"
source: ["Notion: JavaScript"]
migrated-from: "Notion: Firebase"
---

# Firebase Firestore — CRUD

> TL;DR: Firestore는 Google의 NoSQL 클라우드 DB. 컬렉션-문서 계층 구조를 가지며, `addDoc/getDocs/onSnapshot/updateDoc/deleteDoc`으로 CRUD를 처리한다. 실시간 리스너(`onSnapshot`)가 핵심 차별점.

---

## What

Firebase Cloud Firestore는 Google Firebase 플랫폼의 NoSQL 문서형 데이터베이스. 클라이언트에서 직접 연결 가능하며, 실시간 데이터 동기화를 지원한다.

**데이터 구조**: 컬렉션(Collection) > 문서(Document) > 필드(Field)

```
firestore
└── users (컬렉션)
    ├── abc123 (문서 ID)
    │   ├── name: "영민"
    │   └── age: 28
    └── def456 (문서 ID)
        ├── name: "지수"
        └── age: 24
```

---

## How

### 1. 프로젝트 설정 및 SDK 설치

```bash
# Firebase CLI 설치
npm install -g firebase-tools

# Firebase 초기화
firebase login
firebase init

# SDK 설치
npm install firebase
```

```typescript
// src/lib/firebase.ts — Firebase 앱 초기화 (싱글톤)
import { initializeApp, getApps } from 'firebase/app';
import { getFirestore } from 'firebase/firestore';

const firebaseConfig = {
  apiKey: process.env.NEXT_PUBLIC_FIREBASE_API_KEY,
  authDomain: process.env.NEXT_PUBLIC_FIREBASE_AUTH_DOMAIN,
  projectId: process.env.NEXT_PUBLIC_FIREBASE_PROJECT_ID,
  storageBucket: process.env.NEXT_PUBLIC_FIREBASE_STORAGE_BUCKET,
  messagingSenderId: process.env.NEXT_PUBLIC_FIREBASE_MESSAGING_SENDER_ID,
  appId: process.env.NEXT_PUBLIC_FIREBASE_APP_ID,
};

// 중복 초기화 방지 (Next.js HMR 환경)
const app = getApps().length === 0 ? initializeApp(firebaseConfig) : getApps()[0];
export const db = getFirestore(app);
```

---

### 2. Create — 문서 추가

```typescript
import { collection, addDoc, setDoc, doc } from 'firebase/firestore';
import { db } from '@/lib/firebase';

// addDoc — ID 자동 생성
const addUser = async () => {
  const docRef = await addDoc(collection(db, 'users'), {
    name: '영민',
    age: 28,
    createdAt: new Date(),
  });
  console.log('생성된 문서 ID:', docRef.id);
};

// setDoc — ID를 직접 지정 (기존 문서 덮어쓰기)
const setUser = async (userId: string) => {
  await setDoc(doc(db, 'users', userId), {
    name: '영민',
    age: 28,
  });
};
```

---

### 3. Read — 문서 조회

```typescript
import { collection, getDocs, getDoc, doc, query, where, orderBy } from 'firebase/firestore';

// 컬렉션 전체 조회
const getUsers = async () => {
  const snapshot = await getDocs(collection(db, 'users'));
  const users = snapshot.docs.map(doc => ({
    id: doc.id,
    ...doc.data(),
  }));
  return users;
};

// 단일 문서 조회
const getUser = async (userId: string) => {
  const docRef = doc(db, 'users', userId);
  const snapshot = await getDoc(docRef);

  if (snapshot.exists()) {
    return { id: snapshot.id, ...snapshot.data() };
  } else {
    return null;
  }
};

// 쿼리 — 조건부 조회
const getAdultUsers = async () => {
  const q = query(
    collection(db, 'users'),
    where('age', '>=', 18),
    orderBy('age', 'asc')
  );
  const snapshot = await getDocs(q);
  return snapshot.docs.map(doc => ({ id: doc.id, ...doc.data() }));
};
```

---

### 4. 실시간 리스너 — `onSnapshot`

```typescript
import { onSnapshot } from 'firebase/firestore';

// 실시간 리스너 (데이터 변경 시 자동 콜백)
const subscribeUsers = () => {
  const unsubscribe = onSnapshot(collection(db, 'users'), snapshot => {
    const users = snapshot.docs.map(doc => ({
      id: doc.id,
      ...doc.data(),
    }));
    console.log('실시간 업데이트:', users);
  });

  return unsubscribe; // 컴포넌트 언마운트 시 호출해 구독 해제
};

// React에서 사용
useEffect(() => {
  const unsubscribe = subscribeUsers();
  return () => unsubscribe(); // cleanup
}, []);
```

---

### 5. Update — 문서 수정

```typescript
import { updateDoc, doc } from 'firebase/firestore';

// 특정 필드만 업데이트 (나머지는 그대로)
const updateUser = async (userId: string) => {
  const docRef = doc(db, 'users', userId);
  await updateDoc(docRef, {
    age: 29,
    updatedAt: new Date(),
  });
};
```

---

### 6. Delete — 문서 삭제

```typescript
import { deleteDoc, doc } from 'firebase/firestore';

const deleteUser = async (userId: string) => {
  await deleteDoc(doc(db, 'users', userId));
};
```

---

## Pitfalls

- **`NEXT_PUBLIC_` 환경 변수**: Firebase config는 클라이언트에서도 접근하므로 `NEXT_PUBLIC_` prefix 필수. 단, Firebase 보안 규칙(Security Rules)으로 접근 제어.
- **중복 초기화**: Next.js HMR에서 `initializeApp()`을 여러 번 호출하면 에러 → `getApps().length === 0` 체크 필수.
- **`onSnapshot` 메모리 누수**: 컴포넌트 언마운트 시 반드시 `unsubscribe()` 호출. `useEffect` cleanup에서 처리.
- **`doc.data()`에 타입 없음**: TypeScript 사용 시 `as UserType` 단언 또는 Zod로 검증 필요.
- **보안 규칙 기본값**: 테스트 모드로 생성하면 30일 후 모든 읽기/쓰기 차단. 프로덕션 전 Security Rules 설정 필수.

---

## Related

- [[_MOC]] — BE 전체 지도
- [[prisma]] — SQL 기반 ORM과의 비교 (Prisma = 관계형 DB, Firebase = 문서형)

## Sources

- [Firebase 공식 문서 — Firestore](https://firebase.google.com/docs/firestore)
- [Firebase SDK 레퍼런스](https://firebase.google.com/docs/reference/js)
