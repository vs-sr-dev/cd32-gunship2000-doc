# 03 — The boot chain, and the floppy release the CD describes

Reproduce with `tools/strdump.py`.

## `s/startup-sequence`, in full

613 bytes, dated 1994-04-14 13:25:48. Reproduced complete because every line of
it is load-bearing:

```
c:setpatch quiet
c:assign ENV: ram:

c:filteroff
c:cdgsxl cdintro.xl xlspeed 150 blit multipal nopointer patchopenwb
c:filteron
run >nil: backdrop
wait 5
c:cdgsxl intro.xl xlspeed 150 fireabort ham multipal blit nopointer patchopenwb

stack 16384
"Gunship 2000"
avail >nil: flush
status >ram:break.tmp com=backdrop
break <ram:break.tmp >nil: ?
lab loop
c:cdgsxl cdintro.xl xlspeed 150 blit multipal nopointer patchopenwb
c:cdgsxl piratesgold.intro.xl xlspeed 150 fireabort ham multipal blit back frame.lbm x 61 y 25 boxit patchopenwb nopointer
;pirates 2	; replace 5 with the cd music track number
skip back loop
```

The disc boots into AmigaDOS and stays there. SetPatch 40.14 (Workbench 3.1) is
run, `ENV:` is pointed at RAM, the audio filter is toggled around the first
video, a backdrop task is started, the intro plays, and `"Gunship 2000"` — the
launcher, quoted because of the space — is run with a 16 KB stack. When it
returns, the backdrop task is found by name via `status com=backdrop` and killed
with `break`, and the script drops into an infinite attract loop that alternates
the two short videos.

`c:filteroff` and `c:filteron` are 48-byte executables that are four bytes of
code each: `bset #1,$bfe001` and `bclr #1,$bfe001` — see [08-audio.md](08-audio.md)
for the other eleven files that contain the same byte sequence.

The `ham` flag on `intro.xl` and `piratesgold.intro.xl` and its absence on
`cdintro.xl` matches the CDXL headers exactly — see
[07-graphics.md](07-graphics.md).

The last two lines before `skip back loop` are discussed in
[11-leftovers.md](11-leftovers.md).

## The four programs

| file | bytes | hunks | relocations | role |
|---|---:|---:|---:|---|
| `gunship 2000` | 3,532 | 3 | 119 | launcher: assigns volumes, opens the screen, chains |
| `gs` | 218,636 | 30+ | — | front end: roster, briefing, menus, CD audio, saves |
| `gs2.run` | 197,532 | 5 | 6,595 | flight engine: takes the display, drives the blitter |
| `cd32rez` | 641,768 | 1 | 15 | resource archive with a hunk header (see [04](04-compression.md)) |

`Backdrop` (43,444), `CDGSXL` / `c/cdgsxl` (34,776, identical) and the eleven
stock commands in `c/` are supporting programs, not the game.

The split is visible in what they touch. `gs` names `diskfont`, `iffparse`,
`locale`, `intuition`, `graphics`, `dos`, `lowlevel`, `freeanim` and
`nonvolatile.library` plus `audio.device`, `cd.device` and `input.device`, and
makes **zero** blitter writes. `gs2.run` names `dos`, `graphics`, `intuition`,
`lowlevel` and `gameport.device`, and makes 177 blitter writes.

Library-call counts, by `jsr d16(a6)` displacement
([`notes/lvo.txt`](../notes/lvo.txt)). A displacement does not say which base is
in `a6`, and two of these are genuinely ambiguous, so both candidates are given:

| displacement | `gs` | `gs2.run` | meaning |
|---:|---:|---:|---|
| -552 | 8 | 1 | `exec/OpenLibrary` |
| -408 | 2 | 3 | `exec/OldOpenLibrary` |
| -444 | **3** | 0 | `exec/OpenDevice` |
| -456 | 4 | 1 | `exec/DoIO` **or** `graphics/OwnBlitter` |
| -462 | 5 | 1 | `exec/SendIO` **or** `graphics/DisownBlitter` |
| -222 | 0 | 2 | `graphics/LoadView` |
| -120 / -126 | 0 | 9 / 9 | `exec/Disable` / `exec/Enable` |
| -192 | 4 | 0 | `graphics/LoadRGB4` |
| -882 | 1 | 0 | `graphics/LoadRGB32` |

Three `OpenDevice` calls in `gs` against three device-name strings in `gs`; none
in `gs2.run`, whose `gameport.device` string is not opened at any `4E AE FE 44`
site. `gs2.run` takes the display with `LoadView` and brackets nine critical
sections with `Disable`/`Enable`, but never calls `Forbid`, `Permit` or
`AllocMem` through `a6`. It is a cooperative takeover: the OS stays alive
throughout, which matters for [10-band.md](10-band.md).

The launcher's error strings name the two halves:

```
Error while loading flight code !
Error while loading frontend !
```

### A scanning trap worth recording

`Backdrop` and `CDGSXL` appear to name libraries called `udos.library`,
`uutility.library` and `ufreeanim.library`. They do not. `4E 75` is `rts`, and
its ASCII is `Nu`; a printable-run scan glues the `u` onto the string that
follows the return. The real names are `dos.library`, `utility.library` and
`freeanim.library`. Any run that begins with `u` immediately after a routine
ends should be checked against the bytes before it is quoted.

## The floppy release, read off the CD

The compression rule in the shared checklist asks whether a disc has a floppy
ancestor before it asks whether it compresses. On this disc the ancestor is not
inferred — the loader describes it.

`gunship 2000` at 0x969 carries an AmigaDOS assign table:

```
gs_dsk1  gs_dsk2  gs_dsk3  gs_dsk4  fonts  gs_dsk1:fonts
gs_dsk1:gs   gs_dsk1:gs2.run
```

Four volume names for a four-floppy set, and `FONTS:` assigned to
`gs_dsk1:fonts`. `gs` then opens files by volume:

```
gs_dsk2:gs2frt.cat    gs_dsk2:gs2frt.dat
gs_dsk4:gs2end.cat    gs_dsk4:gs2end.dat
gs_dsk3:%s            (flt_snd.bin)
gs_dsk%d:%s           (fe_snd.bin)
```

So the original layout was: disk 1 the programs and fonts, disk 2 the front end,
disk 3 the flight sounds, disk 4 the endgame. On the CD all four names are
assigned to the same place.

Three strings finish the picture:

```
gs_dsk%d:%d
Insert GS2000 disk %d\n
Insert GS2000 disk 4
gs_dsk%d:orig
```

`gs_dsk%d:%d` is why four one-byte files named `1`, `2`, `3` and `4` sit in the
root of a CD. Each contains a single ASCII byte equal to its own name. They are
the disk-identity probes: the game builds `gs_dsk2:2` and opens it to decide
whether the right floppy is in the drive. On the CD all four are present, so the
check always passes and `Insert GS2000 disk %d` can never fire. It is still
compiled in, along with a hard-coded `Insert GS2000 disk 4`.

`gs_dsk%d:orig` is an original-disk check, and **there is no file named `orig`
anywhere on the CD.** Whether the code path that opens it is still reachable is
not established here; what is established is that the name it looks for is not
on the disc.

Two more strings from the launcher belong to a machine that has a desktop:

```
Cannot close the Workbench!
Please close all applications, screens, windows and CLIs.
Install Gunship 2000
```

None of that can happen on a CD32, which has no Workbench to close, no other
applications and nothing to install to.

This is the clearest floppy ancestor in the series so far. On Universe it took a
save system, a keymap and two filenames to establish; here the loader says it in
plain text, with the disk numbers.
