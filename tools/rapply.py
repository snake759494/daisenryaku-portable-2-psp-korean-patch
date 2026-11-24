"""apply: old jobs for rects not covered, then rect-exact rendering for measured rects"""
import numpy as np,rectjob,rassign
from imgtool import expand_jobs,fit_jobs
import imgspec3
def apply(T,c,g,jobs):
    key=c+'|'+g; man=imgspec3.RT.get(key,{})
    R,res=rassign.assign(key,jobs,man)
    used=set(ji for _,ji,_ in res if isinstance(ji,int))
    for r,ji,_ in res:
        if isinstance(ji,int) or ji is None: continue
        x0,y0,x1,y1=r[:4]
        for i,j in enumerate(jobs):
            if j[4] is None: continue
            jx,jy,jw,jh=j[:4]; ix=max(0,min(x1,jx+jw)-max(x0,jx)); iy=max(0,min(y1,jy+jh)-max(y0,jy))
            if ix*iy>=0.5*jw*jh: used.add(i)
    rest=[j for i,j in enumerate(jobs) if i not in used]
    if rest: fit_jobs(T,expand_jobs(T,rest))
    pals=[T.pal]+T.pals
    asg=set(tuple(r[:4]) for r,_,_ in res)
    for x0,y0,x1,y1,pi in R:
        if (x0,y0,x1,y1) in asg: continue
        inside=False
        for j in jobs:
            if j[4] is None: continue
            jx,jy,jw,jh=j[:4]; ix=max(0,min(x1,jx+jw)-max(x0,jx)); iy=max(0,min(y1,jy+jh)-max(y0,jy))
            if ix*iy>=0.6*jw*jh: inside=True
        if not inside: T.idx[y0:y1,x0:x1]=T.orig[y0:y1,x0:x1]
    for r,ji,_ in res:
        x0,y0,x1,y1,pi=r
        if isinstance(ji,int):
            text,o=jobs[ji][4],{}
            off=jobs[ji][0]-x0
            if off>=8 and x1-x0>34:
                sub=T.orig[y0:y1,x0:x1]; b=np.bincount(np.concatenate([sub[0],sub[-1],sub[:,0],sub[:,-1]])).argmax()
                c=(sub!=b).any(0); xs=[x for x in range(1,len(c)) if c[x] and not c[x-1] and x>=off-4]
                if xs and xs[0]<=off+3: o['keepx']=xs[0]-1
        elif ji is None: continue
        elif isinstance(ji,tuple): text,o=ji
        else: text,o=ji,{}
        o={**imgspec3.DEF.get(key,{}),**o}
        T.idx[y0:y1,x0:x1]=T.orig[y0:y1,x0:x1]
        rectjob.render(T,(x0,y0,x1,y1),pals[max(pi,0)],text,o)
    return R,res
