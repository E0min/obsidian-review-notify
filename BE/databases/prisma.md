---
title: Prisma ORM
aliases: [Prisma, ORM, prisma client, prisma schema]
type: concept
status: budding
created: 2026-05-24
updated: 2026-05-24
tags: [be/database, status/budding, typescript]
related:
  - "[[../_MOC]]"
  - "[[../../FE/nextjs/서버-액션]]"
  - "[[../../FE/nextjs/앱라우터-데이터페칭]]"
source: []
migrated-from: ""
---

# Prisma ORM

> TL;DR: TypeScript-first ORM. `schema.prisma`로 모델 정의 → Prisma Client로 타입 안전 DB 쿼리 → Migrate로 스키마 관리.

---

## What

Prisma는 Node.js/TypeScript용 차세대 ORM. 3개 모듈로 구성된다:

| 모듈 | 역할 |
|------|------|
| **Prisma Client** | 자동 생성 타입 안전 쿼리 빌더 |
| **Prisma Migrate** | 선언적 스키마 기반 마이그레이션 |
| **Prisma Studio** | GUI 데이터 브라우저 |

지원 DB: PostgreSQL, MySQL, SQLite, MongoDB, CockroachDB, SQL Server

---

## Why it matters

- **타입 안전**: 쿼리 결과가 TypeScript 타입으로 자동 추론 — 런타임 타입 오류 원천 차단
- **스키마 단일 소스**: `schema.prisma`가 DB 구조 + 타입 정의 + 마이그레이션 이력을 모두 책임
- **생산성**: raw SQL 없이도 복잡한 관계 쿼리 가능 (join, nested include)

---

## How

### 설치 및 초기화

```bash
npm install prisma @prisma/client
npx prisma init  # schema.prisma + .env 생성
```

### schema.prisma 정의

```prisma
datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        Int      @id @default(autoincrement())
  email     String   @unique
  name      String?
  posts     Post[]
  createdAt DateTime @default(now())
  updatedAt DateTime @updatedAt
}

model Post {
  id        Int     @id @default(autoincrement())
  title     String
  content   String?
  published Boolean @default(false)
  author    User    @relation(fields: [authorId], references: [id])
  authorId  Int
}
```

### 마이그레이션

```bash
npx prisma migrate dev --name init        # 개발 마이그레이션 (DB 반영 + 히스토리 저장)
npx prisma migrate deploy                  # 프로덕션 배포 시
npx prisma db push                         # 마이그레이션 없이 스키마만 즉시 적용 (프로토타이핑)
npx prisma generate                        # Prisma Client 재생성
```

### Prisma Client 쿼리

```typescript
import { PrismaClient } from '@prisma/client';

const prisma = new PrismaClient();

// 단건 조회
const user = await prisma.user.findUnique({ where: { id: 1 } });

// 관계 포함 조회 (SQL JOIN)
const userWithPosts = await prisma.user.findUnique({
  where: { email: 'user@example.com' },
  include: { posts: { where: { published: true } } },
});

// 생성
const newUser = await prisma.user.create({
  data: { email: 'new@example.com', name: '홍길동' },
});

// 수정
await prisma.post.update({
  where: { id: 1 },
  data: { published: true },
});

// 삭제
await prisma.user.delete({ where: { id: 1 } });

// 트랜잭션
const [user, post] = await prisma.$transaction([
  prisma.user.create({ data: { email: 'a@b.com' } }),
  prisma.post.create({ data: { title: '첫 글', authorId: 1 } }),
]);
```

### Next.js에서 Prisma 싱글턴 패턴

```typescript
// lib/prisma.ts
import { PrismaClient } from '@prisma/client';

const globalForPrisma = globalThis as unknown as { prisma: PrismaClient };

export const prisma =
  globalForPrisma.prisma ?? new PrismaClient({ log: ['query'] });

if (process.env.NODE_ENV !== 'production') globalForPrisma.prisma = prisma;
```

> 개발 환경에서 핫리로드 시 PrismaClient 인스턴스가 중복 생성되는 것을 방지하는 패턴.

### Server Action에서 사용

```typescript
// app/actions.ts
'use server';
import { prisma } from '@/lib/prisma';

export async function createPost(title: string, authorId: number) {
  return prisma.post.create({ data: { title, authorId } });
}
```

---

## Pitfalls

- **`prisma generate` 누락**: `schema.prisma` 수정 후 반드시 실행. 안 하면 타입과 실제 DB가 불일치.
- **N+1 문제**: 루프 안에서 `findUnique` 반복 금지 → `include` 또는 `findMany` + `where: { id: { in: ids } }` 사용
- **개발 환경 싱글턴**: 위 싱글턴 패턴 없이 핫리로드 하면 "Too many Prisma clients" 경고 발생
- **`db push` vs `migrate dev`**: `db push`는 마이그레이션 히스토리 없음 → 팀 협업·프로덕션에서는 반드시 `migrate dev` 사용
- **`@updatedAt`**: Prisma가 자동 갱신하지만 `$executeRaw`(raw SQL) 사용 시 직접 관리해야 함

---

## Related

- [[../_MOC]] — BE 전체 지도
- [[../../FE/nextjs/서버-액션]] — Server Action에서 Prisma 호출 패턴
- [[../../FE/nextjs/앱라우터-데이터페칭]] — RSC에서 Prisma 직접 호출
- [[../api-design/zod]] — Prisma 결과를 Zod로 추가 검증

## Sources

- [Prisma 공식 문서](https://www.prisma.io/docs)
