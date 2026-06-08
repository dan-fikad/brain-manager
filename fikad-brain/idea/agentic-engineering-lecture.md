---
tags:
  - lecture
  - agentic-engineering
created: 2026-03-31
---

# Agentic Engineering 강의 기획

## 핵심 철학
- 이것은 강의가 아니다. 재밌는 이야기다.
- 각 챕터: 어려움/문제상황 → 공감 및 해결 → 해소된 상황 → 위기 → 결말
- "100개 앱 동시에 만드는 법"을 가르치지 않는다. 사고의 흐름을 가르친다.
- "반드시 본인이 풀고자하는 문제 3가지를 가져와라. 나는 내 문제를 풀 뿐이다."

## 명칭 변경
- "Product Engineering" → "Agentic Engineering" 추천
- Anthropic, McKinsey, JetBrains 등이 공식 용어로 사용 중
- 80% 개발자가 AI 코딩 에이전트 사용, 하지만 신뢰도는 40%→29% 하락
- "Agentic 방식으로 Product를 만드는 것"이 전체 테마

## 리서치 (2026-03-31)

### Comprehension Debt
- AI 코드 생성 위임 시 이해도 40% 이하, 개념적 탐구에 활용 시 65% 이상
- 2년차부터 유지보수 비용 4배 (Addy Osmani)
- Anthropic 리서치: AI 어시스턴트 사용 개발자가 새 라이브러리 이해도에서 17% 낮은 점수

### Self-Improving Agent 패턴
- generate → critique → reflect → commit 루프가 production agent 핵심 패턴
- OpenAI Cookbook에 자율 에이전트 재훈련 가이드 등장
- Yohei Nakajima(BabyAGI 창시자) 방법론
- HuggingFace "Reflective Agent"를 2026 AI 트렌드로 선정

### 경쟁 현황
- <a href="https://prodengineer.org/">prodengineer.org</a> — Claude Code 중심 200p 가이드
- <a href="https://aiproduct.engineer/">aiproduct.engineer</a> — agentic AI 실무 튜토리얼
- <a href="https://productcoder.ai/">Product Coder</a> — PM→빌더 코호트 (2026.02 시작)
- Udemy Complete Agentic AI Engineering Course
- 차별점: 경쟁 강의들은 "빌드하는 법" 집중. "이해하고 검증하고 개선하는 법"까지 다루는 곳은 거의 없음

### 참고 자료
- <a href="https://resources.anthropic.com/hubfs/2026%20Agentic%20Coding%20Trends%20Report.pdf">Anthropic 2026 Agentic Coding Trends Report</a>
- <a href="https://addyosmani.com/blog/comprehension-debt/">Addy Osmani - Comprehension Debt</a>
- <a href="https://addyosmani.com/blog/code-agent-orchestra/">Addy Osmani - Code Agent Orchestra</a>
- <a href="https://addyosmani.com/blog/self-improving-agents/">Addy Osmani - Self-Improving Agents</a>

## Notion 기획안 리뷰 피드백
- "강의 소개"에 좋은 아이디어가 흩어져 있는데 "강의 기획" 섹션 구조에 맵핑 안 됨
- Section 4 "Harness Engineering" → "Workflow Engineering"으로 변경 추천
- "만들 앱 아이디어" 5개로 산발적 — hooksnap이 최적의 예시 (API + Web UI + AI pipeline + 실제 유저)
- Comprehension debt를 특정 섹션에만 넣지 말고 매 섹션 끝 반복 패턴으로 (관통 테마)
- 스토리 구조(어려움 → 해결 → 위기 → 결말)가 메인 철학인데 실제 섹션에 미적용

## 제안 섹션 구조

| Section | 제목 | 핵심 | 스토리 |
|---------|------|------|--------|
| 1 | Intro — 왜 Agentic Engineering인가 | product engineer 정의, AI 시대 역할 변화 | "코드 잘 짜면 됐던 시대 → 이제는 다르다" |
| 2 | Context Engineering | CLAUDE.md, skill, context 설계 | "AI가 맨날 엉뚱한 걸 만든다 → context가 문제였다" |
| 3 | Workflow Engineering | prompting → skill → looping → cron 자동화 | "반복 작업에 지쳐 → 하나씩 자동화 → 거대한 파이프라인" |
| 4 | Agentic Patterns | multi-agent, orchestration, planner-implementer-evaluator | "혼자 다 하기엔 복잡 → agent 팀 구성" |
| 5 | Comprehension & Reflection | comprehension debt, self-reflection, mental model 문서화 | "빠르게 만들었는데 아무도 이해 못함 → 체계적 이해 시스템" |
| 6 | Product Delivery | evaluation, testing, deployment, 실제 유저 피드백 | "만들었다고 끝이 아니다 → 검증과 개선의 루프" |

## 매 챕터 반복 루프
빌드(implement) → 평가(evaluate) → 이해(comprehend) → 개선(reflect & improve)
