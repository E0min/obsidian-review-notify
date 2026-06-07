---
title: Zod 스키마 유효성 검사
aliases: [Zod, zod validation, 스키마 검증, schema validation]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [be/api, status/budding, typescript]
related:
  - "[[../_MOC]]"
  - "[[../../FE/nextjs/서버-액션]]"
  - "[[../databases/prisma]]"
source: []
migrated-from: ""
---

# Zod 스키마 유효성 검사

> TL;DR: TypeScript-first 스키마 선언 라이브러리. 스키마 하나로 런타임 유효성 검사 + TypeScript 타입 추론을 동시에 처리.

---

## What

Zod는 TypeScript 중심의 스키마 선언 및 유효성 검사 라이브러리.
- **런타임 검사**: 외부 입력(API 요청, 폼 데이터, 환경 변수)이 기대 구조인지 확인
- **타입 추론**: `z.infer<typeof schema>`로 TypeScript 타입 자동 생성 — 타입 중복 정의 불필요

---

## Why it matters

- **API 경계 보호**: 서버가 받는 입력을 신뢰하지 않는다는 원칙 구현
- **타입-런타임 일치**: TypeScript 타입은 컴파일 타임에만 존재 — Zod는 런타임에서도 검증
- **에러 메시지**: 중첩된 경로와 함께 구체적인 실패 원인 반환
- **환경 변수 검증**: 앱 시작 시 env 누락을 즉시 crash로 잡을 수 있음

---

## How

### 설치

```bash
npm install zod
```

### 기본 스키마 정의

```typescript
import { z } from 'zod';

// 원시 타입
const nameSchema = z.string().min(1).max(50);
const ageSchema = z.number().int().positive();
const emailSchema = z.string().email();

// 객체 스키마
const userSchema = z.object({
  name: z.string().min(1, '이름은 필수입니다'),
  email: z.string().email('유효한 이메일을 입력하세요'),
  age: z.number().int().min(0).optional(),
  role: z.enum(['admin', 'user', 'guest']).default('user'),
});

// 타입 추론
type User = z.infer<typeof userSchema>;
// { name: string; email: string; age?: number | undefined; role: "admin" | "user" | "guest" }
```

### 파싱 및 검증

```typescript
// parse: 실패 시 ZodError throw
const user = userSchema.parse({ name: '홍길동', email: 'hong@example.com' });

// safeParse: 실패 시 throw 없이 결과 객체 반환 (권장)
const result = userSchema.safeParse(req.body);
if (!result.success) {
  console.error(result.error.flatten()); // { fieldErrors: {...}, formErrors: [] }
  return res.status(400).json({ errors: result.error.flatten().fieldErrors });
}
const { name, email } = result.data; // 타입 안전
```

### 자주 쓰는 메서드

```typescript
// 배열
const tagsSchema = z.array(z.string()).min(1).max(10);

// 유니온
const idSchema = z.union([z.string(), z.number()]);
// 또는
const statusSchema = z.enum(['pending', 'active', 'deleted']);

// 변환 (transform)
const trimmedString = z.string().transform(s => s.trim());

// 세분화된 검증
const passwordSchema = z
  .string()
  .min(8, '8자 이상')
  .regex(/[A-Z]/, '대문자 포함')
  .regex(/[0-9]/, '숫자 포함');

// 조건부 필수 (superRefine)
const signupSchema = z
  .object({
    password: z.string(),
    confirmPassword: z.string(),
  })
  .superRefine(({ password, confirmPassword }, ctx) => {
    if (password !== confirmPassword) {
      ctx.addIssue({
        code: z.ZodIssueCode.custom,
        message: '비밀번호가 일치하지 않습니다',
        path: ['confirmPassword'],
      });
    }
  });
```

### Next.js Server Action에서 사용

```typescript
// app/actions.ts
'use server';
import { z } from 'zod';

const createPostSchema = z.object({
  title: z.string().min(1).max(100),
  content: z.string().min(10),
});

export async function createPost(formData: FormData) {
  const result = createPostSchema.safeParse({
    title: formData.get('title'),
    content: formData.get('content'),
  });

  if (!result.success) {
    return { errors: result.error.flatten().fieldErrors };
  }

  // result.data는 타입 안전한 { title: string; content: string }
  await prisma.post.create({ data: result.data });
}
```

### 환경 변수 검증

```typescript
// lib/env.ts — 앱 시작 시 즉시 실행
const envSchema = z.object({
  DATABASE_URL: z.string().url(),
  NEXT_PUBLIC_API_URL: z.string().url(),
  NODE_ENV: z.enum(['development', 'production', 'test']),
});

export const env = envSchema.parse(process.env);
// 누락된 env var 있으면 앱 구동 시 바로 crash → 프로덕션 배포 전 빠른 발견
```

---

## Pitfalls

- **`parse` vs `safeParse`**: API 핸들러에서 `parse`를 쓰면 try-catch 필수. `safeParse`가 더 안전.
- **`z.infer`는 Input 타입**: `transform`이 있으면 Output 타입은 `z.output<typeof schema>` 사용
- **중첩 객체 업데이트**: `.partial()`로 모든 필드를 optional로 만들거나 `.pick()`으로 특정 필드만 선택
- **`z.object` vs `z.record`**: 키가 고정이면 `object`, 동적 키-값 쌍이면 `record(z.string(), z.number())`
- **폼 데이터**: `FormData`에서 꺼낸 값은 모두 `string | null` — 숫자 필드는 `z.coerce.number()` 사용

```typescript
// FormData의 숫자 처리
const schema = z.object({
  age: z.coerce.number().int().positive(), // "25" → 25 자동 변환
});
```

---

## Related

- [[../_MOC]] — BE 전체 지도
- [[../../FE/nextjs/서버-액션]] — Server Action 입력 검증 패턴
- [[../databases/prisma]] — DB 접근 전 입력 검증 레이어로 조합
- [[../../FE/nextjs/useActionState]] — 서버 액션 에러를 폼에 바인딩

## Sources

- [Zod 공식 문서](https://zod.dev)
