# 07 — Graphics

Reproduce with `tools/iffscan.py`, `tools/iffle.py` and `tools/cdxl.py`.
Results in [`notes/iff-geometry.txt`](../notes/iff-geometry.txt),
[`notes/iff-byteorder.txt`](../notes/iff-byteorder.txt) and
[`notes/cdxl.txt`](../notes/cdxl.txt).

## Everything is IFF, and that is unusual for this series

There is no raw planar image data on this disc and no bespoke picture format.
The stills are ordinary IFF ILBM with `ByteRun1` compression, the video is CDXL,
and the game's own data files are IFF too. There is nothing here to guess the
geometry of, so `geomguess.py` was not needed — a first for this series.

## The loose pictures: 320×200, eight planes, 256 colours

76 IFF files sit loose in the root. 73 are ILBM, 1 is PBM, 2 are locale
catalogues.

```
320x200      8 planes, 256 colours, CAMG $00011000    x70
320x200      8 planes, 256 colours, CAMG $00091000    x1   (GS2LOGO.LBM)
320x200      8 planes, 256 colours, no CAMG           x1   (logo.pix, PBM)
320x200      6 planes,  16 colours, CAMG $00000800    x1   (frame.lbm, HAM)
320x256      5 planes,  32 colours, CAMG $00004000    x1   (colour.lbm)
```

70 of 73 ILBM are the same thing: 320×200, eight bitplanes, a 256-entry CMAP.
Eight planes is AGA. The plane count is read from the `BMHD` field directly, so
the BPLCON0 BPU3 trap that produced two false "zero bitplane" readings elsewhere
in this series does not arise here — but note that the trap would have mattered:
these are eight-plane screens, exactly the case that reads as zero to a scan
looking only at bits 14–12.

Two exceptions are worth naming. `frame.lbm` is the only HAM picture on the
disc (CAMG `$00000800`, 6 planes, 16 colours) and it is the decorative frame the
startup-sequence draws around the Pirates! Gold video at x 61, y 25.
`colour.lbm` is 320×256, five planes, 32 colours — a different resolution from
everything else and 2,788 bytes, of which 2,560 is BODY: 32 colours × 80 bytes,
a palette swatch sheet rather than a picture.

`logo.pix` is a **`PBM `** form, not `ILBM`. PBM is the chunky variant written by
DeluxePaint on the PC. It also carries a `TINY` chunk, which is the DPaint PC
thumbnail. It is the only chunky picture on the disc and it came from a DOS
machine.

66 of the ILBM carry a `DPPS` chunk (DPaint perspective settings) and the set
carries 548 `CRNG` colour-cycling ranges between them.

## The byte-order split

This is the sharpest structural result in this document.

```
loose files (ISO tree)
IFF files 76 : big-endian 76, little-endian 0, neither 0
form types: ILBM x73, CTLG x2, PBM x1

inside the archives
IFF files 158 : big-endian 96, little-endian 41, neither 21
form types: ILBM x93, SCRN x25, SCNR x9, WRLD x9, SHIN x8, SHIP x8,
            PBM x3, THTR x2, WSYS x1
```

IFF is defined big-endian. Every picture on this disc obeys that. Every file
using one of the game's **own** form types — `SCRN`, `SCNR`, `WRLD`, `SHIN`,
`SHIP`, `THTR`, `WSYS` — stores every chunk size in Intel order.

`BASE.SCN` read the standard way declares a FORM of 3,456,827,400 bytes in a
3,031-byte file. Read little-endian: 3,022 bytes of payload + 8 header + 1
archive terminator = 3,031, exactly the file length, and the chunk walk lands on
the last byte. That is the proof, and it holds across all 41.

So the pipeline had two halves. Pictures went through Amiga paint packages —
DPaint, ADPro — and came out correct. The game's own screen, world and shape
definitions were written by a tool that wrote 32-bit sizes in the byte order of
the machine it ran on, and that machine was little-endian.

Combined with `logo.pix` being a PC DeluxePaint PBM, this is direct evidence of a
DOS-side authoring pipeline for an Amiga product — the same question open item 24
tries to answer from timestamps. On this disc the timestamps say nothing (no 1980
epoch at all, [02-filesystem.md](02-filesystem.md)) and the byte order says it
outright. **Byte order is the better probe.**

The 21 "neither" files are entries whose walk misses the file end by more than
the one-byte tolerance; they are not investigated further here and are recorded
in [12-open-questions.md](12-open-questions.md).

### Chunk vocabulary of the game's own forms

