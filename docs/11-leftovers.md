# 11 — Leftovers, placeholders and things that cannot run

Everything here is on a retail pressing.

## 1. A complete second game, and one commented-out line

`pirates.demo` is 386 bytes and it is a full alternative AmigaDOS boot script:

```
;c:setpatch quiet
c:filteroff
c:cdgsxl cdintro.xl xlspeed 150 blit multipal nopointer patchopenwb
c:filteron
c:cdgsxl piratesgold.intro.xl xlspeed 150 fireabort ham multipal blit back frame.lbm x 61 y 25 boxit patchopenwb nopointer
stack 16384
getlang
if warn
	pirates_german 2 ; replace 5 with the cd music track number
else
	pirates 2	; replace 5 with the cd music track number
endif
```

This boots a playable Pirates! Gold demo, in English or German depending on the
console's front-panel language setting. It is not the disc's startup-sequence.
`s/startup-sequence` is, and the one line in it that would have launched the
demo is commented out:

```
;pirates 2	; replace 5 with the cd music track number
```

Note the state that line is in. The comment to the right is a template
instruction to a human — *replace 5 with the cd music track number* — and
someone did replace it, with `2`, without updating the note. Then the whole line
was commented out. The identical stale comment appears twice in `pirates.demo`.

What is therefore present and unreachable:

| file | bytes | |
|---|---:|---|
| `pirates` | 383,568 | the English demo executable |
| `pirates_german` | 383,724 | the German demo executable |
| `Pirates.font` | 2,464 | a self-contained disk font |
| `pirates.demo` | 386 | the boot script |
| `c/getlang` | 104 | the language probe |
| — 15 IFF 8SVX samples | inside `pirates` | [08-audio.md](08-audio.md) |
| — 8 RNC2 streams | inside `pirates` | 198,912 bytes unpacked |

770,246 bytes on disc, 1,168,070 resident. The 21,618,080-byte
`piratesgold.intro.xl` is *not* on this list: the attract loop plays it, and `gs`
carries the string

```
Press RED button to view Pirates! Gold intro, any other button to continue
```

so the video is reachable from inside the game. It is the playable part that is
switched off. 13.1 % of this disc is a video advertising a demo the disc will not
launch.

### `getlang`, decoded

104 bytes, one CODE hunk of 17 longwords:

```
43fa 0030      lea      $30(pc),a1        ; "lowlevel.library"
7000           moveq    #0,d0
2c78 0004      movea.l  $4.w,a6           ; ExecBase
4eae fdd8      jsr      -552(a6)          ; OpenLibrary
2c40           movea.l  d0,a6
7000           moveq    #0,d0
4eae ffdc      jsr      -36(a6)           ; lowlevel/GetLanguageSelection
2f00           move.l   d0,-(sp)
224e           movea.l  a6,a1
2c78 0004      movea.l  $4.w,a6
4eae fe62      jsr      -414(a6)          ; CloseLibrary
201f           move.l   (sp)+,d0
b07c 0003      cmp.w    #3,d0
6604           bne.s    +4
7007           moveq    #7,d0             ; RETURN_WARN
4e75           rts
7000           moveq    #0,d0             ; RETURN_OK
4e75           rts
```

It reads the CD32's front-panel language setting and returns AmigaDOS
`RETURN_WARN` (7) if it is 3 and `RETURN_OK` (0) otherwise, which is exactly what
`if warn` in `pirates.demo` tests. A 104-byte program written for one purpose,
called by one script, and that script is not the one that runs.

### The two demo builds differ only in the strings

`pirates` and `pirates_german` are byte-identical for their first 79 bytes and
diverge inside the hunk size table, at the declared length of hunk 14
(31,824 vs 31,868 bytes). Same 15 hunks, same kinds, same memory flags, same
eight packed streams with identical unpacked SHA-1s, 2,346 vs 2,374 relocations.
Hunk 14 is the string table:

```
English                    German
apprentice                 vielversprechende
journeyman                 Abenteurer
adventurer                 Schaluppe
swashbuckler               Fracht Fluyt
Cargo fluyt                Handelsschiff
Merchantman                Kriegsgaleone
War galleon                Schnelle Galeone
Fast galleon               Frankreich
```

This is the clean case the checklist's open item 23 asks about — two builds of
one program differing in one thing — and it is worth contrasting with Fire & Ice,
where two whole executables differed by 23 scanlines of copper list and a string
but diverged after 154 bytes for pure address arithmetic. Here the divergence
point is *in the size table*, so a byte-level diff correctly reports "differs
from byte 79" and a content-level diff correctly reports "one hunk".

Both builds carry the placeholder

```
Unint String!
```

— an uninitialised-string marker shipped in a retail localisation.

## 2. `roster.dat` says `ERASE ME`

1,680 bytes, and the **last file written to the master**, at 1994-04-19 14:06:50,
two seconds after `gs2.run`:

```
00000000: 4552 4153 4520 4d45 0000 0000 0000 0000  ERASE ME........
00000030: 0000 0000 5448 4520 4552 4153 4142 4c45  ....THE ERASABLE
00000040: 5300 0000 0000 0000 0000 0000 0000 0000  S...............
00000050: 0000 000f 0000 0400 0000 0000 0000 0000  ................
```

