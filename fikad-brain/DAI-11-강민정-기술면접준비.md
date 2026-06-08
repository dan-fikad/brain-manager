---
title: DAI-11 강민정 기술면접 준비
date: 2026-03-26
tags:
  - recruit
  - tech-interview
  - DAI-11
---

# 강민정 - 기술면접 준비 요약

## 후보자 프로필

| 항목 | 내용 |
|------|------|
| 학력 | 성신여대 컴퓨터공학과 졸업 (2022.03~2026.02) |
| 현재 | SSAFY 삼성 청년 SW AI 아카데미 (2026.01~) |
| 주력 언어 | Java, Python, JavaScript |
| 주력 프레임워크 | Spring Boot, Spring Data JPA, MyBatis |
| DB | MySQL, Oracle |
| 인프라 | AWS (EC2, RDS, ALB, S3, ECR), GCP, Docker, GitHub Actions, Jenkins |
| 자격증 | SQLD (2024.12), OPIc IL (2025.03) |
| 수상 | 카카오x구름 제13회 구름톤 in JEJU 최우수상, 멋사 트랜디톤 우수상 |

> [!warning] NestJS/TypeScript 경험 없음
> 채용 포지션은 Nest.js/Node.js 백엔드인데, 이력서상 NestJS/TypeScript 경험이 없음. Node.js Express + Sequelize 경험 1건(요리조리 프로젝트)만 있음. 과제(Yugacrew Point Service)에서 NestJS를 처음 사용한 것으로 추정.

## 프로젝트 경력 (6개, 전부 학교/사이드 프로젝트)

### 1. OlleStaff - 제주도 스텝/게스트하우스 매칭 (2025.03~2025.06)
- **실서비스 운영 중** (ollestaff.com) - 사업화 진행
- Spring Boot, JWT, Spring Data JPA, MySQL, GitHub Actions CI/CD, Sentry
- 공고/리뷰/채팅 핵심 API, RDB 기반 채팅 시스템 설계
- `lastReadMessageId` 기반 unread count 최적화, Soft Delete 설계

### 2. 미드니어 - 쇼핑몰 커머스 (2024.11~2025.02)
- Spring Boot, MyBatis, Docker, Jenkins CI/CD
- `SELECT FOR UPDATE` 기반 재고 동시성 제어 (과제와 유사한 패턴)
- 취소/교환/반품 트랜잭션 정합성, 도메인 책임 분리

### 3. CC - 교환학생 커뮤니티 (2024.06~2024.08)
- AI 챗봇: TextCNN 의도 분류 + KR-SBERT 임베딩 의미 검색
- Socket 기반 단일 응답 파이프라인

### 4. Blendish Back - 레시피 플랫폼 (2024.01~2024.02)
### 5. 요리조리 - Node.js 기반 레시피 서비스 (2024.05~2024.06)
### 6. iDollbom - 아이돌봄 매칭 (2024.07~2024.08)
- Thymeleaf 프론트엔드 직접 구현 (풀스택 경험)

## 활동/리더십
- 멋쟁이 사자처럼 13기 **운영진** - 기술 세션 진행, 코드 리뷰, 해커톤 기획/운영
- BEMORE 개발 소모임 운영
- Node.js 오픈소스 컨트리뷰션 (2025.08~10)
- 오픈소스 기여모임 10기 (2026.01~02)

---

## 과제 분석 (Yugacrew Point Service)

> [!info] 기존 분석 (이력서 미확인 상태에서 작성됨)
> 경로: `~/hr/recruit/web-fullstack-engineer/tech-interview/강민정-배경분석.md`

- NestJS + TypeScript + MySQL + TypeORM + Jest
- Controller-Service-Repository 3계층 분리
- **AsyncLocalStorage 기반 커스텀 트랜잭션 관리** - TypeORM 기본 방식 대신 명시적 제어
- **비관적 락 2단계**: 상품 단위 락 테이블 + 리뷰 레코드 단위 락
- **데이터 정합성**: MySQL generated column, append-only 포인트 이력
- 테스트: in-memory 모킹 서비스 단위 테스트 7개 (통합 테스트 없음)

