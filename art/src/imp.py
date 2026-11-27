from pix import *

def imp(view='front', bob=0, lift=(0, 0), flap=0, tail=0, arms='down', mouth='grin', orb=0):
    """Imp čaroděj 32×32, nohy na řádku 30. view: front/back/side (doprava)."""
    c = Canvas(32, 35)
    y = bob + 3
    if view == 'side':
        # ocas za zády (vlevo), křídlo za tělem
        c.line([(11, 24 + y), (6, 22 + y), (4, 17 + y + tail), (5, 13 + y + tail)], 2, SKIN4, inner=False)
        c.poly([(3, 13 + y + tail), (8, 12 + y + tail), (5, 8 + y + tail)], SKIN4)
        c.poly([(14, 15 + y), (6, 8 + y - flap), (4, 13 + y - flap), (7, 14 + y), (6, 18 + y), (9, 17 + y), (10, 20 + y), (14, 19 + y)], MEMB)
        c.line([(14, 15 + y), (6, 8 + y - flap)], 1, BONE, inner=False)
        # nohy v kroku
        c.ellipse(13.5 + lift[0], 26.5 + y, 2, 3, SKIN4); c.ellipse(18 + lift[1], 26.5 + y, 2, 3, SKIN4)
        c.rect(12 + lift[0], 29 + y, 4, 2, ['1', '3']); c.rect(17 + lift[1], 29 + y, 4, 2, ['1', '3'])
        c.ellipse(16, 21 + y, 5, 5, SKIN)
        c.ellipse(16.5, 22.5 + y, 2.6, 2.4, ['d', 'e', 'f'], bias=.2)
        if arms == 'up':
            c.ellipse(19.5, 13 + y, 1.8, 3.2, SKIN4); c.stamp(19, 9 + y, ['jj'])
        elif arms == 'slash':
            c.ellipse(22, 18 + y, 3.2, 1.8, SKIN4); c.stamp(25, 17 + y, ['j.', '.j', 'j.'])
        else:
            c.ellipse(19.5, 21 + y, 1.8, 3, SKIN4); c.stamp(19, 24 + y, ['jj'])
        # hlava z profilu
        c.poly([(12, 10 + y), (7, 6 + y), (11, 14 + y)], SKIN4)
        c.ellipse(17, 11 + y, 6.5, 6.5, SKIN)
        c.ellipse(22, 13 + y, 2.4, 2, SKIN)  # čenich
        c.line([(15, 6 + y), (12, 3 + y), (9, 1 + y)], 2, BONE, inner=False)
        c.stamp(17, 8 + y, ['aaa.', '.ggh', '.gKg'])
        c.stamp(19, 14 + y, ['KKKK', '.jKj'])
        c.put(23, 12 + y, 'b')
    else:
        back = view == 'back'
        # ocas
        if back:
            c.line([(16, 24 + y), (15, 28 + y), (11, 29 + y), (8, 26 + y + tail)], 2, SKIN4, inner=False)
            c.poly([(6, 25 + y + tail), (10, 24 + y + tail), (8, 22 + y + tail)], SKIN4)
        else:
            c.line([(20, 24 + y), (25, 22 + y), (27, 18 + y + tail), (26, 14 + y + tail)], 2, SKIN4, inner=False)
            c.poly([(24, 14 + y + tail), (29, 14 + y + tail), (27, 10 + y + tail)], SKIN4)
        wings = []
        for s in (0, 1):
            pts = [(12, 15), (4, 8 - flap), (2, 13 - flap), (5, 13), (4, 17), (7, 16), (8, 19), (12, 18)]
            if s: pts = [(31 - x, yy) for x, yy in pts]
            wings.append([(x, yy + y) for x, yy in pts])
        if not back:
            for w in wings:
                c.poly(w, MEMB); c.line([w[0], w[1]], 1, BONE, inner=False)
        # nohy
        c.ellipse(13.5, 26.5 + y - lift[0], 2, 3, SKIN4); c.ellipse(18.5, 26.5 + y - lift[1], 2, 3, SKIN4)
        c.rect(12, 29 + y - lift[0], 4, 2, ['1', '3']); c.rect(17, 29 + y - lift[1], 4, 2, ['1', '3'])
        # tělo
        c.ellipse(16, 21 + y, 5.5, 5, SKIN)
        if not back:
            c.ellipse(15.5, 22.5 + y, 2.8, 2.4, ['d', 'e', 'f'], bias=.15)
        # paže
        if arms == 'up':
            c.ellipse(10, 14 + y, 1.8, 3.4, SKIN4); c.ellipse(22, 14 + y, 1.8, 3.4, SKIN4)
            c.stamp(9, 10 + y, ['jj']); c.stamp(21, 10 + y, ['jj'])
        elif arms == 'slash':
            c.ellipse(9.5, 21 + y, 1.8, 3, SKIN4)
            c.ellipse(23, 17 + y, 3.2, 1.8, SKIN4); c.stamp(26, 15 + y, ['j..', '.j.', 'j.j', '.j.'])
        else:
            c.ellipse(9.5, 21 + y, 1.8, 3.2, SKIN4); c.ellipse(22.5, 21 + y, 1.8, 3.2, SKIN4)
            c.stamp(9, 24 + y, ['jj']); c.stamp(22, 24 + y, ['jj'])
        # uši a hlava
        c.poly([(10, 10 + y), (4, 6 + y), (10, 15 + y)], SKIN4)
        c.poly([(22, 10 + y), (28, 6 + y), (22, 15 + y)], SKIN4)
        c.ellipse(16, 11 + y, 7, 6.5, SKIN)
        c.line([(12, 6 + y), (9, 3 + y), (8, 0 + y)], 2, BONE, inner=False)
        c.line([(20, 6 + y), (23, 3 + y), (24, 0 + y)], 2, BONE, inner=False)
        if back:
            for w in wings:
                c.poly(w, MEMB); c.line([w[0], w[1]], 1, BONE, inner=False)
        else:
            c.stamp(10, 8 + y, ['aa........aa', '.aaa....aaa.', '.ggh....hgg.', '.gKg....gKg.'])
            c.stamp(15, 12 + y, ['bb'])
            if mouth == 'grin':
                c.stamp(11, 13 + y, ['K........K', 'KjjjjjjjjK', '.KjKKKKjK.', '..KKKKKK..'])
            elif mouth == 'open':
                c.stamp(13, 14 + y, ['KjjjjK', 'KKKKKK', '.KKKK.'])
            else:
                c.stamp(13, 14 + y, ['KKKKKK', '..j.j.'])
    if orb:
        r = 2.5 + orb
        c.ellipse(16 if view != 'side' else 20, 4 + y, r, r, MAGIC, inner=False, lo=-.6, hi=.8)
    c.outline('K')
    c.clean_orphans()
    return c


