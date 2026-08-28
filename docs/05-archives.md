# 05 — The `.cat` / `.dat` archives

Reproduce with `tools/catdump.py`. Listings in
[`notes/object-cat.txt`](../notes/object-cat.txt),
[`notes/gs2frt-dat.txt`](../notes/gs2frt-dat.txt) and
[`notes/flight-cat.txt`](../notes/flight-cat.txt).

## The format

Six files use it. Nothing on the disc declares it; it was recovered from the
bytes and then checked arithmetically.

```
u16            entry count N
N x 24 bytes   char name[16]     NUL padded
               u32 length
               u32 offset        absolute from the start of the file
...            payload, beginning at 2 + 24*N
```

The check that this is right and not merely plausible: on all six archives the
**first entry's offset equals `2 + 24*N` exactly**.

```
gs2frt.cat  49 entries, table 2..1178, first payload offset 1178   matches
gs2end.cat  20 entries, table 2..482,  first payload offset 482    matches
flight.cat  33 entries, table 2..794,  first payload offset 794    matches
object.cat 165 entries, table 2..3962, first payload offset 3962   matches
gs2frt.dat  52 entries, table 2..1250, first payload offset 1250   matches
gs2end.dat  10 entries, table 2..242,  first payload offset 242    matches
```

All six are 100.0 % covered by their entries with zero gaps and zero trailing
bytes. The entries are laid out in table order.

## The 0xFF terminator

45 archived entries have a loose namesake on the disc, and in every one of those
45 the archived length is exactly the loose file's length **plus one**, with the
loose file's bytes as a prefix.

```
entries where archived == loose + exactly 1 byte: 45
value of that extra byte: {'0xff': 45}
```

45 of 45 is `0xFF`. This is not an off-by-one in the archive builder: it is a
deliberate one-byte sentinel appended to each entry and counted in the declared
length. It is also why a standard IFF reader run over an extracted entry reports
the FORM as one byte short of the file — see [07-graphics.md](07-graphics.md).

## Contents

| archive | entries | extensions |
|---|---:|---|
| `gs2frt.cat` | 49 | PIX ×49 |
| `gs2end.cat` | 20 | PIX ×20 |
| `flight.cat` | 33 | BBM ×20, LBM ×7, BIN ×6 |
| `object.cat` | 165 | SBN ×165 |
| `gs2frt.dat` | 52 | SCN ×15, SNR ×9, WRL ×9, SHI ×8, SHP ×8, THR ×2, WPN ×1 |
| `gs2end.dat` | 10 | SCN ×10 |

`.cat` carries pictures and models; `.dat` carries the screen, world and shape
definitions that reference them. The pairing follows the floppy layout: `gs2frt`
is disk 2, `gs2end` is disk 4, `flight` and `object` are opened without a
volume prefix.

## 1.83 MiB is stored twice

```
archive entries duplicated by a loose file: 63 = 1,916,310 bytes
archive entries whose loose namesake DIFFERS:  5
```

63 archive entries are byte-identical to a loose file sitting in the root of the
same disc. That is 1,916,310 bytes — 1.83 MiB, or 27.6 % of the 6.62 MiB the game
occupies on disc — present in two places.

The five that differ are more interesting than the 63 that do not:

| name | loose | archived | |
|---|---:|---:|---|
| `cd1.pix` | 34,840 | 31,301 | different picture |
| `cd2.pix` | 35,526 | 30,787 | different picture |
| `cd3.pix` | 34,496 | 31,067 | different picture |
| `RESCUE.PIX` | 28,288 | 28,329 | different picture |
| `PILOT.PIX` | 52,320 | 50,859 (in `gs2end.cat`) | different picture |

`PILOT.PIX` is in both archives: `gs2frt.cat` holds the loose version plus the
terminator, `gs2end.cat` holds a different, smaller one. So there are two
distinct pictures with that name on the disc and the front end and the endgame
each get their own.

Which copy the game reads depends on the path it opens: `gs` names
`gs_dsk2:gs2frt.cat` and `gs_dsk4:gs2end.cat` explicitly, so the archived copies
are the live ones for the front end and endgame. The 63 loose duplicates are
reachable only by a bare filename open. Nothing on the disc says the loose
copies are ever opened.

## `object.cat` — 165 3D models

165 entries, 163 distinct names (two names appear twice, with identical
payloads). 392,549 bytes of payload. Sizes range from 317 bytes (`SPLAT`) to
5,749 (`APACHEB`).

### The header

Every `.SBN` starts with four big-endian 16-bit words. Words 1, 2 and 3 are
strictly increasing and all three are `<=` the file length:

