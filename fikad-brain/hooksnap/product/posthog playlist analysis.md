



playlist analysis
- https://us.posthog.com/project/307101/replay/playlists/gQwVGWM2 - what url formats are people pasting? what do they do after the error?
	  - user 0
	  - user 1
		  - onboarding시 free user는 template 생성이 막힘.(style extraction시 에러)
		  - url 넣었을 때, failed to fetch만 보이고 자세한 에러 메시지가 안보임.
		  - 초기 상단 "paste a youtube url" 이 버튼처럼 보여서 유저가 클릭하게 됨.
		  - 초기에 가입한 유저는 "failed to load workspaces"가 보이면서 워크스페이스 로딩이 안됨.
		  - 인터넷이 느린 환경에서는 workspace/credit loading이 굉장히 느림 -> 아예 video analysis를 할 수 없음.
		  - analyze video -> thread 까지 이어지는 2-step funnel이 friction이 있을 수도 있음. 바로 thread를 생성해주는 게 어떨까.
		  - "Generate thumbnails" 버튼이 inactive 일 때, template을 선택하도록 강제해야 함. -> 처음 template을 default 선택하거나, 아니면 paginated 로 선택할 수 있게.
		  - 아직도 default template에 대한 preview image가 처음 가입시 안나오는 경우가 있음.
		  - thread 생성시, 애초에 로딩바를 보여주는 게 아니라, 추가적으로 다른 thread를 만들거나 다른 project를 만들 수 있도록 nudging을 주는 페이지를 만드는 건 어떨까.
		  - "checkbox"를 눌러 다운로드를 하는게 비직관적임. 주로 thumbnail 자체를 누르게 됨. thumbnail image를 클릭해도 check가 되게끔 하는 건 어떨까.
	  - user 2
		  - landing을 진짜 자세히 본다. 하나하나 다 읽는다. 랜딩을 정말 잘 작성해야 한다.
		  - 질문지 선택을 못바꿔서 이탈하는 경우도 있음.
		  - onboarding 에서 downloading your video를 다 기다리지 못하고 churn.
	- user 3
		- url에서 failed to analyze the video로 몇 번 막히고, 결국 downloading your video에서 churn.
  - https://us.posthog.com/project/307101/replay/playlists/uE7Uk5ow - focus on user 0b36ffb1. where do they get stuck?
	  - user 1
		  - "popular templates" 노출하지 말기. - 어차피 showcases로 바뀔 것.
		  - "generation appears to be stuck" 가 사라졌는지 체크해보기.
		  - 
	- user 2
  - https://us.posthog.com/project/307101/replay/playlists/fUGQwq3u - how long do people wait before leaving?
  - https://us.posthog.com/project/307101/replay/playlists/07y4ZRoU - what do they do after hitting the wall?


#### ideas
- onboarding gamification
	- onboarding을 위해서 해야할 checklist page를 persistent 하게 만들고, 하나하나 완성할 때 마다 checklist complete 하게 한다. percentage를 두고, 각 항목별로 3 credit을 지급한다. 모두다 완료하면 추가 10 credit을 지급한다.
	- youtube channel 연동하고 a/b test를 돌릴 수 있게 한다. 


