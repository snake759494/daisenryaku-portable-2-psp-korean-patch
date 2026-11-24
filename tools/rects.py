"""dump json -> sprite rects on patched textures; also contact sheet: orig|patched crop per rect"""
import sys,json,base64,gedump,cont,numpy as np
from PIL import Image,ImageDraw
from imgtool import Tex
X=None
def tex(c,g,iso):
    import pycdlib,io
    if iso:
        I=pycdlib.PyCdlib(); I.open(iso); f=io.BytesIO(); I.get_file_from_iso_fp(f,iso_path='/PSP_GAME/USRDIR/'+c); d=f.getvalue(); I.close()
    else: d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read()
    it={n:(o,s) for n,o,s in cont.parse(d)}; o,s=it[g]; T=Tex(d[o:o+s]); return T.rgba()[:T.h].astype(np.uint8)
def rects(path,iso):
    global X
    if X is None: X=gedump.texindex(iso)
    r=json.load(open(path)); b=base64.b64decode(r['uri'].split(',',1)[1]); out=[]
    for s in gedump.sprites(b):
        k=X.get(s['tkey'])
        if not k or s['prim']!=6 or not s['through']: continue
        v=s['v']
        for i in range(0,len(v)-1,2):
            (u0,v0,x0,y0),(u1,v1,x1,y1)=v[i],v[i+1]
            out.append(dict(clut=s['clut'][:1024],c=k[0],g=k[1],r=[min(u0,u1),min(v0,v1),max(u0,u1),max(v0,v1)],dst=[x0,y0,x1,y1]))
    return out
if __name__=='__main__':
    iso='../Daisenryaku Portable 2 (Korean).iso'; import imgspec2
    R=rects(sys.argv[1],iso); want=set(imgspec2.SPEC)
    R=[q for q in R if (q['c'],q['g']) in want and (q['r'][2]-q['r'][0])*(q['r'][3]-q['r'][1])<20000]
    cache={}; tiles=[]
    for q in R:
        key=(q['c'],q['g'])
        if key not in cache: cache[key]=(tex(*key,None),tex(*key,iso))
        A,B=cache[key]; x0,y0,x1,y1=q['r']
        if x1-x0<2 or y1-y0<2: continue
        print(q['g'].split('/')[-1],q['r'],q['dst'])
        P=lambda M:np.pad(M,((2,2),(2,2),(0,0)))[y0:y1+4,x0:x1+4]
        if (x1-x0)>=200: continue
        if any(t[0]['g']==q['g'] and t[0]['r']==q['r'] for t in tiles): continue
        tiles.append((q,P(A),P(B)))
    sc=3; W=max(t[1].shape[1] for t in tiles)*sc*2+300; H=sum(t[1].shape[0]*sc+6 for t in tiles)
    im=Image.new('RGB',(W,H),(255,0,255)); dr=ImageDraw.Draw(im); y=0
    for q,a,b in tiles:
        h,w=a.shape[:2]
        for j,c in enumerate((a,b)):
            t=Image.new('RGBA',(w,h),(60,60,90,255)); t.alpha_composite(Image.fromarray(c,'RGBA'))
            t=t.resize((w*sc,h*sc),Image.NEAREST); im.paste(t.convert('RGB'),(j*(w*sc+4),y))
            dr.rectangle([j*(w*sc+4)+2*sc-1,y+2*sc-1,j*(w*sc+4)+(w-2)*sc,y+(h-2)*sc],outline=(255,0,0))
        dr.text((2*w*sc+12,y),'%s %s'%(q['g'].split('/')[-1][3:],q['r']),fill=(255,255,255)); y+=h*sc+6
    im.save(sys.argv[2])
