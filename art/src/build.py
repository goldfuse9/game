import json, random
from pix import *
from imp import imp_frames
from marine import marine_frames, VAR
from env import *
out='out/'
meta={}
# --- sprite sheets ---
def save_sheet(name, frames_dict):
    rows=[];info={}
    for i,(k,fr) in enumerate(frames_dict.items()):
        info[k]={'row':i,'frames':len(fr)}
        rows.append(sheet([f.image() for f in fr]))
    W=max(r.width for r in rows);fw,fh=frames_dict[next(iter(frames_dict))][0].w,frames_dict[next(iter(frames_dict))][0].h
    im=Image.new('RGBA',(W,fh*len(rows)),(0,0,0,0))
    for i,r in enumerate(rows):im.paste(r,(0,i*fh))
    im.save(out+name+'.png');meta[name]={'fw':fw,'fh':fh,'anims':info}
    return im
IMPF=imp_frames();save_sheet('imp',IMPF)
MF={v:marine_frames(v) for v in VAR}
for v in VAR:save_sheet('marine_'+v,MF[v])
HF={'front_walk':[hero(0),hero(1,1)]};save_sheet('hero',HF)
TILES={'floor':[floor_tile(1),floor_tile(2,crack=True),floor_tile(3,blood=True),floor_tile(4,rune='e')],'wall_top':[wall_top()],'lava':[lava_top(0),lava_top(1),lava_top(2),lava_top(3)]}
for k,v in TILES.items():sheet([t.image() for t in v]).save(out+f'tile_{k}.png')
for name,c in {'wall_front':wall_front(),'lava_front':lava_front(),'door_front':door_front(),'crate':crate(),'barrel':barrel(),'candle':candle(),'skulls':skulls()}.items():c.image().save(out+name+'.png')
json.dump(meta,open(out+'sprites.json','w'),indent=1)

# --- ukázková scéna 480x270 se světlem ---
T=32
M=["###############",
   "#.....C...B...#",
   "#..L.....s....#",
   "#.............#",
   "D.....p.......D",
   "#..C......L...#",
   "#.......B.....#",
   "###############"]
W,H=480,270
scene=Image.new('RGBA',(W,H),(0,0,0,255))
ox,oy=0,22
fl=[floor_tile(i,blood=i%5==0,crack=i%7==3,rune='e' if i%11==4 else None).image() for i in range(12)]
for y,row in enumerate(M):
    for x,ch in enumerate(row):
        if ch!='#':scene.alpha_composite(fl[(x*7+y*3)%12],(ox+x*T,oy+y*T))
# krev a pentagram jako dekály
dec=Canvas(W,H)
r=random.Random(9)
for k in range(30):
    x,y=r.randint(60,420),r.randint(60,230);dec.put(x,y,r.choice('abc'));dec.put(x+1,y,'b')
scene.alpha_composite(dec.image())
WT,WF,DF,LT=wall_top().image(),wall_front().image(),door_front().image(),lava_top(1).image()
CR,BA,CA,SK=crate().image(),barrel().image(),candle().image(),skulls().image()
ents=[]  # (y, image, x)
imgs={'imp':IMPF['side_walk'][1].image(),'m1':MF['recruit']['side_walk'][0].mirrored().image() if False else None}
m_front=MF['recruit']['front_walk'][0].image();m_back=MF['heavy']['back_walk'][1].image();m_side=MF['medic']['side_walk'][1].mirrored().image()
elite=MF['elite']['front_walk'][0].image()
ents+= [(3.9,IMPF['front_cast'][2].image(),6.5),(1.9,m_front,9.5),(5.9,m_back,4.5),(4.4,m_side,11.5),(6.6,elite,12.6)]
ents+= [(1.55,CA,2.2),(6.6,CA,1.6),(3.2,SK,12.3),(6.3,SK,6.8)]
souls=[(8.2,4.5),(8.6,4.2),(3.3,5.7)]
for y in range(len(M)):
    for x,ch in enumerate(M[y]):
        sx,sy=ox+x*T,oy+y*T
        if ch=='#':
            near=any(0<=y+j<len(M) and 0<=x+i<len(M[0]) and M[y+j][x+i]!='#' for j in (-1,0,1) for i in (-1,0,1))
            if not near:continue
            scene.alpha_composite(WT,(sx,sy-24))
            if y+1<len(M) and M[y+1][x]!='#':scene.alpha_composite(WF,(sx,sy+8))
        elif ch=='D':scene.alpha_composite(WT,(sx,sy-24));scene.alpha_composite(DF,(sx,sy+8))
        elif ch=='L':scene.alpha_composite(LT,(sx,sy-24));scene.alpha_composite(lava_front().image(),(sx,sy+8))
        elif ch=='C':scene.alpha_composite(CR,(sx,sy-8))
        elif ch=='B':scene.alpha_composite(BA,(sx,sy-8))
    for ey,im,ex in sorted([e for e in ents if int(e[0])==y],key=lambda e:e[0]):
        px,py=int(ox+ex*T-im.width/2),int(oy+ey*T-im.height+2)
        sh=Image.new('RGBA',(im.width,6),(0,0,0,0));ImageDraw.Draw(sh).ellipse((im.width*.25,0,im.width*.75,5),fill=(0,0,0,120))
        scene.alpha_composite(sh,(px,py+im.height-5));scene.alpha_composite(im,(px,py))
