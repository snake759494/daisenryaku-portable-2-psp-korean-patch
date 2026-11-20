# 단순 ISO9660 추출기 (파일명 바이트를 cp932로 해석)
import os,sys,struct
f=open(sys.argv[1],'rb');out=sys.argv[2]
def rd(lba,n):
    f.seek(lba*2048);return f.read(n)
pvd=rd(16,2048);root=pvd[156:156+34]
def walk(lba,size,path):
    data=rd(lba,size);i=0
    while i<len(data):
        l=data[i]
        if l==0: i=(i//2048+1)*2048;continue
        r=data[i:i+l];ext=struct.unpack_from('<I',r,2)[0];ln=struct.unpack_from('<I',r,10)[0];fl=r[25];nl=r[32];nm=r[33:33+nl]
        i+=l
        if nm in(b'\0',b'\1'):continue
        name=nm.split(b';')[0].decode('cp932','replace')
        p=path+'/'+name
        if fl&2: walk(ext,ln,p)
        else:
            lp=os.path.join(out,p.lstrip('/'));os.makedirs(os.path.dirname(lp),exist_ok=True)
            f.seek(ext*2048);open(lp,'wb').write(f.read(ln))
            print(ext,ln,p)
walk(struct.unpack_from('<I',root,2)[0],struct.unpack_from('<I',root,10)[0],'')
