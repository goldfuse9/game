import base64, json
from pix import PAL
b=lambda p:'data:image/png;base64,'+base64.b64encode(open(p,'rb').read()).decode()
meta=json.load(open('out/sprites.json'))
sheets={k:b(f'out/{k}.png') for k in meta}
imgs={k:b(f'out/{k}.png') for k in ['scene','tile_floor','tile_wall_top','tile_lava','wall_front','lava_front','door_front','crate','barrel','candle','skulls']}
ROLES=[('Obrys a tma',['K','1','2']),('Kámen a stíny',['3','4','5','6','7']),('Kůže impa (posun do oranžova)',['a','b','c','d','e','f']),('Oheň',['g','h']),('Kost, drápy, rohy',['i','j']),
 ('Mariňák – olivová',['k','l','m','n','o']),('Ocel a těžkooděnec',['p','q','r','s']),('Hledí a duše',['t','u']),('Magie a pentagram',['v','w','x']),('Elita a Hrdina – zlato',['y','z','Z']),('Kůže a dřevo',['A','B','C','D'])]
pal_html=''.join(f'<div class="ramp"><div class="sw">'+''.join(f'<i style="background:{PAL[k]}" title="{PAL[k]}"></i>' for k in ks)+f'</div><span>{n}</span></div>' for n,ks in ROLES)
ANIMS=[('imp','front_idle','Imp · klid',6),('imp','front_walk','Imp · chůze',8),('imp','side_walk','Imp · chůze z boku',8),('imp','back_walk','Imp · zezadu',8),('imp','front_cast','Imp · kouzlí pentagram',8),('imp','side_slash','Imp · sek drápy',10),
 ('marine_recruit','front_walk','Rekrut',8),('marine_recruit','side_walk','Rekrut z boku',8),('marine_heavy','front_walk','Těžkooděnec',6),('marine_medic','back_walk','Medik zezadu',8),('marine_runner','front_walk','Sebevrah s bombou',10),('marine_elite','back_walk','Elita s pláštěm',8),('marine_recruit','front_shoot','Výstřel',1),('hero','front_walk','Hrdina (boss)',4)]
anim_html=''.join(f'<figure><canvas data-s="{s}" data-a="{a}" data-f="{f}"></canvas><figcaption>{t}<small>{meta[s]["anims"][a]["frames"]} sn. · {f} fps</small></figcaption></figure>' for s,a,t,f in ANIMS)
tiles=[('tile_floor','Podlaha · 4 varianty'),('tile_wall_top','Vrch zdi'),('wall_front','Čelo zdi'),('tile_lava','Láva · 4 snímky'),('lava_front','Čelo lávy'),('door_front','Mříže (zamčeno)'),('crate','Vojenská bedna'),('barrel','Sud'),('candle','Svíčky = světlo'),('skulls','Lebky')]
tile_html=''.join(f'<figure class="t"><img src="{imgs[k]}" alt=""><figcaption>{t}</figcaption></figure>' for k,t in tiles)
html=open('page_tpl.html').read().replace('%SCENE%',imgs['scene']).replace('%PAL%',pal_html).replace('%ANIMS%',anim_html).replace('%TILES%',tile_html).replace('%SHEETS%',json.dumps(sheets)).replace('%META%',json.dumps(meta))
open('out/index.html','w').write(html);print(len(html)//1024,'KB')
