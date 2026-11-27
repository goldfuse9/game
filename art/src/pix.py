"""Malá knihovna pro procedurální pixel art s cel-shadingem (světlo zleva shora).
Postupuje podle pixel-art-studio: silueta -> výplň -> 3-4 stupně stínu -> hue shift -> obrys tmavší než nejtmavší pixel."""
import math
import numpy as np
from PIL import Image, ImageDraw

# ---- paleta IMP (36 barev, odstíny s posunem hue: stíny do fialova, světla do oranžova) ----
PAL = {
    'K': '#0b0910',  # obrys
    '1': '#17131d', '2': '#231c29', '3': '#33283a', '4': '#47394b', '5': '#5f4e5e', '6': '#7d6a73', '7': '#a2908a',
    'a': '#2a0d1c', 'b': '#4c1326', 'c': '#7a1d28', 'd': '#a8302a', 'e': '#d0532e', 'f': '#f08b3c',
    'g': '#ffc65c', 'h': '#fff1b8',
    'i': '#b9a68c', 'j': '#ece0c4',
    'k': '#16211c', 'l': '#27392a', 'm': '#435a33', 'n': '#6c8446', 'o': '#a2ad66',
    'p': '#1a2132', 'q': '#313d58', 'r': '#5a6a8a', 's': '#9cadc6',
    't': '#2aa8d0', 'u': '#9af2ff',
    'v': '#341a56', 'w': '#7438bc', 'x': '#c48cff',
    'y': '#7c4f12', 'z': '#d29a30', 'Z': '#ffe08a',
    'A': '#33201a', 'B': '#5a3622', 'C': '#8c5a38', 'D': '#c8936a',
}
SKIN = ['b', 'c', 'd', 'e', 'f']
SKIN4 = ['b', 'c', 'd', 'e']
MEMB = ['a', 'b', 'c']
BONE = ['5', '7', 'i', 'j']
STONE = ['1', '2', '3', '4', '5']
LEATHER = ['A', 'B', 'C']
FIRE = ['c', 'e', 'f', 'g', 'h']
MAGIC = ['v', 'w', 'x', 'h']
L = np.array([-0.55, -0.68, 0.48]); L = L / np.linalg.norm(L)


def hex2rgb(h):
    h = h.lstrip('#'); return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


