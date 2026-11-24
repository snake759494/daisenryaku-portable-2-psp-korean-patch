"""PPSSPP GE frame dump (gpu.record.dump) parser -> textured sprite UV rects"""
import struct,zstandard,json,base64,sys
def load(b):
    assert b[:8]==b'PPSSPPGE'
    ncmd,psize=struct.unpack_from('<II',b,24); off=32
    dz=zstandard.ZstdDecompressor()
    cs=struct.unpack_from('<I',b,off)[0]; off+=4
    cmds=dz.decompress(b[off:off+cs],max_output_size=ncmd*9); off+=cs
    ps=struct.unpack_from('<I',b,off)[0]; off+=4
    push=dz.decompress(b[off:off+ps],max_output_size=psize)
    C=[struct.unpack_from('<BII',cmds,i*9) for i in range(ncmd)]
    return C,push
def sprites(b):
    C,push=load(b); clut=b''; out=[]; vbuf=b''; texdata={}; reg={}
    for t,sz,ptr in C:
        d=push[ptr:ptr+sz]
        if t==2: vbuf=d
        elif t==4: clut=d
        elif 0x10<=t<0x18: texdata[t-0x10]=d[:4096]
        elif t==1:
            for i in range(0,len(d),4):
                w=struct.unpack_from('<I',d,i)[0]; op=w>>24; reg[op]=w&0xffffff
                if op==0x04:  # PRIM
                    prim=(w>>16)&7; n=w&0xffff; vt=reg.get(0x12,0)
                    tc=vt&3; col=(vt>>2)&7; nrm=(vt>>5)&3; pos=(vt>>7)&3; wt=(vt>>9)&3; idx=(vt>>11)&3; through=(vt>>23)&1
                    if not tc or idx: continue
                    sz_={1:1,2:2,3:4}; csz={0:0,4:2,5:2,6:2,7:4}[col]
                    # layout: (weights) tc pos-ish; assume no weights/normals
                    tcs=sz_[tc]; ps_=sz_[pos]
                    al=max(tcs,ps_,csz if csz else 1)
                    o=0; o_tc=0; o=2*tcs
                    if csz: o=(o+csz-1)//csz*csz; o+=csz
                    o=(o+ps_-1)//ps_*ps_; o_pos=o; o+=3*ps_
                    stride=(o+al-1)//al*al
                    fmt={1:'B',2:'H',3:'f'}
                    tex=reg.get(0xA0,0)|((reg.get(0xA8,0)>>16)&0xff)<<24
                    ts=reg.get(0xB8,0); tw,th=1<<(ts&15),1<<((ts>>8)&15)
                    vs=[]
                    for k in range(n):
                        base=k*stride
                        if base+stride>len(vbuf): break
                        u,v=struct.unpack_from('<2'+fmt[tc],vbuf,base)
                        x,y,_=struct.unpack_from('<3'+('h' if pos==2 else fmt[pos]),vbuf,base+o_pos)
                        vs.append((u,v,x,y))
                    vbuf=vbuf[n*stride:]
                    out.append(dict(clut=clut,tkey=texdata.get(0,b''),prim=prim,tex=tex,tw=tw,th=th,through=through,v=vs))
    return out
if __name__=='__main__':
    r=json.load(open(sys.argv[1])); b=base64.b64decode(r['uri'].split(',',1)[1])
    for s in sprites(b):
        if s['prim']==6 and s['through']:
            v=s['v']
            for i in range(0,len(v)-1,2): print(hex(s['tex']),s['tw'],s['th'],v[i],v[i+1])

def texindex(iso):
    import pycdlib,io,cont,gimfile
    I=pycdlib.PyCdlib(); I.open(iso); idx={}
    for c in ('tex_op.ofs','tex_ui.ofs','tex_sh.ofs','tex_wib.ofs'):
        f=io.BytesIO(); I.get_file_from_iso_fp(f,iso_path='/PSP_GAME/USRDIR/UI/'+c); d=f.getvalue()
        for n,o,s in cont.parse(d):
            try: im=gimfile.info(bytearray(d[o:o+s]))['img']
            except Exception: continue
            idx[d[o+im['pix']:o+im['pix']+4096]]=('UI/'+c,n)
    I.close(); return idx
