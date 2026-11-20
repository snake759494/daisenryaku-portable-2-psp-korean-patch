# 원본 텍스처 확대 + 좌표 격자: python grid.py CONT GIM x0,y0,x1,y1 [scale]
import sys,cont,numpy as np
from PIL import Image,ImageDraw,ImageFont
from imgtool import Tex
c,g=sys.argv[1],sys.argv[2]; x0,y0,x1,y1=map(int,sys.argv[3].split(',')); sc=int(sys.argv[4]) if len(sys.argv)>4 else 3
d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}
o,s=it[g]; T=Tex(d[o:o+s])
im=Image.fromarray(T.rgba().astype(np.uint8)[:T.h],'RGBA'); bg=Image.new('RGBA',im.size,(150,150,150,255)); bg.alpha_composite(im)
bg=bg.crop((x0,y0,x1,y1)).convert('RGB').resize(((x1-x0)*sc,(y1-y0)*sc),Image.NEAREST); dr=ImageDraw.Draw(bg); f=ImageFont.truetype('arial.ttf',11)
for x in range((x0+9)//10*10,x1,10):
    dr.line([((x-x0)*sc,0),((x-x0)*sc,4 if x%50 else 10)],fill=(255,255,0)); 
    if x%50==0: dr.text(((x-x0)*sc+2,0),str(x),fill=(255,255,0),font=f)
for y in range((y0+9)//10*10,y1,10):
    dr.line([(0,(y-y0)*sc),(4 if y%50 else 10,(y-y0)*sc)],fill=(255,255,0))
    if y%50==0: dr.text((2,(y-y0)*sc+2),str(y),fill=(255,255,0),font=f)
bg.save('../work/grid.png')
