# 09 — Hardware: Akiko, the blitter, and where the frame ends

Reproduce with `tools/akiko2.py`, `tools/dffscan.py`, `tools/blitscan.py` and
`tools/chipregs.py`. Results in [`notes/akiko.txt`](../notes/akiko.txt),
[`notes/blitter.txt`](../notes/blitter.txt) and
[`notes/chipregs.txt`](../notes/chipregs.txt).

## Akiko: 0 / 0 / 0 / 0

Scanned with `akiko2.py`, which covers all eight forms of `lea $x.l,An`
(`41f9 43f9 45f9 47f9 49f9 4bf9 4df9 4ff9`) and all eight of
`movea.l #$x,An` (`207c`..`2e7c`), over all eight executables on the disc.

| | Gunship 2000 | series before this |
|---|---:|---|
| `$00B80000` pointer load | **0** | 2 of 14 (Dragonstone, Universe) |
| `$00B80030` I²C / EEPROM | **0** | 1 of 14 (Universe) |
| `$00B80038` / `$00B8003C` C2P | **0** | 0 of 14 |
| `$C0DE0000` | **0** | 0 of 14 |

The prediction written before the scan was that `$00B80000` would be present —
a CD32 flight simulator streaming from disc looked like the second-best Akiko
candidate in the series after Guardian. It was wrong, and the reason is
straightforward: the game reaches the drive through `cd.device`, not through the
chip ([08-audio.md](08-audio.md)), and it saves through `nonvolatile.library`,
not through the I²C port. Universe needed `$B80030` only because it had already
shut down Exec and could not call the library. Gunship never shuts Exec down.

### One `$C0DE0000` hit, and it is a new false-positive class

The raw byte scan reports one `C0 DE 00 00` in `gs2.run` at file offset 0x2a5dc.
It is inside a table of longwords with a stride of 0x10:

```
0002a5c0: 0000 c06e 0000 c07e 0000 c08e 0000 c09e
0002a5d0: 0000 c0ae 0000 c0be 0000 c0ce 0000 c0de
0002a5e0: 0000 c0ee 0000 c0fe ffff ffff 0000 0000
```

The match straddles two entries: the low word `c0de` of one and the high word
`0000` of the next. A stride-16 longword table whose values pass through
`0x0000C0DE` produces the Akiko identification constant exactly once, at an odd
position relative to the entry boundaries.

Add it to the catalogue of `00 B8 00 xx` / Akiko-constant false positives beside
the ProTracker period table (Gloom, HeroQuest II), planar mask data at odd
offsets in a chip hunk (Fire & Ice), and screen coordinates in an object table
(Universe, x=184). The tests that catch it are the ones the checklist already
names: check the alignment, check the hunk, and check whether a table is a table.

The bare `00 B8 00 xx` byte pattern occurs 42 times across the executables.
None of them is a pointer load.

## Custom chip access

```
gs2.run    lea $dff000,aN  (4?f9) : 36     movea.l #$dff000,aN (2?7c) : 0
gs         lea $dff000,aN  (4?f9) : 3      movea.l #$dff000,aN (2?7c) : 0
```

Both forms were scanned, always. The base register is `a5` in 17 of `gs2.run`'s
36 loads, `a0` in 5, `a4` in 5; `a5` is the one held across routines.

The absolute-write histogram needs the Universe correction applied:

```
raw `00 DF F0 xx` in gs2.run: 82 hits
   00 DF F0 00  x36   <- these ARE the 36 base loads themselves
   00 DF F0 96  x13   DMACON
   00 DF F0 02  x12   DMACONR
   00 DF F0 80  x5    COP1LCH
   00 DF F0 9A  x3    INTENA
   00 DF F0 66  x2    BLTDMOD
   00 DF F0 06  x2    VHPOSR
   ... 8 more registers, one hit each
```

36 of the 82 raw hits are the `lea $00dff000,aN` instructions, leaving **46 real
absolute writes**. Everything else goes through `d16(a5)`.

`tools/chipregs.py` scans for the `d16(An)` effective-address encoding directly
rather than walking forward from a base load — the inherited `regscan.py` finds
exactly one access on this program, because the base is loaded in one routine
and used in another and a linear walk cannot follow that. The new scan is
deliberately an upper bound: small displacements collide with immediates, so its
output is useful for *which* registers appear, not for counting them. The
figures quoted in this document come from `blitscan.py`, which matches whole
instruction encodings.

