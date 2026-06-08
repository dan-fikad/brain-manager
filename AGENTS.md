# Brain Manager Codex Guide

이 저장소는 일식(김일식)의 개인 업무 루틴 관리 허브다. `fikad-brain/` Obsidian vault를 최초 지식 허브로 삼고, 여기서 Linear, Jira, Notion, Slack으로 파생되는 업무 흐름을 관리한다.

## 기본 원칙

- 모든 응답은 한국어로 한다.
- Obsidian은 최초 지식 허브다. 파생 문서, 티켓, 미팅 노트, 공유 문서의 원본 맥락은 먼저 `fikad-brain/`에 남긴다.
- 사용자가 알거나 결정한 맥락이 저장소에 없으면 누락 가능성을 먼저 짚고, 필요한 경우 데일리 노트나 관련 문서에 반영한다.
- Claude Code 전용 설정은 참고용 레거시로만 본다. Codex 운영 기준은 이 `AGENTS.md`와 `~/.codex/config.toml`이다.
- 사용자가 남긴 Obsidian vault 변경분을 임의로 정리하거나 되돌리지 않는다.
- Notion은 사용자가 명시적으로 요청하거나 링크를 제공한 경우에만 조회한다. 데일리 노트 작성 시 Notion을 기본 체크하지 않는다.

## 도구 통합

| 도구 | 용도 | 핵심 정보 |
| --- | --- | --- |
| Obsidian | 지식 허브, 데일리 노트 | vault: `fikad-brain/` |
| Linear | 개인 태스크 트래킹 | workspace: `daily-routine-dan`, team ID: `c45a1d0c-63ad-4b98-a2e0-66b9a944a38a` |
| Jira | 팀 프로젝트 트래킹 | 프로젝트: TG (hooksnap), SCRUM (피카클립). TG는 `Task` 타입만 지원한다. |
| Notion | 공유 문서, 미팅 노트, HR 문서 | fikadev workspace |
| Slack | 데일리 스크럼 포스팅, 맥락 검색 | 데일리 채널: `#1_daily-scrum` (ID: `C06112AHUKG`) |

외부 도구 쓰기 작업은 관련 문서와 티켓을 먼저 읽고, 사용자가 요구한 범위 안에서만 수행한다. 인증이 없거나 MCP가 연결되지 않은 도구는 대체 가능한 로컬 작업을 먼저 처리하고, 남은 연결 작업을 명확히 보고한다.

## Linear 규칙

티켓 생성 시 적절한 라벨을 붙인다.

- `HookSnap` - hooksnap 제품 관련
- `Bug` - 버그 수정
- `Improvement` - 개선
- `Feature` - 신규 기능
- `Meeting` - 미팅, 없으면 생성
- `HR` - 채용/면접, 없으면 생성
- `Ops` - 운영/관리, 없으면 생성
- `SNS` - SNS 콘텐츠, 없으면 생성

## 데일리 노트

위치: `fikad-brain/YYYY-MM-DD.md`

템플릿:

```markdown
### DS

##### 어제 한 일
(카테고리별 정리)

##### 오늘 할 일
(카테고리별 정리)

##### 오늘의 workflow update
(일을 진행하면서 느낀 점, 프로세스 개선 아이디어)

---

### Materials
(참고 링크, 자료)

### 김아영

##### 오늘 그녀가 나를 따뜻하게 대한 장면
(사실 기반으로 한 장면 기록)

##### 오늘 그녀가 나를 생각해준 장면
(사실 기반으로 한 장면 기록)

##### 오늘 그녀의 부드러움이 관계에 준 가치
(관계에 준 긍정적 가치 기록)

##### 오늘 내가 그녀에게 고마웠던 것
(감사한 점 기록)

### Skill Update
(워크플로 자동화 아이디어, 스킬 개선 사항)
```

작성 규칙:

- 티켓 번호나 링크를 본문에 넣지 않는다. 항목 텍스트만 간결하게 작성한다.
- "어제 한 일"은 Jira/Linear Done 티켓 기반으로 카테고리별 집계한다.
- 집계 항목은 `- {주제} - {성과 요약}` 한 줄 형태로 압축하고, 하위 내용은 3줄 이내로 제한한다.
- 전날 데일리 노트의 "오늘 할 일"과 반드시 크로스체크해 누락을 줄인다.
- Notion은 사용자가 명시적으로 요청하거나 링크를 제공한 경우에만 확인한다. 데일리 노트의 "오늘 할 일"이나 Materials에 Notion 내용을 자동 반영하지 않는다.
- 하루에 하나씩 `김아영` 섹션을 작성한다. 존중할 점과 감사한 점을 사실 기반으로 남기고, 장면을 모르면 추측하지 말고 항목만 비워 둔다.

