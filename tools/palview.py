import sys,cont,numpy as np
from imgtool import Tex
from PIL import Image
c,g,pi,box,sc,out=sys.argv[1],sys.argv[2],int(sys.argv[3]),[int(v) for v in sys.argv[4].split(',')],int(sys.argv[5]),sys.argv[6]
iso=len(sys.argv)>7
if iso:
    import pycdlib,io
    I=pycdlib.PyCdlib(); I.open('../Daisenryaku Portable 2 (Korean).iso'); f=io.BytesIO(); I.get_file_from_iso_fp(f,iso_path='/PSP_GAME/USRDIR/'+c); d=f.getvalue()
else: d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read()
it={n:(o,s) for n,o,s in cont.parse(d)}; o,s=it[g];T=Tex(d[o:o+s])
p=([T.pal]+T.pals)[pi]
im=Image.fromarray(p[T.idx][:T.h].astype(np.uint8),'RGBA').crop(box)
b=Image.new('RGBA',im.size,(60,60,90,255));b.alpha_composite(im)
b.resize((im.width*sc,im.height*sc),Image.NEAREST).save(out)
