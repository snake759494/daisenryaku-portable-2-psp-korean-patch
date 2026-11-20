# 각 라벨: 새 글자 잉크가 원본 글자 잉크 영역을 벗어나는지 검사 (1편 imgdet 기준)
import sys,cont,numpy as np,collections
from imgtool import Tex,expand_jobs,fit_jobs
import imgspec2
out=[]
for (c,g),jobs in imgspec2.SPEC.items():
    d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}
    o,s=it[g]; A=Tex(d[o:o+s]); B=Tex(d[o:o+s]); J=expand_jobs(B,jobs); fit_jobs(B,J)
    for j in J:
        x,y,w,h,t=j[:5]
        if not t: continue
        a=A.idx[y:y+h,x:x+w]; b=B.idx[y:y+h,x:x+w]
        if a.size==0: continue
        bg=collections.Counter(np.concatenate([a[0],a[-1],a[:,0],a[:,-1]]).tolist()).most_common(1)[0][0]
        bg2=collections.Counter(np.concatenate([b[0],b[-1],b[:,0],b[:,-1]]).tolist()).most_common(1)[0][0]
        ia=np.nonzero((a!=bg).any(0))[0]; ib=np.nonzero(((b!=bg2)&(b!=a)).any(0))[0]
        ra=np.nonzero((a!=bg).any(1))[0]; rb=np.nonzero(((b!=bg2)&(b!=a)).any(1))[0]
        if len(ia)==0 or len(ib)==0: continue
        dx0=ia[0]-ib[0]; dx1=ib[-1]-ia[-1]; dy0=ra[0]-rb[0]; dy1=rb[-1]-ra[-1]
        if max(dx0,dx1)>0 or max(dy0,dy1)>0:
            out.append((g.split('/')[-1],t,(x,y,w,h),'orig x%d-%d y%d-%d'%(x+ia[0],x+ia[-1],y+ra[0],y+ra[-1]),'new x%d-%d y%d-%d'%(x+ib[0],x+ib[-1],y+rb[0],y+rb[-1])))
for r in out: print(*r)
print(len(out),'flags')
