"""collect sprite rects (+palette index) from all dumps -> ../work/rects.json"""
import glob,json,os,numpy as np,cont
import rects
from imgtool import Tex
ISO='../Daisenryaku Portable 2 (Korean).iso'
def pals(c,g):
    d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}; o,s=it[g]; T=Tex(d[o:o+s])
    return [p.astype(np.uint8).tobytes() for p in [T.pal]+T.pals]
def main():
    db=json.load(open('../work/rects.json')) if os.path.exists('../work/rects.json') else {}
    done=set(db.get('_files',[])); P={}
    for f in sorted(glob.glob('../work/dumps/*.json')):
        if f in done: continue
        try: R=rects.rects(f,ISO)
        except Exception as e: print('bad',f,e); continue
        for q in R:
            x0,y0,x1,y1=q['r']
            if x1-x0>=300 or x1-x0<3 or y1-y0<3: continue
            key=q['c']+'|'+q['g']
            if key not in P: P[key]=pals(q['c'],q['g'])
            cl=q['clut']; pi=-1
            for i,p in enumerate(P[key]):
                n=min(len(cl),len(p))
                if n and cl[:n]==p[:n]: pi=i; break
            L=db.setdefault(key,[])
            e=[x0,y0,x1,y1,pi]
            if e not in L: L.append(e)
        done.add(f)
    db['_files']=sorted(done); json.dump(db,open('../work/rects.json','w'))
    for k,v in db.items():
        if k!='_files': print(k,len(v))
if __name__=='__main__': main()
