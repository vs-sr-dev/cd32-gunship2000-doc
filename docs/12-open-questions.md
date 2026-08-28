# 12 — Open questions

Everything here is unresolved and has a measurement attached. An honest question
beats a plausible answer.

---

## 1. What is the 100 MiB hole for?

`LBA 25..51224`, 104,857,600 bytes, all zero, sha1
`2c2ceccb5ec5574f791d45b63c940cff20550f9a`. Exactly 100 × 1024 × 1024. It is
inside the declared volume, so ISOCD counted it deliberately: `volume space size`
is 80,735, which includes it.

A round binary number to the byte is a *reservation*. Nothing on the disc says
what for. Candidates not distinguishable from here: a fixed-size staging
partition the master was built from; a placeholder for content that was cut; a
deliberate outer-edge push to keep the files on faster tracks (but the files sit
at LBA 51,225–80,502, which is the *outer* part of a 45 %-full disc, so this
would be backwards); an artefact of the tool that assembled the source tree.

This is the fourth gap-before-files in the series (Prey CD32 6,000; Microcosm
15,000; HeroQuest II 24,272) and the first that is a round number. **Measurement
that would settle it:** any other ISOCD 1.04 master with a round-number gap, or
any Gunship 2000 CD32 pressing with a different one.

## 2. The 232, and the correlation that is now five for five

| disc | preparer | unclaimed tail | overrun |
|---|---|---:|---:|
| Liberation | D J Pocock | 232 | 103 |
| Banshee | D J Pocock | 232 | 86 |
| Fire & Ice | D J Pocock | 232 | 87 |
| Universe | D J Pocock | 232 | 80 |
| **Gunship 2000** | **D J Pocock** | **232** | **78** |
| the other ten | nine other names | 32 | 34–106 |

Five studios, five publishers, **two countries** — Gunship adds a US label to
four British ones — one name, one number. The prediction was written before the
filesystem was parsed and confirmed exactly.

232 − 32 = 200 sectors = 409,600 bytes still corresponds to nothing. Already
excluded and re-excluded on this disc: volume size (80,735, unremarkable), ISOCD
version (1.04, same as all fifteen), image overrun (78 here, which *widens* the
Pocock range to 78–103 and leaves Dragonstone's 106 outside it — so the
separation is still not clean, exactly as Universe established), audio track
count (5 here; the Pocock group now spans 2–23 and the non-Pocock group 0–28),
studio, publisher, field padding, duplicate PVD, the `.TM` block (identical),
directory record order, `;1` suffixes, root extent.

**The file-level lead from Universe is dead.** Universe's finding was that
`C/FreeAnim` and `C/noopenwb` are byte-identical on Universe and Liberation, the
only two Pocock masters with a `c/`, suggesting a build kit shared across
studios. Two independent refutations on this disc:

* **Dragonstone carries the same pair, byte-identical**, and Dragonstone's
  preparer is `Sajjad Majid`. The pair crosses the Pocock boundary.
* **Gunship 2000, the fifth Pocock master, has a `c/` and neither file is in
  it.**

```
FreeAnim  3492 bytes  sha1 449c6100...   Liberation, Universe, Dragonstone
noopenwb   204 bytes  sha1 e0538ef1...   Liberation, Universe, Dragonstone
```

What Gunship's `c/` shares instead is stock Commodore material:

```
Assign    3220  b5b7edb6   Gunship, Liberation, Banshee
execute   4432  ef1e6f6d   Gunship, Banshee
setpatch 13200  00d74a35   Gunship, Universe, Banshee, Fire & Ice, Dragonstone
```

`SetPatch` 40.14 at 13,200 bytes is on five discs including a non-Pocock one, so
it says nothing beyond "everyone copied the same Workbench 3.1 `C:`". The
correlation therefore remains a **field-level** one with no mechanism attached.

**Measurement that would settle it:** a sixth Pocock master. A 232 under a
different preparer name still kills it.

## 3. Open item 24 — the 1980 epoch, and a better probe than timestamps

The hypothesis is that the FAT-day-zero timestamps on Guardian (one file) and
Fire & Ice (ten files over 64 days) come from a staging tree on a PC with an
unset clock, ISOCD being a DOS program. A DOS-first publisher was the best
available test.

**MicroProse produces zero.** No 1980 file, no 1978 file, 148 dated records over
24 calendar days, all of them coherent. Prediction wrong.

But the same disc answers the underlying question a different way, and better:

```
loose files      IFF 76 : big-endian 76, little-endian 0
inside archives  IFF 158: big-endian 96, little-endian 41
```

Every picture is correct big-endian IFF. Every file using one of the game's own
form types — `SCRN`, `SCNR`, `WRLD`, `SHIN`, `SHIP`, `THTR`, `WSYS` — stores
every chunk size **little-endian**. And `logo.pix` is a `PBM ` with a `TINY`
chunk, which is PC DeluxePaint's chunky format.

