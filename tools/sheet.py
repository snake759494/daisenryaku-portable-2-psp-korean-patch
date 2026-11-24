"""contact sheet per texture from rects.json: orig | patched (actual palette)"""
import sys,json,numpy as np,cont
from PIL import Image,ImageDraw
from imgtool import Tex
import pycdlib,io
ISO='../Daisenryaku Portable 2 (Korean).iso'
def load(c,g,iso=None,data=None):
    if data is not None: d=data
    elif iso:
        I=pycdlib.PyCdlib(); I.open(iso); f=io.BytesIO(); I.get_file_from_iso_fp(f,iso_path='/PSP_GAME/USRDIR/'+c); d=f.getvalue(); I.close()
    else: d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read()
    it={n:(o,s) for n,o,s in cont.parse(d)}; o,s=it[g]; return Tex(d[o:o+s])
def rgba(T,pi): return ([T.pal]+T.pals)[max(pi,0)][T.idx][:T.h].astype(np.uint8)
def sheet(key,out,B=None,sc=3,only=None):
    db=json.load(open('../work/rects.json')); c,g=key.split('|')
    A=load(c,g); B=B or load(c,g,ISO)
    R=sorted(db[key],key=lambda r:(r[1],r[0]))
    if only: R=[r for r in R if only(r)]
    tiles=[]
    for x0,y0,x1,y1,pi in R:
        P=lambda M:np.pad(M,((2,2),(2,2),(0,0)))[y0:y1+4,x0:x1+4]
        tiles.append(((x0,y0,x1,y1,pi),P(rgba(A,pi)),P(rgba(B,pi))))
    W=max(t[1].shape[1] for t in tiles)*sc*2+200; H=sum(t[1].shape[0]*sc+4 for t in tiles)
    im=Image.new('RGB',(W,H),(255,0,255)); dr=ImageDraw.Draw(im); y=0
    for r,a,b in tiles:
        h,w=a.shape[:2]
        for j,cimg in enumerate((a,b)):
            t=Image.new('RGBA',(w,h),(60,60,90,255)); t.alpha_composite(Image.fromarray(cimg,'RGBA'))
            t=t.resize((w*sc,h*sc),Image.NEAREST); X=j*(w*sc+4); im.paste(t.convert('RGB'),(X,y))
            dr.rectangle([X+2*sc,y+2*sc,X+(w-2)*sc-1,y+(h-2)*sc-1],outline=(255,0,0))
        dr.text((2*w*sc+12,y),str(list(r)),fill=(255,255,255)); y+=h*sc+4
    im.save(out); return len(tiles)
if __name__=='__main__':
    print(sheet(sys.argv[1],sys.argv[2]))
