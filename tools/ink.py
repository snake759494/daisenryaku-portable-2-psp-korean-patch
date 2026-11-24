import sys,cont,numpy as np
from imgtool import Tex
c,g,y0,y1=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}
o,s=it[g];T=Tex(d[o:o+s]);a=T.rgba()[:T.h]
m=(a[y0:y1,:,0]>150)&(a[y0:y1,:,1]>150)&(a[y0:y1,:,2]>150)
print('rows',[y0+i for i in np.where(m.any(1))[0]])
c=m.any(0);runs=[];x=0
while x<len(c):
  if c[x]:
    s_=x
    while x<len(c) and c[x]:x+=1
    runs.append((s_,x-1))
  x+=1
print(runs)