# --- světlo ---
import numpy as np
A=np.array(scene).astype(float)/255
lum=np.full((H,W),.05)
Y,X=np.mgrid[0:H,0:W]
def light(x,y,r,s,col=(1,1,1)):
    d=np.sqrt((X-x)**2+(Y-y)**2);v=np.clip(1-d/r,0,1)**1.6*s
    for i in range(3):tint[...,i]+=v*col[i]
    return v
tint=np.zeros((H,W,3))
def add(v):
    global lum;lum=lum+v
add(light(ox+6.5*T,oy+3.6*T,95,1.0,(.9,.5,1.2)))
for (cx,cy) in ((2.2,1.4),(1.6,6.4)):add(light(ox+cx*T,oy+cy*T,70,.8,(1.2,.7,.3)))
for y,row in enumerate(M):
    for x,ch in enumerate(row):
        if ch=='L':add(light(ox+x*T+16,oy+y*T-6,80,.9,(1.4,.6,.2)))
        if ch=='D':add(light(ox+x*T+16,oy+y*T+14,60,.6,(1.3,.4,.2)))
def cone(x,y,ang,rng,s=.9):
    d=np.sqrt((X-x)**2+(Y-y)**2);a=np.arctan2(Y-y,X-x)-ang;a=np.arctan2(np.sin(a),np.cos(a))
    v=np.where(np.abs(a)<.55,np.clip(1-d/rng,0,1)**1.2*s*np.clip((.55-np.abs(a))/.15,0,1),0)
    tint[...,0]+=v*1.0;tint[...,1]+=v*.95;tint[...,2]+=v*.7;return v
add(cone(ox+9.9*T,oy+1.6*T,1.7,170));add(cone(ox+4.6*T,oy+5.6*T,-1.2,150));add(cone(ox+11.1*T,oy+4.1*T,3.0,160));add(cone(ox+12.9*T,oy+6.3*T,3.6,140))
for sx,sy in souls:add(light(ox+sx*T,oy+sy*T,22,.6,(.4,1,1.3)))
for ey,im,ex in ents[1:5]:add(light(ox+ex*T,oy+ey*T-14,30,.45,(1,.95,.8)))
lum=np.clip(lum,0,1.15)
col=np.clip((tint/np.maximum(lum,1e-3)[...,None]),0,1.6)
col=np.where(lum[...,None]>0.08,col,np.array([.5,.4,.7]))
L3=lum[...,None]*(0.55+0.45*col)
out_img=A[...,:3]*L3
# glow aditivně
glow=np.zeros((H,W,3))
def g(x,y,r,c,s):
    d=np.sqrt((X-x)**2+(Y-y)**2);v=np.clip(1-d/r,0,1)**2*s
    for i in range(3):glow[...,i]+=v*c[i]
g(ox+6.5*T,oy+3.0*T,40,(.55,.2,.9),.6)
for (cx,cy) in ((2.2,1.25),(1.6,6.25)):g(ox+cx*T,oy+cy*T,20,(1,.6,.2),.35)
for sx,sy in souls:g(ox+sx*T,oy+sy*T,10,(.3,.9,1),.8)
out_img=np.clip(out_img+glow,0,1)
fin=Image.fromarray((out_img*255).astype('uint8'))
# duše
d2=ImageDraw.Draw(fin)
for sx,sy in souls:
    x,y=ox+sx*T,oy+sy*T-8;d2.polygon([(x,y-5),(x+3,y),(x,y+5),(x-3,y)],fill=(95,240,255));d2.line([(x,y-2),(x,y+2)],fill=(230,255,255))
fin.save(out+'scene.png');fin.resize((W*3,H*3),Image.NEAREST).save(out+'scene_x3.png')
print('done')
