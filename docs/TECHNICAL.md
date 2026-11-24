# 기술 문서

## 디스크 구성
- `PSP_GAME/SYSDIR/BOOT.BIN` — 암호화되지 않은 실행 파일. 세이브 제목·시나리오 이름 31개·시나리오 정보 형식 문자열 등 UTF-8 문자열이 0xE4200–0xE4600 부근에 있습니다(`tools/bootpatch.py`). 수정본을 `EBOOT.BIN` 자리에도 넣습니다.
- `PSP_GAME/PARAM.SFO` — 게임 제목(「대전략 포터블2」).
- `PSP_GAME/USRDIR/` — 게임 데이터. 같은 내용이 무압축 파일과 LZSS 압축본(`*_ash.dat`) 두 벌로 들어 있어 둘 다 교체합니다(`tools/lzss.py`).

## 문자열 (`STRING/string.ofs`)
- 섹션 표 → 섹션마다 항목 표가 있는 구조이고, 각 문자열은 16비트 글자 코드 배열입니다(`tools/strfile.py`).
- 글자 코드는 게임 글꼴의 칸 번호입니다. 0x1FF는 줄바꿈입니다. 일본어 문자표는 `tools/jtable.py`·`tools/jtable2.json`.
- 번역에 쓰인 한글 글자를 모아, 번역 후 쓰이지 않게 된 글꼴 칸에 배정합니다(`tools/kfont.py`).
- 번역문 앞의 `#` 는 도움말 상자(원문 폭에 맞춰 자동 줄바꿈, 최대 4줄), `@` 는 시나리오 줄거리(문단 구분 `|`)를 뜻합니다(`tools/build.py`).

## 글꼴 (`STRING/font.gim`)
- 8비트 인덱스 GIM 한 장에 모든 글자가 격자로 들어 있습니다(`tools/gim.py`, `tools/gimfile.py`).
- 빈 칸에 갈무리11로 그린 한글 550자를 넣었습니다. 원본 글자와 같은 팔레트 단계(그림자 포함)를 씁니다.

## 그림 글자
- 메뉴·창 그림은 `UI/tex_op.ofs`·`tex_sh.ofs`·`tex_ui.ofs`·`tex_wib.ofs` 컨테이너에 여러 GIM으로 묶여 있습니다(`tools/cont.py`).
- `tools/imgspec2.py` 에 텍스처별로 「영역(x, y, 폭, 높이), 한국어 문구, 스타일」을 적어 두면 `tools/imgtool.py` 가 원본 글자를 지우고 한글을 그립니다(`tools/extras.py` 에서 호출). 전작과 같은 그림은 `tools/imgspec_p1.py` 를 좌표만 옮겨(`tools/relocate.py`) 재사용합니다.
- 게임은 각 라벨을 원본 일본어 글자의 잉크 영역만큼만 잘라 씁니다. 그래서 원본 글자의 잉크 열·행을 측정해 그 안에 한글을 맞추고, 그린 뒤에는 영역 밖 픽셀을 원본으로 되돌립니다. 맞는 크기가 없으면 갈무리 글꼴을 가로로 줄여 넣습니다.
- 화면에 어떤 텍스처가 쓰이는지는 PPSSPP의 텍스처 덤프(`SaveNewTextures`)로 찾았습니다.

## ISO 재구성
- `tools/isobuild.py` 가 원본 ISO를 복사한 뒤 바뀐 파일을 같은 자리(들어가지 않으면 이미지 끝)에 다시 써서 디렉터리 레코드를 고칩니다.

## v1.1: GPU 덤프로 그림 글자 영역 측정
- PPSSPP 디버거의 `gpu.record.dump` 로 화면 하나를 그리는 GE 명령을 저장하고(`tools/gedump.py`), through 모드 스프라이트의 UV에서 게임이 실제로 잘라 쓰는 텍스처 영역과 CLUT(팔레트)를 찾습니다(`tools/rects.py`, `tools/rectdb.py`).
- 텍스처 한 장에 팔레트가 여러 개 있어, 잘못된 팔레트 기준으로 색을 고르면 글자 뒤에 박스가 생깁니다. 이제 영역마다 실제 팔레트로 배경·글자색·외곽선을 판별합니다(`tools/rectjob.py`).
- 측정한 영역에 번역 문구를 배정하고(`tools/rassign.py`), 원본을 복원한 뒤 그 안에만 다시 그립니다(`tools/rapply.py`). 수동 지정은 `tools/imgspec3.py`.
