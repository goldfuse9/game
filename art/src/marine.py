from pix import *
VAR = {
 'recruit': dict(ar=['k','l','m','n'], hi='o', vis=['p','t','u'], kind=''),
 'heavy':   dict(ar=['p','q','r','s'], hi='s', vis=['a','d','f'], kind='heavy'),
 'medic':   dict(ar=['4','6','7','j'], hi='j', vis=['p','t','u'], kind='medic'),
 'elite':   dict(ar=['y','y','z','Z'], hi='Z', vis=['v','w','x'], kind='elite'),
 'runner':  dict(ar=['A','B','C','D'], hi='D', vis=['a','d','f'], kind='bomb'),
}
STEEL=['p','q','r']
def marine(var='recruit', view='front', lift=(0,0), bob=0, flash=False):
    V=VAR[var]; A=V['ar']; c=Canvas(32,35); y=bob+3; kind=V['kind']
    big = 1 if kind=='heavy' else 0
    if view=='side':
        if kind=='elite': c.poly([(10,13+y),(14,13+y),(13,29+y),(7,28+y)],['a','b','c'])
        c.rect(10,14+y,5,10,LEATHER if kind!='medic' else ['5','7','j'])   # batoh
        c.rect(13+lift[0],23+y,4,7,A); c.rect(16+lift[1],23+y,4,7,A)
        c.rect(12+lift[0],29+y,6,2,['K','2']); c.rect(15+lift[1],29+y,6,2,['K','2'])
        c.ellipse(16,18+y,5,6,A)
        c.rect(12,23+y,9,2,LEATHER)
        c.ellipse(17,15+y,3.5+big,3,A)
        if kind=='bomb':
            c.rect(19,16+y,4,7,['a','c','d']); c.stamp(19,17+y,['f.f.','....','f.f.'])
        elif kind=='medic':
            c.rect(19,19+y,6,5,LEATHER); c.stamp(21,20+y,['.d.','ddd','.d.'])
        else:
            c.line([(12,21+y),(26,20+y)],2+big,STEEL); c.rect(18,22+y,2,4,['p','q']); c.put(27,20+y,'K')
            c.put(26,19+y,'h')
            if flash: c.ellipse(29,20.5+y,2.5,2.5,FIRE,inner=False)
        c.ellipse(18,17.5+y,2,3,A)
        c.ellipse(17,9+y,5,5,A)
        c.rect(20,8+y,3,2,V['vis']); c.put(22,8+y,V['vis'][2])
        c.rect(18,12+y,4,2,['C','D'])
    else:
        back=view=='back'
        if back and kind=='elite': c.poly([(10,13+y),(22,13+y),(24,30+y),(8,30+y)],['a','b','c'])
        c.rect(12,23+y-lift[0],4,7,A); c.rect(17,23+y-lift[1],4,7,A)
        c.rect(12,25+y-lift[0],4,2,[A[2],V['hi']]); c.rect(17,25+y-lift[1],4,2,[A[2],V['hi']])
        c.rect(11,29+y-lift[0],6,2,['K','2']); c.rect(16,29+y-lift[1],6,2,['K','2'])
        c.ellipse(16,18+y,6.5,6,A)
        c.rect(10,23+y,13,2,LEATHER)
        if not back:
            c.rect(12,15+y,4,4,[A[1],A[3]]); c.rect(17,15+y,4,4,[A[1],A[3]])
        for sx in (8.5-big,23.5+big):
            c.ellipse(sx,14+y,3.2+big,2.6+big*.5,A)
            c.ellipse(sx,19+y,1.8,3,A)
        if back:
            c.rect(11,14+y,10,9,LEATHER if kind!='medic' else ['5','7','j'])
            c.rect(11,17+y,10,1,['A']); 
            if kind=='medic': c.stamp(14,15+y,['.dd.','dddd','dddd','.dd.'])
            if kind=='heavy': c.line([(19,13+y),(20,4+y)],1,['K','5']); c.put(20,3+y,'d')
        else:
            if kind=='bomb':
                c.rect(11,15+y,10,7,['a','c','d']); c.stamp(12,16+y,['f.f.f.f.','........','f.f.f.f.']); c.put(16,14+y,'h' if flash else 'd')
            elif kind=='medic':
                c.rect(12,15+y,8,6,['6','j']); c.stamp(14,15+y,['.dd.','dddd','dddd','.dd.'])
            else:
                for k in range(5): c.put(12+k*2,15+y+k,'z')
                c.line([(9,21+y),(23,20+y)],2+big,STEEL)
                c.rect(21,19+y,4,3+big,STEEL); c.put(25,20+y,'K'); c.put(24,19+y,'h')
                c.rect(14,22+y,2,4,['p','q'])
                if flash: c.ellipse(27,20.5+y,3,3,FIRE,inner=False)
        c.ellipse(16,9+y,5.5,5.5,A)
        if back: c.rect(11,12+y,10,2,[A[0],A[1]])
        else:
            c.rect(11,8+y,10,3,V['vis']); c.stamp(12,8+y,[V['vis'][2]*2])
            c.rect(13,12+y,6,2,['C','D']); c.stamp(14,13+y,['BBBB'])
    c.outline('K'); c.clean_orphans()
    return c

def marine_frames(var):
    o={}
    for v in ('front','back','side'):
        L=((2,0),(0,0),(0,2),(0,0)) if v!='side' else ((-2,2),(0,0),(2,-2),(0,0))
        o[f'{v}_walk']=[marine(var,v,lift=l,bob=b) for l,b in zip(L,(0,1,0,1))]
    o['front_shoot']=[marine(var,'front',flash=True)]
    return o

if __name__=='__main__':
    rows=[]
    for var in VAR:
        fr=marine_frames(var); rows.append(sheet([f.image() for k in fr for f in fr[k][:2 if k!='front_shoot' else 1]]))
    W=max(r.width for r in rows);H=sum(r.height for r in rows)
    im=Image.new('RGBA',(W,H),(40,30,40,255));y=0
    for r in rows: im.paste(r,(0,y),r);y+=r.height
    im.resize((W*5,H*5),Image.NEAREST).save('/tmp/mar_preview.png')