```
163 SBN files: 163 have w1<w2<w3<=size
```

163 of 163. They are three section offsets into the file. Word 0 varies and its
meaning is not established — its low byte is only ever 0 (99 files) or 1 (64
files), and its high byte increments across runs of files in archive order but
not monotonically over the whole set. Recorded in
[12-open-questions.md](12-open-questions.md).

The body is signed 16-bit values dominated by `0x4000`, `0xC000` and small
magnitudes — vertex coordinates on a fixed-point scale.

### The models name the game's order of battle

```
2S6 A10 AFRAME1 AFRAME2 AH-1W AH66 AML90 AMMO1 AMMO2 AMMO3 AMX AN72 APACHE4
APACHEB ARCH ARCH1 ARCHBR AT5 BARN1 BASEGUY BED BILLB BILLB2 BILLB3 BLD31
BLKDEAD BLUEBOX BMP1 BMP2 BOXBLD2 BOXBLD3 BOXBLD4 BOXBLD5 BOXBUILD BOXS BRDM2
BTR BUNKER1 BUNKWRK BURKE2 CAB CAMELH CAMELSIT CAPE CAPE1 CEMENT CHALL CHURCH
COALCAR COVERED COW CRANE CRNWRK DEFENDER DERRK DESAIR DRAW DRONE DROPOFF EE11
EE9 ENGINE ENGINE2 F15 F162 FARP FLATCAR FOX2 FOX3 FUELTNK GAZ GAZELLE GHTENT
HANGER1 HANGER2 HANGER3 HELDEAD HINDN HIP HOKUM HOUSE2 HOUSE3 HUMMER IRON IRON2
LRGAIR M109 M113 M163VADS M1974 M1A1 M2 M60A3 MATKA MI-28 MIG23 MIG23LG MIG29
MIG29LG MIRAGE MIRAGELG MRLS MTLB OFFICE OH58D OILRIG OILRIGWK OILTANK OILWRK
OSA11 POPTENT RAIL1 RAIL2 RAIL3 RAILB2 RAT315 REFINE REFWRK ROADB2 ROWHOUSE SA13
SA2 SA6 SCORPION SCUD SHIPBOOM SMAIR SPLAT STRBOOM STRBOOM2 SU25 SU27 T4 T4WTANK
T62 T72 T72B2 TANKBOOM TANKCAR TANKTR TARAWA TARMAC TARP TEMPAIR TENT3 TENT5
TOWED TOWER1 TOWER2 TRAILER TRAILTR TRBOOM TRKWRK TRS2230 UH60 URAL WARRIOR WAVE
WAVE2 WHITEBOX ZRKSD ZSU23 ZSU57
```

Aircraft, helicopters, ships, armour, air defence, and a great deal of scenery.
`BLUEBOX`, `WHITEBOX` and `BOXS` are untextured primitives and read as
placeholders; `COW`, `CAMELH` and `CAMELSIT` are set dressing;
`BLKDEAD`/`HELDEAD` are wreck states; `SPLAT` at 317 bytes is the smallest model
on the disc.

### Each model carries its own description

`object.cat` holds 14,984 bytes of English prose across 245 runs — a name and a
recognition-guide description per model, stored inside the model file:

```
0x001f9a  Friendly fixed wing. No threat.
0x00352e  AML-90 Reconnaissance Vehicle
0x00354c  Lightly armored vehicle that's usually armed with...
0x003a26  Small weapon storage facility that may be armed ...
```

This is where most of the game's prose lives. See [06-text.md](06-text.md).

## `gs2frt.dat` — the screen definitions

52 entries in seven form types. These are the files that make the front end
work: `BASE.SCN`, `BRIEFING.SCN`, `ROSTER.SCN`, `OUTFIT.SCN`, `ORDNANCE.SCN`,
`REPLAY.SCN`, `THEATER.SCN` and so on, plus `EURO6..8.WRL` / `GULF3..6.WRL`
worlds, `SHIP_00..07.SHP` and `SHIN_00..07.SHI`, `CENT_*.SNR` / `PERS_*.SNR`,
two `.THR` theatres and one `.WPN`.

They are IFF, and they are little-endian IFF. `BASE.SCN` declares a 3.4 GB FORM
to a standard reader; read with Intel byte order it is 3,022 bytes of payload
plus the 8-byte header plus the 1-byte archive terminator = 3,031, the exact file
length. The chunk vocabulary is `SCHD` (screen header), `AREA` (39 across the
set — the clickable regions behind `gs`'s string `Select Action Area.`), `LORI`,
and `CMPX` (302). Full census in [07-graphics.md](07-graphics.md).
