# 직접 빌드하기

필요한 것: Python 3.11 이상, `pip install pillow numpy scipy pycdlib capstone websocket-client`, 원본 ISO(README 해시와 일치), 글꼴(`FONT_CREDITS.md`), 번역 대본.

1. 원본 ISO를 프로젝트 루트에 `Daisenryaku Portable 2 (Japan).iso` 이름으로 둡니다.
2. 파일 추출: `python tools/extract.py "Daisenryaku Portable 2 (Japan).iso" work/ext`
3. 원문 목록 만들기: `tools` 폴더에서 `python dump.py` → `work/ja_dump.txt` (`섹션.항목` 번호와 원문)
4. 번역 대본을 `work/trans/ko_*.tsv` 에 둡니다. 한 줄에 `번호<TAB>번역문` 형식입니다. 대본은 저장소에 없습니다.
5. 빌드: `python tools/build.py` → `Daisenryaku Portable 2 (Korean).iso` 생성 (원본 ISO는 수정하지 않음)
6. 배포 파일: `xdelta3 -0 -e -s "Daisenryaku Portable 2 (Japan).iso" "Daisenryaku Portable 2 (Korean).iso" DaisenryakuPortable2_KO_v1.0.xdelta`

## 확인용 도구
- `tools/emu.py` — PPSSPP 디버거(WebSocket)로 실행·버튼 입력·화면 캡처 (`PPSSPP_EXE` 환경 변수로 실행 파일 지정)
- `tools/sbs.py` — 그림 글자 원본/한글 나란히 미리보기
- `tools/inkcheck.py`, `tools/emptycheck.py` — 한글이 원본 글자 영역을 벗어나거나 빈 라벨이 남았는지 검사
- `tools/imgprev.py`, `tools/imgdet.py` — 그림 글자 미리보기·원본 글자 영역 검출 (`IMG_PREVIEW_DIR` 에 저장)
- `tools/scan.py` — 실행 파일·데이터에서 게임 문자 코드 문자열 찾기