def imp_frames():
    out = {}
    for v in ('front', 'back', 'side'):
        out[f'{v}_idle'] = [imp(v, bob=b, flap=f, tail=t) for b, f, t in ((0, 0, 0), (0, 1, 0), (1, 1, 1), (1, 0, 1))]
        out[f'{v}_walk'] = [imp(v, bob=b, lift=l, flap=f, tail=t) for b, l, f, t in
                            ((0, (2, 0), 0, 0), (1, (0, 0), 1, 1), (0, (0, 2), 0, 0), (1, (0, 0), -1, 1))] if v != 'side' else \
            [imp(v, bob=b, lift=l, flap=f, tail=t) for b, l, f, t in ((0, (-2, 2), 0, 0), (1, (0, 0), 1, 1), (0, (2, -2), 0, 0), (1, (0, 0), -1, 1))]
    out['front_cast'] = [imp('front', bob=-1, arms='up', flap=-1, orb=0, mouth='open'), imp('front', bob=-2, arms='up', flap=-2, orb=1, mouth='open'),
                         imp('front', bob=-3, arms='up', flap=-1, orb=2, mouth='open'), imp('front', bob=-2, arms='up', flap=-2, orb=3, mouth='open')]
    out['side_slash'] = [imp('side', bob=1, arms='down', mouth='grin'), imp('side', bob=0, arms='slash'), imp('side', bob=0, arms='slash', flap=1)]
    return out

if __name__ == '__main__':
    fr = imp_frames()
    rows = [sheet([f.image() for f in fr[k]], pad=0) for k in fr]
    W = max(r.width for r in rows); H = sum(r.height for r in rows)
    im = Image.new('RGBA', (W, H), (40, 30, 40, 255)); y = 0
    for r in rows: im.paste(r, (0, y), r); y += r.height
    im.resize((W * 6, H * 6), Image.NEAREST).save('/tmp/imp_preview.png')
    print(list(fr))
