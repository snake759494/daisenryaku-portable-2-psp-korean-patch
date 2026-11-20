import json,os
_J=json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'jtable2.json'),encoding='utf8'))
J={int(k):v for k,v in _J.items()}
CTRL={0xff:'',0x1ff:'\n'}
def dec(codes):
    o=[]
    for c in codes:
        if c in J: o.append(J[c])
        elif c in CTRL: o.append(CTRL[c])
        else: o.append('{%X}'%c)
    return ''.join(o)