## The blitter

177 exact-encoding blitter writes in `gs2.run`. **Zero in `gs`.**

```
BLTSIZE  x44    BLTDMOD  x31    BLTAMOD  x22    BLTBMOD  x16
BLTCON0  x15    BLTCMOD  x13    BLTCON1  x11    BLTAFWM   x9
BLTADAT   x6    BLTBDAT   x4    BLTALWM   x4    BLTCDAT   x2
```

The three checklist questions, answered:

**Is there a `BLTCON1` write, and does it have FILL bits?** Eleven `BLTCON1`
writes. Three take an immediate and all three are `$0000` — no `FILL_OR`, no
`FILL_XOR`, no `FILL_CARRYIN`, no `BLITREVERSE`, no `LINE`. The other eight take
their value from a register, so fill cannot be *excluded* by this scan; what can
be said is that no fill bit is written as a constant anywhere in the program.
That is the same answer Universe gave.

**What are the BLTSIZE heights and the modulos?** Nine of the 44 `BLTSIZE`
writes are immediate:

```
#$C814   h=800  w=20 words   x2     with BLTAMOD=0 and BLTDMOD=0
#$0542   h=21   w=2  words   x6     with BLTAMOD/BLTDMOD = $009C
#$0502   h=20   w=2  words   x1
```

`#$C814` is the screen. Twenty words is 320 pixels; height 800 is **200 rows ×
4 bitplanes**, blitted as one operation with both modulos zero — that is a
contiguous four-plane 320×200 buffer, 32,000 bytes, all four planes moved in a
single blit. It is the same idiom Guardian uses.

`#$0542` is a 32×21 object. A modulo of `$009C` = 156 gives a row stride of
156+4 = 160 bytes = 320 pixels, so these are blits into that same screen.

**For minterm `$CA`, is USEA on?** Both `$CA` sites read `BLTCON0 #$0FCA`, which
is `USEABCD` — **USEA is on**. That is the ordinary masked bob, as on Banshee,
Fire & Ice and Universe. Guardian's cookie-cut is the same minterm with USEA
*off* and `BLTADAT` loaded outside the loop; this is not that. The other two
immediate `BLTCON0` values are `#$09F0` (`minterm $F0`, `USEAD`) — a straight
A→D copy — and one `#$FFFF`, which is `minterm $FF`, `USEABCD`, ASH 15: a
constant-fill of `$FFFF`.

## Where does the frame end

This is the question the checklist says to ask before asking what shape the
frame is, and on a polygonal game it is the one that decides.

**The frame ends planar.** There is no chunky-to-planar step anywhere on the
disc.

The test: a scan for the C2P merge masks as immediate operands of
`andi.l`/`eori.l`/`ori.l` — `$F0F0F0F0`, `$CCCCCCCC`, `$AAAAAAAA`, `$0F0F0F0F`,
`$33333333`, `$55555555` — returns **zero hits in `gs2.run`**, and zero in every
other executable. The mask bytes do occur as data (320 runs of `CCCCCCCC` inside
`cd32rez`, 318 inside `pirates`) but never as an immediate to a merge
instruction. There is no Akiko C2P port access either, so both routes are
excluded.

What the blitter numbers say instead is that the renderer draws straight into a
four-bitplane 320×200 buffer and the only whole-screen operation is a
planar-to-planar copy of all four planes at once. Sixteen colours, planar in,
planar out.

This is the **eighth planar-in-planar case** in the series, and it is worth
saying why it is not surprising here even though a 3D flight simulator is the
genre where a chunky buffer would be expected: the flight view is 16 colours, and
at four planes the per-pixel cost of writing planar directly is low enough that
the conversion buys nothing. The front end, which does use 256 colours, is
eight-plane IFF displayed through `graphics.library` and never touches the
blitter at all.

## OS status

`gs2.run` calls `graphics/LoadView` twice, brackets nine regions with
`exec/Disable`/`Enable`, and makes one call each at displacements -456 and -462,
which on a program holding `GfxBase` in `a6` are `OwnBlitter`/`DisownBlitter`.
It opens libraries rather than patching over them. AmigaDOS is alive for the
whole run — the startup-sequence depends on it, since it regains control after
the game exits in order to kill the backdrop task by name.

This matters for [10-band.md](10-band.md), where it falsifies a standing
hypothesis.
