from pix import *
import random
ORANGE=['b','c','d','e','f']
def hero(fr=0, rev=0):
    c=Canvas(48,52);y=4
    A=['c','d','e','f']
    l=(2,0) if fr==0 else (0,2)
    c.rect(15,34+y-l[0],7,11,['a','b','c']);c.rect(26,34+y-l[1],7,11,['a','b','c'])
    c.rect(15,37+y-l[0],7,3,A);c.rect(26,37+y-l[1],7,3,A)
    c.rect(13,44+y-l[0],10,4,['K','2']);c.rect(25,44+y-l[1],10,4,['K','2'])
    c.ellipse(24,27+y,10,9,A)
    c.rect(13,33+y,22,3,LEATHER);c.rect(22,33+y,4,3,['y','z'])
    c.rect(17,21+y,6,7,['c','e']);c.rect(25,21+y,6,7,['c','e'])
    for sx in (11,37): c.ellipse(sx,20+y,5.5,4.5,A)
    c.ellipse(10,28+y,3,5,['C','D']);c.ellipse(38,28+y,3,5,['C','D'])
    # motorová pila
    c.rect(33,27+y,8,7,['y','z','Z'])
    c.rect(39,22+y,5,16,['q','r','s'])
    for k in range(9):
        c.put(38 if (k+rev)%2 else 44, 22+y+k*2, 'j')
    c.put(41,21+y,'s')
    c.ellipse(24,12+y,8,8,['y','z','Z'])
    c.rect(17,11+y,14,4,['K','1']);c.stamp(19,12+y,['dd....dd']);c.stamp(19,13+y,['dd....dd'])
    c.rect(20,17+y,8,3,['y','z']);c.stamp(21,18+y,['K.K.K.K'])
    c.outline('K');c.clean_orphans();return c

def floor_tile(seed, blood=False, crack=False, rune=None):
    r=random.Random(seed);c=Canvas(32,32)
    c.rect(0,0,32,32,['K'],inner=False,flat=True)
    # 4 kamenné desky s nepravidelnými spárami
    xs=[0,15+r.randint(-2,2),32];ys=[0,15+r.randint(-2,2),32]
    for i in range(2):
        for j in range(2):
            x0,x1=xs[i]+1,xs[i+1]-1;y0,y1=ys[j]+1,ys[j+1]-1
            tone=r.choice([STONE[1:4],STONE[1:4],STONE[0:3]])
            c.rect(x0,y0,x1-x0,y1-y0,tone,inner=False,flat=True)
            c.rect(x0,y0,x1-x0,1,[tone[2]],inner=False,flat=True); c.rect(x0,y0,1,y1-y0,[tone[2]],inner=False,flat=True)
            c.rect(x0,y1-1,x1-x0,1,[tone[0]],inner=False,flat=True); c.rect(x1-1,y0,1,y1-y0,[tone[0]],inner=False,flat=True)
            for k in range(6):
                px,py=r.randint(x0+2,x1-3),r.randint(y0+2,y1-3);c.stamp(px,py,[tone[0]*2] if r.random()<.5 else [tone[2]+tone[2]])
    if crack:
        x,yy=r.randint(6,24),2
        for k in range(14):
            c.put(x,yy,'K');x+=r.choice((-1,0,1));yy+=1
            if yy>29:break
    if blood:
        cx,cy=r.randint(10,22),r.randint(10,22)
        c.ellipse(cx,cy,5,3,['a','b','c'],inner=False,flat=False)
        c.stamp(cx+4,cy+2,['b.','.a'])
    if rune:
        c.stamp(8,10,[rune*6,'.'+rune+'..'+rune+'.','..'+rune*2+'..'])
    return c
def wall_front():
    r=random.Random(7);c=Canvas(32,24)
    c.rect(0,0,32,24,['K'],inner=False,flat=True)
    for row in range(3):
        off=(row%2)*8
        for bx in range(-8,32,16):
            x0=bx+off+1;y0=row*8+1
            t=r.choice([['b','c','d'],['a','b','c'],['b','c','d']])
            c.rect(x0,y0,14,7,[t[1]],inner=False,flat=True)
            c.rect(x0,y0,14,1,[t[2]],inner=False,flat=True);c.rect(x0,y0+6,14,1,[t[0]],inner=False,flat=True)
            c.put(x0+r.randint(3,10),y0+r.randint(2,4),t[0]);c.put(x0+r.randint(3,10)+1,y0+r.randint(2,4),t[0])
    c.rect(0,21,32,3,['1'],inner=False,flat=True)
    for k in range(3):
        x=r.randint(2,29);l=r.randint(3,9);c.rect(x,2,1,l,['a'],inner=False,flat=True);c.put(x,2+l,'b')
    return c
