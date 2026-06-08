---
title: 피카디 클로드코드 스터디 - Harness Engineering & AI Workflow Design
date: 2026-04-01
tags:
  - study
  - claude-code
  - harness-engineering
  - ai-workflow
  - meeting
---

# 피카디 클로드코드 스터디 (2026-04-01)

> [!abstract] 요약
> Harness engineering의 개념, 주요 기업들(OpenAI, Anthropic, Toss, Channel.io)의 접근법, OPSX workflow, AI workflow 설계 패러다임을 정리한 스터디 문서.

---

## 1. Harness Engineering이란?

### 정의

Harness(마구)는 원래 말의 힘을 인간이 활용할 수 있게 해주는 도구. AI에서 harness란 **AI 에이전트가 안전하고 예측 가능한 방식으로 작동하도록 설계된 제어 구조 전체**를 말한다.

> [!important] 핵심 공식
> 모델 = CPU, 컨텍스트 윈도우 = RAM, 에이전트 하네스 = 운영체제, 에이전트 = 애플리케이션
> — Phil Schmid

### Harness ≠ 프롬프트

Harness에는 **리포지토리 구조, 문서 체계, 린터/CI, 피드백 루프, 에이전트 간 통신 프로토콜, 컨텍스트 관리 전략**이 모두 포함된다.

### 왜 지금인가?

- 2025년 = 에이전트의 해
- 2026년 = **하네스의 해**
- "모델이 다 해결해줄거다" → 아직은 아닌 것으로 확인됨
- 에이전트 수 증가 → 동작 불안정, 출력 품질 편차, 보안 사고가 현실적 문제로 부상

### Harness의 3대 기능

| 기능 | 설명 |
|------|------|
| **제어(Control)** | 에이전트가 허용된 범위 밖의 행동을 하지 않도록 제한 |
| **감시(Monitoring)** | 동작 상태와 출력 결과를 실시간 추적/기록 |
| **개선(Feedback)** | 오류/이상 동작을 감지하고 다음 동작에 반영하는 피드백 루프 |

---

## 2. 주요 기업들의 접근법

### 2-1. OpenAI — "에이전트의 세계를 구축하라"

> <a href="https://openai.com/index/harness-engineering/">OpenAI — Harness Engineering</a>

5개월간 **수동 코드 0줄**로 100만 줄 제품을 만든 실험. 3명 → 7명 엔지니어, 1,500 PR, 엔지니어당 3.5 PR/일.

**핵심 원칙:**

1. **지도를 주지, 백과사전을 주지 마라** — AGENTS.md는 ~100줄짜리 "목차". 상세 지식은 구조화된 `docs/` 디렉토리에. Progressive disclosure.
2. **에이전트 가독성이 목표** — 코드베이스를 인간이 아닌 **Codex의 가독성**에 최적화. 에이전트가 접근할 수 없는 것은 존재하지 않는 것과 같다.
3. **불변량은 코드로 강제** — 아키텍처 규칙을 커스텀 린터로 검증. 린트 에러 메시지에 해결 방법까지 포함.
4. **"지루한" 기술 선택** — 에이전트가 모델링하기 쉬운 boring technology 선호.
5. **엔트로피 가비지 컬렉션** — 초기엔 매주 금요일(20%) AI slop 청소 → "golden principles"를 레포에 코드화하고 백그라운드 Codex 태스크로 자동 정리.

### 2-2. Anthropic — "GAN 영감의 적대적 피드백 루프"

> <a href="https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents">Effective Harnesses for Long-Running Agents</a>
> <a href="https://www.anthropic.com/engineering/harness-design-long-running-apps">Harness Design for Long-Running Apps</a>

**Phase 1: 2-agent 구조**

장기 실행 에이전트의 2가지 실패 패턴 해결:
- **Initializer agent** — 첫 세션에서 환경 구성: init.sh, feature_list.json, claude-progress.txt, 초기 git commit
- **Coding agent** — 매 세션마다 점진적 진행. 기능 하나씩만 작업. 끝날 때 git commit + progress 업데이트.

| 문제 | Initializer 해결 | Coding agent 해결 |
|------|-------------------|-------------------|
| 너무 일찍 완료 선언 | feature list JSON 설정 | 세션 시작 시 feature list 읽기 |
| 버그/미문서화 상태로 남김 | git repo + progress file 초기화 | 세션 시작 시 progress 읽기 + 기본 테스트 실행 |
| 기능 미검증 완료 표시 | feature list 설정 | Puppeteer MCP로 end-to-end 테스트 후에만 "passing" |

**Phase 2: 3-agent 구조 (GAN 영감)**

