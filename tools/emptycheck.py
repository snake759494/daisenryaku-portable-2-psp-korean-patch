import cont,numpy as np
from imgtool import Tex,expand_jobs,lum
import imgspec2
for (c,g),jobs in imgspec2.SPEC.items():
    d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}
    o,s=it[g]; A=Tex(d[o:o+s]); R=A.rgba(); L=lum(R)
    for j in expand_jobs(A,jobs):
        x,y,w,h,t=j[:5]
        if not t: continue
        b=L[y:y+h,x:x+w]
        if b.size==0: continue
        # 글자 = 강한 명암 변화(가로 방향 고주파)
        e=np.abs(np.diff(b,axis=1)).mean()
        if e<12: print(g.split('/')[-1],repr(t),(x,y,w,h),'edge=%.1f'%e)
