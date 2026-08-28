# 08 — Audio

Reproduce with `tools/cueaudio.py`. Results in
[`notes/audio-tracks.txt`](../notes/audio-tracks.txt).

## Red Book

Five audio tracks, 70,136 frames, 15:35.11, all 44,100 Hz 16-bit stereo, all
five distinct by SHA-1.

```
tr  format            bytes   frames      time    sha1
2   44100/2ch/16b   23011968     9784   2:10.34   0e3aa1eed7ac
3   44100/2ch/16b   42578256    18103   4:01.28   77094b655704
4   44100/2ch/16b   42881664    18232   4:03.07   ea79992af587
5   44100/2ch/16b   41301120    17560   3:54.10   be5cc7ceca19
6   44100/2ch/16b   15186864     6457   1:26.07   ace2221df855
```

Audio is 46.5 % of the sectors this disc uses. Every one of the five is a whole
number of frames with no partial trailing frame.

The one-frame pregap declared on tracks 4, 5 and 6, and the fact that it
corresponds to nothing in the samples, is measured in
[01-disc-image.md](01-disc-image.md).

## How the game reaches the tracks

The TOC column in the shared checklist had three answers before this disc:
Guardian reads the disc TOC and filters on the CONTROL bits; Banshee and
Fire & Ice do not read it and name tracks as constants; Universe bypasses the OS
entirely and builds the command inside Akiko's register block.

Gunship 2000 gives a **fourth**: it uses `cd.device` through the OS.

`gs` carries exactly three device-name strings — `cd.device`, `audio.device`
and `input.device` — and makes exactly **three** `exec/OpenDevice` calls
(`4E AE FE 44`). `gs2.run` makes none. `gs` is therefore the program that plays
music: it is the front end, it opens `cd.device` through the OS, and it makes
zero blitter writes. There is no Akiko access anywhere on the disc
([09-hardware.md](09-hardware.md)), so the Universe route is excluded by
measurement rather than assumed.

The three-strings/three-calls agreement is the check. An earlier pass of this
document quoted `OpenDevice` counts taken from a displacement table that had
exec and graphics LVOs mixed together — `-456` is `exec/DoIO` *and*
`graphics/OwnBlitter`, `-462` is `exec/SendIO` *and* `graphics/DisownBlitter`,
and `-222` is `graphics/LoadView`, not an exec entry at all.
`tools/lvoscan.py` prints every candidate per displacement for that reason.

The checklist's warning about `io_Command` is worth restating with this disc's
numbers rather than taken on trust. A naive `moveq #34,dN` scan (`70 22`) gives
**28 hits in `gs`**, 3 in `CDGSXL`, 2 in `Backdrop` and 1 in `gs2.run` — 34 in
total against 3 real `OpenDevice` calls. On Fire & Ice sixty such hits were all
false; here the same scan would be wrong by an order of magnitude in the same
direction. The count that is defensible is the `OpenDevice` count, because it
matches a whole instruction encoding and agrees with the device-name strings.

**How many of the five tracks the game can reach is not established here.** The
number is small enough that the question is answerable and it was not answered:
no track-number table was located in `gs`. What the disc does say is that the
track numbers are passed around as small integers — `pirates.demo` and the
commented line in `s/startup-sequence` both take a CD music track number as a
command-line argument, and both were set to `2`, with a stale comment saying
"replace 5". So at least the demo path parameterises the track rather than
hard-coding it. Recorded in [12-open-questions.md](12-open-questions.md).

## Sampled audio in the filesystem

Two raw sample blobs, no IFF wrapper, no module:

| file | bytes | date |
|---|---:|---|
| `fe_snd.bin` | 62,836 | 1993-12-20 11:52:03 |
| `flt_snd.bin` | 183,528 | 1994-03-26 14:06:11 |

`fe` is the front end, `flt` the flight code, matching the two halves of the
game and the floppy layout (`gs_dsk3:` holds `flt_snd.bin`). Together 246,364
bytes — 3.5 % of the game's on-disc bytes.