class Canvas:
    def __init__(self, w, h):
        self.w, self.h = w, h
        self.a = np.full((h, w), '', dtype='<U1')

    def copy(self):
        c = Canvas(self.w, self.h); c.a = self.a.copy(); return c

    def put(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < self.w and 0 <= y < self.h:
            self.a[y, x] = c

    def _shade(self, mask, ramp, cx, cy, rx, ry, bias=0.0, inner=True, flat=False, lo=-0.3, hi=1.0):
        prev = self.a.copy()
        ys, xs = np.nonzero(mask)
        n = len(ramp)
        for y, x in zip(ys, xs):
            if flat:
                idx = n - 1
            else:
                nx = (x + .5 - cx) / max(rx, .5); ny = (y + .5 - cy) / max(ry, .5)
                r2 = min(nx * nx + ny * ny, 1.0)
                nz = math.sqrt(1 - r2) * 1.1 + .05
                v = np.array([nx, ny, nz]); v /= np.linalg.norm(v)
                i = float(v @ L) + bias
                idx = int((i - lo) / (hi - lo) * n)
                idx = max(0, min(n - 1, idx))
            self.a[y, x] = ramp[idx]
        if inner:
            # vnitřní kontura: okraj tvaru, který leží přes jinou už nakreslenou část, dostane nejtmavší odstín
            dark = ramp[0]
            for y, x in zip(ys, xs):
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    X, Y = x + dx, y + dy
                    if 0 <= X < self.w and 0 <= Y < self.h and not mask[Y, X] and prev[Y, X] != '':
                        self.a[y, x] = dark
                        break

    def ellipse(self, cx, cy, rx, ry, ramp, **kw):
        Y, X = np.mgrid[0:self.h, 0:self.w]
        mask = ((X + .5 - cx) / rx) ** 2 + ((Y + .5 - cy) / ry) ** 2 <= 1.0
        self._shade(mask, ramp, cx, cy, rx, ry, **kw)
        return mask

    def _mask_from(self, fn):
        im = Image.new('L', (self.w, self.h), 0); d = ImageDraw.Draw(im); fn(d)
        return np.array(im) > 0

    def poly(self, pts, ramp, **kw):
        mask = self._mask_from(lambda d: d.polygon([(x, y) for x, y in pts], fill=255))
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx, cy = (min(xs) + max(xs) + 1) / 2, (min(ys) + max(ys) + 1) / 2
        self._shade(mask, ramp, cx, cy, (max(xs) - min(xs) + 1) / 2, (max(ys) - min(ys) + 1) / 2, **kw)
        return mask

    def line(self, pts, width, ramp, **kw):
        mask = self._mask_from(lambda d: d.line([(x, y) for x, y in pts], fill=255, width=width))
        xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
        cx, cy = (min(xs) + max(xs) + 1) / 2, (min(ys) + max(ys) + 1) / 2
        self._shade(mask, ramp, cx, cy, (max(xs) - min(xs) + 2) / 2, (max(ys) - min(ys) + 2) / 2, **kw)
        return mask

    def rect(self, x, y, w, h, ramp, **kw):
        mask = np.zeros((self.h, self.w), bool)
        mask[max(0, y):max(0, y + h), max(0, x):max(0, x + w)] = True
        self._shade(mask, ramp, x + w / 2, y + h / 2, w / 2, h / 2, **kw)
        return mask

    def stamp(self, x, y, rows):
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch not in '. ':
                    self.put(x + i, y + j, ch)

    def outline(self, col='K', diag=False):
        prev = self.a.copy()
        for y in range(self.h):
            for x in range(self.w):
                if prev[y, x] != '':
                    continue
                nb = [(1, 0), (-1, 0), (0, 1), (0, -1)] + ([(1, 1), (-1, -1), (1, -1), (-1, 1)] if diag else [])
                for dx, dy in nb:
                    X, Y = x + dx, y + dy
                    if 0 <= X < self.w and 0 <= Y < self.h and prev[Y, X] != '':
                        self.a[y, x] = col; break

    def clean_orphans(self):
        """Odstraní osamělé pixely (žádný soused stejné barvy v 8-okolí) – nahradí je převládající barvou okolí."""
        a = self.a.copy()
        for y in range(self.h):
            for x in range(self.w):
                c = a[y, x]
                if c in ('', 'K'):
                    continue
                same = 0; cnt = {}
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        if dx == dy == 0: continue
                        X, Y = x + dx, y + dy
                        if 0 <= X < self.w and 0 <= Y < self.h:
                            n = a[Y, X]
                            if n == c: same += 1
                            if n not in ('', 'K'): cnt[n] = cnt.get(n, 0) + 1
                if same == 0 and cnt:
                    self.a[y, x] = max(cnt, key=cnt.get)

    def image(self, scale=1):
        im = Image.new('RGBA', (self.w, self.h), (0, 0, 0, 0)); px = im.load()
        for y in range(self.h):
            for x in range(self.w):
                c = self.a[y, x]
                if c:
                    px[x, y] = hex2rgb(PAL[c]) + (255,)
        return im.resize((self.w * scale, self.h * scale), Image.NEAREST) if scale != 1 else im

    def mirrored(self):
        c = Canvas(self.w, self.h); c.a = self.a[:, ::-1].copy(); return c


def sheet(frames, cols=None, pad=0):
    cols = cols or len(frames)
    w, h = frames[0].width, frames[0].height
    rows = (len(frames) + cols - 1) // cols
    im = Image.new('RGBA', (cols * (w + pad), rows * (h + pad)), (0, 0, 0, 0))
    for i, f in enumerate(frames):
        im.paste(f, ((i % cols) * (w + pad), (i // cols) * (h + pad)))
    return im