카테고리:

- `meeting` - 미팅
- `hooksnap` - hooksnap 제품 작업
- `ops` - 운영 업무
- `hr` - 채용/면접
- `etc` - 기타

## 업무 루프

### 0. 데일리 노트 초안 생성

1. Jira Done과 Linear Done 티켓을 조회해 "어제 한 일"을 카테고리별로 집계한다.
2. 전날 "오늘 할 일"과 크로스체크한다.
3. 전날 "내일 할 일" 캐리오버, Jira rough ideas, 오늘 예정 미팅을 바탕으로 "오늘 할 일"을 작성한다.
4. 어제 미팅 로그가 사용자가 제공한 링크나 로컬 문서에 있으면 요약하고, action item은 Linear 또는 Jira 티켓으로 생성한다.

### 1. 아침 티켓 생성 및 우선순위 배정

1. 오늘 데일리 노트의 "오늘 할 일"을 읽는다.
2. 티켓 생성 전 Jira TG/SCRUM, Slack에서 관련 맥락을 확인한다. Notion은 사용자가 명시적으로 요청하거나 링크를 제공한 경우에만 확인한다.
3. 수집한 정보를 바탕으로 Linear 티켓을 생성하고 cross-reference를 포함한다.
4. 우선순위를 매기고 첫 번째 작업을 할당한다.
5. 각 작업에 대해 "꼭 해야 하는지" 관점의 피드백을 제공한다.

### 2. 작업 중 상태 관리

- Linear: Backlog -> Todo -> In Progress -> Done
- 필요 시 Jira 티켓을 생성하거나 업데이트한다.
- 필요 시 Notion 문서를 작성하거나 업데이트한다.
- 사용자가 완료 또는 진행 중 상태를 보고하면 즉시 반영한다.

### 3. 하루 마무리

- Linear 기준으로 오늘 한 일을 정리한다.
- 데일리 노트에 "오늘의 workflow update"를 추가한다.
- 내일 할 일 초안을 작성한다.
- `#1_daily-scrum` Slack 포스팅 초안을 만들거나 게시한다.

## 미팅 처리

데일리 노트에 `meeting` 항목이 있으면:

1. 미팅 로그가 있는지 사용자에게 확인한다. 예: Notion 링크, 녹취 요약, 회의록.
2. 미팅 로그가 제공되면 핵심 컨텍스트를 읽고 데일리 노트에 정리한다.
3. 액션 아이템이 있으면 별도 Linear 티켓 또는 Jira 티켓으로 생성한다.

## SNS 파이프라인

- 초안 위치: `fikad-brain/sns/threads/`, `fikad-brain/sns/linkedin/`
- 플로우: 초안 작성 -> 노출/팔로워 극대화를 위한 리라이트 -> 포스팅
- 사용자가 업로드 전에 리라이트를 요청하면 초안의 의도와 톤을 보존하면서 개선한다.

## 연관 프로젝트 디렉터리

작업 위임이나 컨텍스트 참조 시 해당 디렉터리의 repo 지침을 먼저 확인한다.

`~/fikad/`는 피카(fika.d) 회사 프로젝트 저장소다.

| 디렉터리 | 용도 |
| --- | --- |
| `~/fikad/product-iteration/hooksnap/` | hooksnap 제품 (Vercel, FastAPI, Next.js) |
| `~/fikad/gen-shorts/` | 영상 생성 서비스 |
| `~/fikad/fika-d-team-claude-skills/` | 팀 공유 스킬 플러그인 |
| `~/product-iteration/` | 비즈니스 컨셉/PRD 저장소 |
| `~/hr/recruit/web-fullstack-engineer/` | 채용 관련 |
| `~/hr/mentoring/` | 인프런 멘토링 |
| `~/lecture-maker/` | 인프런 강의 제작 |
| `~/trading/` | 트레이딩 |
| `~/presentation/` | 발표 자료 |

## Jira 규칙

- TG 프로젝트의 issue type은 반드시 `Task`를 사용한다. `Bug` 타입은 지원하지 않는다.
- 새 티켓 기본 상태는 `rough ideas`다.
- QA 항목, 버그 리포트도 `Task`로 생성하고 설명에 성격을 명시한다.