def wall_top():
    r=random.Random(3);c=Canvas(32,32);c.rect(0,0,32,32,['2'],inner=False,flat=True)
    for k in range(40):c.put(r.randint(0,31),r.randint(0,31),r.choice('13'))
    c.rect(0,29,32,3,['4'],inner=False,flat=True);c.rect(0,31,32,1,['5'],inner=False,flat=True)
    c.rect(0,0,32,1,['1'],inner=False,flat=True);return c
def lava_top(ph=0):
    r=random.Random(5);c=Canvas(32,32);c.rect(0,0,32,32,['1','2'],inner=False,flat=True)
    for k in range(6):
        x,y=r.randint(0,31),r.randint(0,31)
        for s in range(10):
            col=FIRE[min(4,1+((s+ph)%4))];c.put(x,y,col);c.put(x+1,y,FIRE[1]);x+=r.choice((1,1,0));y+=r.choice((-1,0,1))
    c.rect(0,29,32,3,['a'],inner=False,flat=True);return c
def lava_front():
    r=random.Random(8);c=Canvas(32,24);c.rect(0,0,32,24,['1','2','3'],inner=False)
    for k in range(4):
        x=r.randint(3,28);y=0
        for s in range(14):
            c.put(x,y,FIRE[2+(s%3)]);y+=1;x+=r.choice((-1,0,1))
            if y>21:break
    c.rect(0,21,32,3,['K'],inner=False,flat=True);return c
def door_front():
    c=Canvas(32,24);c.rect(0,0,32,24,['c'],inner=False,flat=True);c.rect(0,6,32,10,['e'],inner=False,flat=True);c.rect(0,9,32,4,['f'],inner=False,flat=True)
    for x in range(2,32,6):c.rect(x,0,3,24,['p','q','r'],inner=False);c.rect(x,0,1,24,['r'],inner=False,flat=True)
    c.rect(0,2,32,3,['p','q'],inner=False);c.rect(0,18,32,3,['p','q'],inner=False)
    for x in range(3,32,6):c.put(x,3,'s');c.put(x,19,'s')
    return c
def crate():
    c=Canvas(32,40);c.rect(1,12,30,27,['k','l'],inner=False);c.rect(1,1,30,13,['l','m','n'],inner=False)
    for yy in (4,8):c.rect(2,yy,28,1,['k'],inner=False,flat=True)
    for yy in (19,26,33):c.rect(2,yy,28,1,['k'],inner=False,flat=True)
    c.rect(4,14,2,24,['k'],inner=False,flat=True);c.rect(26,14,2,24,['k'],inner=False,flat=True)
    c.stamp(11,21,['.ii...ii.','i..i.i..i','iiii.iiii'])
    c.rect(1,1,30,1,['o'],inner=False,flat=True)
    c.outline('K');return c
def barrel():
    c=Canvas(32,40);c.rect(4,7,24,31,['A','B','C'],inner=False)
    c.ellipse(16,7,12,5,['B','C','D'],inner=False);c.ellipse(16,7,8,3,['A','K'],inner=False)
    for yy in (14,28):c.rect(4,yy,24,2,['1','3'],inner=False)
    c.rect(8,12,2,20,['D'],inner=False,flat=True);c.stamp(18,18,['b.','bb','.b'])
    c.outline('K');return c
def candle():
    c=Canvas(16,20);c.rect(3,10,3,8,['7','i','j'],inner=False);c.rect(8,7,3,11,['7','i','j'],inner=False);c.rect(12,12,2,6,['7','i'],inner=False)
    c.stamp(4,7,['g','f']);c.stamp(9,3,['h','g','f']);c.stamp(12,10,['g'])
    c.rect(2,17,13,2,['a','b'],inner=False);c.outline('K');return c
def skulls():
    c=Canvas(20,14)
    for (x,y) in ((4,6),(12,7),(8,2)):
        c.ellipse(x+3,y+3,3.5,3,BONE);c.stamp(x+1,y+3,['K.K']);c.stamp(x+2,y+5,['K'])
    c.line([(0,12),(19,10)],1,['i','j'],inner=False);c.outline('K');return c

if __name__=='__main__':
    tiles=[floor_tile(1),floor_tile(2,crack=True),floor_tile(3,blood=True),floor_tile(4,rune='e'),wall_top(),lava_top()]
    row1=sheet([t.image() for t in tiles],pad=2)
    row2=sheet([wall_front().image(),door_front().image()],pad=2)
    row3=sheet([crate().image(),barrel().image(),candle().image(),skulls().image()],pad=2)
    row4=sheet([hero(0).image(),hero(1,1).image()],pad=2)
    rows=[row1,row2,row3,row4];W=max(r.width for r in rows);H=sum(r.height for r in rows)
    im=Image.new('RGBA',(W,H),(60,50,60,255));y=0
    for r in rows:im.paste(r,(0,y),r);y+=r.height
    im.resize((W*4,H*4),Image.NEAREST).save('/tmp/env_preview.png')
