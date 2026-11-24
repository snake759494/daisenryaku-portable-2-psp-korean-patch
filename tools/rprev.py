"""preview: run full pipeline on one texture in memory, sheet of all measured rects (orig|new), mark unassigned"""
import sys,cont,numpy as np,json
from imgtool import Tex
import imgspec2,rapply,rectjob,sheet
from PIL import Image,ImageDraw
def build(c,g):
    d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}; o,s=it[g]
    T=Tex(d[o:o+s]); R,res=rapply.apply(T,c,g,imgspec2.SPEC.get((c,g),[])); return T,R,res
if __name__=='__main__':
    key=sys.argv[1]; c,g=key.split('|'); T,R,res=build(c,g)
    A=sheet.load(c,g); asg={tuple(r[:4]):ji for r,ji,_ in res}
    mode=sys.argv[3] if len(sys.argv)>3 else 'all'
    sc=3; tiles=[]
    for x0,y0,x1,y1,pi in sorted(R,key=lambda r:(r[1],r[0])):
        k=(x0,y0,x1,y1); a=k in asg
        if mode=='a' and not a: continue
        if mode=='u' and a: continue
        P=lambda M:np.pad(M,((2,2),(2,2),(0,0)))[y0:y1+4,x0:x1+4]
        tiles.append((k,pi,a,P(sheet.rgba(A,pi)),P(sheet.rgba(T,pi))))
    W=max(t[3].shape[1] for t in tiles)*sc*2+220; H=sum(t[3].shape[0]*sc+4 for t in tiles)
    im=Image.new('RGB',(W,H),(255,0,255)); dr=ImageDraw.Draw(im); y=0
    for k,pi,a,A_,B_ in tiles:
        h,w=A_.shape[:2]
        for j,ci in enumerate((A_,B_)):
            t=Image.new('RGBA',(w,h),(60,60,90,255)); t.alpha_composite(Image.fromarray(ci,'RGBA'))
            X=j*(w*sc+4); im.paste(t.resize((w*sc,h*sc),Image.NEAREST).convert('RGB'),(X,y))
            dr.rectangle([X+2*sc,y+2*sc,X+(w-2)*sc-1,y+(h-2)*sc-1],outline=(255,0,0) if a else (0,255,0))
        dr.text((2*w*sc+12,y),'%s p%d'%(list(k),pi),fill=(255,255,255)); y+=h*sc+4
    im.save(sys.argv[2]); print(len(tiles),rectjob.LOG[:20])