```
SHIP   COMP  x498      SCRN   CMPX  x302      SHIP   WEAP  x200
SCRN   AREA   x39      SCRN   LORI   x27      WSYS   WSHD   x22
SCRN   SCHD   x13      SCNR   SNHD    x9      SHIN   SHHD    x8
```

`AREA` chunks are 10 or 12 bytes of coordinates and there are 39 of them across
the 25 `SCRN` files — the clickable regions behind `gs`'s string
`Select Action Area.` `SHIP`'s `COMP` (498) and `WEAP` (200) are the component
and weapon tables of the eight helicopter definitions.

## CDXL video

Three streams, 51,945,914 bytes, **86.9 % of the file bytes on this disc**.

The 32-byte chunk header was read as type, info, `u32` chunk size, two `u32`
counters, then width, height, planes, palette bytes and audio bytes as `u16`.
The check is arithmetic, not trust:

```
chunkSize - 32 - paletteSize - audioSize == planes * height * ceil(width/16)*2
```

| | `cdintro.xl` | `INTRO.XL` | `piratesgold.intro.xl` |
|---|---:|---:|---:|
| bytes | 3,497,550 | 26,830,284 | 21,618,080 |
| chunk size | 19,986 | 29,614 | 24,566 |
| geometry | 300×100 | 304×125 | 200×152 |
| planes | 5 | 6 | 6 |
| palette | 64 B / 32 colours | 32 B / 16 colours | 32 B / 16 colours |
| audio | 890 B/frame | 1,050 B/frame | 790 B/frame |
| video payload | 19,000 | 28,500 | 23,712 |
| planes × h × rowbytes | 19,000 | 28,500 | 23,712 |
| | **EXACT** | **EXACT** | **EXACT** |
| frames | **175** | **906** | **880** |

All three divide by their chunk size with zero remainder, and a walk of every
chunk in all three confirms the size never varies and lands exactly on the file
end. The streams are seekable by multiplication.

Six planes with a sixteen-entry palette is not a broken picture: it is HAM6, and
the startup-sequence confirms it independently. `intro.xl` and
`piratesgold.intro.xl` are passed the `ham` flag; `cdintro.xl` — the only one
with 5 planes and a full 32-colour palette — is not. The header arithmetic and
the shell script agree without either being derived from the other.

The reserved eight bytes at offset 24 are zero in all three. The two `u32`
counters at offsets 6 and 10 are not what the usual field names suggest: across
chunks the first holds the *previous chunk's byte size* (0, then 19986, 19986…)
and the second an incrementing *frame ordinal* (1, 2, 3…).

### Frame rate

The startup-sequence asks for `xlspeed 150`. 150 sectors per second is CD
double speed, 307,200 bytes/s, which is what a CD32 delivers. Dividing:

| | frames/s | duration | implied audio rate |
|---|---:|---:|---:|
| `cdintro.xl` | 15.37 | 11.4 s | 13,680 Hz |
| `INTRO.XL` | 10.37 | 87.3 s | 10,892 Hz |
| `piratesgold.intro.xl` | 12.51 | 70.4 s | 9,879 Hz |

The frame rates and durations follow directly from the chunk arithmetic. The
audio rates are derived from them and are not confirmed by any field on the
disc — three different sample rates in three files from the same production is
possible but not established. Recorded in
[12-open-questions.md](12-open-questions.md).

## Copper lists

`gs2.run` writes `COP1LCH` five times and calls `LoadView` three times. A
scan for stored copper lists returns 205 candidates in a 197 KB file, which is
the signature of a false-positive sweep rather than a finding — the strong hits
decode to nonsense (`BPLCON0 $fe80`, which would be HIRES+HAM+DUALPF+UHRES at
once). No stored copper list is claimed here. The `LoadView` calls and the
`OwnBlitter`/`DisownBlitter` pair say the program hands the display back and
forth with `graphics.library` rather than installing a list of its own from
ROM-free memory.

## Palette

The one-line test is `LoadRGB4` against `LoadRGB32`. This disc answers **both**,
which is a new answer for the series:

| program | LoadRGB4 | LoadRGB32 |
|---|---:|---:|
| `gs` | 4 | 1 |
| `Backdrop` | 1 | 3 |
| `CDGSXL` | 4 | 1 |
| `gs2.run` | 0 | 0 |

Five discs of fourteen called neither. Gunship calls both in three programs and
neither in the fourth. That is consistent with what the files show: the front end
displays 256-colour AGA stills and needs `LoadRGB32`, while the 16-colour
elements and the CDXL palettes fit `LoadRGB4`. The flight engine calls neither
because it writes `COLORxx` itself.

The counts are matched on the `jsr d16(a6)` encoding and assume `a6` is
`GfxBase` at those sites; they are reported as such rather than as verified call
sites.