- **Planner** — 1~4문장 프롬프트를 풀 프로덕트 스펙으로 확장
- **Generator** — 스프린트 단위 구현. React + Vite + FastAPI + SQLite 스택
- **Evaluator** — Playwright MCP로 실제 앱을 조작하며 QA. 4가지 기준으로 평가

평가 기준:
1. **Design quality** — 색상, 타이포, 레이아웃이 하나의 정체성을 이루는가
2. **Originality** — 커스텀 결정이 있는가, 아니면 템플릿 기본값인가
3. **Craft** — 기술적 실행력 (타이포 계층, 간격, 색상 조화)
4. **Functionality** — 미적 요소와 독립적인 사용성

**Phase 3: Opus 4.6에서의 단순화**

> [!tip] 핵심 원칙
> 하네스의 모든 구성요소는 "모델이 혼자 못하는 것"에 대한 가정. 모델이 좋아지면 가정을 재검증하고 불필요한 것을 제거하라.

- Opus 4.5 → 4.6: 스프린트 분해와 컨텍스트 리셋 제거
- Evaluator는 태스크가 모델의 "솔로 능력" 경계에 있을 때만 가치 있음
- **4시간, $124로 브라우저 DAW 구현** (Planner 5분 $0.5 / Build 3시간 $114 / QA 25분 $10)

### 2-3. 두 접근법 비교

| 관점 | OpenAI | Anthropic |
|------|--------|-----------|
| 핵심 은유 | 에이전트의 "세계" 구축 | GAN 영감의 적대적 피드백 루프 |
| 품질 보장 | 린터 + CI + 정기 가비지 컬렉션 | 독립 Evaluator + Playwright QA |
| 인간의 역할 | "환경 설계자" — 코드 0줄 | "하네스 튜너" — 평가 기준과 프롬프트 조정 |
| 문서 철학 | Progressive disclosure (AGENTS.md = 목차) | Structured artifacts (feature_list.json + progress) |

### 2-4. Toss — "Software 1.0의 눈으로 3.0 바라보기"

> <a href="https://toss.tech/article/software-3-0-era">소프트웨어 3.0 시대란?</a>
> <a href="https://toss.tech/article/harness-for-team-productivity">당신의 팀은 같은 LLM을 쓰고 있나요?</a>

**Software 3.0 = LLM에게 자연어로 What을 말하면 되는 시대**

Claude Code harness를 레이어드 아키텍처로 매핑:

| Claude Code | Software 1.0 |
|-------------|-------------|
| Slash Command | Controller |
| Sub-agent | Service Layer |
| Skills | Domain Component (SRP) |
| MCP | Infrastructure / Adapter |
| CLAUDE.md | package.json |

**안티패턴도 그대로:**
- God Class → God Skill (3000줄짜리 skill)
- Spaghetti Code → Spaghetti CLAUDE.md
- Tight Coupling → MCP 없는 하드코딩

**팀 생산성 관점:**
- LLM 활용 격차 = "LLM Literacy" 노하우 격차
- 플러그인으로 정의된 지식 = **Executable SSOT** (사람이 읽으면 가이드, LLM이 읽으면 시스템 프롬프트)
- 마켓플레이스 = **워크플로우 배포 플랫폼 1.0** — B 엔지니어도 `/new-feature` 하나로 A 엔지니어와 동일한 품질

### 2-5. Channel.io — 보안 관점의 하네스

> <a href="https://channel.io/ko/blog/articles/what-is-harness-2611ddf1">하네스란? AI 에이전트를 안전하게 제어하는 설계 구조</a>

3대 구성요소: **가드레일 설치** (입출력 필터링) + **데이터 거버넌스** (접근 권한, 익명화) + **모니터링/피드백 순환**

Shadow AI(무단 AI 도입) 위험도 함께 다룸.

---

## 3. Comprehension Debt

> <a href="https://addyosmani.com/blog/comprehension-debt/">Addy Osmani — Comprehension Debt</a>

> [!warning] 핵심 경고
> Comprehension debt = 시스템에 존재하는 코드량과 인간이 실제로 이해하는 양 사이의 **점점 커지는 격차**. Technical debt와 달리 **거짓된 자신감**을 낳는다.

- Anthropic 연구: AI 어시스턴스 사용자가 후속 이해도 퀴즈에서 **17% 낮은 점수** (50% vs 67%)
- **속도 비대칭 문제** — AI는 인간이 평가할 수 있는 것보다 훨씬 빠르게 코드 생성
- 테스트만으론 불충분 — AI가 구현 변경 + 수백 개 테스트 케이스 동시 업데이트하면, "그 변경이 필요했는가?"는 이해력만이 답할 수 있음
- 스펙만으로도 불충분 — 프로그램을 완전히 기술하는 스펙은 비실행 언어로 작성된 프로그램과 같음
- **"코드 생성을 저렴하게 만든다고 이해를 건너뛸 수 있는 건 아니다. 이해 작업이 곧 일이다."**

