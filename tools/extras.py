import os,sys,hashlib
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import cont,lzss
from imgtool import Tex,expand_jobs,fit_jobs
import imgspec2
ASH={'UI/tex_op.ofs':'UI/tex_op_ash.dat','UI/tex_ui.ofs':'UI/tex_ui_ash.dat','UI/tex_sh.ofs':'UI/tex_sh_ash.dat'}
def apply(W,c,lst):
    d=bytearray(open(W('work','ext','PSP_GAME','USRDIR',*c.split('/')),'rb').read())
    it={n:(o,s) for n,o,s in cont.parse(bytes(d))}
    for g,jobs in lst:
        o,s=it[g]; T=Tex(bytes(d[o:o+s]))
        fit_jobs(T,expand_jobs(T,jobs))
        nb=T.save_back(); assert len(nb)==s; d[o:o+s]=nb
    return bytes(d)
def build(W):
    out={}; groups={}
    for (c,g),jobs in imgspec2.SPEC.items(): groups.setdefault(c,[]).append((g,jobs))
    for c,lst in groups.items():
        d=apply(W,c,lst); out['PSP_GAME/USRDIR/'+c]=d
        if c in ASH:
            h=hashlib.md5(d).hexdigest(); cp=W('work','out','cache_'+c.replace('/','_')+'_'+h)
            if os.path.exists(cp): z=open(cp,'rb').read()
            else:
                for f in os.listdir(W('work','out')):
                    if f.startswith('cache_'+c.replace('/','_')): os.remove(W('work','out',f))
                z=lzss.compress(d); open(cp,'wb').write(z)
            out['PSP_GAME/USRDIR/'+ASH[c]]=z
        print('img',c)
    try:
        import bootpatch; out.update(bootpatch.build(W))
    except ImportError: pass
    return out
