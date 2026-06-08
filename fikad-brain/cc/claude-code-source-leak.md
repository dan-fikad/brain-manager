---
tags:
  - claude-code
  - security
  - leak
date: 2026-03-31
---

# Claude Code 소스코드 유출 사건 (2026-03-31)

## 사건 개요

2026년 3월 31일, Anthropic이 Claude Code CLI v2.1.88을 npm에 배포하면서 59.8MB 소스맵 파일(.map)을 실수로 포함시켜 **1,900개 TypeScript 파일, 512,000+ 줄**의 전체 소스코드가 공개됐다.

- 최초 발견자: 보안 연구자 Chaofan Shou
- 원인: `.npmignore` 또는 `package.json`의 `files` 필드 설정 누락
- Bun 번들러의 버그가 root cause일 수 있다는 분석도 존재
- 이것이 **두 번째 동일 실수** (2025년 2월에도 같은 소스맵 유출 발생)
- 같은 주에 Mythos 모델 스펙 유출까지 겹쳐 "내부자 의도적 유출설"까지 제기됨

## 유출된 핵심 내용

### 아키텍처
- React + Ink 기반 CLI 인터페이스
- 66개 빌트인 도구 (concurrent/serialized 분리)
- 멀티에이전트 오케스트레이션: Fork, Teammate, Worktree 3가지 모드
- 프롬프트 캐시 공유를 통한 병렬 서브에이전트 최적화

### 시스템 프롬프트 & 메모리
- `claude.md`가 **매 턴마다** 로드됨 (40,000자 제한)
- 5단계 컴팩션: micro compact, context collapse, session memory, full compact, PTL truncation
- 세션 영속성: JSON-L 포맷으로 저장, resume/fork 가능

### Feature Flags (89개)
- 미공개 모델: Opus 47, Sonnet 48, Capybara(Mythos)
- Dream Mode: 에이전트가 밤새 아이디어를 구상하는 모드
- Buddy Mode: Tamagotchi 스타일 AI 펫 컴패니언 (20종 동물)
- Auto Mode: ML 기반 지능형 권한 승인
- Proactive Mode: 자율적으로 태스크를 생성하고 실행
- X42 Protocol: 크립토 기반 에이전트 자율 결제

### 논란이 된 기능
- **Undercover Mode**: AI가 작성한 코드임을 숨기는 모드. 오픈소스 PR에서 AI 작성 여부를 감추는 용도로 우려
- **Frustration Regexes**: 사용자의 불만/짜증을 감지하는 정규식 패턴
- **Fake Tools**: 실제로는 존재하지 않는 도구를 모델에게 제시하는 구조

### 권한 시스템
- 3단계: Bypass (전체 허용), Allow Edits (파일 편집 자동 허용), Auto (ML 분류기 기반)
- Hooks: pre-tool-use, post-tool-use, user-prompt-submit, session-start, session-end

## 커뮤니티 반응

### Reddit
| 서브레딧 | 포인트 | 댓글 | 핵심 반응 |
|----------|--------|------|-----------|
| r/ClaudeAI | 4,070 | 494 | "anthropic's codebase is absolutely unhinged" |
| r/LocalLLaMA | 3,378 | 653 | "Wow did their AI not catch that lol — Or maybe an Anthropic employee started vibe coding too hard" (944 upvotes) |
| r/technology | 3,048 | 134 | "The real value of Claude is its Model and API. Claude Code is just a frontend" (665 upvotes) |
| r/cybersecurity | 1,577 | 165 | 보안 관점의 심각성 분석 |
| r/webdev | 731 | 128 | "The ultimate irony" |

### Hacker News
- 메인 스레드: 1,939 포인트, 951 코멘트
- "The big loss for Anthropic here is how it reveals their product roadmap via feature flags"
- "Undercover mode is the most concerning part here"
- Bun 버그 원인설 스레드도 별도 등장

### X/Twitter
- @BrianRoemmele (79 likes): "The Claude Code Leak Dropped the Real Blueprint"
- @automate_archit: "the most useful architecture leak" — 보안 실패가 아닌 학습 자료로 보는 시각
- @vnjogani: "code is cheap these days. It is not the core IP anymore"
- 프랑스, 브라질, 터키 등 글로벌 반응 확산

### YouTube
- 19개 이상의 분석 영상 (24시간 내)
- 총 230,000+ 조회수
- STARTUP HAKK (22,923 views): "The Death of Vibe Coding?"
- Alex Finn (29,891 views): feature flag 기반 로드맵 분석
- Matthew Berman (24,057 views): 아키텍처 심층 분석
- Theo - t3.gg: 기술적 분석

## Anthropic 대응

- npm에서 해당 버전 제거
- GitHub에 올라간 소스코드 레포에 DMCA 테이크다운 발송
- 그러나 이미 41,500+ fork 발생
- Python, Rust로 재작성된 버전이 저작권 우회 시도 중

## 실질적 영향

### 개발자 커뮤니티
- 유출 소스를 분석해 token drain 버그를 찾고 패치한 사용자 등장 (r/ClaudeAI, 1,029 upvotes)
- 멀티에이전트 오케스트레이션을 추출해 오픈소스 프레임워크로 공개
- Claude Code의 프롬프트 구조/tool calling 패턴이 경쟁 제품에 반영될 전망

### Anthropic 비즈니스
- IPO 계획에 투자자 신뢰도 타격 가능성
- "Safety-first" 브랜딩과의 모순: "$10B 기업이 .npmignore 한 줄을 빠뜨린 기초적 실수"
- 다만 "모델이 진짜 해자(moat)이지 코드가 아니다"라는 의견도 다수

### 교훈
- CI/CD 파이프라인에서 소스맵 포함 여부 자동 검증 필수
- npm 패키지 크기 급증 모니터링 필요
- Vibe coding의 한계: AI 코딩 선두주자가 기본적인 빌드 프로세스에서 실수
