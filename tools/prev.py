# 미리보기: python prev.py CONT GIM [scale]  -> work/prev.png (적용 결과, 빨간 상자=DROP, 녹색=SPEC)
import sys,os,cont,numpy as np
from PIL import Image,ImageDraw
from imgtool import Tex,expand_jobs,fit_jobs
import importlib,imgspec2
c,g=sys.argv[1],sys.argv[2]; sc=int(sys.argv[3]) if len(sys.argv)>3 else 2
d=open('../work/ext/PSP_GAME/USRDIR/'+c,'rb').read(); it={n:(o,s) for n,o,s in cont.parse(d)}
o,s=it[g]; T=Tex(d[o:o+s]); jobs=imgspec2.SPEC.get((c,g),[])
if jobs: fit_jobs(T,expand_jobs(T,jobs))
im=Image.fromarray(T.rgba().astype(np.uint8)[:T.h],'RGBA'); bg=Image.new('RGBA',im.size,(40,40,60,255)); bg.alpha_composite(im)
crop=[int(v) for v in sys.argv[4].split(',')] if len(sys.argv)>4 else [0,0,T.w,T.h]
bg=bg.crop(crop); big=bg.convert('RGB').resize((bg.width*sc,bg.height*sc),Image.NEAREST); dr=ImageDraw.Draw(big)
if '-b' in sys.argv:
  for j in imgspec2.DROP.get((c,g),[]): dr.rectangle([(j[0]-crop[0])*sc,(j[1]-crop[1])*sc,(j[0]-crop[0]+j[2])*sc,(j[1]-crop[1]+j[3])*sc],outline=(255,0,0))
  for j in jobs: dr.rectangle([(j[0]-crop[0])*sc,(j[1]-crop[1])*sc,(j[0]-crop[0]+j[2])*sc,(j[1]-crop[1]+j[3])*sc],outline=(0,255,0))
big.save('../work/prev.png')
