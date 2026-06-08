
- 현재 tenant 개념이 없음. organization 정의.
- organization 안에 유저가 있는 게 아니라, organization/user 연결 membership table을 따로 둘 것.
- organization 안에 workspace를 여러개 둘 수 있음.
- 어떻게 organization을 바꿀건지 design 고민 필요.
- api key는 organization 소유 관리.

**api mvp**
- gen 요청, job 상태 조회, gen 결과 조회, webhook callback.
	- webhook 제공 필요.
	- sjs. 파일업로드 scope out.
- bulk 제공할지 말지. 영상 여러개에 대한 생성 요청.
	- w. bulk scheduling.
- q. 어느정도
- w. bulk 처리 니즈 보다는 rate limit이 더 중요하지 않을까.
	- w. 동시에 5개 job 이 요청되지 않는 형태인데, api 자체에서 rate limit을 걸어야.

기존 ui 기반 사용 경로
- org 유저는 api key 뿐만 아니라
- observability에 대한 것들.

**org onboarding**
- 디자인 창이 나와야. db 직접 조작 방식.
- self signup 온보딩 ui는 나중에.
	- il. claude code로 가면.
- sjs. 유저는 여러 org를 가질 수 있는 ui가 되지 않을까.

**phase 1 추천 제품**
- user는 여러 org 를 가질 수 있음. OrganizationMembership 연결 테이블로 연결.
- `Channel` 
- w. 하나의 병원에서 운영하지만, 원장님마다 채널을 가져감. 알고리즘 세팅이 다르게 들어가야 함. 하나 workspace는 여러 멀티플
- w. 하나 채널 컨텐츠들을 구분하려면 선택해야. workspace 안에 채널들이 종속되는 게 맞다.
	- jh. 비디오 템플릿처럼 분리할 수는 없지 않을까.
- w. workspace 단위로 데이터 인사이트 모듈이 묶인다.
	- w. 같은 채널이라도, 다른 insight를 사용하고 싶다면 다른 workspace로 분리해야.
	- q. `Channel` 과 `Workspace` 는 다르되, `Workspace` 하위로 여러 채널을 연동할 수 있다..?
- 과금체계를 org로 가져와야 함. org 안에 두명이 있다면 과금 어떻게.
- js. 입금을 받으면 되지만, 크레딧 부여만 고민.
- org list로 기준되면 어떨까.
- migration 으로 가면 어떨까.
- org 단위로 과금하는 게 깔끔하긴 한데, 그러면 중간 테이블로.

---

- q. `workspaceId`를 외부로 다는 게 어떨까.
- b2b 고객은 org 만들어지고 default workspace 만들고, 관련 유저 resource는 workspace 부여.
- org 안에는 1명의 유저만 있어야.
- q. shared credit 모델은 어떻게 가져가는가.
	- credit은 org로 할당하되, total quota를 workspace로 나눈다.
- q. billing으로 가져가는가.
	- js. organization의 credit 문제로 이어짐.
- w. 빌링에 대한 유스케이스는 미루자.
	- w. 크래프톤은 지금 형태에 가까움.

---

- admin dashboard가 나와야.
- w. usage에 대한 니즈가 있는 건 아님. phase1 단에선 고객의 니즈는 해결이 되지 않나.
- organization에 한 사람만 있다. 이걸 확장해 나간다.
- migration