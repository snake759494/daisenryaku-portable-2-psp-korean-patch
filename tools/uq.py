import re,sys
jp=re.compile('[぀-ヿ一-鿿]')
secs=set(sys.argv[1].split(',')); seen=set()
for l in open('../work/ja_dump.txt',encoding='utf8'):
    k,t=l.rstrip('\n').split('\t',1)
    if k.split('.')[0] in secs and jp.search(t) and t not in seen: seen.add(t); print(k+'\t'+t)
