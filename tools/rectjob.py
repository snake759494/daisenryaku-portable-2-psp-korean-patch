"""Rect-exact label renderer.
Rects come from PPSSPP GE frame dumps (../work/rects.json): the exact texture area the game draws,
plus the CLUT index it is drawn with.  Each translated label is redrawn strictly inside its rect, in
index space (palette independent), and the Japanese glyphs (fill + outline) are erased by row/column
inpainting from the surrounding background pixels."""
import os,json,numpy as np
from PIL import Image,ImageDraw,ImageFont
from scipy import ndimage as nd
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
F_NANUM={'r':'NanumSquareNeo-bRg.ttf','b':'NanumSquareNeo-cBd.ttf','eb':'NanumSquareNeo-dEb.ttf'}
GALS=[('fonts/Galmuri14.ttf',15),('fonts/Galmuri11.ttf',12),('fonts/Galmuri9.ttf',10)]
LOG=[]
def load_db():
    p=os.path.join(ROOT,'work','rects.json')
    return json.load(open(p)) if os.path.exists(p) else {}

def classify(T,r,pal):
    """-> bgmask, inkmask(Japanese glyph incl. outline) for rect r in orig"""
    x0,y0,x1,y1=r; sub=T.orig[y0:y1,x0:x1]
    P=pal[sub]; h,w=sub.shape
    border=np.concatenate([sub[0],sub[-1],sub[:,0],sub[:,-1]])
    cnt=np.bincount(border,minlength=256)
    bgset=set(np.nonzero(cnt>=max(2,0.12*len(border)))[0])
    order=np.argsort(-cnt); acc=0
    for i in (order if not bgset else []):
        if acc>=0.85*len(border) or cnt[i]==0: break
        bgset.add(int(i)); acc+=cnt[i]
    bg=np.isin(sub,list(bgset))
    # colour-similar pixels to bg are bg too (gradients)
    bcols=pal[list(bgset)][:,:4]
    d=np.abs(P[:,:,None,:]-bcols[None,None]).sum(-1).min(-1)
    bg|=d<40
    ink=~bg
    # drop tiny isolated specks that touch border (frame details)
    lab,n=nd.label(ink,structure=np.ones((3,3)))
    for i in range(1,n+1):
        c=lab==i
        ys,xs=np.nonzero(c)
        if c.sum()<=2 and (ys.min()==0 or xs.min()==0 or ys.max()==h-1 or xs.max()==w-1): ink[c]=False
    return ~ink,ink

def inpaint(sub,ink):
    out=sub.copy(); h,w=sub.shape
    if not ink.any(): return out
    # nearest non-ink along row, fallback column
    idx=np.where(~ink,np.arange(w)[None,:],-10**6)
    left=np.maximum.accumulate(idx,axis=1)
    idx2=np.where(~ink,np.arange(w)[None,:],10**6)
    right=np.minimum.accumulate(idx2[:,::-1],axis=1)[:,::-1]
    for y,x in zip(*np.nonzero(ink)):
        l,rr=left[y,x],right[y,x]
        if l>=0 and (rr>=w or x-l<=rr-x): out[y,x]=sub[y,l]
        elif rr<w: out[y,x]=sub[y,rr]
        else:
            col=np.nonzero(~ink[:,x])[0]
            if len(col): out[y,x]=sub[col[np.abs(col-y).argmin()],x]
    return out

def _pm(c): return np.array([c[0]*c[3]/255.,c[1]*c[3]/255.,c[2]*c[3]/255.,c[3]])
def _d(a,b): return np.abs(_pm(a)-_pm(b)).sum()
def style(sub,ink,bgm,pal):
    bc=np.bincount(sub[bgm],minlength=256) if bgm.any() else np.bincount(sub.ravel(),minlength=256)
    bgi=int(bc.argmax()); B=pal[bgi]
    cnt=np.bincount(sub[ink],minlength=256); tot=cnt.sum()
    cand=[i for i in np.nonzero(cnt)[0] if cnt[i]>=0.08*tot]
    fill=int(max(cand,key=lambda i:_d(pal[i],B)))
    fm=(sub==fill)&ink
    ring=ink&~fm&nd.binary_dilation(fm,structure=np.ones((3,3)))
    outline=None
    if ring.sum()>=0.3*fm.sum():
        oc=np.bincount(sub[ring],minlength=256); oi=int(oc.argmax())
        if oc[oi]>=0.5*ring.sum() and _d(pal[oi],B)>60 and _d(pal[oi],pal[fill])>150: outline=oi
    return fill,outline

def _mask(text,font,size):
    F=ImageFont.truetype(os.path.join(ROOT,font),size)
    b=F.getbbox(text)
    im=Image.new('L',(b[2]-b[0]+4,b[3]-b[1]+4),0); dr=ImageDraw.Draw(im)
    if 'Galmuri' in font: dr.fontmode='1'
    dr.text((2-b[0],2-b[1]),text,font=F,fill=255)
    a=np.asarray(im)>(110 if 'Galmuri' not in font else 127)
    ys,xs=np.nonzero(a)
    return a[ys.min():ys.max()+1,xs.min():xs.max()+1] if len(xs) else a[:0,:0]

