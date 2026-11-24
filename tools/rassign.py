import json,rectjob,imgspec2
def dedupe(L):
    seen={};out=[]
    for x0,y0,x1,y1,pi in L:
        k=(x0,y0,x1,y1)
        if k in seen: continue
        seen[k]=1; out.append([x0,y0,x1,y1,pi])
    return out
def assign(key,jobs,manual=None):
    import imgspec3
    db=rectjob.load_db(); R=dedupe(db.get(key,[])+imgspec3.EXTRA.get(key,[]))
    res=[];used={}
    manual=manual or {}
    for r in R:
        if tuple(r[:4]) in manual:
            res.append((r,manual[tuple(r[:4])],1.0)); continue
        x0,y0,x1,y1,pi=r; A=(x1-x0)*(y1-y0)
        best=None
        for ji,j in enumerate(jobs):
            if j[4] is None: continue
            jx,jy,jw,jh=j[:4]
            ix=max(0,min(x1,jx+jw)-max(x0,jx)); iy=max(0,min(y1,jy+jh)-max(y0,jy))
            ov=ix*iy/A; jv=ix*iy/max(1,jw*jh)
            if ov>=0.3 and jv>=0.6 and (best is None or ov>best[0]): best=(ov,ji)
        if best: res.append((r,best[1],best[0]))
    return R,res
if __name__=='__main__':
    import sys
    for (c,g),jobs in imgspec2.SPEC.items():
        R,res=assign(c+'|'+g,jobs)
        if not R: continue
        print('==',g,len(R),'rects',len(res),'assigned')
        for r,ji,ov in res: print('  ',r[:4],'pal',r[4],'<-',jobs[ji][:5],round(ov,2))
