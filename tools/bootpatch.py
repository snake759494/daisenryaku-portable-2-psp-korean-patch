import re,struct
T={'大戦略ポータブル２セーブデータ':'대전략 포터블2 세이브 데이터','新規作成データ':'신규 작성 데이터',
'決起':'궐기','反乱の炎':'반란의 불길','離反':'이반','奪還':'탈환','陽動':'양동','奇襲':'기습','帰還命令':'귀환 명령',
'勝利者':'승리자','極東の火事場':'극동의 화약고','反攻':'반격','残存部隊襲撃':'잔존부대 습격','撤退':'철수','防衛線突破':'방어선 돌파',
'急襲':'급습','後顧のうれい':'후방의 근심','アッカド作戦':'아카드 작전','防御陣地':'방어 진지','軍司令部攻略':'군사령부 공략',
'首都への道（西方戦線）':'수도로 가는 길(서부전선)','首都への道（東方戦線）':'수도로 가는 길(동부전선)',
'最終防衛線Ⅰ':'최종 방어선Ⅰ','最終防衛線Ⅱ':'최종 방어선Ⅱ','激流':'격류','首都包囲Ⅰ':'수도 포위Ⅰ','首都包囲Ⅱ':'수도 포위Ⅱ',
'首都包囲Ⅲ':'수도 포위Ⅲ','終局Ⅰ':'종국Ⅰ','終局Ⅱ':'종국Ⅱ',
'シナリオ名：%s\n出現マップ数：%d\nクリアミッション数：%d\n生産可能ユニット数：%d':'시나리오명：%s\n등장 맵 수：%d\n클리어 미션 수：%d\n생산 가능 유닛 수：%d'}
def patch(b):
    b=bytearray(b); base=0xe4200; seg=bytes(b[base:0xe4600]); n=0
    for m in re.finditer(rb'[^\x00]+',seg):
        try: t=m.group().decode('utf8')
        except: continue
        if t not in T: continue
        st=base+m.start(); room=st+len(m.group())
        while b[room]==0: room+=1
        room=room-st-1; ko=T[t].encode('utf8')
        if len(ko)>room: ko=T[t].replace(' ','').encode('utf8')
        if len(ko)>room: print('too long',T[t],len(ko),room); continue
        b[st:st+room]=ko+b'\0'*(room-len(ko)); n+=1
    print('boot strings',n,'/',len(T)); return bytes(b)
def build(W):
    b=bytearray(patch(open(W('work','ext','PSP_GAME','SYSDIR','BOOT.BIN'),'rb').read()))
    # OSK (nickname input) description, UTF-16LE, 16 slots incl. terminator
    o=0xee8cc; assert b[o:o+4]==bytes.fromhex('00672759')
    k='최대 ８글자까지 입력 가능'.encode('utf-16-le')+bytes(2); assert len(k)<=32
    b[o:o+32]=k+bytes(32-len(k)); b=bytes(b)
    sf=bytearray(open(W('work','ext','PSP_GAME','PARAM.SFO'),'rb').read())
    kt,dt,n=struct.unpack_from('<III',sf,8)
    for i in range(n):
        ko,fmt,ln,mx,do=struct.unpack_from('<HHIII',sf,20+16*i)
        if sf[kt+ko:kt+ko+6]==b'TITLE\0':
            t='대전략 포터블2'.encode('utf8')+b'\0'
            sf[dt+do:dt+do+mx]=t+b'\0'*(mx-len(t)); struct.pack_into('<I',sf,20+16*i+4,len(t))
    return {'PSP_GAME/SYSDIR/BOOT.BIN':b,'PSP_GAME/SYSDIR/EBOOT.BIN':b,'PSP_GAME/PARAM.SFO':bytes(sf)}