`fe_snd.bin` does not begin with sample data. Its first bytes are
`48 E7 F1 FE 61 00 02 9A 4C DF 7F 8F 4E 75` — `movem.l d0-d3/d7/a0-a6,-(sp)`,
`bsr`, `movem.l (sp)+,...`, `rts`. It is a code stub followed by its data, not a
bare blob, and the census's "prose" hit inside it (112 bytes, 4 runs) is
consistent with a small dispatcher carrying names.

### No modules, but fifteen IFF samples where a census cannot see them

A scan for `M.K.`, `M!K!`, `FLT4`, `MMD0`, `MMD1`, `THX` and `SMUS` returns
nothing real: the only hits are two three-byte `THX` sequences inside
`piratesgold.intro.xl`, neither preceded by a `FORM`, both coincidences in video
data. **No tracker module of any kind is on this disc.**

`8SVX` is a different matter. There are **fifteen IFF 8SVX samples embedded
inside the `pirates` executable**, every one preceded by a correct `FORM` header
with a plausible chunk size:

```
0x03bac8  FORM 0x000011e4 8SVX     0x043e82  FORM 0x00001b8a 8SVX
0x03ccb4  FORM 0x000008bc 8SVX     0x045a14  FORM 0x00002168 8SVX
0x03d578  FORM 0x00000668 8SVX     0x047b84  FORM 0x0000268c 8SVX
0x03dbe8  FORM 0x000005c0 8SVX     0x04a218  FORM 0x00002eb8 8SVX
0x03e1b0  FORM 0x00002d80 8SVX     0x04d0d8  FORM 0x00001720 8SVX
0x040f38  FORM 0x0000243e 8SVX     0x04e800  FORM 0x00000c12 8SVX
0x04337e  FORM 0x00000afc 8SVX     0x04f41a  FORM 0x0000107a 8SVX
                                   0x05049c  FORM 0x00001988 8SVX
```

All fifteen sit inside hunk 11, a 91,584-byte **chip** DATA hunk spanning file
0x3b864 to 0x51e64 — chip memory because Paula has to reach them. A file
census sees one 383 KB executable; the samples are only visible to a magic scan
that reads inside it. They belong to the Pirates! Gold demo, so this is fifteen
more assets on the reachable-by-nothing pile
([11-leftovers.md](11-leftovers.md)).

Of the four places the checklist says to look, this disc uses three: Red Book
tracks, raw PCM blobs, and IFF 8SVX inside an executable — plus the CDXL audio
interleaved in the video streams. No modules.

## CDXL audio

Each CDXL frame carries a fixed audio payload alongside its bitplanes: 890, 1,050
and 790 bytes per frame for the three streams. Over the whole of the three files
that is 155,750 + 951,300 + 695,200 = **1,802,250 bytes of interleaved audio**,
which is 7.3 times as much sampled sound as the two `.bin` blobs together.

The implied sample rates that fall out of the `xlspeed 150` arithmetic are
13,680 / 10,892 / 9,879 Hz. Nothing on the disc states them and the three
differing is not explained; see [07-graphics.md](07-graphics.md) and
[12-open-questions.md](12-open-questions.md).

## The audio filter

`c/filteron` and `c/filteroff` are 48-byte hunk executables containing four
bytes of code each:

```
filteroff   08 B9 00 01 00 BF E0 01    bset #1,$bfe001
filteron    08 F9 00 01 00 BF E0 01    bclr #1,$bfe001
```

They are not the only code on the disc that touches `$bfe001`. The byte sequence
`00 BF E0 01` occurs 34 times across eleven files:

```
gs2.run x6   Backdrop x5   gs x4   pirates x4   pirates_german x4
CDGSXL x3    c/cdgsxl x3   fe_snd.bin x2   INTRO.XL x1
c/filteron x1   c/filteroff x1
```

Those are raw byte occurrences, not verified instructions — the hit inside
`INTRO.XL` is a coincidence in video data, and the two inside `fe_snd.bin` are
unverified. What is certain is the two 48-byte programs, because each is four
bytes of code and an `rts` with nothing else in it to be wrong about. The
startup-sequence brackets the first video with them: filter off for
`cdintro.xl`, back on afterwards. The second video in the attract loop is not
bracketed, which is either an oversight or deliberate; the disc does not say.
