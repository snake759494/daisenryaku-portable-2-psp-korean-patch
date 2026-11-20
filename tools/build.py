"""대전략 포터블2 한글 패치 빌드: python tools/build.py [--noiso]"""
import os,sys,json,glob,re
sys.path.insert(0,os.path.dirname(os.path.abspath(__file__)))
import lzss,strfile,jtable,kfont,isobuild
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
W=lambda *p:os.path.join(ROOT,*p)
ORIG=W('Daisenryaku Portable 2 (Japan).iso')
OUT=W('Daisenryaku Portable 2 (Korean).iso')
USR=W('work','ext','PSP_GAME','USRDIR')
def load_trans():
    ids={}
    for l in open(W('work','ja_dump.txt'),encoding='utf8'):
        k,t=l.rstrip('\n').split('\t',1); ids[k]=t.replace('⏎','\n')
    T={}
    for f in sorted(glob.glob(W('work','trans','ko_*.tsv'))):
        for l in open(f,encoding='utf8'):
            l=l.rstrip('\n')
            if not l or l.startswith('//'): continue
            k,v=l.split('\t',1); T[ids[k]]=v.replace('⏎','\n')
    return T
def w(s):  # display width in half units
    return sum(1 if (ch in kfont.HALF) else 2 for ch in s)
def wrap_words(text,width):
    out=[];cur=''
    for word in text.split(' '):
        cand=(cur+' '+word) if cur else word
        if w(cand)<=width: cur=cand
        else:
            if cur: out.append(cur)
            while w(word)>width:
                n=0
                while w(word[:n+1])<=width: n+=1
                out.append(word[:n]); word=word[n:]
            cur=word
    out.append(cur); return out
def conv(ja,ko,warn,key):
    if ko.startswith('#'):   # help box: wrap to original width
        lines=ja.split('\n'); width=max(24,max(w(l) for l in lines))
        out=wrap_words(ko[1:],width)
        if len(out)>max(len(lines),4):
            warn.append('%s LINES %d>%d %s'%(key,len(out),len(lines),out))
        elif len(out)>len(lines): warn.append('%s LINES+ %d>%d'%(key,len(out),len(lines)))
        return '\n'.join(out)
    if ko.startswith('@'):   # story: "　line\n\n" * N
        n=ja.count('\n\n'); lines=ja.split('\n\n')[:n]
        width=max(w(l) for l in lines)-2
        out=[]
        for para in ko[1:].split('|'):
            out+= [''] if para=='' else wrap_words(para,width)
        if len(out)>n: warn.append('%s STORY %d>%d'%(key,len(out),n))
        out+=['']*(n-len(out))
        return ''.join('　'+l+'\n\n' for l in out)
    if '\n\n' in ja and '\n\n' not in ko: ko=ko.replace('\n','\n\n')+('\n\n' if ja.endswith('\n\n') else '')
    ol=max(w(l) for l in ja.split('\n')); nl=max(w(l) for l in ko.split('\n'))
    if nl>ol and '\n' in ja: warn.append('%s WIDTH %d>%d %r'%(key,nl,ol,ko))
    return ko
def main():
    T=load_trans()
    S=strfile.parse(open(os.path.join(USR,'STRING','string.ofs'),'rb').read())
    base=kfont.base_map(); warn=[]; final={}
    for si,ents in enumerate(S):
        for ei,e in enumerate(ents):
            ja=jtable.dec(e)
            if ja in T: final[(si,ei)]=conv(ja,T[ja],warn,'%d.%d'%(si,ei))
    jp=re.compile('[぀-ヿ一-鿿]')
    untrans=set(jtable.dec(e) for ents in S for e in ents if jp.search(jtable.dec(e)) and jtable.dec(e) not in T)
    used=set()
    for si,ents in enumerate(S):
        for ei,e in enumerate(ents):
            if (si,ei) not in final: used.update(e)
    chars=sorted(set(ch for v in final.values() for ch in v if ch!='\n' and ch not in base))
    slots=kfont.free_slots(used)
    assert len(chars)<=len(slots),(len(chars),len(slots))
    cmap=dict(zip(chars,slots)); enc=dict(base); enc.update(cmap)
    for (si,ei),v in final.items():
        codes=[0x1ff if ch=='\n' else enc[ch] for ch in v]
        S[si][ei]=strfile.pad(codes)
    print('translated',len(final),'untranslated jp',len(untrans),'glyphs',len(cmap),'/',len(slots))
    for u in sorted(untrans)[:20]: print('UNTRANS',repr(u))
    for x in warn: print('WARN',x)
    sb=strfile.build(S)
    fb=kfont.build(open(os.path.join(USR,'STRING','font.gim'),'rb').read(),cmap)
    os.makedirs(W('work','out'),exist_ok=True)
    open(W('work','out','string.ofs'),'wb').write(sb); open(W('work','out','font.gim'),'wb').write(fb)
    files={'PSP_GAME/USRDIR/STRING/string.ofs':sb,'PSP_GAME/USRDIR/STRING/font.gim':fb,'PSP_GAME/USRDIR/STRING/string_ash.dat':lzss.compress(sb),'PSP_GAME/USRDIR/STRING/font_ash.dat':lzss.compress(fb)}
    try:
        import extras; files.update(extras.build(W))
    except ImportError: pass
    if '--noiso' in sys.argv: return
    tmp=OUT+'.tmp'; iso=isobuild.Iso(ORIG,tmp)
    for p,b in files.items(): print(p,len(b),iso.replace(p,b))
    iso.close(); os.replace(tmp,OUT); print('->',OUT)
if __name__=='__main__': main()