### 대응: Managing Comprehension Debt

- **ARCHITECTURE.md** — <a href="https://architecture.md/">architecture.md 템플릿</a> 활용. 에이전트가 코드베이스를 빠르게 이해할 수 있는 구조화된 문서.
- RELIABILITY.md, SECURITY.md, DESIGN.md 등 지식 구조 설정
- Manual QA 유지
- Notion docs, Mermaid UML, Slack notification, summaries 등 보조 도구

---

## 4. OPSX Workflow

> <a href="https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md">OpenSpec — OPSX Workflow</a>

### OPSX란?

OpenSpec의 표준 워크플로우. **유동적이고 반복적인 워크플로우** — 고정된 단계가 아닌 언제든 취할 수 있는 액션.

### 핵심 철학: 단계가 아닌 액션

```
Legacy: PLANNING → IMPLEMENTING → ARCHIVING (locked)
OPSX:   new ↔ continue ↔ apply ↔ archive (fluid)
```

### 명령어 체계

| 명령어 | 역할 |
|--------|------|
| `/opsx:explore` | 아이디어 탐색, 문제 조사, 요구사항 명확화 |
| `/opsx:propose` | 변경 생성 + 기획 산출물 한번에 |
| `/opsx:continue` | 다음 산출물 생성 (의존성 기반) |
| `/opsx:ff` | 기획 산출물 일괄 생성 |
| `/opsx:apply` | 태스크 구현 |
| `/opsx:verify` | 구현 검증 |
| `/opsx:archive` | 완료 후 보관 |

### Looping Skill 활용

전체 흐름: `explore → refine → propose → implement → in review → review-pr → monitor-pr → deploy-verification → done`

- cron으로 `implement`, `review-pr`, `monitor-pr`, `deploy-verification` 자동 루핑
- `opsx:cron all`로 각 step을 looping

### Jira Board 매핑

| Jira 상태 | OPSX 단계 |
|-----------|-----------|
| Rough Ideas | explore 후 |
| Spec Drafting | propose 단계 |
| Backlog | spec 완성 시 |
| Ready for Automation | AI agent가 자유롭게 pickup, implement, PR |
| Awaiting Human Ops | 사람 개입 필요 작업 |
| Deploy Verification | 배포 체크 |

### 스펙 작성

- OpenSpec 기반의 타이트한 조건의 spec doc
- Spec delta 작성
- capability에 따른 스펙 구분
- taskmaster-ai는 implement agent가 활용

---

## 5. AI Workflow 설계 패러다임

### 5-1. SDD (Spec-Driven Development)

- OpenSpec 기반 spec doc 작성 → task 분해 → local 저장
- capability에 따른 스펙 구분
- Spec docs archiving

### 5-2. AI Workflow Pattern

> [!important] 핵심 패턴
> **Plan → Implement → Evaluate → Improve**
> 더 구체적으론: explore → spec → implement → test → validate → reflect → improve

어떤 loop를 돌든 이 4가지 flow를 따름.

예시 — merge agent:
- **Plan**: merge 순서의 dependency 정리, 각 PR이 통과해야 할 CI 처리
- **Implement**: 실제 merge 진행
- **Evaluate**: deploy가 잘 되는지 체크
- **Improve**: 고려하지 못한 것 체크

### 5-3. Task Routing / Ordering / Throttling

| 개념 | 설명 |
|------|------|
| **Task routing** | 티켓 사이즈에 따라 어떤 flow를 탈지 (full spec definition vs debugging) |
| **Task ordering** | task analysis(taskmaster-ai), ticket analysis로 우선순위 결정 |
| **Task throttling** | monitoring + cron. 빠르게 시도했을 때 시스템이 충분히 warmup 되지 않을 수 있음 |

### 5-4. Global Looping vs Local Looping

> [!tip] 핵심 인사이트
> Local looping = context optimization의 **local minimum**을 찾는 작업
> Global looping = 전체 context를 숲을 보는 눈으로 리팩터링하는 작업 → **global minimum**

- **Local looping의 한계** — 틀을 벗어나는 변경을 만들기 힘듦
- 예: session-wrap은 그 세션 기준으로 context를 업데이트 (local)
- 전체 context를 리팩터링하는 별도 작업이 필요 (global)
- **두 가지 루프를 따로 운영**해야 함

