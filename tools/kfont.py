"""STRING/font_ash.dat: 512x512 idx8 swizzled GIM, 12x12 cells (42x42), palette = white with alpha ramp."""
import numpy as np, os, struct
from PIL import Image, ImageDraw, ImageFont
import gim, gimfile, jtable
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT=os.path.join(ROOT,'fonts','Galmuri11.ttf')
# half-width codes: 0x80+col of row0
HALF={' ':0x9B,',':0x80,'.':0x81,':':0x83,';':0x84,'/':0x86,'|':0x87,'(':0x8C,')':0x8D,'[':0x8E,']':0x8F,'-':0x95,'+':0x94,'*':0x98,'=':0x97}
FULL={}
for code,ch in jtable.J.items():
    if code<0x80 or code>=0x100: FULL.setdefault(ch,code)
for o in range(0x21,0x7f):
    fw=chr(o+0xfee0)
    if fw in FULL and chr(o) not in HALF: FULL[chr(o)]=FULL[fw]
FULL['　']=0x622; FULL['~']=FULL['～']; FULL['·']=FULL['・']
def base_map(): 
    m=dict(FULL); m.update(HALF); return m
def is_jp(ch):
    o=ord(ch); return 0x3040<=o<=0x30ff or 0x4e00<=o<=0x9fff
def free_slots(used):
    """cells usable for hangul: empty cells first, then kanji, then kana, never codes still in use"""
    empty=[];kan=[];kana=[]
    for r in range(42):
        for c in range(42):
            code=(r<<8)|c
            if code in used or code==0x622: continue
            ch=jtable.J.get(code)
            if ch is None:
                if r>=7: empty.append(code)
            elif 0x4e00<=ord(ch)<=0x9fff: kan.append(code)
            elif 0x3040<=ord(ch)<=0x30ff: kana.append(code)
    return empty+kan+kana
def render(ch,font):
    im=Image.new('L',(12,12),0); ImageDraw.Draw(im).text((0,0),ch,font=font,fill=255)
    return np.asarray(im)
def build(orig,cmap):
    d=bytearray(orig); I=gimfile.info(d); p=I['img']['pix']; pp=I['pal']['pix']
    pal=[tuple(d[pp+4*i:pp+4*i+4]) for i in range(256)]
    cand=[i for i in range(256) if pal[i][:3]==(255,255,255)]
    idx=np.array([min(cand,key=lambda i:abs(pal[i][3]-a)) for a in range(256)])
    px=np.frombuffer(gim.unswizzle(bytes(d[p:p+512*512]),512,512),np.uint8).reshape(512,512).copy()
    font=ImageFont.truetype(FONT,12)
    for ch,code in cmap.items():
        r,c=code>>8,code&0xff; a=render(ch,font)
        px[r*12:r*12+12,c*12:c*12+12]=idx[a]
    d[p:p+512*512]=gim.swizzle(px.tobytes(),512,512)
    return bytes(d)