So there was a DOS side to the pipeline, and it left its byte order in the data
rather than its clock in the directory. **Byte order is the better probe and
should be added to the checklist as one.** Whether that generalises — whether
Guardian's and Fire & Ice's 1980 files are also accompanied by little-endian
data — is untested and cheap to test.

## 4. What are the 21 "neither" IFF files?

Of 158 IFF files inside the archives, 96 walk cleanly big-endian, 41 cleanly
little-endian, and **21 walk cleanly neither way** — the chunk walk misses the
file end by more than the one-byte terminator tolerance. Not investigated. They
may be a third layout, a nested form, or a tolerance that is simply too tight.

## 5. What is word 0 of an `.SBN`?

Words 1–3 of every model header are section offsets: 163 of 163 satisfy
`w1 < w2 < w3 <= filesize`. Word 0 is not explained. Its low byte is only ever
0 (99 files) or 1 (64 files). Its high byte increments in runs across the archive
order but is not monotonic over the whole set, and values as high as 0x8B00 and
0x7D01 occur. An object ID plus a one-bit flag is the obvious guess and is not
established.

## 6. Why are `T72.SBN` and `T62.SBN` stored twice?

`object.cat` has 165 entries and 163 distinct names. `T72.SBN` and `T62.SBN` each
appear twice, and in each case the two entries point at **different offsets
holding identical bytes** — the archive covers 100.0 % of its payload with no
gaps, so they cannot be aliases of one region. Two Soviet tanks, two copies each,
2,882 wasted bytes. Whether the game's lookup takes the first or the last is not
established.

## 7. What sample rate is the CDXL audio?

The chunk geometry is exact and the frame counts are exact. The frame rate
follows from `xlspeed 150` (150 sectors/s = 307,200 B/s):

| | frames/s | duration | implied audio |
|---|---:|---:|---:|
| `cdintro.xl` | 15.37 | 11.4 s | 13,680 Hz |
| `INTRO.XL` | 10.37 | 87.3 s | 10,892 Hz |
| `piratesgold.intro.xl` | 12.51 | 70.4 s | 9,879 Hz |

Three different rates from one production is possible but odd, and nothing on the
disc states any of them. Either `xlspeed` is not sectors per second, or the audio
is not one channel at a fixed rate, or the three were simply authored at
different rates. Reading `CDGSXL`'s argument parser would settle it and was not
done.

## 8. How many of the five audio tracks does the game reach?

Five tracks, 15:35. `gs` opens `cd.device` (three `OpenDevice` calls against
three device-name strings), so the OS route is established, but no track-number
table was located. The two places on the disc where a track number appears in
plain text are `pirates.demo` and the commented line in `s/startup-sequence`,
both passing `2` under a stale comment saying "replace 5". With only five tracks
this is answerable and was not answered.

## 9. Slack tracks nothing yet

| disc | slack | AmigaDOS alive? |
|---|---:|---|
| **Gunship 2000** | **0.004 %** | **yes** |
| Fire & Ice | 0.3 % | no |
| Universe | 0.5 % | no |
| Banshee | 3.9 % | — |
| Dragonstone | 9.1 % | yes |

Universe weakened "studio habit" (Core Design at both extremes, 18:1). Gunship
falsifies "OS alive vs machine seized": it keeps AmigaDOS alive throughout and
has the tightest slack of the five, two orders of magnitude below Dragonstone.
No replacement hypothesis is offered. The plainest remaining candidate is that it
tracks the asset build tool's padding behaviour and nothing about the game.

## 10. Is the `gs_dsk%d:orig` check still reachable?

`gs` carries the format string `gs_dsk%d:orig` and no file named `orig` exists
anywhere on the CD. Whether the code path that opens it is still called, and what
it does when the open fails, was not traced. This is a copy-protection remnant
and the disc plainly works, so either the path is dead or its failure is benign.

## 11. Where is `freeanim.library`?

`gs` and `CDGSXL` both name `freeanim.library`. It is not in `/libs/`, which
holds only `diskfont.library`, `iffparse.library` and `locale.library`, and it is
not anywhere else on the disc. Note the connection: `c/FreeAnim` on Liberation,
Universe and Dragonstone is the command that frees this library's resources, and
Gunship uses the library while shipping neither the library nor the command.
Presumably it is opened optionally and its absence tolerated. Not traced.

## 12. Why is the PVD older than four of its own files?

```
PVD creation        1994-04-19 13:46:56
/gunship 2000       1994-04-19 14:06:08
/gs                 1994-04-19 14:06:30
/gs2.run            1994-04-19 14:06:48
/roster.dat         1994-04-19 14:06:50
```