> [!bug] 잠재적 이슈
> - `deleteReview`에서 리뷰 락 -> 상품 락 순서가 `createReview`와 반대 -> **데드락 가능성**
> - `getUserPointSummary`에서 전체 이력 JS 합산 -> DB SUM 대비 비효율
> - Git 커밋 5개뿐, AI 도구 관련 문서 없음

---

## 이력서 기반 업데이트된 분석

> [!tip] 이력서에서 새로 파악된 점
> 1. **신입** - 직무 경력 0년, 전부 프로젝트 경험
> 2. **NestJS는 과제에서 처음 사용**한 것으로 보임 (이력서에 NestJS 미기재)
> 3. **동시성 제어 경험 있음** - 미드니어 프로젝트에서도 SELECT FOR UPDATE 사용
> 4. **AI/NLP 경험** - TextCNN, SBERT, KoNLPy 등 (CC 프로젝트)
> 5. **실서비스 운영 경험** - OlleStaff 사업화 진행 중
> 6. **리더십** - 멋사 운영진으로 기술 세션, 코드 리뷰, 해커톤 운영
> 7. **오픈소스 기여 경험** - Node.js 컨트리뷰션

---

## 기술면접 질문 (최종안)

> [!abstract] 면접 시간: 60분
> Intro 5분 / 질문 5개 x 8-10분 / Q&A 10분
> 시니어리티: 신입 (학부 졸업 직후, SSAFY 재학 중)

### Q1. 트랜잭션 관리 아키텍처 (8분)
**"AsyncLocalStorage 기반으로 TransactionManager를 직접 구현하셨는데, 이 방식을 선택한 이유가 뭔가요?"**

- 핵심 탐사: TypeORM 기본 방식 대비 장단점 인식, 중첩 트랜잭션/전파 이해, 롤백 시나리오
- ==이력서 기반 추가 질문==: "이력서에는 Spring Boot + JPA/MyBatis 경험이 주로 있는데, NestJS + TypeORM은 이번 과제에서 처음 쓴 건가요? Spring의 @Transactional과 비교하면 어떤 차이가 있었나요?"

### Q2. 동시성 제어 설계 (10분)
**"첫 리뷰 보너스에서 동시성 문제를 비관적 락으로 해결하셨는데, 이 문제를 어떻게 인식하게 됐나요?"**

- 핵심 탐사: 락 테이블 분리 의도, 비관적/낙관적 락 트레이드오프, 데드락 가능성
- ==이력서 기반 추가 질문==: "미드니어 프로젝트에서도 SELECT FOR UPDATE로 재고 동시성 제어를 하셨는데, 그때 경험이 이번 과제 설계에 영향을 줬나요? 두 프로젝트에서의 접근 방식 차이가 있다면?"
- 데드락 시나리오: createReview(상품락->리뷰저장) vs deleteReview(리뷰락->상품락) 순서 불일치

### Q3. 포인트 시스템 데이터 모델링 (8분)
**"포인트 이력을 append-only로 저장하고, 총점을 매번 이력 합산으로 계산하는 구조인데, 이 설계를 선택한 이유가 뭔가요?"**

- 핵심 탐사: totalPoints 컬럼 vs append-only 합산, JS 합산 vs DB SUM, 캐싱 전략
- 확장 시나리오: 포인트 만료, 포인트 사용(차감), 대규모 이력 시 성능

### Q4. 테스트 전략 (8분)
**"서비스 단위 테스트 7개를 작성하셨는데, 테스트 대상과 범위를 어떻게 정했나요?"**

- 핵심 탐사: in-memory 모킹 한계 인식, 통합 테스트 부재 이유, 실제 DB 테스트 경험
- ==이력서 기반 추가 질문==: "멋사 운영진으로 코드 리뷰를 하셨는데, 다른 분들의 테스트 코드를 리뷰할 때 어떤 기준으로 피드백했나요?"

