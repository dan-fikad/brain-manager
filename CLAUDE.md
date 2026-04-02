# Brain Manager

일식(김일식)의 개인 업무 루틴 관리 허브. Obsidian vault(`fikad-brain/`)를 중심으로 Linear, Jira, Notion, Slack을 연동해 일일 업무를 관리한다.

## 핵심 원칙

- Obsidian은 **최초 지식 허브**다. 모든 파생 문서(Notion, Jira, Linear)는 여기서 생성된다.
- 나만 알고 있는 컨텍스트가 없도록, 아는 모든 것을 빠짐없이 Obsidian에 적는다.
- 각 프로젝트 디렉터리의 CLAUDE.md와 skill을 적극 참조/위임한다.
- 모든 응답은 한국어로 한다.

## 도구 통합

| 도구 | 용도 | 핵심 정보 |
|------|------|-----------|
| **Obsidian** | 지식 허브, 데일리 노트 | vault: `fikad-brain/`, obsidian-cli + obsidian-skills 사용 |
| **Linear** | 개인 태스크 트래킹 | workspace: `daily-routine-dan`, team ID: `c45a1d0c-63ad-4b98-a2e0-66b9a944a38a` |
| **Jira** | 팀 프로젝트 트래킹 | 프로젝트: TG (hooksnap), SCRUM (피카클립). **TG는 "Task" 타입만 지원** ("Bug" 불가) |
| **Notion** | 공유 문서, 미팅 노트, HR 문서 | fikadev workspace |
| **Slack** | 데일리 스크럼 포스팅, 맥락 검색 | 데일리 채널: `#1_daily-scrum` (ID: `C06112AHUKG`) |

## Linear 라벨

티켓 생성 시 반드시 적절한 라벨을 붙인다:
- `HookSnap` - hooksnap 제품 관련
- `Bug` - 버그 수정
- `Improvement` - 개선
- `Feature` - 신규 기능
- `Meeting` - 미팅 (없으면 생성)
- `HR` - 채용/면접 (없으면 생성)
- `Ops` - 운영/관리 (없으면 생성)
- `SNS` - SNS 콘텐츠 (없으면 생성)

## 데일리 노트

### 위치
`fikad-brain/YYYY-MM-DD.md`

### 템플릿
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

### Skill Update
(워크플로 자동화 아이디어, 스킬 개선 사항)
```

### 작성 규칙
- 티켓 번호나 링크를 본문에 넣지 않는다. 항목 텍스트만 간결하게 작성한다.
- "어제 한 일"은 Jira/Linear Done 티켓 기반으로 카테고리별 집계한다. `- {주제} - {성과 요약}` 한 줄 형태로 압축하고, 하위 내용은 3줄 이내로 제한한다.

### 카테고리
- `meeting` - 미팅
- `hooksnap` - hooksnap 제품 작업
- `ops` - 운영 업무
- `hr` - 채용/면접
- `etc` - 기타

## 업무 루프

### 0. 데일리 노트 초안 생성
1. **"어제 한 일" 작성**: Jira Done + Linear Done 티켓 조회 → 카테고리별 집계. 전날 데일리 노트의 "오늘 할 일"과 반드시 크로스체크하여 누락 방지.
2. **"오늘 할 일" 작성**: 전날 "내일 할 일" 캐리오버 + Jira rough ideas 중 우선순위 선정 + 오늘 예정 미팅 확인
3. **미팅 노트 반영**: 어제 미팅이 있었다면 Notion 미팅 노트 요약 추가, action item은 Linear 티켓 생성

### 1. 아침: 티켓 생성 및 우선순위 배정
1. 데일리 노트의 "오늘 할 일" 읽기
2. **컨텍스트 수집** (티켓 생성 전 필수):
   - Jira TG/SCRUM에서 관련 티켓 검색
   - Notion에서 관련 문서/미팅 노트 확인
   - Slack 최근 대화에서 추가 맥락 수집
3. 수집한 정보 기반으로 Linear 티켓 생성 (cross-reference 포함)
4. 우선순위 매기고 첫 번째 작업 할당
5. 각 작업에 대해 "꼭 해야 하는지" 피드백 제공

### 2. 작업 중: 상태 관리
- Linear: Backlog → Todo → In Progress → Done
- 필요 시 Jira 티켓 생성/업데이트
- 필요 시 Notion 문서 작성/업데이트
- 사용자가 완료/진행중 보고하면 즉시 상태 반영

### 3. 하루 마무리
- Linear 기준으로 오늘 한 일 정리
- "오늘의 workflow update" 섹션 데일리 노트에 추가
- 내일 할 일 초안 작성
- `#1_daily-scrum` Slack 포스팅

## 미팅 처리 규칙

데일리 노트에 `meeting` 항목이 있으면:
1. **미팅 로그가 있는지 사용자에게 확인한다** (Notion 링크 등)
2. 미팅 로그가 제공되면 핵심 컨텍스트를 읽고 데일리 노트에 정리
3. 액션 아이템이 있으면 별도 Linear 티켓 또는 Jira 티켓으로 생성

## SNS 파이프라인

- 초안 위치: `fikad-brain/sns/threads/`, `fikad-brain/sns/linkedin/` 등
- 플로우: 초안 작성 → **노출/팔로워 극대화를 위한 리라이트 스킬 실행** → 포스팅
- 사용자가 업로드 전에 리라이트 스킬을 실행한다

## 연관 프로젝트 디렉터리

작업 위임이나 컨텍스트 참조 시 해당 디렉터리의 CLAUDE.md와 skill을 활용한다.

`~/fikad/`는 피카(fika.d) 회사 프로젝트 저장소다.

| 디렉터리 | 용도 |
|----------|------|
| `~/fikad/product-iteration/hooksnap/` | hooksnap 제품 (Vercel, FastAPI, Next.js) - 피카 프로젝트 |
| `~/fikad/gen-shorts/` | 영상 생성 서비스 - 피카 프로젝트 |
| `~/fikad/fika-d-team-claude-skills/` | 팀 공유 스킬 플러그인 - 피카 프로젝트 |
| `~/product-iteration/` | 비즈니스 컨셉/PRD 저장소 |
| `~/hr/recruit/web-fullstack-engineer/` | 채용 관련 |
| `~/hr/mentoring/` | 인프런 멘토링 |
| `~/lecture-maker/` | 인프런 강의 제작 |
| `~/trading/` | 트레이딩 |
| `~/presentation/` | 발표 자료 |

## Jira 규칙

- TG 프로젝트: issue type은 반드시 `Task` 사용 (`Bug` 타입 미지원)
- 새 티켓 기본 상태: `rough ideas`
- QA 항목, 버그 리포트 등도 `Task`로 생성 후 설명에 성격 명시
