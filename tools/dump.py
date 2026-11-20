import jtable,strfile
S=strfile.parse(open('../work/ext/PSP_GAME/USRDIR/STRING/string.ofs','rb').read())
with open('../work/ja_dump.txt','w',encoding='utf8') as f:
  for i,sec in enumerate(S):
    for k,e in enumerate(sec): f.write('%d.%d\t%s\n'%(i,k,jtable.dec(e).replace('\n','⏎')))
