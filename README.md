# Gunship 2000 (MicroProse, 1994) — Amiga CD32

Structural documentation of the Amiga CD32 release of **Gunship 2000**, a
helicopter flight simulator published by MicroProse.

Documentation only. No game code, artwork, audio or other asset is committed
here — the tools in [`tools/`](tools/) reproduce every figure and table in these
documents from a disc image you supply.

This is the fifteenth disc in a running Amiga CD32 / CDTV series and the first
flight simulator in it. The shared checklist those discs feed is
[cd32-platformnotes-doc](https://github.com/vs-sr-dev/cd32-platformnotes-doc).

## The disc

```
CATALOG 5015352330281                       (a real EAN-13)
TRACK 01  MODE1/2048   80,735 sectors declared, 80,813 in the image
TRACK 02..06  AUDIO    70,136 sectors, 15:35.11, 5 distinct tracks
```

140 files, nine directories. Data 53.5 % / audio 46.5 % — the first disc in the
series where the data track is the larger half — and 45.3 % of a CD used in all.

Publisher `Microprose`, preparer `D J Pocock`, application identifier
`Gunship 2000 CD32`, volume created 1994-04-19 13:46:56. Version
`Gunship 2000     V3.32 - 15/4/1994`, from a bare banner in the launcher, because
there is no `$VER:` in any game program. The only person the disc names is
**Wayne D. Lutz**, author of the third-party CDXL player. Nobody who made the
game is credited anywhere in the filesystem.

All of that read off the disc, none of it taken on trust.

## Highlights

**A 100 MiB hole, to the byte.** LBA 25 to 51,224 is 104,857,600 bytes of zero —
exactly 100 × 1024 × 1024 — sitting between the volume descriptors and the first
file, inside the declared volume so the mastering tool counted it deliberately.
It is 63.4 % of the disc. This is the fourth gap-before-files in the series and
the first that is a round number, which makes it a *reservation* rather than a
layout artefact. Nothing on the disc says what for.

**The second-largest data track in the series is 4.2 % game.** 157.84 MB, within
2 % of Liberation's, and the best candidate the series has had to break the
13.3 MB ceiling from above. It does not come close: 63.4 % is the zero hole,
86.9 % of the *file* bytes are three CDXL video streams, and the game itself is
6.62 MiB on disc and **7.98 MiB resident**. The band holds — fifteen discs,
eleven studios, five years, floor 2.25 MB, ceiling 13.3 MB, nothing through it.

**A complete second game that never runs.** `pirates.demo` is a full alternative
boot script for a playable Pirates! Gold demo, with CD32 front-panel language
detection via a 104-byte `c/getlang` that returns `RETURN_WARN` for German. It
ships with two 383 KB executables, a disk font, 15 IFF 8SVX samples buried inside
a chip hunk, and a 21.6 MB intro video. The active `s/startup-sequence` never
calls it, and the one line that would have launched it is commented out with its
template instruction still attached: `;pirates 2	; replace 5 with the cd music
track number`. The video *is* reachable — `gs` says
`Press RED button to view Pirates! Gold intro` — so 13.1 % of the disc advertises
a demo the disc will not launch.

**The game's own data files are little-endian IFF.** All 76 loose pictures are
correct big-endian ILBM/PBM. All 41 files using the game's own form types —
`SCRN`, `WRLD`, `SHIP`, `SHIN`, `SCNR`, `THTR`, `WSYS` — store every chunk size
in Intel order, so `BASE.SCN` declares a 3.4 GB FORM inside a 3 KB file. Read
little-endian the walk lands exactly on the last byte, on all 41. Together with
`logo.pix` being a PC DeluxePaint `PBM ` with a `TINY` thumbnail, this is direct
evidence of a DOS-side authoring pipeline — which is what open item 24 has been
trying to get out of timestamps. The timestamps on this disc say nothing at all
(zero 1980 files, zero 1978 files, from the most DOS-first publisher in the
series). **Byte order is the better probe.**

**The floppy release, described by the CD in plain text.** The loader assigns
`gs_dsk1`–`gs_dsk4`, opens `gs_dsk2:gs2frt.cat` and `gs_dsk4:gs2end.cat`, and
carries `Insert GS2000 disk %d`, `Insert GS2000 disk 4`, `Cannot close the
Workbench!` and `Install Gunship 2000`. The four one-byte files named `1`, `2`,
`3` and `4` in the root are the disk-identity probes for the format string
`gs_dsk%d:%d`. `gs_dsk%d:orig` is an original-disk check whose target file is not
on the CD. With the ancestor established this way rather than inferred, the
compression rule goes to **[10 of 10]**: 542 validated RNC method 2 streams,
despite there being no space pressure whatsoever on a 45 %-full disc.

**`cd32rez` uses `LoadSeg` as its own pointer fixup.** 641,768 bytes that begin
`00 00 03 F3`, one CODE hunk, and exactly fifteen relocations — all fifteen
pointing at the first sixty bytes, which are a fifteen-entry group table
terminated by `FFFFFFFF`. The "code" is the table; the other 641,596 bytes are
526 concatenated RNC2 streams. The archive does no fixup of its own: it declares
its group pointers as relocations and lets the OS loader patch them while it
loads.

**Akiko 0 / 0 / 0 / 0, and a new false positive.** No `$B80000`, no `$B80030`, no
C2P port, scanned across all eight address registers in both load forms. The
single `$C0DE0000` byte hit is a straddle across two entries of a stride-16
longword table passing through `0x0000C0DE` — a new entry for the catalogue. The
disc reaches the drive through `cd.device` and saves through
`nonvolatile.library`, because unlike Universe it never shuts Exec down.

**Where the frame ends: planar.** Zero C2P mask immediates anywhere, zero Akiko
C2P. The flight engine's only whole-screen blit is `BLTSIZE #$C814` — height 800
is 200 rows × 4 bitplanes, width 20 words is 320 pixels, both modulos zero: a
contiguous four-plane buffer moved in one operation, the Guardian idiom. The
`$CA` minterm appears with `USEA` **on**, so it is the ordinary masked bob and
not Guardian's cookie-cut. Eighth planar-in-planar case in the series. The
prediction said chunky, on genre grounds, and the arithmetic beat the genre.

**Leftovers.** `roster.dat` — the last file written to the master, two seconds
after `gs2.run` — is a saved pilot roster whose squadron is called `ERASE ME` and
whose unit is `THE ERASABLES`. `gsfnt9.font` points at `gsfnt9/11`, a directory
that does not exist, while the font it wants sits orphaned in `gs2000/11`.
`/GS2000/` is an empty directory. 1.83 MiB of assets are stored twice, and five
more exist in two places as *different files*. `T72.SBN` and `T62.SBN` are each
stored twice inside the same archive. `Ami.catalog` is an internal toolkit's
developer error messages, localised and shipped. Both Pirates builds carry
`Unint String!`.

**Seven predictions right, six wrong, one split**, all written down before the
corresponding measurement and all listed with their outcomes at the end of
[docs/12-open-questions.md](docs/12-open-questions.md).

## Documents

| | |
|---|---|
| [00-overview.md](docs/00-overview.md) | what the disc says about itself, and the five things worth knowing |
| [01-disc-image.md](docs/01-disc-image.md) | tracks, sector map, the 100 MiB hole, the pregap that describes nothing |
| [02-filesystem.md](docs/02-filesystem.md) | ISO 9660 volume, the empty directory, the PVD dated before its own files |
| [03-boot-chain.md](docs/03-boot-chain.md) | startup-sequence, the four programs, the floppy release read off the CD |
| [04-compression.md](docs/04-compression.md) | RNC method 2, `cd32rez`, the rule at [10 of 10] |
| [05-archives.md](docs/05-archives.md) | the `.cat` / `.dat` format, 165 3D models, 1.83 MiB stored twice |
| [06-text.md](docs/06-text.md) | 104,838 bytes of prose against both denominators |
| [07-graphics.md](docs/07-graphics.md) | IFF geometry, the byte-order split, three CDXL streams |
| [08-audio.md](docs/08-audio.md) | five Red Book tracks, `cd.device`, 15 hidden 8SVX |
| [09-hardware.md](docs/09-hardware.md) | Akiko, the blitter, where the frame ends |
| [10-band.md](docs/10-band.md) | the three figures, and a hypothesis that dies |
| [11-leftovers.md](docs/11-leftovers.md) | Pirates! Gold, `ERASE ME`, the dangling font |
| [12-open-questions.md](docs/12-open-questions.md) | thirteen open items, and the prediction table |

## Offset convention

Declared here once, as step 25 of the shared checklist requires, and used
consistently throughout.

* Every address written `0x......` in these documents is a **file offset** in the
  file being discussed, unless the sentence says otherwise.
* Where a hunk-relative offset is meant it is written `hunk0+0x...`, and the file
  offset is given beside it.
* `tools/relocs.py` prints the file offset of every hunk body, so the two can
  always be converted. `tools/relocs.py FILE --at 0x...` answers whether a
  constant at a given file offset is covered by a `HUNK_RELOC32` entry — a
  constant that is **not** covered is a literal, not a relocatable address. This
  is how the fifteen pointers in `cd32rez` were shown to be the whole of its
  "code".
* Capstone's M68K backend prints wrong-but-plausible immediates, displacements
  and absolute addresses on this code. Every constant quoted in these documents
  was re-read from the raw bytes. `tools/dis68k.py` recomputes branch targets
  from the encoding; nothing else it prints is trusted.

## Tools

Run any of them with no arguments for usage. They need Python 3 and, for
`dis68k.py` only, `capstone`.

### New in this repository

| tool | what it does |
|---|---|
| `containers2.py` | container walk accepting RNC method 1 **and** 2 — the inherited `containers.py` reports zero streams on this disc |
| `catdump.py` | the `.cat` / `.dat` archive format, with loose-file cross-check |
| `cdxl.py` | CDXL geometry validated by arithmetic, not by trusting fields |
| `iffscan.py` | IFF ILBM/PBM BMHD, CAMG and palette census |
| `iffle.py` | the little-endian IFF variant, and the byte-order census |
| `blitscan.py` | exact-encoding blitter writes, with BLTCON0/1 and BLTSIZE decoded |
| `chipregs.py` | every `d16(An)` chip access for a chosen base register (upper bound, by design) |
| `lvoscan.py` | `jsr d16(a6)` counts by displacement, printing **every** candidate meaning |
| `cueaudio.py` | per-track WAV geometry and measured leading silence vs declared pregap |
| `timeline.py` | directory write order with gaps, and the DOS epoch counts |
| `textcensus.py` | prose against both denominators, with a defensible floor definition |
| `bandcalc.py` | the three figures by category, with per-file slack |
| `magiccensus.py` | size, magic and SHA-1 census of an extracted tree |
| `strdump.py` | printable runs with file offsets and hunk attribution (`strings` is absent here) |

### Inherited unchanged

From [cd32-universe-doc](https://github.com/vs-sr-dev/cd32-universe-doc):
`isodump.py`, `packscan.py`, `rnc.py`, `rnc2.py`, `pp20.py`, `relocs.py`,
`dis68k.py`, `akiko2.py`, `dffscan.py`, `regscan.py`, `dispatch.py`,
`copperfind.py`, `copperpal.py`, `planar.py`, `geomguess.py`, `picture.py`,
`band.py`, `census.py`, `containers.py`, `unpackall.py`, `textscan.py`,
`langsplit.py`, `slots.py`, `audiotracks.py`, `akiko.py`.

Two inherited tools return clean, confident, **wrong** negatives on this disc and
are kept as they are so that stays visible: `containers.py` and `unpackall.py`
find zero streams because they only decode RNC method 1, and `audiotracks.py`
finds zero tracks because it assumes one BIN with byte offsets rather than one
WAV per track. `regscan.py` finds one chip access in a program with 36 base loads
because it walks forward from each load and this program holds the base across
routines. That is the same failure mode `akiko.py` had on Universe, three times
over.

## Reproducing

Put the disc image and its cue in the repository root, then:

```sh
python tools/isodump.py "Gunship 2000 (1994)(MicroProse)(Track 1 of 6)[!].iso" \
    --extract _work/iso --json _work/iso.json
python tools/containers2.py _work/iso --out _work/unpacked
python tools/magiccensus.py _work/iso
python tools/bandcalc.py  _work/iso _work/unpacked
python tools/cueaudio.py  "Gunship 2000 (1994)(MicroProse)[!].cue"
python tools/iffle.py     _work/iso
python tools/blitscan.py  _work/iso/gs2.run
python tools/cdxl.py      _work/iso/*.xl _work/iso/*.XL
```

`_work/` is git-ignored and nothing from it is committed. Regenerated output is
in [`notes/`](notes/).
