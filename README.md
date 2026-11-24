# 대전략 포터블2 (PSP) 비공식 한글패치

PSP 일본판 **大戦略ポータブル2 (대전략 포터블2, ULJM-05205, v1.01)** 비공식 한국어 패치입니다. 이 저장소에는 제작 도구와 기술 문서만 있고, 패치 파일(xdelta)은 [Releases](../../releases)에서 받을 수 있습니다. 게임 원본·일본어 원문·번역 대본은 포함하지 않습니다.

## 적용 방법

1. 아래 해시와 일치하는 **원본 `.iso`** 를 준비합니다. (CSO·CHD 등으로 변환한 이미지에는 적용할 수 없습니다.)
   - PowerShell: `Get-FileHash -Algorithm MD5 -LiteralPath '.\Daisenryaku Portable 2 (Japan).iso'`
2. xdeltaUI 같은 도구로 원본 `.iso` 에 `DaisenryakuPortable2_KO_v1.1.xdelta` 를 적용합니다. (Patch = xdelta, Source File = 원본 ISO, Output File = 새 파일명)
   - 명령줄: `xdelta3 -d -s "Daisenryaku Portable 2 (Japan).iso" DaisenryakuPortable2_KO_v1.1.xdelta "Daisenryaku Portable 2 (Korean).iso"`
3. 만들어진 ISO를 PPSSPP 또는 커스텀 펌웨어(PSP·PS Vita Adrenaline 등)에서 실행합니다.

| 항목 | 값 |
| --- | --- |
| 원본 ISO 크기 | 414,941,184 바이트 |
| 원본 ISO MD5 | `8451acb4b5513679d494ce246d1e341d` |
| 원본 ISO SHA-256 | `f4018d3f38c9a0d8df12f498f702fc91babe6b0993eda8a7028bb2f5a956de9c` |
| xdelta SHA-256 | `80d635876d3eb05e42db4ec61b825242ec2227359c29defc1430c22666f7d796` |
| 결과 ISO 크기 | 415,105,024 바이트 |
| 결과 ISO SHA-256 | `5c562f9171d579e831a1a522cc3a890718f086458eb5ea4da94c094bb7ba40a7` |

## 주의
- 암호화되지 않은 수정 실행 파일(BOOT.BIN)을 EBOOT.BIN 자리에도 넣었기 때문에 **PPSSPP·커스텀 펌웨어 전용**입니다. 정품 펌웨어에서는 부팅되지 않습니다.
- v1.01 원본 전용입니다.
- 원본에서 만든 **상태저장(세이브 스테이트)** 은 불러오지 마세요. 일반 세이브 데이터는 그대로 쓸 수 있습니다.
- 전작 『대전략 포터블』 세이브 연동(특전 유닛)도 그대로 동작합니다.
- xdelta는 2차 압축을 쓰지 않은 형식입니다(약 1.3MB).

## 한글화 내용
- 게임 문자열 1,280항목(시나리오 줄거리·미션 브리핑, 유닛 이름·설명, 지형, 무기, 메뉴, 도움말, 확인창, 승리 조건 등) 전체 직접 번역 (기계 번역 사용하지 않음)
- 게임 글꼴에 한글 550자 추가 (갈무리11 기반 도트 글꼴)
- 실행 파일 문자열: 세이브 데이터 제목·설명, 시나리오 이름 31개, 시나리오 정보 표시 형식, 게임 제목(PARAM.SFO)
- 그림 글자 19장·라벨 449개: 메뉴 제목, 모드 선택, 진영 선택, 병기 생산, 부대 정리, 전황·부대표·유닛 상세·지형 정보 창, 옵션, 버튼 안내, 대화상자, 결과 화면 등
  - 원본과 비슷한 글꼴(나눔스퀘어네오·서울한강체)을 쓰고, 작은 글씨는 갈무리 글꼴로 선명하게 그렸습니다.
  - 각 글자는 원본 일본어 글자의 잉크 영역을 측정해 그 안에 맞췄습니다.
- 타이틀 로고 아래에 「대전략 포터블2」 한글 자막을 넣었습니다.

## 그대로 둔 것
- 타이틀 로고 그림 자체(한글 자막만 추가), 부팅 시 회사 로고, 「press start button」·저작권 표기
- 「Name」·「Category」·「Weapon」·「RESULT」·「Map:」 같은 영문 장식 글자
- 실제 무기 이름(PzH2000, Wiesel 등)

## 검증 범위
PPSSPP에서 타이틀, 전작 세이브 확인, 모드 선택, 시나리오 서장·미션 브리핑, 진영 선택, 군자금 수입, 전장 맵, 병기 생산·확인창, 전황, 맵 메뉴·도움말, 옵션, 부대표, 지형 정보 화면을 실제로 확인했습니다. 그림 글자는 원본 글자 영역을 벗어나는지 전수 검사했고, 번역문에 일본어가 남지 않았음을 검사했습니다. 후반 시나리오 화면과 실기 PSP는 직접 확인하지 못했습니다. 문제를 발견하면 Issues로 알려 주세요.

## 문서
- [CHANGELOG.md](CHANGELOG.md) — 변경 기록
- [docs/TECHNICAL.md](docs/TECHNICAL.md) — 파일 형식과 한글화 방법
- [docs/BUILD.md](docs/BUILD.md) — 직접 빌드하는 방법
- [docs/TRANSLATION_GUIDE.md](docs/TRANSLATION_GUIDE.md) — 번역 지침
- [docs/FONT_CREDITS.md](docs/FONT_CREDITS.md) — 글꼴
- [RIGHTS.md](RIGHTS.md) — 권리 및 외부 자료
