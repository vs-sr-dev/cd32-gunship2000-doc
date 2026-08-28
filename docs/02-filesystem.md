# 02 — The ISO 9660 filesystem

Reproduce with `tools/isodump.py` and `tools/timeline.py`. Full listing in
[`notes/iso-volume.txt`](../notes/iso-volume.txt).

## Volume descriptor

| field | value |
|---|---|
| system identifier | `CDTV`, space padded |
| volume identifier | `Gunship_2000`, NUL padded |
| volume space size | 80,735 sectors (LE and BE agree) |
| block size | 2,048 |
| path table size | 116 bytes; L at 20, M at 19 |
| root directory | extent 22, 6,144 bytes, 1994-04-19 13:38:40 |
| volume set identifier | empty (all NUL) |
| publisher | `Microprose`, NUL padded |
| data preparer | `D J Pocock - ISOCD 1.04 by Pantaray, Inc. USA -`, NUL padded |
| application identifier | `Gunship 2000 CD32`, NUL padded |
| copyright / abstract / bibliographic | all empty |
| creation | 1994-04-19 13:46:56 +0 |
| modification / expiration / effective | all empty |
| file structure version | 1 |

Sector 17 is byte-identical to sector 16, as on every disc in this series.
Sector 18 is the terminator.

ISOCD version **1.04** — the same version as all fourteen previous discs.
Fifteen discs, five years of release dates, one tool version.

## The .TM block

The pointer in the application-use area is followed rather than assumed: tag
`TM` at offset 888, constant `0x0014`, length 2,048, LBA 21.

```
whole block          sha1 c5ffcef2a5e33d2df606185823cd95d1c174d65f
banner 0x000..0x44C  sha1 8d84115154d70360b3469acc99cdad3db0ed2c92
object 0x44C..0x7B8  sha1 690aae24a96b69659066e691d0b07db301260572
```

All three match the twelve other CD32-era discs in the series. Prediction
confirmed. Speris remains the only disc with something else there.

## Directories

Nine directories, 140 files.

```
/                     lba     22   6144 bytes
/c                    lba  51227   2048   1994-04-14 11:12:17
/Catalogs             lba  51651   2048   1994-03-22 17:23:46
/Catalogs/English     lba  55111   2048   1994-03-22 17:23:47
/fonts                lba  52640   2048   1994-01-04 13:22:14
/fonts/gs2000         lba  55112   2048   1993-12-29 11:45:55
/GS2000               lba  52652   2048   1994-04-19 13:38:54
/libs                 lba  51278   2048   1994-03-22 17:23:56
/s                    lba  51225   2048   1994-04-14 13:25:48
```

### `/GS2000/` is empty

Its 2,048-byte extent contains two directory records and nothing else:

```
reclen 34  lba 52652  size 2048  name '\x00'   (.)
reclen 34  lba 22     size 6144  name '\x01'   (..)
```

This is the fourth empty directory found across the series (three on two discs
before this). Its timestamp, 1994-04-19 13:38:54, is 14 seconds after the root
directory's own and 8 minutes before the PVD — so it was created during the
master build, and the pattern from the earlier discs holds: empty directories
appear among the last records written, not among the first.

Note the case: `/GS2000/` at the root is empty, while `/fonts/gs2000/` in
lowercase holds the seven font files the game actually opens. The font
descriptors name `gs2000/N` relative to `FONTS:`, and the startup assigns
`FONTS:` to `gs_dsk1:fonts`, so the lowercase one is the live path. The
uppercase root directory is reached by nothing on the disc.

## File naming and record shape

All 140 file records carry the `;1` version suffix in `raw_name` and none carry
anything else. Root records are in ISO 9660 sorted order. Directory records for
the nine directories carry no suffix. This matches the rest of the series and is
not further remarked on.

## `.info` icons

Four Workbench icons: `/.info` (76), `/disk.info` (369), `/Backdrop.info` (835),
`/gunship 2000.info` (4,442).

None of the four matches any `.info` on any other disc in the series. In
particular the 396-byte Blitz Basic 2 project icon shared by Guardian and Gloom
is not here. The presence of `disk.info` and a project icon for the launcher
means the title *is* launchable from Workbench, unlike Universe, which had no
icons at all.

## Timestamps

Full write-order log in [`notes/timestamps.txt`](../notes/timestamps.txt).

Range 1993-12-20 11:46:08 to 1994-04-19 14:06:50 — four months, 24 distinct
calendar days, 148 dated records.

```
by year: 1993 x24, 1994 x124
epoch 1978: none
epoch 1980: none
```

**No MS-DOS zero epoch at all.** This was predicted the other way round: open
item 24 supposes the 1980 (FAT day zero) timestamps on Guardian and Fire & Ice
come from a staging tree on a PC with an unset clock, and a DOS-first publisher
is the best available test of that. MicroProse produces zero of them. See
[12-open-questions.md](12-open-questions.md); the byte-order evidence in
[07-graphics.md](07-graphics.md) turns out to be the better probe for the same
question.

### The clock is coherent, with one inversion

The four busiest days are 1994-02-21 (42 records, the front-end picture set),
1994-01-13 (14), 1994-03-22 (12) and 1993-12-20 (23, the fonts, the four
one-byte probes, `flight.cat` and `object.cat` in one 6-minute pass).

The last four files are written in 42 seconds:

```
1994-04-19 14:06:08   3532   /gunship 2000
1994-04-19 14:06:30 218636   /gs
1994-04-19 14:06:48 197532   /gs2.run
1994-04-19 14:06:50   1680   /roster.dat
```

**The PVD is dated 1994-04-19 13:46:56, which is 19 minutes and 12 seconds
before the oldest of those four and 19 minutes 54 seconds before the newest.**
On every other disc in this series the PVD is later than everything it indexes —
on Universe by 2h17m45s. Here four files carry timestamps *after* the volume
creation date they are indexed under.

The root directory (13:38:40) and `/GS2000/` (13:38:54) are earlier still. So
the ordering of the build is: directories at 13:38, PVD stamped at 13:46, and
the three programs plus a scratch file dropped in at 14:06. Either the source
tree was still being written while the image was assembled, or ISOCD stamps the
PVD when it starts rather than when it finishes. Both are consistent with the
banner in the launcher reading `15/4/1994` — four days before any of this.

Nothing here needs the "wrong clock" explanation that Liberation, Banshee and
Fire & Ice needed: the sequence is internally consistent and matches the
version banner.
