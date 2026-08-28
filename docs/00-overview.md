# 00 — Overview

Gunship 2000, Amiga CD32, published by MicroProse. The fifteenth disc in this
Amiga CD32 / CDTV series and the first flight simulator in it.

Everything below is read off the disc. Studio, year, publisher, version and
floppy ancestry were all treated as unknown at the start and are cited here only
where a field, a string or a byte on the disc says so.

## What the disc says about itself

| field | value | where |
|---|---|---|
| system identifier | `CDTV` | PVD, LBA 16 |
| volume identifier | `Gunship_2000` | PVD |
| publisher | `Microprose` | PVD |
| data preparer | `D J Pocock - ISOCD 1.04 by Pantaray, Inc. USA -` | PVD |
| application identifier | `Gunship 2000 CD32` | PVD |
| volume creation | 1994-04-19 13:46:56 UTC | PVD |
| CATALOG | 5015352330281 (a real EAN-13) | cue sheet |
| version banner | `Gunship 2000     V3.32 - 15/4/1994` | `gunship 2000` +0xae6 |

The publisher field is spelled `Microprose`, one word, lowercase *p*. It is the
first non-British client of ISOCD by Pantaray, Inc. USA in this series: the
fourteen previous discs are UK, UK+DE or UK+DK labels.

There is **no `$VER:` string in any of the four game programs.** The version came
from a bare banner in the launcher, which is the third instance of that pattern
in the series after Banshee and Fire & Ice. The seven `$VER:` strings that do
exist are all in stock Commodore commands, the two locale catalogues, one
third-party tool and one paint-package annotation.

## The shape of the disc in one table

| | sectors | bytes | share |
|---|---:|---:|---:|
| data track (image) | 80,813 | 165,505,024 | |
| — declared volume | 80,735 | 165,345,280 | |
| — 100 MiB zero hole before the files | 51,200 | 104,857,600 | 63.4 % of the volume |
| — filesystem and files | 29,278 | 59,961,344 | 36.3 % of the volume |
| — unclaimed tail (all zero) | 232 | 475,136 | |
| — image overrun past the volume (all zero) | 78 | 159,744 | |
| audio, 5 tracks | 70,136 | | 15:35.11 |
| **total used of a 333,000-sector CD** | **150,949** | | **45.3 %** |

Data 53.5 %, audio 46.5 % — the first disc in the series where the data track
is the larger half.

Of the 59,789,206 bytes the 140 files occupy, **86.9 % is streamed CDXL video**
and 1.3 % is a second, unreachable game. See [10-band.md](10-band.md).

## The five things worth knowing

1. **A 100 MiB hole, to the byte.** LBA 25 to 51,224 is 104,857,600 bytes of
   zero — exactly 100 × 1024 × 1024 — sitting between the filesystem descriptors
   and the first file. Not approximately: exactly. This is the fourth disc in
   the series with a gap in front of the files and the first one whose size is a
   round number. [01-disc-image.md](01-disc-image.md)

2. **A complete second game that never runs.** `pirates.demo` is a full
   alternative boot script for a playable Pirates! Gold demo, with German
   language detection, two 383 KB executables, a font and a language probe. The
   active `s/startup-sequence` never calls it, and the one line that would have
   launched it is commented out with a note to a human still attached.
   [11-leftovers.md](11-leftovers.md)

3. **The floppy release is described by the CD, in its own words.** The loader
   assigns four volumes `gs_dsk1`–`gs_dsk4`, opens `gs_dsk2:gs2frt.cat`, and
   carries the string `Insert GS2000 disk %d`. Four one-byte files named `1`,
   `2`, `3` and `4` sit in the root: they are the disk-identity probes the
   format string `gs_dsk%d:%d` opens. [03-boot-chain.md](03-boot-chain.md)

4. **The game's own data files are little-endian IFF.** All 76 loose pictures
   are correct big-endian ILBM/PBM. All 41 files inside the archives that use
   the game's own form types — `SCRN`, `WRLD`, `SHIP`, `SHIN`, `SCNR`, `THTR`,
   `WSYS` — store every chunk size in Intel order. A standard IFF reader sees a
   3.4 GB FORM in a 3 KB file. [07-graphics.md](07-graphics.md)

5. **`D J Pocock` again, and 232 again.** Fifth Pocock master, fifth 232-sector
   unclaimed tail, now across five studios, five publishers and two countries.
   And the file-level lead that came out of Universe is dead.
   [12-open-questions.md](12-open-questions.md)

## Document index

| | |
|---|---|
| [01-disc-image.md](01-disc-image.md) | tracks, sector map, the 100 MiB hole, the pregaps |
| [02-filesystem.md](02-filesystem.md) | ISO 9660 volume, 140 files, the empty directory |
| [03-boot-chain.md](03-boot-chain.md) | startup-sequence, the four programs, the floppy ancestor |
| [04-compression.md](04-compression.md) | RNC method 2, `cd32rez`, the [10 of 10] rule |
| [05-archives.md](05-archives.md) | the `.cat` / `.dat` format, 165 3D objects |
| [06-text.md](06-text.md) | the prose census against both denominators |
| [07-graphics.md](07-graphics.md) | IFF geometry, the byte-order split, CDXL video |
| [08-audio.md](08-audio.md) | five Red Book tracks, `cd.device`, the sound blobs |
| [09-hardware.md](09-hardware.md) | Akiko, the blitter, where the frame ends |
| [10-band.md](10-band.md) | the three figures and the 13.3 MB ceiling |
| [11-leftovers.md](11-leftovers.md) | Pirates! Gold, `ERASE ME`, the dangling font |
| [12-open-questions.md](12-open-questions.md) | what is still open, and the prediction table |