### Q5. 기술 적응력과 성장 방향 (10분)
**"이력서 보면 주로 Spring Boot를 쓰셨는데, NestJS로 과제를 구현한 경험이 어땠나요?"**

- 탐사 포인트:
  - Spring -> NestJS 전환 시 학습 방법, 어려웠던 점
  - AI 도구 활용 여부 (코드에 한글 주석 다수 -> AI 생성 부산물 가능성)
  - OlleStaff 실서비스 운영하면서 가장 도전적이었던 기술 이슈
  - 육아크루 기술 스택(NestJS, PostgreSQL, AWS)과 본인 경험의 갭을 어떻게 메울 계획인지
  - SSAFY에서 현재 무엇을 배우고 있고, 앞으로 어떤 방향으로 성장하고 싶은지

---

## 면접 진행 가이드

| 시간 | 활동 | 비고 |
|------|------|------|
| 0-5분 | Intro, 자기소개 | 이력서 확인 완료 상태 |
| 5-13분 | Q1: 트랜잭션 관리 | NestJS 첫 경험 여부 확인 |
| 13-23분 | Q2: 동시성 제어 | 미드니어 경험과 연결 |
| 23-31분 | Q3: 데이터 모델링 | 성능 인식 |
| 31-39분 | Q4: 테스트 전략 | 실무 감각 |
| 39-49분 | Q5: 기술 적응력 | 성장 가능성 핵심 |
| 49-60분 | Q&A / 마무리 | |

> [!note] 평가 포인트
> - **신입이므로** 정답보다 사고 과정, 학습 태도, 트레이드오프 인식 능력 중심 평가
> - 과제 코드를 직접 작성했는지 자연스럽게 드러나도록 (Q1-Q3 구체적 질문)
> - 미드니어/OlleStaff 실전 경험과 과제 설계를 연결시키는 질문으로 깊이 확인
> - 육아크루 스택(NestJS + PostgreSQL + TypeORM)과의 갭 인식 및 메울 의지 확인

---

## 커피챗 (2026-03-17) 핵심 요약

- SSAFY 취업 시 중단하고 나올 것
- NestJS/TypeScript 학습 → "AI를 활용해서 공부하겠다"
- OlleStaff **실운영 서비스 아닌 것으로 확인됨**
- 성장 의지 매우 강함, 토스 가고 싶었다고 함
- PM/기획/디자인도 해보고 싶다고 함
- 장애 대응 → "바로 출동, 시니어에게 물어볼 것, 근본적 안정화 추구"

## 과제 상세 평가

| 평가 항목 | 점수 (5점) |
|----------|----------|
| 기능 완성도 | 4.5 |
| DB 설계 | 4.5 |
| 코드 구조 | 4.0 |
| 테스트 | 3.5 |
| 에러 처리 | 3.0 |
| OOP/설계 유연성 | 3.0 |
| 실무 관행 | 3.0 |

추가 발견:
- **.env 파일이 git에 커밋됨** (DB 비밀번호 포함)
- 인터페이스/추상 클래스 미사용 (구체 클래스 직접 DI)
- 글로벌 ExceptionFilter 부재
- README에 로컬 절대경로 링크 (`/Users/kangminjeong/...`)

## 채용 맥락

- **강소라** 님이 스택/경험 면에서 더 적합 (NestJS 주력, 3년 3개월 실무, 1인 백엔드 경험)
- 강민정은 **장기 투자 관점**에서의 평가 — AI/NLP 역량이 차별점

## Notion 기술면접 질문 (최종)

<a href="https://www.notion.so/fikadev/2026-3-32f73d236ad68054aa7dc3711f4526fe">강민정님 2026-3 (Notion)</a>

9개 질문, 60분 구성:
- Part A (20분): 코드 소유권 검증 — generated column, 트랜잭션, 동시성(데드락)
- Part B (15분): 설계 확장 — 포인트 성능, 요구사항 변경, 에러처리/.env
- Part C (10분): 실무 역량 — 테스트 전략, 육아크루 시나리오 + AI
- Part D (5분): 커밋 전략 & 회고