### 5-5. Parallelizing Task Management

관련 도구:
- <a href="https://github.com/cline/kanban">Cline Kanban</a>
- <a href="https://github.com/openai/symphony">OpenAI Symphony</a>
- <a href="https://github.com/makeplane/plane">Plane</a>

핵심 질문: 어떻게 parallel하게, conflict 없이, 효율적으로 schedule 할 것인가.

### 5-6. Minimizing the Input Surface

> [!danger] 원칙
> **"에이전트가 접근할 수 없는 것은 존재하지 않는 것과 같다."**

- 시스템의 input surface는 **1개**가 가장 좋음
- agent가 추적할 수 없는 input이 많을수록 → 중요한 context 누락
- 여러 input surface 운영 시 → 반드시 전체 통합 검색 필요 → 복잡, 싱크 문제
- output surface는 여러 곳이어도 OK

---

## 6. 보조 도구들

### Loki Mode

> <a href="https://github.com/asklokesh/loki-mode">GitHub — Loki Mode</a>

PRD를 입력하면 복잡도를 분류하고, 8개 스웜의 41개 전문 에이전트 팀을 구성하여 자율 RARV 사이클(Reason - Act - Reflect - Verify)을 실행. 9개 품질 게이트 통과 시에만 완료. 5개 AI provider(Claude, Codex, Gemini, Cline, Aider) 자동 페일오버 지원.

### architecture.md

> <a href="https://architecture.md/">architecture.md 템플릿</a>

에이전트가 코드베이스를 빠르게 이해할 수 있도록 설계된 구조화 템플릿. 프로젝트 구조, 시스템 다이어그램, 핵심 컴포넌트, 데이터 스토어, 외부 통합, 배포/인프라, 보안, 용어집까지 포함.

---

## 7. 하네스 설계 7원칙 (갓대희 정리)

> <a href="https://goddaehee.tistory.com/565">하네스 엔지니어링 — OpenAI와 Anthropic의 접근법 비교 분석</a>

1. **지도를 주지, 백과사전을 주지 마라** — AGENTS.md 100줄 이내
2. **불변량은 코드로 강제하라** — 린터와 CI
3. **생성과 평가를 분리하라** — 독립된 Evaluator
4. **에이전트에게 앱을 "보여줘라"** — Chrome DevTools, Playwright MCP
5. **모델이 바뀌면 하네스를 재검증하라**
6. **엔트로피를 가비지 컬렉션하라**
7. **"지루한" 기술을 선택하라**

---

## 8. OPSX Skill이 이 모든 걸 반영했는가?

| 패러다임 | OPSX 반영 여부 |
|----------|---------------|
| Harness engineering (spec → implement → evaluate → improve) | ✅ explore → propose → apply → verify → archive |
| session-wrap / global-wrap | ✅ 세션 업데이트 + archiving |
| Parallel task management | ✅ Jira board + GitHub PR 기반 |
| Global / local looping | ✅ cron으로 local loop + 별도 global wrap |
| AI workflow pattern | ✅ Plan → Implement → Evaluate → Improve 패턴 |
| Minimizing input surface | ⚠️ Jira가 single input surface 역할하나, 완전 통합은 미확인 |
| Managing comprehension debt | ⚠️ OpenSpec 기반 spec docs가 일부 해결하나, ARCHITECTURE.md 등은 별도 |

---

## 참고 자료

- <a href="https://toss.tech/article/software-3-0-era">Toss — 소프트웨어 3.0 시대란?</a>
- <a href="https://toss.tech/article/harness-for-team-productivity">Toss — 당신의 팀은 같은 LLM을 쓰고 있나요?</a>
- <a href="https://openai.com/index/harness-engineering/">OpenAI — Harness Engineering</a>
- <a href="https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents">Anthropic — Effective Harnesses for Long-Running Agents</a>
- <a href="https://www.anthropic.com/engineering/harness-design-long-running-apps">Anthropic — Harness Design for Long-Running Apps</a>
- <a href="https://channel.io/ko/blog/articles/what-is-harness-2611ddf1">Channel.io — 하네스란?</a>
- <a href="https://goddaehee.tistory.com/565">갓대희 — OpenAI와 Anthropic 접근법 비교</a>
- <a href="https://addyosmani.com/blog/comprehension-debt/">Addy Osmani — Comprehension Debt</a>
- <a href="https://github.com/Fission-AI/OpenSpec/blob/main/docs/opsx.md">OpenSpec — OPSX Workflow</a>
- <a href="https://architecture.md/">architecture.md</a>
- <a href="https://github.com/asklokesh/loki-mode">Loki Mode</a>
