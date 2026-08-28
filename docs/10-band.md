# 10 — The band: the three figures

Reproduce with `tools/bandcalc.py`. Results in
[`notes/band.txt`](../notes/band.txt).

Any claim about how big a CD32 game is has to say which of three numbers it is:
**on disc**, the bytes of the file in the ISO 9660 volume; **resident**, the
bytes after every packed stream inside it has been unpacked at every nesting
level; **used**, resident minus the trailing zeros of each blob.

## Unpack depth

**One level.** Every packed stream on this disc is RNC method 2 at depth 0, and a
re-scan of every unpacked output found no second level
([04-compression.md](04-compression.md)). Universe needed three levels and a
one-level read understated its resident figure by 38 %; here one level is the
whole story and the resident figure is complete.

## By category

```
category  files      on disc     resident         used
game        118      6939994      8363560      8363199
os           15       133156       133156       133156
video         3     51945914     51945914     51945796
pirates       4       770142      1167966      1167966
TOTAL       140     59789206     61610596     61610117
```

The categories matter because the band measures the **game**, not the disc. A
157.84 MB data track is not a 157.84 MB game: Liberation is 168 MB of data track
and 2.9 MB of game.

* **video** — the three CDXL streams, 86.9 % of the file bytes.
* **pirates** — the bundled Pirates! Gold demo that never runs
  ([11-leftovers.md](11-leftovers.md)).
* **os** — SetPatch, the ten stock AmigaDOS commands, the three shared libraries
  and the third-party CDXL player.
* **game** — everything else.

## The figure

```
GAME ONLY
   on disc    6,939,994 bytes = 6.62 MiB
   resident   8,363,560 bytes = 7.98 MiB
   used       8,363,199 bytes = 7.98 MiB
```

**The band holds.** Floor 2.25 MB (Guardian), ceiling 13.3 MB (Marvin), and
Gunship 2000 sits at 7.98 MiB resident — comfortably inside, a little above the
middle.

The prediction written before the measurement was that the band would survive,
and it does. It is worth being explicit about how much room there was to be
wrong: this disc has the **second-largest data track in the series**, 157.84 MB,
within 2 % of Liberation's. It was the best candidate the series has had to break
the ceiling from above. It does not come close. 63.4 % of the volume is a zero
hole, 86.9 % of the file bytes are video, and what is left is an ordinary
mid-size Amiga game.

Fifteen discs, eleven studios, five years, and nothing has passed 13.3 MB.

## Slack, and a hypothesis that does not survive

```
   slack    361 bytes = 0.004 % of resident
```

Three hundred and sixty-one bytes of trailing zeros across 118 files. This is the
fifth data point:

| disc | slack | AmigaDOS alive during play? |
|---|---:|---|
| **Gunship 2000** | **0.004 %** | **yes** |
| Fire & Ice | 0.3 % | no |
| Universe | 0.5 % | no |
| Banshee | 3.9 % | — |
| Dragonstone | 9.1 % | yes |

The hypothesis after Universe was that the two tight discs take the machine
completely and allocate nothing, while the two wide ones keep AmigaDOS alive.
Universe had already weakened the "studio habit" reading by putting Core Design
at both extremes (0.5 % and 9.1 %, 18:1).

Gunship 2000 falsifies the replacement. It keeps AmigaDOS alive throughout —
it boots from a startup-sequence, opens eight libraries and three devices, calls
`LoadView` rather than seizing the display, and *returns to the shell* so the
script can kill the backdrop task by name ([09-hardware.md](09-hardware.md)) —
and it has the **tightest slack of all five**, by two orders of magnitude over
Dragonstone.

So slack does not track OS survival, and it does not track studio. It probably
tracks nothing more interesting than whether the assets were built by a tool
that pads to a block size. Recorded in
[12-open-questions.md](12-open-questions.md).

### Per-file slack

The checklist warns that a low total can hide a deliberate buffer — on Universe
the 0.5 % total was entirely inside two files at 48.3 % and 49.3 %. That check
was run and there is nothing hiding here:

```
 slack bytes     pct     resident  file
         245   14.6%         1680  roster.dat
         118    0.0%     21618080  piratesgold.intro.xl
           4    0.1%         5046  Catalogs/English/Ami.catalog
           2    0.0%         5914  POINTER.PIX
           2    0.0%         9118  MENU8085.PIX
```

The largest single slack on the disc is 245 bytes, and it is in `roster.dat` —
the 1,680-byte scratch file whose first bytes are `ERASE ME`
([11-leftovers.md](11-leftovers.md)). Everything else is one or two bytes of
even-length padding on an IFF file.

## Where the 157.84 MB actually goes

| | bytes | share of image |
|---|---:|---:|
| 100 MiB zero hole | 104,857,600 | 63.4 % |
| `INTRO.XL` | 26,830,284 | 16.2 % |
| `piratesgold.intro.xl` | 21,618,080 | 13.1 % |
| `cdintro.xl` | 3,497,550 | 2.1 % |
| the game | 6,939,994 | 4.2 % |
| the Pirates! Gold demo programs | 770,142 | 0.5 % |
| OS binaries and libraries | 133,156 | 0.1 % |
| filesystem, .TM, unclaimed tail, overrun | ~858,218 | 0.5 % |

**The game is 4.2 % of its own disc.** Of the rest, 63.4 % is nothing, 31.4 % is
video and 13.1 percentage points of that video advertise a different game.

## Duplication

1,916,310 bytes — 27.6 % of the game's on-disc bytes — exist twice, once loose in
the root and once inside a `.cat` archive ([05-archives.md](05-archives.md)).
Removing the duplicates would bring the game to 5.02 MiB on disc. The figures
above do not do that, because both copies are genuinely present and the band is a
measure of what shipped.
