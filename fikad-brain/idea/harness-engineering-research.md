---
title: Harness Engineering 리서치
date: 2026-04-01
tags:
  - research
  - claude-code
  - harness-engineering
  - study
---

# Harness Engineering 리서치

> [!info] 조사 배경
> "harness engineering"이라는 용어가 Claude Code에서 어떻게 쓰이는지, 어떤 것들을 포함하는지, 가르친다면 어떻게 가르쳐야 할지 조사.

## 용어 정의

**Harness engineering** = 모델 자체가 아닌, 모델을 감싸는 모든 것을 설계하는 분야.

Raw model은 agent가 아니다. Harness가 상태(state), 도구 실행(tool execution), 피드백 루프(feedback loops), 제약 조건(constraints)을 부여할 때 비로소 agent가 된다.

- 2026년 초에 주류 진입한 용어
- OpenAI Codex 팀이 100만 줄+ 코드를 AI만으로 작성한 프로덕션 앱을 공개하면서 본격화
- ML 연구보다 **시스템 엔지니어링/DevOps**에 가까운 분야

## Claude Code에서의 Harness 구성요소

| 구성요소 | 설명 |
|----------|------|
| **Rules files** | CLAUDE.md, `.claude/rules/` — 매 세션 로드되는 영구 지시사항 |
| **Skills** | 필요 시 활성화되는 재사용 가능 instruction set (SKILL.md + 참조파일/스크립트) |
| **Hooks** | 에이전트 라이프사이클의 특정 시점에 실행되는 deterministic 스크립트 |
| **MCP servers** | 외부 도구/API 연결 |
| **Sub-agents** | 독립된 Claude 인스턴스로 작업 위임 |
| **Plugins** | skills, agents, hooks, MCP를 번들로 묶어 팀 간 공유 |

## 핵심 개념: Progressive Disclosure

스킬이 수천 개 설치돼도 Claude가 처음 읽는 건 **YAML front matter(이름+설명)뿐**이다.

1. Front matter(요약) → 스킬 선택 시점에 로드
2. skill.md 본문(프로세스) → 해당 스킬을 쓰기로 결정한 후 로드
3. 참조 파일/스크립트(지식) → skill.md가 지시할 때만 로드

이것이 context window를 보호하는 핵심 메커니즘.

## Matt Pocock의 5가지 실전 스킬

> [!tip] 출처
> "5 Claude Code skills I use every single day" (207K views, 6.1K likes)

1. **Grill Me** — LLM에게 설계의 모든 분기(design tree)를 질문하게 하여 shared understanding 도달. 단 3문장짜리 스킬이지만 30~50개 질문을 유도.
2. **Write PRD** — grill me로 도달한 이해를 바탕으로 GitHub issue로 PRD 작성. 사용자 스토리 포함.
3. **PRD to Issues** — PRD(목적지)를 vertical slice 이슈들(여정)로 분해. Tracer bullet 원칙 — 통합 리스크가 높은 것부터.
4. **TDD** — Red-green-refactor 루프. 인터페이스 변경을 먼저 확인하고, 한 번에 하나의 테스트를 작성.
5. **Improve Codebase Architecture** — shallow module을 deep module로 리팩터링. 3개 sub-agent가 병렬로 다른 인터페이스 설계 제안.

## 커뮤니티 반응 (Reddit)

### 주요 쓰레드

- **"Anthropic shares how to make Claude code better with a harness"** — r/ClaudeAI, 860pts, 135댓글
- **"Must-have settings / hacks for Claude Code?"** — r/ClaudeCode, 335pts, 160댓글
- **"Inside a 116-Configuration Claude Code Setup"** — r/ClaudeCode, 44댓글
- **"Claude Code now supports hooks"** — r/ClaudeAI, 152댓글
- **"Petition: Claude Code should support AGENTS.md"** — r/ClaudeCode, 83댓글

### 커뮤니티 인사이트

- 스킬 활성화 성공률 테스트: 기본 설정 **20%**, 최적화해도 **84%**가 한계
- 1000개 제네릭 스킬보다 **20~30개 잘 만든 맞춤 스킬**이 압도적으로 우수
- 15,000 character limit이 available skills list에 존재 — 과도한 스킬은 context 오염

## 가르친다면: 커리큘럼 프레임워크

### Module 1: 개념 이해
- raw model ≠ agent — harness가 부여하는 것
- LLM의 제약 (무기억, context window, smart/dumb zone)
- Claude Code vs Codex vs Cursor의 harness 비교

### Module 2: Rules & Steering
- CLAUDE.md 작성법 — 프로젝트별/글로벌
- `.claude/rules/` 디렉토리 활용
- "Point, don't dump" 원칙

### Module 3: Skills 설계
- Skill 아키텍처: front matter → skill.md → 참조/스크립트
- Progressive disclosure 이해와 실습
- Matt Pocock의 5가지 실전 스킬 분석
- 스킬 디버깅: 프로세스 문제 vs 지식 문제 분리

### Module 4: Hooks & 자동화
- Hook 이벤트 종류와 실행 시점
- 보안 스캐닝, 린팅, 정책 적용
- Settings.json 설정

### Module 5: MCP & 외부 통합
- MCP 서버 설정과 연결
- 외부 API/도구 통합 패턴

### Module 6: Sub-agents & 병렬화
- 작업 위임 패턴
- Background tasks와 worktree 격리
- Autonomous agent loop (Ralph loop 패턴)

### Module 7: 실전 프로젝트
- 자신의 업무 프로세스를 스킬로 인코딩
- 피드백 루프 설계와 반복 개선
- 20~30개 맞춤 스킬 라이브러리 구축

## 참고 자료

- <a href="https://www.nxcode.io/resources/news/what-is-harness-engineering-complete-guide-2026">NxCode - What Is Harness Engineering? Complete Guide (2026)</a>
- <a href="https://openai.com/index/harness-engineering/">OpenAI - Harness engineering: leveraging Codex in an agent-first world</a>
- <a href="https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents">HumanLayer - Skill Issue: Harness Engineering for Coding Agents</a>
- <a href="https://www.paradime.io/guides/claude-code-skills-plugins-rules-guide">Paradime - Claude Code Skills & Harness Engineering Guide</a>
- <a href="https://blog.langchain.com/the-anatomy-of-an-agent-harness/">LangChain - The Anatomy of an Agent Harness</a>
- <a href="https://harnessengineering.academy/">Harness Engineering Academy</a>
- <a href="https://www.youtube.com/watch?v=EJyuu6zlQCg">Matt Pocock - 5 Claude Code skills I use every single day</a>
- <a href="https://www.youtube.com/watch?v=6-D3fg3JUL4">Simon Scrapes - How to Use Claude Code Skills Like the 1%</a>