Nineteen minutes twelve seconds of inversion. On every other disc in the series
the PVD is later than everything it indexes — on Universe by 2h17m45s. Either
ISOCD stamps the PVD when it starts rather than when it finishes, or the source
tree was written to during the build. The `/GS2000/` directory at 13:38:54 and
the root at 13:38:40 are earlier than the PVD, which is consistent with either.
**Measurement that would settle it:** the PVD-to-newest-file delta on the other
fourteen discs, computed with sign. It has only ever been reported as a positive
gap.

## 13. What is the 10-entry `bra.w` table in `gs`?

The dispatch scan (`tools/dispatch.py`, inherited from `cd32-universe-doc`)
reports **zero** dispatch tables of the Universe shape — no
`lea $12(pc),a6 / neg.b d0 / subq / andi / asl #2 / jsr (a6,d0.w)` preamble
anywhere in `gs`, `gs2.run`, `cd32rez` or `pirates`. Open item 25 gets a clean
negative from this disc: **a mission-based simulator does not need a bytecode
interpreter**, and this one does not have one.

The scan's second pass, which finds runs of consecutive `bra.w` without
reference to whatever jumps into them, finds exactly one on the whole disc:

```
table 00001122   10 entries   10 distinct handlers
```

Ten branches at `gs` file offset 0x1122. The count is the length of the run, as
always — it is not stored anywhere. Whether it is a menu action table, a
state machine or a compiler-generated `switch` was not traced. It is too small
and too isolated to be an interpreter.

---

## Predictions written before measurement, with outcomes

| # | prediction | written before | outcome |
|---|---|---|---|
| P1 | preparer `D J Pocock` ⇒ 232-sector unclaimed tail; a fifth name ⇒ 32 | parsing the filesystem | **RIGHT** — `D J Pocock`, 232 sectors, all zero |
| P2 | if a `c/` exists, `FreeAnim` and `noopenwb` are byte-identical to Liberation's and Universe's | hashing `c/` | **WRONG** — a `c/` exists with eleven files and neither is among them; and Dragonstone (non-Pocock) has both, killing the lead from the other side too |
| P3a | `$00B80000` pointer load present | any scan | **WRONG** — 0. It reaches the drive via `cd.device` |
| P3b | `$00B80030` I²C absent | any scan | **RIGHT** — 0; it saves via `nonvolatile.library` |
| P3c | `$00B80038`/`$3C` C2P absent | any scan | **RIGHT** — 0 |
| P3d | `$C0DE0000` absent | any scan | **RIGHT** as a pointer load — the single byte-pattern hit is a stride-16 table straddle, a new false-positive class |
| P4 | the band survives; the game is under 13.3 MB despite a 157.84 MB data track | unpacking | **RIGHT** — 6.62 MiB on disc, 7.98 MiB resident |
| P5 | compression present; the rule goes to [10 of 10] | the magic scan | **RIGHT** — 542 validated RNC2 streams |
| P6 | the publisher field names MicroProse, making this the first US client of ISOCD in the series | reading the PVD | **RIGHT** — `Microprose` |
| P7 | 1980-epoch files present and more numerous than Guardian's one or Fire & Ice's ten, because MicroProse is DOS-first | the timestamp sort | **WRONG** — zero 1980 files, zero 1978 files. The DOS pipeline shows up in byte order instead |
| P8 | a script/dispatch VM present, because a sim has missions and campaigns | the dispatch scan | **WRONG** — zero dispatch tables of the Universe shape in any of the four programs. The one `bra.w` run on the disc is 10 entries at `gs`+0x1122 with 10 distinct handlers, and nothing dispatches into it by complemented index. The front end is data-driven by little-endian IFF `SCRN` files, not by bytecode |
| P9 | chunky-to-planar conversion present, because a 3D flight sim renders to a chunky buffer | the mask scan | **WRONG** — zero C2P mask immediates, zero Akiko C2P. The frame ends planar: 4 planes, one BLTSIZE `$C814` |
| P10 | substantial text, over 100 KB resident | the text census | **RIGHT on the number, wrong on the reading** — 104,838 bytes, but 47.6 % of it belongs to the bundled demo. The game's own prose is 54,885 bytes, 0.65 % of its resident image |
| P11 | the `.TM` block matches the twelve other CD32-era discs | following the pointer | **RIGHT** — all three SHA-1s match |
| P12 | no gap before the files, no giant container, a normal tree | the sector map | **WRONG** — a 100 MiB zero hole, 63.4 % of the volume |

**Seven right, six wrong, one split.** The wrong ones are the useful ones. P9 was
wrong for a reason worth keeping: the genre argument ("a flight sim renders
chunky") beat the arithmetic argument (four planes at 320×200 is cheap to write
directly), and the arithmetic was right. P8 was wrong the same way — a
simulator's mission structure turned out to live in data files, not in an
interpreter. P12 was wrong because the disc's headline number, 157.84 MB, was
63.4 % nothing.
