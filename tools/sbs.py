import sys,cont,numpy as np
from PIL import Image
from imgtool import Tex,expand_jobs,fit_jobs
import imgspec2
c,g=sys.argv[1],sys.argv[2]; box=[int(v) for v in sys.argv[3].split(',')]; sc=int(sys.argv[4])
d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}
o,s=it[g]; A=Tex(d[o:o+s]); B=Tex(d[o:o+s]); fit_jobs(B,expand_jobs(B,imgspec2.SPEC[(c,g)]))
ims=[Image.fromarray(T.rgba().astype(np.uint8)[:T.h],'RGBA').crop(box) for T in (A,B)]
w,h=ims[0].size; out=Image.new('RGBA',(w*2+4,h),(255,0,0,255))
bg=Image.new('RGBA',(w,h),(60,60,80,255))
for i,im in enumerate(ims):
    t=bg.copy(); t.alpha_composite(im); out.paste(t,(i*(w+4),0))
out.resize(((w*2+4)*sc,h*sc),Image.NEAREST).save(sys.argv[5])