def pick(text,maxw,maxh,prefer,bold=False):
    """largest crisp mask fitting maxw x maxh"""
    cands=[]
    if maxh>=17 and prefer!='gal':
        fn=F_NANUM.get(prefer,F_NANUM['b'])
        for sz in range(maxh+4,9,-1):
            for t in (text,text.replace(' ','')) if ' ' in text else (text,):
                m=_mask(t,fn,sz)
                if m.shape[0]<=maxh and m.shape[1]<=maxw: return m
                if m.shape[0]<=maxh: cands.append(m)
    gl=([GALS[0]] if maxh>=17 else [])+([('fonts/Galmuri11-Bold.ttf',12)] if bold else [])+GALS[1:]
    for fn,sz in gl:
        if not os.path.exists(os.path.join(ROOT,fn)): continue
        for t in (text,text.replace(' ','')) if ' ' in text else (text,):
            m=_mask(t,fn,sz)
            if m.shape[0]<=maxh and m.shape[1]<=maxw: return m
            if m.shape[0]<=maxh: cands.append(m)
    # squeeze horizontally the tallest fitting candidate
    m=max(cands,key=lambda a:a.shape[0]) if cands else _mask(text,GALS[-1][0],GALS[-1][1])
    LOG.append(('squeeze',text,maxw,maxh,m.shape))
    im=Image.fromarray((m*255).astype(np.uint8)).resize((max(1,min(maxw,m.shape[1])),max(1,min(maxh,m.shape[0]))),Image.BOX)
    return np.asarray(im)>100

def render(T,r,pal,text,o=None):
    o=o or {}
    x0,y0,x1,y1=r; sub=T.orig[y0:y1,x0:x1].copy(); h,w=sub.shape
    bgm,ink=classify(T,r,pal)
    if 'ink' in o: ink=o['ink'](sub); bgm=~ink
    if o.get('allink'):
        hi=np.zeros(256,bool); hi[o['allink']]=True; ink=hi[sub]; bgm=~ink
    kx=o.get('keepx',0)
    if kx: ink[:,:kx]=False; bgm[:,:kx]=True
    if not ink.any(): LOG.append(('noink',text,r)); return
    fill,outline=style(sub,ink,bgm,pal)
    if o.get('sample'):
        core=nd.binary_erosion(ink); ring=nd.binary_dilation(ink)&~ink
        cc=np.bincount(sub[ink].ravel(),minlength=256); lum=pal[:,:3].sum(1)*pal[:,3]
        ok=cc>=max(3,0.05*cc.sum()); fill=int(np.argmax(np.where(ok,lum,-1)))
        rc=np.bincount(sub[ring].ravel(),minlength=256); ol=int(rc.argmax())
        outline=ol if lum[ol]<lum[fill]*0.5 else None
    if 'fill' in o: fill=o['fill']
    if 'outline' in o: outline=o['outline']
    base=inpaint(sub,ink)
    ys,xs=np.nonzero(ink)
    iy0,iy1,ix0,ix1=ys.min(),ys.max()+1,xs.min(),xs.max()+1
    pad=1 if outline is not None else 0
    # vertical: keep the Japanese ink band; horizontal: whole rect minus 1px margin
    ty0,ty1=max(iy0+pad,0),min(iy1-pad,h)
    mw=w-2-2*pad-kx if not o.get('inkw') else (ix1-ix0)-2*pad
    fm_=(sub==fill)&ink; dens=fm_[iy0:iy1,ix0:ix1].mean() if fm_.any() else 0
    m=pick(text,mw,ty1-ty0,o.get('font','b' if ty1-ty0>=18 else 'r'),o.get('bold',True))
    mh,mw_=m.shape
    al=o.get('align') or ('l' if ix0<=3 and (w-ix1)>ix0+4 else 'c')
    if al=='l': ox=max(ix0,pad)
    elif al=='r': ox=ix1-mw_
    else: ox=(ix0+ix1)//2-mw_//2
    ox=int(min(max(ox,pad+kx),w-pad-mw_)); oy=int(ty0+(ty1-ty0-mh+1)//2)+o.get('dy',0)
    oy=min(max(oy,pad),h-pad-mh)
    M=np.zeros((h,w),bool); M[oy:oy+mh,ox:ox+mw_]=m
    out=base.copy()
    if outline is not None:
        D=nd.binary_dilation(M,structure=np.ones((3,3)) if o.get('o8',False) else None)&~M
        ext=~M; lab,_=nd.label(ext); edge=set(np.unique(np.concatenate([lab[0],lab[-1],lab[:,0],lab[:,-1]])))-{0}
        outer=np.isin(lab,list(edge))
        out[D&outer]=outline
    out[M]=fill
    T.idx[y0:y1,x0:x1]=out
