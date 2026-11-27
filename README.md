# IMP 2 – Temné patro

Pixel-art roguelite z pohledu shora. Hraješ za malého impa čaroděje, plížíš se tmou kolem mariňáků s baterkami, sekáš drápy, stahuješ je pentagramem do pekla a sestupuješ kruhy pekla až k Hrdinovi.

## Rychlé spuštění (bez instalace)

Otevři `game/index.html` v Chrome, Edge nebo Firefoxu. Hotovo.

## Desktopová aplikace (Windows, macOS, Linux)

Potřebuješ [Node.js](https://nodejs.org) 20 nebo novější.

```bash
npm install
npm start
```

Samostatný `.exe` pro Windows (složka `dist/`):

```bash
npm run dist
```

## Ovládání

| Akce | PC | Mobil |
|---|---|---|
| Chůze | WASD | táhni palcem |
| Míření | myš | automaticky |
| Ohnivé koule | samy | samy |
| Drápy | levé tlačítko / F / mezerník | DRÁPY |
| Pentagram (na kurzor) | pravé tlačítko / Q | PENTAGRAM |
| Rozpolcená duše | E | DUŠE |
| Plížení | C / Shift | PLÍŽIT |
| Hudba | M | ♪ |
| Celá obrazovka (aplikace) | F11 | – |

## Obsah repozitáře

| Složka | Co tam je |
|---|---|
| `game/` | IMP 2 – hlavní hra (jeden HTML soubor, sprity jsou vložené uvnitř) |
| `game-fps/` | IMP – první verze z pohledu první osoby |
| `art/art-bible.html` | art bible: paleta, pravidla, živé animace |
| `art/sprites/` | sprite sheety a dlaždice v PNG + `sprites.json` (rozměry a řádky animací) |
| `art/src/` | Python generátor pixel artu (`python3 build.py` vytvoří sprity znovu, potřebuje Pillow, numpy, scipy) |

## Další kroky k vydání na Steam

1. Přepis hry do TypeScriptu po modulech.
2. Napojení na Steam přes [steamworks.js](https://github.com/ceifa/steamworks.js) (achievementy, cloud save).
3. Podpora gamepadu (Steam Deck).
4. Stránka „Coming soon“ a sbírání wishlistů.