A saved pilot roster, with the squadron named `ERASE ME` and the unit named
`THE ERASABLES`. Somebody made a scratch save while testing, called it what it
was so it would be obvious, and it went onto the master anyway — as the very last
file, in the same 42-second window as the three game programs. It also holds the
largest single block of buffer slack on the disc (245 trailing zeros, 14.6 % of
the file, [10-band.md](10-band.md)).

## 3. `gsfnt9.font` points at a directory that does not exist

Seven font descriptors in `/fonts/`, seven font data files in `/fonts/gs2000/`,
and they do not line up:

```
gsfnt1.font  -> gs2000/1    ysize  7  flags 0xe2   target exists: True
gsfnt2.font  -> gs2000/2    ysize  8  flags 0xe2   target exists: True
gsfnt3.font  -> gs2000/3    ysize  7  flags 0xe2   target exists: True
gsfnt4.font  -> gs2000/4    ysize  8  flags 0xe2   target exists: True
gsfnt5.font  -> gs2000/5    ysize  9  flags 0xe2   target exists: True
gsfnt6.font  -> gs2000/6    ysize  9  flags 0xe2   target exists: True
gsfnt9.font  -> gsfnt9/11   ysize 11  flags 0x40   target exists: FALSE
```

There is no `/fonts/gsfnt9/` directory on the disc. The size-11 font the
descriptor wants is sitting in `/fonts/gs2000/11`, 3,192 bytes, with nothing
pointing at it. So the disc carries one dangling descriptor and one orphaned font
at the same time, and they are two halves of the same font.

The flags byte gives it away: the six working descriptors all read `0xe2` and the
broken one reads `0x40`. It was made by a different tool or at a different time,
and the path inside it was never fixed up.

## 4. The floppy machinery, still wired in

Covered in full in [03-boot-chain.md](03-boot-chain.md); listed here because it
is the same kind of thing.

* Four AmigaDOS volumes `gs_dsk1`–`gs_dsk4` assigned on a single-volume CD.
* Four one-byte files `/1 /2 /3 /4` in the root, each containing its own name as
  ASCII — the disk-identity probes for `gs_dsk%d:%d`.
* `Insert GS2000 disk %d\n` and a hard-coded `Insert GS2000 disk 4`, on a console
  with no disk to insert.
* `gs_dsk%d:orig`, an original-disk check whose target file **is not on the CD**.
* `Cannot close the Workbench!`, `Please close all applications, screens, windows
  and CLIs.` and `Install Gunship 2000`, on a machine with no Workbench, no other
  applications and nothing to install to.

## 5. `/GS2000/`, an empty directory

2,048 bytes containing `.` and `..` and nothing else, dated 1994-04-19 13:38:54.
Reached by nothing. The lowercase `/fonts/gs2000/` is the live path.
([02-filesystem.md](02-filesystem.md))

## 6. Placeholder geometry among the 3D models

Of the 163 models in `object.cat`: `BLUEBOX`, `WHITEBOX` and `BOXS` are named
primitives, and `BOXBUILD`, `BOXBLD2`, `BOXBLD3`, `BOXBLD4` and `BOXBLD5` are box
buildings. Eight of 163 models are boxes with box names. Whether they are
placeholders that shipped or deliberate low-detail scenery is not decidable from
the disc.

Set dressing that survived into the product: `COW`, `CAMELH`, `CAMELSIT`, `BED`,
`BASEGUY`, `SPLAT` (317 bytes, the smallest model on the disc).

## 7. Assets stored twice, and five that diverged

63 pictures and models exist both loose in the root and inside a `.cat` archive,
byte for byte — 1.83 MiB. Five more exist in both places as **different files**:
`cd1.pix`, `cd2.pix`, `cd3.pix`, `RESCUE.PIX` and `PILOT.PIX`. `PILOT.PIX`
exists three times: loose, in `gs2frt.cat` identical to the loose copy, and in
`gs2end.cat` as a different, smaller picture.
([05-archives.md](05-archives.md))

## 8. An internal toolkit's error messages, localised and shipped

`Catalogs/English/Ami.catalog` is not game text. It is the developer-facing
diagnostic catalogue of an internal display framework called *Ami*, complete with
messages nobody playing the game can cause:

```
Can't get clearing buffer userdata with no display open
Can't set viewing buffer userdata with no display open
Not enough free graphics memory in system
```

`User.catalog` next to it declares `$VER: ami.catalog 1.00 (15.2.94)` in
lowercase where `Ami.catalog` declares `Ami.catalog 1.00 (22.03.94)`.
([06-text.md](06-text.md))

## 9. People and tools the disc names

* **Wayne D. Lutz** — `$VER: cdgsxl 1.50 (15.10.93)`, the CDXL player. The only
  person named anywhere on the disc.
* **D J Pocock** — the PVD data preparer, the mastering engineer.
* **ASDG Art Department Professional IFF3.0.4 (02.12.93)** — annotation inside
  `frame.lbm`.
* **DeluxePaint** — 66 `DPPS` chunks across the ILBM set, and `logo.pix` is a
  PC-side `PBM ` with a `TINY` thumbnail.
* **Pantaray, Inc. USA** — ISOCD 1.04, in the preparer field.

No programmer, artist or musician is credited anywhere in the filesystem. For a
disc with 104,838 bytes of prose on it, that is a result in itself: unlike
Universe, which named its programmer, three artists and its composer in plain
text, Gunship 2000 names nobody who made it.
