# P1 작업 영역을 P2 텍스처에서 템플릿 매칭으로 재배치 -> imgspec_reloc.py
import cont,numpy as np,cv2,pprint
from imgtool import Tex
import imgspec
P1D='../../대전략포터블1/work/dec/'; P1E='../../대전략포터블1/work/ext/PSP_GAME/USRDIR/'; P2='../work/ext/PSP_GAME/USRDIR/'
m2={'UI/tex_op_ash.dat':'UI/tex_op.ofs','UI/tex_ui_ash.dat':'UI/tex_ui.ofs','UI/tex_sh_ash.dat':'UI/tex_sh.ofs','UI/tex_wib.ofs':'UI/tex_wib.ofs'}
def tex(p,g):
    d=open(p,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}; o,s=it[g]; T=Tex(d[o:o+s]); R=T.rgba()[:T.h]
    return (R[...,:3]*(R[...,3:4]/255)).astype(np.float32)
out={}; rep=[]
for (c,g),jobs in imgspec.SPEC.items():
    a=tex(P1D+c.replace('/','__') if not c.endswith('.ofs') else P1E+c,g); b=tex(P2+m2[c],g)
    L=[]
    for j in jobs:
        x,y,w,h=j[:4]; t=a[y:y+h,x:x+w]
        if t.shape[0]!=h or t.shape[1]!=w or t.std()<5: L.append(j); rep.append((c,g,j[4],'flat')); continue
        if b[y:y+h,x:x+w].shape==t.shape and np.abs(b[y:y+h,x:x+w]-t).mean()<4: L.append(j); continue
        r=cv2.matchTemplate(b,t,cv2.TM_SQDIFF); mn,_,loc,_=cv2.minMaxLoc(r); err=np.sqrt(mn/t.size)
        if err<6:
            j=[loc[0],loc[1]]+list(j[2:]); L.append(j); rep.append((c,g,j[4],'moved',(x,y),loc))
        else: L.append(j); rep.append((c,g,j[4],'LOST',(x,y),round(float(err),1)))
    out[(m2[c],g)]=L
open('imgspec_p1.py','w',encoding='utf8').write('SPEC='+pprint.pformat(out,width=220)+'\n')
for r in rep:
    if r[3]!='flat': print(r[1],r[2],r[3],r[4:])
